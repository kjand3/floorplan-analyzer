from floorplan_analyzer.data_processing.handlers.base_data_handler import (
    BaseDataHandler,
)
from PIL import Image
from typing import Any
import logging


class ImageHandler(BaseDataHandler):
    def process(self, data: list[dict[str, Any]]) -> list[Image.Image]:
        logging.info("Processing image data...")

        processed_data = []
        for file in data:
            image = Image.open(file)
            # https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#Image.convert
            if image.mode != "RGB":
                image = image.convert("RGB")

            processed_data.append({"filename": file, "image": image})

        return processed_data
