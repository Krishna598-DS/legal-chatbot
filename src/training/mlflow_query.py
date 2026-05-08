"""
MLflow Query Examples
Shows how to retrieve experiment data programmatically.
This is what production ML pipelines do to select the best model.
"""

import os
import mlflow
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "./mlflow_runs"))
mlflow.set_experiment("legal-chatbot-finetuning")


def show_all_runs():
    """Show all runs in the experiment."""
    runs = mlflow.search_runs(
        experiment_names=["legal-chatbot-finetuning"]
    )
    logger.info(f"Total runs logged: {len(runs)}")
    for _, row in runs.iterrows():
        logger.info(f"  Run ID: {row['run_id'][:8]}...")
        logger.info(f"  Final train loss: {row.get('metrics.final_training_loss', 'N/A')}")
        logger.info(f"  Loss reduction: {row.get('metrics.loss_reduction_pct', 'N/A')}%")
        logger.info(f"  Model ID: {row.get('tags.fine_tuned_model_id', 'N/A')}")
        logger.info("  ---")


def get_best_model_id():
    """
    Get the model ID from the best run.
    In a real pipeline, this feeds directly into deployment.
    """
    runs = mlflow.search_runs(
        experiment_names=["legal-chatbot-finetuning"],
        order_by=["metrics.final_training_loss ASC"],
        max_results=1
    )
    if not runs.empty:
        model_id = runs.iloc[0].get("tags.fine_tuned_model_id", "")
        loss = runs.iloc[0].get("metrics.final_training_loss", "N/A")
        logger.success(f"Best model: {model_id}")
        logger.success(f"Best training loss: {loss}")
        return model_id
    return None


if __name__ == "__main__":
    show_all_runs()
    get_best_model_id()
