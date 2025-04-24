from floorplan_analyzer.config.settings import ModelConfig
from torchvision.models.detection import (
    fasterrcnn_resnet50_fpn,
    FasterRCNN_ResNet50_FPN_Weights,
)
from torch.nn import Module
from typing import List, Any
from PIL import Image
import torch


class Model(Module):
    def __init__(self, config: ModelConfig) -> None:
        super(Model, self).__init__()
        self.config = config
        self.weights = None

        if self.config.pretrained:
            self.weights = FasterRCNN_ResNet50_FPN_Weights.COCO_V1

        self.model = fasterrcnn_resnet50_fpn(weights=self.weights)

    def load_weights(self, model_path: str) -> Module:
        """
        load the weights into the model for inferencing

        args:
        - model_path: path where model is stored
        returns:
        - loaded torch model

        """
        if model_path is None:
            return self.model
        else:
            self.model = torch.load(model_path, weights_only=False)
            # self.model = self.model.load_state_dict(state_dict)
            return self.model

    def forward(self, input: List[Image.Image], target=None) -> List[torch.Tensor]:
        """
        forward pass through the model

        args:
        - input: list of pillow images
        returns:
        - model output

        """
        if self.model.training:
            return self.model(input, target)

        return self.model(input)
