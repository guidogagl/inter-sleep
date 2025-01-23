import torch
import pytorch_lightning as pl


class PhysioExDataset(torch.utils.data.Dataset):
    """
    A PyTorch Dataset class for handling physiological data from multiple datasets.

    Attributes:
        datasets (List[str]): List of dataset names.
        L (int): Sequence length.
        channels_index (List[int]): Indices of selected channels.
        readers (List[DataReader]): List of DataReader objects for each dataset.
        tables (List[pd.DataFrame]): List of data tables for each dataset.
        dataset_idx (np.ndarray): Array indicating the dataset index for each sample.
        target_transform (Callable): Optional transform to be applied to the target.
        len (int): Total number of samples across all datasets.

    Methods:
        __len__(): Returns the total number of samples.
        split(fold: int = -1, dataset_idx: int = -1): Splits the data into train, validation, and test sets.
        get_num_folds(): Returns the minimum number of folds across all datasets.
        __getitem__(idx): Returns the input and target for a given index.
        get_sets(): Returns the indices for the train, validation, and test sets.
    """

    def __init__(self):
        """
        Initializes the PhysioExDataset.

        Args:
            datasets (List[str]): List of dataset names.
            data_folder (str): Path to the folder containing the data.
            preprocessing (str, optional): Type of preprocessing to apply. Defaults to "raw".
            selected_channels (List[int], optional): List of selected channels. Defaults to ["EEG"].
            sequence_length (int, optional): Length of the sequence. Defaults to 21.
            target_transform (Callable, optional): Optional transform to be applied to the target. Defaults to None.
            hpc (bool, optional): Flag indicating whether to use high-performance computing. Defaults to False.
            indexed_channels (List[int], optional): List of indexed channels. Defaults to ["EEG", "EOG", "EMG", "ECG"]. If you used a custom Preprocessor and you saved your signal channels in a different order, you should provide the correct order here. In any other case ignore this parameter.
        """
        pass

    def __len__(self):
        """
        Returns the total number of sequences of epochs across all the datasets.

        Returns:
            int: Total number of sequences.
        """
        pass

    def split(self, fold: int = -1, dataset_idx: int = -1):
        """
        Splits the data into train, validation, and test sets.

        if fold is -1, and dataset_idx is -1 : set the split to a random fold for each dataset
        if fold is -1, and dataset_idx is not -1 : set the split to a random fold for the selected dataset
        if fold is not -1, and dataset_idx is -1 : set the split to the selected fold for each dataset
        if fold is not -1, and dataset_idx is not -1 : set the split to the selected fold for the selected dataset

        Args:
            fold (int, optional): Fold number to use for splitting. Defaults to -1.
            dataset_idx (int, optional): Index of the dataset to split. Defaults to -1.
        """
        pass

    def get_num_folds(self):
        """
        Returns the minimum number of folds across all datasets.

        Returns:
            int: Minimum number of folds.
        """
        pass

    def __getitem__(self, idx):
        """
        Returns the input and target sequence for a given index.

        Args:
            idx (int): Index of the sample to retrieve.

        Returns:
            tuple: Input and target for the given index.
        """
        pass

    def get_sets(self):
        """
        Returns the indices for the train, validation, and test sets.

        Returns:
            tuple: Indices for the train, validation, and test sets.
        """
        pass


class PhysioExDataModule(pl.LightningDataModule):
    """
    A PyTorch Lightning DataModule for handling physiological data from multiple datasets.

    Attributes:
        datasets_id (List[str]): List of dataset names.
        num_workers (int): Number of workers for data loading.
        dataset (PhysioExDataset): The dataset object.
        batch_size (int): Batch size for the DataLoader.
        hpc (bool): Flag indicating whether to use high-performance computing.
        train_dataset (Union[PhysioExDataset, Subset]): Training dataset.
        valid_dataset (Union[PhysioExDataset, Subset]): Validation dataset.
        test_dataset (Union[PhysioExDataset, Subset]): Test dataset.
        train_sampler (Union[SubsetRandomSampler, Subset]): Sampler for the training dataset.
        valid_sampler (Union[SubsetRandomSampler, Subset]): Sampler for the validation dataset.
        test_sampler (Union[SubsetRandomSampler, Subset]): Sampler for the test dataset.

    Methods:
        setup(stage: str): Sets up the datasets for different stages.
        train_dataloader(): Returns the DataLoader for the training dataset.
        val_dataloader(): Returns the DataLoader for the validation dataset.
        test_dataloader(): Returns the DataLoader for the test dataset.
    """

    def __init__(self):
        """
        Initializes the PhysioExDataModule.

        Args:
            datasets (List[str]): List of dataset names.
            batch_size (int, optional): Batch size for the DataLoader. Defaults to 32.
            preprocessing (str, optional): Type of preprocessing to apply. Defaults to "raw".
            selected_channels (List[int], optional): List of selected channels. Defaults to ["EEG"].
            sequence_length (int, optional): Length of the sequence. Defaults to 21.
            target_transform (Callable, optional): Optional transform to be applied to the target. Defaults to None.
            folds (Union[int, List[int]], optional): Fold number(s) for splitting the data. Defaults to -1.
            data_folder (str, optional): Path to the folder containing the data. Defaults to None.
            num_nodes (int, optional): Number of nodes for distributed training. Defaults to 1.
            num_workers (int, optional): Number of workers for data loading. Defaults to os.cpu_count().
        """
        pass

    def train_dataloader(self):
        """
        Returns the DataLoader for the training dataset.

        Returns:
            DataLoader: DataLoader for the training dataset.
        """
        pass

    def val_dataloader(self):
        """
        Returns the DataLoader for the validation dataset.

        Returns:
            DataLoader: DataLoader for the validation dataset.
        """
        pass

    def test_dataloader(self):
        """
        Returns the DataLoader for the test dataset.

        Returns:
            DataLoader: DataLoader for the test dataset.
        """
        pass
