def train():
    """
    Trains a model using the provided datasets and configuration.

    Args:
        datasets (Union[List[str], str, PhysioExDataModule]): The datasets to be used for training. Can be a list of dataset names, a single dataset name, or a PhysioExDataModule instance.
        datamodule_kwargs (dict, optional): Additional keyword arguments to be passed to the PhysioExDataModule. Defaults to {}.
        model (SleepModule, optional): The model to be trained. If provided, `model_class`, `model_config`, and `resume` are ignored. Defaults to None.
        model_class (type, optional): The class of the model to be trained. Required if `model` is not provided. Defaults to None.
        model_config (dict, optional): The configuration dictionary for the model. Required if `model` is not provided. Defaults to None.
        batch_size (int, optional): The batch size to be used for training. Defaults to 128.
        fold (int, optional): The fold index for cross-validation. Defaults to -1.
        hpc (bool, optional): Whether to use high-performance computing (HPC) settings. Defaults to False.
        num_validations (int, optional): The number of validation steps per epoch. Defaults to 10.
        checkpoint_path (str, optional): The path to save the model checkpoints. If None, a new path is generated. Defaults to None.
        max_epochs (int, optional): The maximum number of epochs for training. Defaults to 10.
        num_nodes (int, optional): The number of nodes to be used for distributed training. Defaults to 1.
        resume (bool, optional): Whether to resume training from the last checkpoint. Defaults to True.

    Returns:
        str: The path to the best model checkpoint.

    Raises:
        ValueError: If `datasets` is not a list, a string, or a PhysioExDataModule instance.
        ValueError: If `model` is None and any of `model_class` or `model_config` are also None.

    Notes:
        - The function sets up the data module, model, and trainer, and then starts the training process.
        - If `resume` is True and a checkpoint is found, training resumes from the last checkpoint.
        - The function returns the path to the best model checkpoint based on validation accuracy.
    """
    pass


def test():
    """
    Tests a model using the provided datasets and configuration.

    Args:
        datasets (Union[List[str], str, PhysioExDataModule]): The datasets to be used for testing. Can be a list of dataset names, a single dataset name, or a PhysioExDataModule instance.
        datamodule_kwargs (dict, optional): Additional keyword arguments to be passed to the PhysioExDataModule. Defaults to {}.
        model (SleepModule, optional): The model to be tested. If provided, `model_class`, `model_config`, and `resume` are ignored. Defaults to None.
        model_class (type, optional): The class of the model to be tested. Required if `model` is not provided. Defaults to None.
        model_config (dict, optional): The configuration dictionary for the model. Required if `model` is not provided. Defaults to None.
        batch_size (int, optional): The batch size to be used for testing. Defaults to 128.
        fold (int, optional): The fold index for cross-validation. Defaults to -1.
        hpc (bool, optional): Whether to use high-performance computing (HPC) settings. Defaults to False.
        checkpoint_path (str, optional): The path to the checkpoint from which to load the model. Required if `model` is not provided. Defaults to None.
        results_path (str, optional): The path to save the test results. If None, results are not saved. Defaults to None.
        num_nodes (int, optional): The number of nodes to be used for distributed testing. Defaults to 1.
        aggregate_datasets (bool, optional): Whether to aggregate the datasets for testing. Defaults to False.

    Returns:
        pd.DataFrame: A DataFrame containing the test results.

    Raises:
        ValueError: If `datasets` is not a list, a string, or a PhysioExDataModule instance.
        ValueError: If `model` is None and any of `model_class` or `model_config` are also None.

    Notes:
        - The function sets up the data module, model, and trainer, and then starts the testing process.
        - The function returns a DataFrame containing the test results for each dataset.
        - If `results_path` is provided, the results are saved as a CSV file in the specified path.
    """
    pass


def finetune():
    """
    Fine-tunes a pre-trained model using the provided datasets and configuration.

    Args:
        datasets (Union[List[str], str, PhysioExDataModule]): The datasets to be used for fine-tuning. Can be a list of dataset names, a single dataset name, or a PhysioExDataModule instance.
        datamodule_kwargs (dict, optional): Additional keyword arguments to be passed to the PhysioExDataModule. Defaults to {}.
        model (Union[dict, SleepModule], optional): The model to be fine-tuned. If provided, `model_class`, `model_config`, and `model_checkpoint` are ignored. Defaults to None.
        model_class (type, optional): The class of the model to be fine-tuned. Required if `model` is not provided. Defaults to None.
        model_config (dict, optional): The configuration dictionary for the model. Required if `model` is not provided. Defaults to None.
        model_checkpoint (str, optional): The path to the checkpoint from which to load the model. Required if `model` is not provided. Defaults to None.
        learning_rate (float, optional): The learning rate to be set for fine-tuning. If `None`, the learning rate is not updated. Default is 1e-7.
        weight_decay (Union[str, float], optional): The weight decay to be set for fine-tuning. If `None`, the weight decay is not updated. If "auto", it is set to 10% of the learning rate. Default is "auto".
        train_kwargs (Dict, optional): Additional keyword arguments to be passed to the `train` function. Defaults to {}.

    Returns:
        str: The path of the best model checkpoint.

    Raises:
        ValueError: If `model` is `None` and any of `model_class`, `model_config`, or `model_checkpoint` are also `None`.
        ValueError: If `model` is not a dictionary or a `SleepModule`.

    Notes:
        - Models cannot be fine-tuned from scratch; they must be loaded from a checkpoint or be a pre-trained model from `physioex.models`.
        - Typically, when fine-tuning a model, you want to set up the learning rate.
    """
    pass
