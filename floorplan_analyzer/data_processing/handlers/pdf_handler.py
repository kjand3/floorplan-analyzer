from floorplan_analyzer.data_processing.handlers.base_data_handler import (
    BaseDataHandler,
)
from typing import Any
from PIL import Image
import logging
import fitz


class PDFHandler(BaseDataHandler):
    def process(self, data: list[dict[str, Any]]) -> list[Image.Image]:
        logging.info("Processing pdf data...")

        processed_data = []
        for file in data:
            pdf_doc = fitz.open(file)
            for page_num, page in enumerate(pdf_doc):
                pdf_pixmap = page.get_pixmap()
                processed_data.append(
                    {"filename": file, "image": pdf_pixmap.pil_image()}
                )
        return processed_data
