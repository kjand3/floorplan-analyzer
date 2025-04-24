from floorplan_analyzer.data_processing.data_manager import DataManager
from floorplan_analyzer.models.model import Model
from floorplan_analyzer.training_pipeline import TrainingPipeline
from floorplan_analyzer.inference_pipeline import InferencePipeline
from floorplan_analyzer.config.settings import settings
import logging
import argparse

# import yaml

logging.basicConfig(level=logging.INFO)


def run(data_path: str | None = None) -> None:

    # Initialize model
    model = Model(settings.mod_config)

    if data_path is not None:
        settings.data_config.raw_data_path = data_path

    # Initialize and preprocess data
    data_manager = DataManager(settings.data_config)
    processed_data = data_manager.process(settings.mode)

    # Run model in selected mode
    if settings.mode == "inference":
        logging.info("Running Floorplan Anlayzer in INFERENCE mode...")
        model = model.load_weights(settings.inference_config.trained_model_path)
        inference_pipeline = InferencePipeline(settings.inference_config, model)
        inference_pipeline.predict(processed_data)
        output_dir = settings.inference_config.results_output_path
        logging.info(f"Inferencing complete!\n\nModel results located in: {output_dir}")

    elif settings.mode == "train":
        logging.info("Running Floorplan Anlayzer in TRAIN mode...")
        training_pipeline = TrainingPipeline(model, settings.trainer_config)
        training_pipeline.train(processed_data)

        logging.info("Training complete!")

    else:
        raise ValueError(f"Selected mode {settings.mode} is not supported...")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="Floorplan Analyzer")
    parser.add_argument("--data_path", type=str, help="Data path for model inferencing")

    parser.add_argument(
        "--config_file", type=str, help="Configuration file for analysis"
    )

    args = parser.parse_args()
    run(args.data_path)
