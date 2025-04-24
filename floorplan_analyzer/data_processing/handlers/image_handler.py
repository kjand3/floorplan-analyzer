import logging
from typing import Any

from PIL import Image

from floorplan_analyzer.data_processing.handlers.base_data_handler import (
    BaseDataHandler,
)

# reference: https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#Image.convert


class ImageHandler(BaseDataHandler):
    def process(self, data: list[dict[str, Any]]) -> list[Image.Image]:
        """
        process image data (.png and .jpg)
        """
        logging.info("Processing image data...")
        processed_data = []

        for file in data:
            image = Image.open(file)
            if image.mode != "RGB":
                image = image.convert("RGB")
            processed_data.append({"filename": file, "image": image})

        return processed_data
