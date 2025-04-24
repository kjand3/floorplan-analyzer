from typing import Any, List

from PIL import Image
from torch.nn import Module
from torchvision import transforms

from floorplan_analyzer.config.settings import InferenceConfig
from floorplan_analyzer.visualizer import Visualizer


class InferencePipeline:
    def __init__(self, config: InferenceConfig, model: Module) -> None:
        self.config = config
        self.model = model
        self.image_to_tensor = transforms.ToTensor()
        self.visualizer = Visualizer(
            self.config.label_def_file, self.config.results_output_path
        )
        self.results: list[dict[str, Any]] = []

    def _save_results(self) -> None:
        for pred in self.results:
            if self.config.visualize:
                self.visualizer.visualize(pred)

    def predict(self, input: List[Image.Image]) -> None:
        self.model.eval()

        for image_data in input:
            image_tensor = self.image_to_tensor(image_data["image"])
            output = self.model.forward([image_tensor])
            self.results.append(
                {
                    "filename": image_data["filename"],
                    "image": image_data["image"],
                    "output": output,
                }
            )

        self._save_results()
