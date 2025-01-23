def train():
    """
    Training script for training and testing a model.

    This script allows you to train a model using specified configurations and parameters.

    Usage:
       `$ train [PARAMS]`
        You can use the `train -h, --help` command to access the command documentation.

    Args:
        --model (str, optional): Specify the model to train, can be a yaml file if the model is not registered. Defaults to "chambon2018".
            If a yaml file is provided, it should contain the model configuration details.
        --checkpoint_dir (str, optional): Specify where to save the checkpoint. Defaults to None.
            Note: Provide the path to the directory where the model checkpoints will be saved.
        --datasets (list, optional): Specify the datasets list to train the model on. Defaults to ['mass'].
            Note: Provide a list of dataset names to be used for training.
        --selected_channels (list, optional): Specify the channels to train the model. Defaults to ['EEG'].
            Note: Channels refer to the data modalities (e.g., EEG, EOG) used for training.
        --sequence_length (int, optional): Specify the sequence length for the model. Defaults to 21.
            Note: Sequence length refers to the number of time steps in each input sequence.
        --loss (str, optional): Specify the loss function to use. Defaults to "cel".
            Note: The loss function determines how the model's performance is measured during training.
        --max_epoch (int, optional): Specify the maximum number of epochs for training. Defaults to 20.
            Note: An epoch is one complete pass through the training dataset.
        --num_validations (int, optional): Specify the number of validations steps to be done in each epoch. Defaults to 10.
            Note: Validation steps are used to evaluate the model's performance on a validation set during training.
        --batch_size (int, optional): Specify the batch size for training. Defaults to 32.
            Note: Batch size refers to the number of samples processed before the model's weights are updated.
        --data_folder (str, optional): The absolute path of the directory where the physioex dataset are stored, if None the home directory is used. Defaults to None.
            Note: Provide the path to the directory containing the datasets.
        --test (bool, optional): Test the model after training. Defaults to False.
            Note: If specified, the model will be tested on the validation set after training.
        --aggregate (bool, optional): Aggregate the results of the test. Defaults to False.
            Note: If specified, the test results will be aggregated across multiple datasets.
        --hpc (bool, optional): Using high performance computing setups or not, need to be called when datasets have been compressed into .h5 format with the compress_datasets command. Defaults to False.
            Note: Use this option if you are running the script on a high-performance computing cluster.
        --num_nodes (int, optional): Specify the number of nodes to be used for distributed training, only used when hpc is True. Defaults to 1.
            Note: In slurm this value needs to be coherent with '--ntasks-per-node' or 'ppn' in torque. This option is relevant for distributed training setups.
        --config (str, optional): Specify the path to the configuration file where to store the options to train the model with. Defaults to None.
            Note: The configuration file can override command line arguments.

    Example:
        The basic usage is as follows:

        ```bash
        train --model chambon2018 --datasets mass --checkpoint_dir ./checkpoints --max_epoch 20 --batch_size 32
        ```

        or you can specify a yaml file containing the configuration details:

        === ".yaml"
            ```yaml
            model_package: physioex.train.networks.seqsleepnet
            model_class: SeqSleepNet
            module_config:
                seq_len: 21
                in_channels: 1
                loss_call: cel # in this case you can pass the loss call as a string
                loss_params: {}
            preprocessing: xsleepnet
            target_transform: get_mid_label
            # check the train documentaion for more details
            ```
        === "bash"
            ```bash
            train --model my_model_config.yaml --datasets mass hmc --checkpoint_dir ./checkpoints --max_epoch 20 --batch_size 32
            ```

    Notes:
        - Ensure that the datasets are properly formatted and stored in the specified data folder using the preprocess script.
        - The script supports both single-node and multi-node training setups.
        - The configuration file, if provided, should be in YAML format and contain valid key-value pairs for the script options.

    """
    pass


