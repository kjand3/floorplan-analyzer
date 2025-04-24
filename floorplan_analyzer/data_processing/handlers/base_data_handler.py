from typing import Any
from PIL import Image


class BaseDataHandler:
    def process(self, data: list[dict[str, Any]]) -> list[Image.Image]:
        raise NotImplemented("A process() method must be implemented!")
