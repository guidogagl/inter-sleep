import torch
from pytorch_lightning import LightningModule

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

import matplotlib.pyplot as plt
import scipy as sp
import numpy as np 
import seaborn as sns
import pandas as pd
import re
import os

from joblib import Parallel, delayed

from physioex.explain.base import PhysioExplainer

from physioex.train.networks import config 
from physioex.train.networks.utils.loss import config as loss_config
from physioex.data import datasets, TimeDistributedModule

from loguru import logger
from tqdm import tqdm

import torch
torch.set_float32_matmul_precision('medium')

def compute_band_importance( freq_band, model, dataloader, model_device):
    y_pred = []
    y_true = []
    importance = []

    for batch in dataloader:
        inputs, y_true_batch = batch
        
        # store the true label of the input element
        y_true.append(y_true_batch.numpy())

        # compute the prediction of the model
        pred_proba = model(inputs.to(model_device)).cpu().detach().numpy()
        y_pred.append( np.argmax( pred_proba, axis = -1) )
        n_class = pred_proba.shape[-1]

        # port the input to numpy
        inputs = inputs.cpu().detach().numpy()
        batch_size, seq_len, n_channels, n_samples = inputs.shape

        # in our experiments n_channels is always 1
        # in our experiments n_samples is always 3000 ( 30 seconds of data sampled at 100 Hz )
        # in our experiments seq_len is always 3 ( 3 consecutive 30 seconds windows )
        # in our experiments batch_size is always 32 ( the batch size is the number of samples used to compute the gradient )
        # in our experiments the number of classes (y_true) is always 5 ( wake, N1, N2, N3, REM ) each element of y_true is an integer in [0, 4]
        # y_true size = batch_size, 1
        
        # reshape the input to consider only the input signal ( 30 seconds of data sampled at 100 Hz )
        inputs = inputs.reshape(-1, seq_len * n_samples)

        # now inputs size is batch_size * (seq_len * n_channels (1) * n_samples)
        # remove the frequency band from the input using scipy
        sampling_rate = 100

        for index in range(batch_size):
            # filter bandstop - reject the frequencies specified in freq_band
            lowcut = freq_band[0]
            highcut = freq_band[1]
            order = 4
            nyq = 0.5 * sampling_rate
            low = lowcut / nyq
            high = highcut / nyq
            sos = signal.butter(order, [low, high], btype='bandstop', output='sos')
            inputs[index] = signal.sosfilt(sos, inputs[index])

        # reshape the input signal to the original size and port it to tensor
        inputs = inputs.reshape(batch_size, seq_len, n_channels, n_samples)
        inputs = torch.from_numpy(inputs)

        # compute the prediction of the model with the filtered input, the prediction is a tensor of size batch_size * seq_len, n_classes
        batch_importance = model(inputs.to(model_device)).cpu().detach().numpy()

        # the importance is the difference between the prediction with the original input and the prediction with the filtered input
        batch_importance = pred_proba - batch_importance
        importance.append(batch_importance)

    # reshape the lists to ignore the batch_size dimension

    y_pred = np.concatenate(y_pred).reshape(-1)
    y_true = np.concatenate(y_true).reshape(-1)
    importance = np.concatenate(importance).reshape(-1, n_class)

    return importance, y_pred, y_true

class FreqBandsExplainer(PhysioExplainer):
    def __init__(self,
            model_name : str = "chambon2018", 
            dataset_name : str = "sleep_physioex",
            loss_name : str = "cel", 
            ckp_path : str = None,
            version : str = "2018", 
            use_cache : bool = True, 
            sequence_lenght : int = 3, 
            batch_size : int = 32
        ):
        super().__init__(model_name, dataset_name, loss_name, ckp_path, version, use_cache, sequence_lenght, batch_size)

    def compute_band_importance(self, band, fold : int = 0, plot_pred : bool = False, plot_true : bool = False):
        logger.info("JOB:%d-Loading model %s from checkpoint %s" % (fold, str(self.model_call), self.checkpoints[fold]))
        model = self.model_call.load_from_checkpoint(self.checkpoints[fold], module_config = self.module_config).eval()

        model_device = next(model.parameters()).device

        logger.info("JOB:%d-Splitting dataset into train, validation and test sets" % fold)
        self.dataset.split(fold)

        datamodule = TimeDistributedModule(
            dataset = self.dataset, 
            sequence_lenght = self.module_config["seq_len"], 
            batch_size = self.batch_size, 
            transform = self.input_transform, 
            target_transform = self.target_transform
        )

        self.module_config["loss_params"]["class_weights"] = datamodule.class_weights()

        importance, y_pred, y_true = compute_band_importance(band, model, datamodule.train_dataloader(), model_device)
        
        if plot_true:
            # boxplot of the band importance of the true label
            logger.info("JOB:%d-Plotting band importance for true label" % fold)
            true_importance = []
            
            for i in range(len(y_true)):
                true_importance.append(importance[i][y_true[i]])
            
            true_importance = np.array(true_importance)

            df = pd.DataFrame({
                'Band ' + str(band) + ' Importance': true_importance,
                'Class': y_true
            })

            # boxplot of the true importance of the band with seaborn
            plt.figure(figsize=(10, 10))
            sns.boxplot(x='Class', y='Importance', data=df)
            plt.title('Band Importance for True Label')
            plt.xlabel('Class')
            plt.ylabel('Importance')
            plt.savefig(self.ckpt_path + ("fold=%d_true_band=" + str(band) + "_importance.png") % fold)
            plt.close()

        if plot_pred:
            logger.info("JOB:%d-Plotting band importance for predicted label" % fold)
            pred_importance = []
            
            for i in range(len(y_true)):
                pred_importance.append(importance[i][y_pred[i]])
            
            pred_importance = np.array(pred_importance)

            df = pd.DataFrame({
                'Band ' + str(band) + ' Importance': pred_importance,
                'Class': y_true
            })

            # boxplot of the true importance of the band with seaborn
            plt.figure(figsize=(10, 10))
            sns.boxplot(x='Class', y='Importance', data=df)
            plt.title('Band Importance for Predicted Label')
            plt.xlabel('Class')
            plt.ylabel('Importance')
            plt.savefig(self.ckpt_path + ("fold=%d_pred_band=" + str(band) + "_importance.png") % fold)
            plt.close()
        
        result = np.concatenate( [ importance, y_pred, y_true] , axis = -1 )
        return result
    
    def explain(self, band, save_csv : bool = False, plot_pred : bool = False, plot_true : bool = False, n_jobs : int = 10):
        results = []

        logger.debug("fold che si sta cercando di usare come key: %d", int(fold))
        # Esegui compute_ari per ogni checkpoint in parallelo
        results = Parallel(n_jobs=n_jobs)(delayed(self.compute_band_importance)(int(fold), band, plot_pred, plot_true) for fold in self.checkpoints.keys())

        # Converte i risultati in una matrice numpy
        results = np.array(results)
        
        df = pd.DataFrame([])

        for fold in self.checkpoints.keys():
            df = df.append(pd.DataFrame({
                "Band Importance": results[fold][:, :-2],
                "Predicted Label": results[fold][:, -2],
                "True Label": results[fold][:, -1],
                "Fold": int(fold)
            }))
        
        if save_csv:
            df.to_csv(self.ckpt_path + "band=" + str(band) + "_importance.csv", index=False)
            
        return df