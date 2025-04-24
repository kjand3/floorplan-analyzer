import logging
from typing import Any

import torch
from torch.nn import Module
from torch.optim import Adam
from torch.utils.data import DataLoader
from tqdm import tqdm

from floorplan_analyzer.config.settings import TrainerConfig


class TrainingPipeline:
    def __init__(self, model: Module, config: TrainerConfig) -> None:
        self.model = model
        self.config = config
        self.optimizer = Adam(
            params=self.model.parameters(), lr=self.config.learning_rate
        )

    def _save_model(self) -> None:
        """
        save trained model
        """
        try:
            torch.save(self.model, self.config.model_output_path)
        except Exception as e:
            logging.error(f"Failed to save trained model: {e}")
            raise

    def train(self, data: Any) -> None:
        """
        train model with specified parameters
        """

        logging.info("Starting model training...")

        data_loader = DataLoader(data, batch_size=self.config.batch_size, shuffle=True)

        self.model.train()
        for epoch in tqdm(range(self.config.total_epochs)):
            for idx, batch in enumerate(data_loader):

                images = batch[0][0]
                targets = {
                    "boxes": batch[1]["boxes"][0],
                    "labels": batch[1]["labels"][0],
                }

                self.optimizer.zero_grad()
                loss_data = self.model([images], [targets])

                loss_classifier = loss_data["loss_classifier"]
                loss_box_reg = loss_data["loss_box_reg"]
                loss_objectness = loss_data["loss_objectness"]
                loss_rpn_box_reg = loss_data["loss_rpn_box_reg"]
                total_loss = (
                    loss_classifier + loss_box_reg + loss_objectness + loss_rpn_box_reg
                )

                total_loss.backward()
                self.optimizer.step()

        logging.info("Training complete, attempting to save model...")
        self._save_model()
        logging.info("Model saved successfully...")