def test():
    """
    Testing script for evaluating a model.

    This script allows you to test a pre-trained model using specified configurations and parameters.

    Usage:
       `$ test_model [PARAMS]`
        You can use the `test_model -h, --help` command to access the command documentation.

    Args:
        `--model` (str, optional): Specify the model to test, can be a yaml file if the model is not registered. Defaults to "chambon2018".
            If a yaml file is provided, it should contain the model configuration details.
        `--checkpoint_path` (str, optional): Specify the model checkpoint. Defaults to None.
            Note: Provide the path to a specific checkpoint file to load the model state.
        `--datasets` (list, optional): Specify the datasets list to test the model on. Defaults to ['mass'].
            Note: Provide a list of dataset names to be used for testing.
        `--selected_channels` (list, optional): Specify the channels to test the model. Defaults to ['EEG'].
            Note: Channels refer to the data modalities (e.g., EEG, EOG) used for testing.
        `--sequence_length` (int, optional): Specify the sequence length for the model. Defaults to 21.
            Note: Sequence length refers to the number of time steps in each input sequence.
        `--loss` (str, optional): Specify the loss function to use. Defaults to "cel".
            Note: The loss function determines how the model's performance is measured during testing.
        `--batch_size` (int, optional): Specify the batch size for testing. Defaults to 32.
            Note: Batch size refers to the number of samples processed before the model's weights are updated.
        `--data_folder` (str, optional): The absolute path of the directory where the physioex dataset are stored, if None the home directory is used. Defaults to None.
            Note: Provide the path to the directory containing the datasets.
        `--aggregate` (bool, optional): Aggregate the results of the test. Defaults to False.
            Note: If specified, the test results will be aggregated across multiple datasets.
        `--hpc` (bool, optional): Using high performance computing setups or not, need to be called when datasets have been compressed into .h5 format with the compress_datasets command. Defaults to False.
            Note: Use this option if you are running the script on a high-performance computing cluster.
        `--num_nodes` (int, optional): Specify the number of nodes to be used for distributed testing, only used when hpc is True. Defaults to 1.
            Note: In slurm this value needs to be coherent with '--ntasks-per-node' or 'ppn' in torque. This option is relevant for distributed testing setups.
        `--config` (str, optional): Specify the path to the configuration file where to store the options to test the model with. Defaults to None.
            Note: The configuration file can override command line arguments.

    Example:
        ```bash
        $ test_model --model tinysleepnet --loss cel --sequence_length 21 --selected_channels EEG --checkpoint_path /path/to/checkpoint
        ```

        This command tests the `tinysleepnet` model using the CrossEntropy Loss

    Notes:
        - Ensure that the datasets are properly formatted and stored in the specified data folder using the preprocess script.
        - The script supports both single-node and multi-node testing setups.
        - The configuration file, if provided, should be in YAML format and contain valid key-value pairs for the script options.
    """
    pass


def finetune():
    """
    Finetuning script for training and testing a model.

    This script allows you to fine-tune a pre-trained model using specified configurations and parameters.

    Usage:
       `$ finetune [PARAMS]`
       You can use the `finetune -h --help` command to access the command documentation.

    Args:
        --model (str, optional): Specify the model to train, can be a yaml file if the model is not registered. Defaults to "chambon2018".
            If a yaml file is provided, it should contain the model configuration details.
        --learning_rate (float, optional): Specify the learning rate for the model. Defaults to 1e-7.
            Note: A smaller learning rate is often used for fine-tuning to avoid large updates that could disrupt the pre-trained weights.
        --checkpoint_path (str, optional): Specify the model checkpoint, if None physioex searches into its pretrained models. Defaults to None.
            Note: Provide the path to a specific checkpoint file to resume training from a saved state.
        --checkpoint_dir (str, optional): Specify the checkpoint directory where to store the new finetuned model checkpoints. Defaults to None.
            Note: This directory will be used to save checkpoints during training.
        --datasets (list, optional): Specify the datasets list to train the model on. Defaults to ['mass'].
            Note: Provide a list of dataset names to be used for training.
        --selected_channels (list, optional): Specify the channels to train the model. Defaults to ['EEG'].
            Note: Channels refer to the data modalities (e.g., EEG, EOG) used for training.
        --sequence_length (int, optional): Specify the sequence length for the model. Defaults to 21.
            Note: Sequence length refers to the number of time steps in each input sequence.
        --loss (str, optional): Specify the loss function to use. Defaults to "cel".
            Note: The loss function determines how the model's performance is measured during training.
        --max_epoch (int, optional): Specify the maximum number of epochs for training. Defaults to 20.
            Note: An epoch is one complete pass through the training dataset.
        --num_validations (int, optional): Specify the number of validations steps to be done in each epoch. Defaults to 10.
            Note: Validation steps are used to evaluate the model's performance on a validation set during training.
        --batch_size (int, optional): Specify the batch size for training. Defaults to 32.
            Note: Batch size refers to the number of samples processed before the model's weights are updated.
        --data_folder (str, optional): The absolute path of the directory where the physioex dataset are stored, if None the home directory is used. Defaults to None.
            Note: Provide the path to the directory containing the datasets.
        --test (bool, optional): Test the model after training. Defaults to False.
            Note: If specified, the model will be tested on the validation set after training.
        --aggregate (bool, optional): Aggregate the results of the test. Defaults to False.
            Note: If specified, the test results will be aggregated across multiple datasets.
        --hpc (bool, optional): Using high performance computing setups or not, need to be called when datasets have been compressed into .h5 format with the compress_datasets command. Defaults to False.
            Note: Use this option if you are running the script on a high-performance computing cluster.
        --num_nodes (int, optional): Specify the number of nodes to be used for distributed training, only used when hpc is True. Defaults to 1.
            Note: In slurm this value needs to be coherent with '--ntasks-per-node' or 'ppn' in torque. This option is relevant for distributed training setups.
        --config (str, optional): Specify the path to the configuration file where to store the options to train the model with. Defaults to None.
            Note: The configuration file can override command line arguments.


    Example:
        ```bash
        $ finetune --model tinysleepnet --loss cel --sequence_length 21 --selected_channels EEG --checkpoint_path /path/to/checkpoint
        ```
        This command fine-tunes the `tinysleepnet` model using the CrossEntropy Loss (`cel`), with a sequence length of 21 and the `EEG` channel, starting from the specified checkpoint.

    Notes:
        - Ensure that the datasets are properly formatted and stored in the specified data folder using the preprocess script.
        - The script supports both single-node and multi-node training setups.
        - The configuration file, if provided, should be in YAML format and contain valid key-value pairs for the script options.
    """
    pass


