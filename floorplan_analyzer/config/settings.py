from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


# ------------------------
# Tool Mode Configuration
# ------------------------
class ModeEnum(str, Enum):
    TRAIN = "train"
    INFERENCE = "inference"


# ------------------------
# Data Configuration
# ------------------------
class DataConfig(BaseSettings):
    raw_data_path: str = Field(
        default="data/train/floorplans/", description="Data path"
    )
    file_format: str = Field(default="pdf", description="File extension for input data")
    bbox_data_file: str = Field(
        default="data/train/train.csv", description="Bounding box csv file for training"
    )


# ------------------------
# Model Configuration
# ------------------------
class ModelConfig(BaseSettings):
    pretrained: bool = Field(default=True, description="Pretrained weights for model")


# ------------------------
# Training Configuration
# ------------------------
class TrainerConfig(BaseSettings):
    total_epochs: int = Field(default=2, description="Number of training epochs")
    optimizer: str = Field(default="adam", description="Model training optimizer")
    batch_size: int = Field(default=2, description="Batch size")
    learning_rate: float = Field(
        default=0.0001, description="Learning rate for training"
    )
    model_output_path: str = Field(
        default="model_output_path", description="Output path for trained model"
    )


# ------------------------
# Inference Configuration
# ------------------------
class InferenceConfig(BaseSettings):
    label_mapping_file: str = Field(
        default="floorplan_analyzer/config/label_definition.json",
        description="Label definition for object detection",
    )
    trained_model_path: str | None = Field(
        default=None, description="Trained model path"
    )
    results_output_path: str = Field(
        default="results_output/", description="Output path for inference results"
    )


# ------------------------
# General Configuration
# ------------------------
class Settings(BaseSettings):
    mode: ModeEnum = Field(default=ModeEnum.TRAIN, description="Detector mode")
    mod_config: ModelConfig = ModelConfig()
    data_config: DataConfig = DataConfig()
    trainer_config: TrainerConfig = TrainerConfig()
    inference_config: InferenceConfig = InferenceConfig()


settings = Settings()
