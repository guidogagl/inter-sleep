import pytorch_lightning as pl


class SleepModule(pl.LightningModule):
    """
    A PyTorch Lightning module for sleep stage classification and regression tasks.

    This module is designed to handle both classification and regression experiments for sleep stage analysis. It leverages PyTorch Lightning for training, validation, and testing, and integrates various metrics for performance evaluation.

    Parameters:
        `nn` (nn.Module): The neural network model to be used for sleep stage analysis.
        `config` (Dict): A dictionary containing configuration parameters for the module. Must include:
            - `n_classes` (int): The number of classes for classification tasks. If `n_classes` is 1, the module performs regression.
            - `loss_call` (callable): A callable that returns the loss function.
            - `loss_params` (dict): A dictionary of parameters to be passed to the loss function.

    Attributes:
        `nn` (nn.Module): The neural network model.
        `n_classes` (int): The number of classes for classification tasks.
        `loss` (callable): The loss function.
        `module_config` (Dict): The configuration dictionary.
        `learning_rate` (float): The learning rate for the optimizer. Default is 1e-4.
        `weight_decay` (float): The weight decay for the optimizer. Default is 1e-6.
        `val_loss` (float): The best validation loss observed during training.

    Example:
        ```python
        import torch.nn as nn
        from your_module import SleepModule

        config = {
            "n_classes": 5,
            "loss_call": nn.CrossEntropyLoss,
            "loss_params": {}
        }

        model = SleepModule(nn=YourNeuralNetwork(), config=config)
        ```

    Notes:
        - This module supports both classification and regression tasks. The behavior is determined by the `n_classes` argument of the config dictionary.
        - Various metrics are logged during training, validation, and testing to monitor performance.
        - The learning rate scheduler is configured to reduce the learning rate when the validation loss plateaus.

    """

    def configure_optimizers(self):
        """
        Configures the optimizer and learning rate scheduler.

        Returns:
            Tuple[List[Optimizer], List[Dict]]: A tuple containing the optimizer and the learning rate scheduler.
        """
        pass

    def forward(self, x):
        """
        Defines the forward pass of the neural network.

        Parameters:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The output tensor.
        """
        pass

    def encode(self, x):
        """
        Encodes the input data using the neural network.

        Parameters:
            x (torch.Tensor): The input tensor.

        Returns:
            torch.Tensor: The encoded tensor.
        """
        pass

    def compute_loss(
        self,
    ):
        """
        Computes the loss and logs metrics.

        Parameters:
            embeddings (torch.Tensor): The embeddings tensor.
            outputs (torch.Tensor): The outputs tensor.
            targets (torch.Tensor): The targets tensor.
            log (str, optional): The log prefix. Defaults to "train".
            log_metrics (bool, optional): Whether to log additional metrics. Defaults to False.

        Returns:
            torch.Tensor: The computed loss.
        """
        pass

    def training_step(self, batch, batch_idx):
        """
        Defines a single training step.

        Parameters:
            batch (Tuple[torch.Tensor, torch.Tensor]): The input batch.
            batch_idx (int): The index of the batch.

        Returns:
            torch.Tensor: The computed loss.
        """
        pass

    def validation_step(self, batch, batch_idx):
        """
        Defines a single validation step.

        Parameters:
            batch (Tuple[torch.Tensor, torch.Tensor]): The input batch.
            batch_idx (int): The index of the batch.

        Returns:
            torch.Tensor: The computed loss.
        """
        pass

    def test_step(self, batch, batch_idx):
        """
        Defines a single test step.

        Parameters:
            batch: The input batch.
            batch_idx (int): The index of the batch.

        Returns:
            torch.Tensor: The computed loss.
        """
        pass
