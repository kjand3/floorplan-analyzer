from floorplan_analyzer.data_processing.handlers.pdf_handler import PDFHandler
from floorplan_analyzer.data_processing.handlers.image_handler import ImageHandler
from typing import Any


class DataHandlerFactory:
    def __init__(self):
        self.data_handlers = {
            "pdf": PDFHandler,
            "png": ImageHandler,
            "jpg": ImageHandler,
        }

    def get_handler(self, filetype: str) -> Any:
        if filetype not in self.data_handlers:
            raise ValueError(f"Data processing for {filetype} is not yet supported...")

        return self.data_handlers[filetype]()
