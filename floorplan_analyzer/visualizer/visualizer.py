import json
import logging
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from torch import Tensor


class Visualizer:
    def __init__(self, label_mapping_file: str, output_path: str) -> None:
        self.label_file = self._get_label_mapping(label_mapping_file)
        self.output_path = output_path

    def _get_label_mapping(self, file_path: str) -> dict[str, str]:
        try:
            # load label mapping from json
            with open(file_path, "r") as f:
                label_def = json.load(f)
            return label_def
        except Exception as e:
            logging.error(f"Failed to load label file for object classification: {e}")
            return {}

    def _extract_bbox(self, box: Tensor) -> tuple[float, float, float, float]:
        # extract bounding box coordinates
        x1, y1, x2, y2 = box.detach().numpy()
        width = x2 - x1
        height = y2 - y1
        return x1, y1, width, height

    def visualize(self, result: dict[str, Any]) -> None:
        fig, ax = plt.subplots()
        ax.set_axis_off()
        ax.imshow(result["image"])

        # plot each bounding box on original image
        for pred in result["output"]:
            for label, box in zip(pred["labels"], pred["boxes"]):
                label_name = self.label_file[str(label.detach().numpy())]
                x1, y1, width, height = self._extract_bbox(box)

                bbox = Rectangle(
                    (x1, y1), width=width, height=height, color="red", fill=None
                )
                ax.add_patch(bbox)
                ax.text(x1, y1, label_name)

        # save image w/ bounding boxes locally
        output_filename = result["filename"].split("/")[-1].split(".")[0]
        Path(self.output_path).mkdir(exist_ok=True)
        fig.savefig(f"{self.output_path}{output_filename}.png")
