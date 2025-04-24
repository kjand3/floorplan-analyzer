from pydantic_settings import BaseSettings
from pydantic import Field
from enum import Enum


class ModeEnum(str, Enum):
    TRAIN = "train"
    INFERENCE = "inference"


class DataConfig(BaseSettings):
    raw_data_path: str = Field(
        default="data/train/floorplans/", description="Data path"
    )
    file_format: str = Field(default="pdf", description="File extension for input data")
    bbox_data_file: str = Field(
        default="data/train/train.csv", description="Bounding box csv file for training"
    )


class ModelConfig(BaseSettings):
    pretrained: bool = Field(default=True, description="Pretrained weights for model")
    model_name: str = Field(default="fasterrcnn", description="Model name")


class TrainerConfig(BaseSettings):
    total_epochs: int = Field(default=2, description="Number of training epochs")
    optimizer: str = Field(default="adam", description="Model training optimizer")
    batch_size: int = Field(default=1, description="Batch size")
    learning_rate: float = Field(
        default=0.0001, description="Learning rate for training"
    )
    model_output_path: str = Field(
        default="model_output_path", description="Output path for trained model"
    )


class InferenceConfig(BaseSettings):
    label_def_file: str = Field(
        default="floorplan_analyzer/config/label_definition.json",
        description="Label definition for object detection",
    )
    trained_model_path: str | None = Field(
        default=None, description="Trained model path"
    )
    visualize: bool = Field(default=True, description="Visualize results")
    results_output_path: str = Field(default="results_output/")


class Settings(BaseSettings):
    mode: ModeEnum = Field(default=ModeEnum.TRAIN, description="Detector mode")
    mod_config: ModelConfig = ModelConfig()
    data_config: DataConfig = DataConfig()
    trainer_config: TrainerConfig = TrainerConfig()
    inference_config: InferenceConfig = InferenceConfig()


settings = Settings()
