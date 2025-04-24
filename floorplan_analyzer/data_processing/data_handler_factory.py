from typing import Any

from floorplan_analyzer.data_processing.handlers.image_handler import ImageHandler
from floorplan_analyzer.data_processing.handlers.pdf_handler import PDFHandler


class DataHandlerFactory:
    def __init__(self) -> None:
        self.data_handlers = {
            "pdf": PDFHandler,
            "png": ImageHandler,
            "jpg": ImageHandler,
        }

    def get_handler(self, filetype: str) -> Any:
        """
        extract the file handler based on file type
        """
        if filetype not in self.data_handlers:
            raise ValueError(f"Data processing for {filetype} is not yet supported...")

        return self.data_handlers[filetype]()
