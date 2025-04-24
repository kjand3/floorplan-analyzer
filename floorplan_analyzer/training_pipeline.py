from floorplan_analyzer.config.settings import TrainerConfig
from torch.utils.data import DataLoader
from torch.optim import Adam
from torch.nn import Module
from typing import List
from PIL import Image
import torch
import logging
import numpy as np
from tqdm import tqdm


class TrainingPipeline:
    def __init__(self, model: Module, config: TrainerConfig) -> None:
        self.model = model
        self.config = config
        self.optimizer = Adam(
            params=self.model.parameters(), lr=self.config.learning_rate
        )

    def _save_model(self) -> None:
        torch.save(self.model, self.config.model_output_path)

    def train(self, data) -> None:
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
