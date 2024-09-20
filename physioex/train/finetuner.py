from typing import List
import os

import uuid
from pathlib import Path

import pandas as pd
import pytorch_lightning as pl
import torch

from lightning.pytorch import seed_everything
from loguru import logger
from pytorch_lightning.callbacks import ModelCheckpoint, RichProgressBar
from pytorch_lightning.loggers import CSVLogger

from physioex.data import (
    PhysioExDataModule,
    PhysioExDataset,
    get_datasets,
    HPCPhysioExDataset,
)
from physioex.train.networks import get_config
from physioex.train.networks.utils.loss import config as loss_config
from physioex.train.networks.finetuned import FineTunedModule
from physioex.train.networks.multisource import MultiSourceModule

torch.set_float32_matmul_precision("medium")
seed_everything(42, workers=True)


class FineTuner:
    def __init__(
        self,
        train_datasets: List[str] = ["mass"],
        train_versions: List[str] = None,
        test_datasets: List[str] = [],
        test_versions: List[str] = None,
        batch_size: int = 32,
        selected_channels: List[int] = ["EEG"],
        sequence_length: int = 21,
        learning_rate: float = 1e-7,
        # task: str = "sleep",
        data_folder: str = None,
        random_fold: bool = False,
        model_name: str = "chambon2018",
        loss_name: str = "cel",
        ckp_path: str = None,
        max_epoch: int = 20,
        val_check_interval: int = 3,
        multisource: bool = False,
        multisource_ckp: str = None,
        hpc: bool = False,
    ):
        ###### module setup ######
        network_config = get_config()[model_name]

        module_config = network_config["module_config"]
        module_config["seq_len"] = sequence_length
        module_config["loss_call"] = loss_config[loss_name]
        module_config["loss_params"] = dict()
        module_config["in_channels"] = len(selected_channels)
        module_config["model_name"] = model_name
        # module_config["n_train"] = len(train_datasets)
        module_config["n_train"] = 4

        self.hpc = hpc

        self.module_config = module_config
        self.module_config["lr"] = learning_rate

        if multisource:
            self.model_call = MultiSourceModule
            self.module_config["module_checkpoint"] = multisource_ckp
        else:
            self.model_call = FineTunedModule

        ###### datamodule setup ######


        self.folds = [-1]
        
        self.train_datasets = train_datasets
        self.train_versions = train_versions

        self.test_datasets = test_datasets
        self.test_versions = test_versions

        self.batch_size = batch_size
        self.preprocessing = network_config["input_transform"]
        self.selected_channels = selected_channels
        self.sequence_length = sequence_length
        self.data_folder = data_folder
        self.target_transform = network_config["target_transform"]

        ##### trainer setup #####

        self.batch_size = batch_size
        self.max_epoch = max_epoch
        self.val_check_interval = val_check_interval

        self.ckp_path = (
            ckp_path if ckp_path is not None else "models/" + str(uuid.uuid4()) + "/"
        )
        Path(self.ckp_path).mkdir(parents=True, exist_ok=True)

        #############################

    def train_evaluate(self, fold: int = 0):

        ###### module setup ######

        module = self.model_call(module_config=self.module_config)

        ###### trainer setup ######

        # Definizione delle callback
        checkpoint_callback = ModelCheckpoint(
            monitor="val_acc",
            save_top_k=1,
            mode="max",
            dirpath=self.ckp_path,
            filename="fold=%d-{epoch}-{step}-{val_acc:.2f}" % fold,
            save_weights_only=False,
        )

        progress_bar_callback = RichProgressBar()

        my_logger = CSVLogger(save_dir=self.ckp_path)

        # Configura il trainer con le callback
        trainer = pl.Trainer(
            devices="auto",
            max_epochs=self.max_epoch,
            val_check_interval=self.val_check_interval,
            callbacks=[checkpoint_callback, progress_bar_callback],
            deterministic=True,
            logger=my_logger,
            # enable ddp if hpc is active
            
            # num_sanity_val_steps = -1
        )

        ###### training ######
        val_results = {}
        test_results = {}
        if len(self.train_datasets) > 0:
            logger.info(
                "JOB:%d-Splitting dataset into train, validation and test sets" % fold
            )

            #### datamodules setup ####

            train_datamodule = PhysioExDataModule(
                datasets=self.train_datasets,
                versions=self.train_versions,
                folds=fold,
                batch_size=self.batch_size,
                selected_channels=self.selected_channels,
                sequence_length=self.sequence_length,
                data_folder=self.data_folder,
                preprocessing=self.preprocessing,
                target_transform=self.target_transform,
                hpc=self.hpc,
            )
            
            num_steps = train_datamodule.dataset.__len__() * 0.7 // self.batch_size
            val_check_interval = max(1, num_steps // self.val_check_interval)
            
            trainer = pl.Trainer(
                devices="auto",
                max_epochs=self.max_epoch,
                val_check_interval= val_check_interval,
                callbacks=[checkpoint_callback, progress_bar_callback],
                deterministic=True,
                logger=my_logger,
                strategy="ddp",
                num_nodes=4
                # num_sanity_val_steps = -1
            )
            # trainer.validate(module, datamodule.val_dataloader())
            # Addestra il modello utilizzando il trainer e il DataModule

            # check if the checkpoint exists already:
            saved_checks = os.listdir(self.ckp_path)
            saved_checks = [
                check for check in saved_checks if "fold=%d" % fold in check
            ]
            if len(saved_checks) > 0:
                # take the absolute path
                saved_checks = os.path.join(self.ckp_path, saved_checks[0])

                logger.info("FOLD:%d-Loading checkpoint %s" % (fold, saved_checks))

                module = self.model_call.load_from_checkpoint(
                    saved_checks, module_config=self.module_config
                )
            else:
                logger.info("FOLD:%d-Training model" % fold)
                trainer.fit(module, datamodule=train_datamodule)

                # load the best model
                module = self.model_call.load_from_checkpoint(
                    checkpoint_callback.best_model_path,
                    module_config=self.module_config,
                )

            logger.info("FOLD:%d-Evaluating model" % fold)
            val_results = trainer.test(
                module, dataloaders=train_datamodule.val_dataloader()
            )[0]

            val_results["fold"] = fold

            test_results = trainer.test(module, datamodule=train_datamodule)[0]

            test_results["fold"] = fold

        multi_source_results = []

        if len(self.test_datasets) > 0:
            for test_dataset in ["mass", "hmc", "mros", "dcsm", "mesa"]:
                test_datamodule = PhysioExDataModule(
                    datasets=[test_dataset],
                    batch_size=self.batch_size,
                    selected_channels=self.selected_channels,
                    sequence_length=self.sequence_length,
                    data_folder=self.data_folder,
                    preprocessing=self.preprocessing,
                    target_transform=self.target_transform,
                    folds=fold,
                    hpc=self.hpc,
                )

                if self.hpc:
                    test_datamodule.dataset.load()

                multi_source_result = trainer.test(module, datamodule=test_datamodule)[
                    0
                ]

                print(multi_source_result)

                multi_source_result["fold"] = fold
                multi_source_result["dataset"] = test_dataset

                multi_source_results.append(multi_source_result)

        return {
            "val_results": val_results,
            "test_results": test_results,
            "msd_results": multi_source_results,
        }

    def run(self):

        results = [self.train_evaluate(fold) for fold in self.folds]

        val_results = pd.DataFrame([result["val_results"] for result in results])
        test_results = pd.DataFrame([result["test_results"] for result in results])
        msd_results = pd.concat(
            [pd.DataFrame(result["msd_results"]) for result in results]
        )

        val_results.to_csv(self.ckp_path + "val_results.csv", index=False)
        test_results.to_csv(self.ckp_path + "test_results.csv", index=False)
        msd_results.to_csv(self.ckp_path + "msd_results.csv", index=False)

        logger.info("Results successfully saved in %s" % self.ckp_path)


if __name__ == "__main__":
    # parse the arguments from the command line with defaults:
    import argparse

    parser = argparse.ArgumentParser(description="Fine-tuning a model")

    parser.add_argument(
        "--train_datasets", nargs="+", default=[], help="List of training datasets"
    )
    parser.add_argument(
        "--train_versions",
        nargs="+",
        default=None,
        help="List of training dataset versions",
    )
    parser.add_argument(
        "--test_datasets",
        nargs="+",
        default=[],
        help="List of test datasets",
    )
    parser.add_argument(
        "--test_versions", nargs="+", default=None, help="List of test dataset versions"
    )
    parser.add_argument("--batch_size", type=int, default=128, help="Batch size")
    parser.add_argument(
        "--selected_channels",
        nargs="+",
        default=["EEG", "EOG", "EMG"],
        help="List of selected channels",
    )
    parser.add_argument(
        "--sequence_length", type=int, default=21, help="Sequence length"
    )
    parser.add_argument("--data_folder", type=str, default=None, help="Data folder")
    parser.add_argument("--random_fold", action="store_true", help="Use random fold")
    parser.add_argument(
        "--model_name", type=str, default="seqsleepnet", help="Model name"
    )
    parser.add_argument("--loss_name", type=str, default="cel", help="Loss name")
    parser.add_argument("--ckp_path", type=str, default=None, help="Checkpoint path")
    parser.add_argument(
        "--max_epoch", type=int, default=1, help="Maximum number of epochs"
    )
    parser.add_argument(
        "--val_check_interval", type=int, default=10, help="Validation check interval"
    )
    parser.add_argument(
        "--learning_rate", type=float, default=1e-7, help="Learning rate"
    )
    parser.add_argument(
        "--multisource", action="store_true", help="Use multisource model"
    )
    parser.add_argument(
        "--multisource_ckp", type=str, default=None, help="Multisource checkpoint path"
    )
    parser.add_argument(
        "--hpc",
        "-hpc",
        action="store_true",
        help="Weather or not to use the HPC dataset. Expected type: bool. Optional. Default: False",
    )

    args = parser.parse_args()
    
    if isinstance( args.selected_channels, str): 
        if " " in args.selected_channels:
            args.selected_channels = args.selected_channels.split(" ")
        else:
            args.selected_channels = [args.selected_channels]
    
    if isinstance( args.train_datasets, str): 
        if " " in args.train_datasets:
            args.train_datasets = args.train_datasets.split(" ")
        else:
            args.train_datasets = [args.train_datasets]
    
    fine_tuner = FineTuner(
        train_datasets=args.train_datasets,
        train_versions=args.train_versions,
        test_datasets=args.test_datasets,
        test_versions=args.test_versions,
        batch_size=args.batch_size,
        selected_channels=args.selected_channels,
        sequence_length=args.sequence_length,
        data_folder=args.data_folder,
        random_fold=args.random_fold,
        model_name=args.model_name,
        loss_name=args.loss_name,
        ckp_path=args.ckp_path,
        max_epoch=args.max_epoch,
        val_check_interval=args.val_check_interval,
        multisource=args.multisource,
        multisource_ckp=args.multisource_ckp,
        hpc=args.hpc,
        learning_rate=args.learning_rate,
    )

    fine_tuner.run()


def chunked_iterable(iterable, size):
    import itertools

    """Divide un iterable in chunk di data dimensione."""
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk