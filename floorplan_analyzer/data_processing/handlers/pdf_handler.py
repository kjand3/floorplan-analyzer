import logging
from typing import Any

import fitz
from PIL import Image

from floorplan_analyzer.data_processing.handlers.base_data_handler import (
    BaseDataHandler,
)


class PDFHandler(BaseDataHandler):
    def process(self, data: list[dict[str, Any]]) -> list[Image.Image]:
        """
        process pdf data (.pdf)
        """
        logging.info("Processing pdf data...")
        processed_data = []

        for file in data:
            pdf_doc = fitz.open(file)
            for page in pdf_doc:
                pdf_pixmap = page.get_pixmap()
                image = pdf_pixmap.pil_image()
                processed_data.append(
                    {
                        "filename": file,
                        "image": image,
                        "width": image.size[0],
                        "height": image.size[1],
                    }
                )

        return processed_data
