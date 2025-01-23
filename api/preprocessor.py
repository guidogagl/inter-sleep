class Preprocessor:
    def __init__(self):
        """
        Initializes the Preprocessor class.

        Parameters:
            dataset_name (str):
                The name of the dataset to be processed.
            signal_shape (List[int]):
                A list containing two elements representing the number of channels and the number of timestamps in the signal.
            preprocessors_name (List[str]):
                A list of names for the preprocessing functions.
            preprocessors (List[Callable]):
                A list of callable preprocessing functions to be applied to the signals.
            preprocessors_shape (List[List[int]]):
                A list of shapes corresponding to the output of each preprocessing function.
            data_folder (str, optional):
                The folder where the dataset is stored. If None, the default data folder is used.
        """
        pass

    def download_dataset(self):
        """
        Downloads the dataset if it is not already present on disk.

        (Optional) Method to be implemented by the user.
        """
        pass

    def get_subjects_records(self):
        """
        Returns a list containing the paths to each subject's record.

        (Required) Method to be implemented by the user.

        Returns:
            List[str] : A list of paths to each subject's record.
        """
        pass

    def read_subject_record(self):
        """
        Reads a subject's record and returns a tuple containing the signal and labels.

        (Required) Method should be provided by the user.

        Parameters:
            record (str): The path to the subject's record.

        Returns:
            Tuple[np.array, np.array]: A tuple containing the signal and labels with shapes [n_windows, n_channels, n_timestamps] and [n_windows], respectively. If the record should be skipped, the function should return None, None.
        """
        pass

    def customize_table(self):
        """
        Customizes the dataset table before saving it.

        (Optional) Method to be provided by the user.

        Parameters:
            table (pd.DataFrame): The dataset table to be customized.

        Returns:
            pd.DataFrame: The customized dataset table.
        """
        pass

    def get_sets(self):
        """
        Returns the train, validation, and test subjects.

        (Optional) Method to be provided by the user. By default, the method splits the subjects randomly with 70% for training, 15% for validation, and 15% for testing.

        Returns:
            Tuple[List, List, List]: A tuple containing the train, validation, and test subjects.
        """
        pass
