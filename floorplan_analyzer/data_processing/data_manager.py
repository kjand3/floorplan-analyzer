import glob
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any

from floorplan_analyzer.config.settings import DataConfig
from floorplan_analyzer.data_processing.data_handler_factory import DataHandlerFactory
from floorplan_analyzer.data_processing.training_dataset import TrainingDataset


class DataManager:
    def __init__(self, config: DataConfig) -> None:
        self.factory = DataHandlerFactory()
        self.config = config

    def _extract_file_formats(self) -> dict[str, list[str]]:
        raw_files = defaultdict(list)
        data_path = Path(self.config.raw_data_path)

        for file in glob.glob(str(data_path) + "/*"):
            ext = file.split(".")[-1]
            raw_files[ext].append(file)
        return raw_files

    def process(self, mode: str) -> Any:
        raw_files = self._extract_file_formats()
        dataset = []
        for file_format in raw_files:
            raw_data = raw_files[file_format]
            handler = self.factory.get_handler(file_format)
            dataset.extend(handler.process(raw_data))

        logging.info(f"Size of dataset: {len(dataset)}")

        if mode == "train":
            dataset = TrainingDataset(dataset, self.config.bbox_data_file)

        return dataset
