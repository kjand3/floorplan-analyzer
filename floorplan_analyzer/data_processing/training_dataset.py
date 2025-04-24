from typing import Any

import numpy as np
import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


class TrainingDataset(Dataset):
    def __init__(self, images: list[Image.Image], bbox_data: str) -> None:
        self.images = images
        self.bbox_data = pd.read_csv(bbox_data)
        self.image_to_tensor = transforms.ToTensor()

    def __len__(self) -> int:
        """
        get dataset length
        """
        return len(self.images)

    def __getitem__(self, index: int) -> tuple[Image.Image, dict[str, Any]]:
        """
        get data file from training dataset
        """
        image_fn = self.images[index]["filename"]
        image = self.images[index]["image"]
        matches = self.bbox_data.loc[self.bbox_data["filename"] == image_fn]
        boxes = torch.from_numpy(np.array(matches[["x1", "y1", "x2", "y2"]]))
        labels = torch.from_numpy(np.array(matches[["label"]])).view(-1)

        target = {
            "boxes": boxes,
            "labels": labels,
        }

        image = self.image_to_tensor(image)
        return image, target
