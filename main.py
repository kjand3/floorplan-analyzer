import argparse
import logging

import yaml

from floorplan_analyzer.config.settings import ModeEnum, Settings, settings
from floorplan_analyzer.data_processing.data_manager import DataManager
from floorplan_analyzer.inference_pipeline import InferencePipeline
from floorplan_analyzer.models.model import Model
from floorplan_analyzer.training_pipeline import TrainingPipeline

logging.basicConfig(level=logging.INFO)


def run(settings: Settings) -> None:

    # Initialize model
    model = Model(settings.mod_config)

    # Initialize and preprocess data
    data_manager = DataManager(settings.data_config)
    processed_data = data_manager.process(settings.mode)

    # Run model in selected mode
    if settings.mode == ModeEnum.INFERENCE:
        logging.info("Running Floorplan Anlayzer in INFERENCE mode...")
        model = model.load_weights(settings.inference_config.trained_model_path)
        inference_pipeline = InferencePipeline(settings.inference_config, model)
        inference_pipeline.predict(processed_data)
        output_dir = settings.inference_config.results_output_path
        logging.info(f"Inferencing complete!\n\nModel results located in: {output_dir}")

    elif settings.mode == ModeEnum.TRAIN:
        logging.info("Running Floorplan Anlayzer in TRAIN mode...")
        training_pipeline = TrainingPipeline(model, settings.trainer_config)
        training_pipeline.train(processed_data)

        logging.info("Training complete!")

    else:
        raise ValueError(f"Selected mode {settings.mode} is not supported...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Floorplan Analyzer")
    parser.add_argument("--data_path", type=str, help="Data path for model inferencing")
    parser.add_argument("--mode", type=str, help="Mode for running tool")
    parser.add_argument("--config", type=str, help="Configuration for model execution")
    args = parser.parse_args()

    # Configure run from command line args
    if args.config is not None:
        logging.info("Configuration file was passed all other flags will be ignored...")
        with open(args.config, "r") as f:
            yaml_config = yaml.safe_load(f)
        custom_settings = Settings(**yaml_config)
        run(custom_settings)
    else:
        if args.data_path is not None:
            settings.data_config.raw_data_path = args.data_path
        if args.mode is not None:
            settings.mode = ModeEnum(args.mode)
        run(settings)