def preprocess():
    """
    Preprocessing script for preparing datasets.

    This script allows you to preprocess datasets for training and testing models.

    Usage:
       `$ preprocess [PARAMS]`
       You can use the `preprocess -h --help` command to access the command documentation.

    Args:
        --dataset (str, optional): The name of the dataset to preprocess. Defaults to "hmc".
            Note: The dataset name should be one of the supported datasets (e.g., "hmc", "mass", "shhs", "mesa", "mros", "dcsm"). If a custom dataset is used use the `preprocessor` argument.
        --data_folder (str, optional): The absolute path of the directory where the physioex dataset are stored, if None the home directory is used. Defaults to None.
            Note: Provide the path to the directory containing the datasets.
        --preprocessor (str, optional): The name of the preprocessor in case of a custom Preprocessor. Defaults to None.
            Note: The preprocessor should extend `physioex.preprocess.proprocessor:Preprocessor` and be passed as a string in the format `path.to.preprocessor.module:PreprocessorClass`.
        --config (str, optional): Specify the path to the configuration .yaml file where to store the options to preprocess the dataset with. Defaults to None.
            Note: The configuration file can override command line arguments. You can specify also the preprocessor_kwargs in the configuration file.

    Example:
        ```bash
        $ preprocess --dataset mass --data_folder /path/to/datasets
        ```
        This command preprocesses the `mass` dataset using the `MASSPreprocessor` preprocessor.

        For HMC and DCSM datasets, PhysioEx will automatically download the datasets.
        The other datasets needs to be obtained first, most of them are easily accessible from sleepdata.org.

        The SHHS and MASS dataset needs to be further processed after download with the script in:

            - MASS: https://github.com/pquochuy/xsleepnet/tree/master/mass
            - SHHS: https://github.com/pquochuy/SleepTransformer/tree/main/shhs

        Once you obtain the mat/ folder using this processing scripts place them into data_folder/dataset_name/mat/ and run the preprocess command.

        The command can use a .yaml configuration file to specify the preprocessor_kwargs:

        ```yaml
            dataset: null
            data_folder : /path/to/your/data
            preprocessor : physioex.preprocess.hmc:HMCPreprocessor # can be also your custom preprocessor
            preprocessor_kwargs:
                # signal_shape: [4, 3000]
                preprocessors_name:
                    - "your_preprocessor"
                    - "xsleepnet"
                preprocessors:
                    - path.to.your.module:your_preprocessor
                    - physioex.preprocess.utils.signal:xsleepnet_preprocessing
                preprocessors_shape:
                    - [4, 3000]
                    - [4, 3000]
                    - [4, 29, 129]

        ```

    Notes:
        - Ensure that the datasets are properly formatted and stored in the specified data folder using the preprocess script.
        - The configuration file, if provided, should be in YAML format and contain valid key-value pairs for the script options.
    """
    pass
