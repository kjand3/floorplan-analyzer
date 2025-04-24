from matplotlib.patches import Rectangle
from typing import Any
from pathlib import Path
import matplotlib.pyplot as plt
import json


class Visualizer:
    def __init__(self, label_def_file: str, output_path: str) -> None:
        self.label_file = self._get_label_def(label_def_file)
        self.output_path = output_path

    def _get_label_def(self, file_path: str) -> dict[int, str]:
        with open(file_path, "r") as f:
            label_def = json.load(f)
        return label_def

    def _extract_bbox(self, box: list[float]) -> tuple[float]:
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        bl_x = ((x1 + x2) / 2).detach().numpy()
        bl_y = ((y1 + y2) / 2).detach().numpy()
        width = (x2 - x1).detach().numpy()
        height = (y2 - y1).detach().numpy()
        return bl_x, bl_y, width, height

    def visualize(self, result: dict[str, Any]) -> None:
        fig, ax = plt.subplots()
        ax.set_axis_off()
        ax.imshow(result["image"])

        for pred in result["output"]:
            for label, box in zip(pred["labels"], pred["boxes"]):
                label_name = self.label_file[str(label.detach().numpy())]
                bl_x, bl_y, width, height = self._extract_bbox(box)

                bbox = Rectangle(
                    (bl_x, bl_y), width=width, height=height, color="red", fill=None
                )
                ax.add_patch(bbox)
                ax.text(bl_x, bl_y, label_name)

        output_filename = result["filename"].split("/")[-1].split(".")[0]
        Path(self.output_path).mkdir(exist_ok=True)
        fig.savefig(f"{self.output_path}{output_filename}.png")
