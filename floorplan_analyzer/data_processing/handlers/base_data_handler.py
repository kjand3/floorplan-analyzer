from typing import Any

from PIL import Image


class BaseDataHandler:
    def process(self, data: list[dict[str, Any]]) -> list[Image.Image]:
        """
        base data handler for future format support
        """
        raise NotImplementedError("A process() method must be implemented!")
