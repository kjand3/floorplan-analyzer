from typing import Any, List

import torch
from PIL import Image
from torch.nn import Module
from torchvision.models.detection import (
    FasterRCNN_ResNet50_FPN_Weights,
    fasterrcnn_resnet50_fpn,
)

from floorplan_analyzer.config.settings import ModelConfig


class Model(Module):
    def __init__(self, config: ModelConfig) -> None:
        super(Model, self).__init__()
        self.config = config
        self.weights = None

        if self.config.pretrained:
            self.weights = FasterRCNN_ResNet50_FPN_Weights.COCO_V1

        self.model = fasterrcnn_resnet50_fpn(weights=self.weights)

    def load_weights(self, model_path: str | None) -> Module:
        """
        load pretrained weights
        """
        if model_path is not None:
            self.model = torch.load(model_path, weights_only=False)
        return self.model

    def forward(
        self, input: List[Image.Image], target: dict[str, Any] | None = None
    ) -> List[torch.Tensor]:
        """
        define forward method based on model mode
        """
        if self.model.training:
            return self.model(input, target)

        return self.model(input)
