import glob
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image

from floorplan_analyzer.config.settings import DataConfig
from floorplan_analyzer.data_processing.data_handler_factory import DataHandlerFactory
from floorplan_analyzer.data_processing.training_dataset import TrainingDataset


class DataManager:
    def __init__(self, config: DataConfig) -> None:
        self.factory = DataHandlerFactory()
        self.config = config

    def _extract_file_formats(self) -> dict[str, list[str]]:
        """
        extract the file formats from raw data
        """
        raw_files = defaultdict(list)
        data_path = Path(self.config.raw_data_path)

        for file in glob.glob(str(data_path) + "/*"):
            ext = file.split(".")[-1]
            raw_files[ext].append(file)

        return raw_files

    def _resize_images(self, dataset: list[Image.Image]) -> list[Image.Image]:
        """
        resize image data for batching purposes
        """
        resized_dataset = []
        max_width = max([image["width"] for image in dataset])
        max_height = max([image["height"] for image in dataset])
        center = (max_width // 2, max_height // 2)

        for image_data in dataset:
            old_image = image_data["image"]
            upper_left_corner = (
                center[0] - image_data["width"] // 2,
                center[1] - image_data["height"] // 2,
            )

            new_image = Image.new("RGB", size=(max_width, max_height))
            new_image.paste(old_image, upper_left_corner)
            resized_dataset.append(
                {"filename": image_data["filename"], "image": new_image}
            )
        return resized_dataset

    def process(self, mode: str) -> Any:
        """
        process raw data for model usage
        """
        raw_files = self._extract_file_formats()
        dataset = []

        for file_format in raw_files:
            raw_data = raw_files[file_format]
            handler = self.factory.get_handler(file_format)
            dataset.extend(handler.process(raw_data))

        logging.info(f"Size of dataset: {len(dataset)}")

        dataset = self._resize_images(dataset)
        if mode == "train":
            dataset = TrainingDataset(dataset, self.config.bbox_data_file)

        return dataset
