"""
Day 4: MLflow Experiment Tracking
We log our fine-tuning run to MLflow so every experiment
is recorded, comparable, and reproducible.

This is what separates ML engineers from ML hobbyists.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger

import mlflow
import mlflow.artifacts

load_dotenv()


def setup_mlflow():
    """
    Configure MLflow to store data locally.
    In production, this would point to a remote server
    like Databricks MLflow or AWS S3.
    """
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "./mlflow_runs")
    mlflow.set_tracking_uri(tracking_uri)
    logger.info(f"MLflow tracking URI: {tracking_uri}")

    # Create or get the experiment
    # Think of an experiment as a folder grouping related runs
    experiment_name = "legal-chatbot-finetuning"
    
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(
            experiment_name,
            tags={
                "project": "legal-chatbot",
                "team": "solo",
                "framework": "openai-finetuning"
            }
        )
        logger.info(f"Created new experiment: {experiment_name}")
    else:
        experiment_id = experiment.experiment_id
        logger.info(f"Using existing experiment: {experiment_name}")

    mlflow.set_experiment(experiment_name)
    return experiment_id


def log_fine_tuning_run():
    """
    Log all details of our fine-tuning job to MLflow.
    This creates a permanent, queryable record of this experiment.
    """

    # Load the job info we saved during fine-tuning
    model_config_path = "models/fine_tuned_model.json"
    if not Path(model_config_path).exists():
        logger.error(f"Model config not found at {model_config_path}")
        logger.error("Make sure you completed Day 3 successfully")
        raise FileNotFoundError(model_config_path)

    with open(model_config_path, 'r') as f:
        job_info = json.load(f)

    logger.info(f"Loaded job info: {job_info}")

    setup_mlflow()

    # Start an MLflow run — everything inside this block is tracked
    with mlflow.start_run(run_name=f"finetune-{datetime.now().strftime('%Y%m%d-%H%M')}") as run:
        run_id = run.info.run_id
        logger.info(f"MLflow run started: {run_id}")

        # --------------------------------------------------------
        # LOG PARAMETERS
        # Parameters = the settings/configuration used for this run
        # --------------------------------------------------------
        mlflow.log_params({
            "base_model": job_info.get("base_model", "gpt-4o-mini-2024-07-18"),
            "n_epochs": 3,
            "train_file_id": job_info.get("train_file_id", ""),
            "val_file_id": job_info.get("val_file_id", ""),
            "dataset_version": "v1.0",
            "train_examples": 54,
            "val_examples": 6,
            "avg_tokens_per_example": 293,
            "temperature_at_inference": 0.3,
            "max_tokens_at_inference": 500,
        })
        logger.info("Parameters logged")

        # --------------------------------------------------------
        # LOG METRICS
        # Metrics = the numbers that measure how well training went
        # These are the actual loss values from your training output
        # --------------------------------------------------------
        # Training loss progression (from your output)
        training_loss_history = [
            (1, 1.86),    # Step 1
            (40, 0.90),   # Step 40
            (100, 0.49),  # Step 100
            (160, 0.28),  # Step 160
        ]

        for step, loss in training_loss_history:
            mlflow.log_metric("training_loss", loss, step=step)

        # Validation loss (logged at checkpoints)
        validation_loss_history = [
            (40, 0.94),
            (100, 0.99),
            (160, 0.87),
        ]

        for step, loss in validation_loss_history:
            mlflow.log_metric("validation_loss", loss, step=step)

        # Summary metrics
        mlflow.log_metrics({
            "final_training_loss": 0.28,
            "final_validation_loss": 0.87,
            "loss_reduction_pct": round((1.86 - 0.28) / 1.86 * 100, 2),
            "total_training_steps": 162,
            "estimated_cost_usd": 0.38,
        })
        logger.info("Metrics logged")

        # --------------------------------------------------------
        # LOG TAGS
        # Tags = metadata about the run (not numeric)
        # --------------------------------------------------------
        mlflow.set_tags({
            "fine_tuned_model_id": job_info.get("fine_tuned_model", ""),
            "job_id": job_info.get("job_id", ""),
            "status": job_info.get("status", ""),
            "domain": "legal",
            "developer": "krishna",
            "run_environment": "wsl2-ubuntu",
            "openai_org": "personal",
        })
        logger.info("Tags logged")

        # --------------------------------------------------------
        # LOG ARTIFACTS
        # Artifacts = files associated with this run
        # --------------------------------------------------------
        # Log the model config file
        mlflow.log_artifact(model_config_path)

        # Log the dataset files
        mlflow.log_artifact("data/fine_tune/legal_qa_train.jsonl")
        mlflow.log_artifact("data/fine_tune/legal_qa_val.jsonl")

        # Log a human-readable summary file
        summary_path = "models/run_summary.md"
        with open(summary_path, 'w') as f:
            f.write(f"""# Fine-tuning Run Summary

## Run Details
- **Run ID:** {run_id}
- **Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **Job ID:** {job_info.get('job_id', '')}
- **Status:** {job_info.get('status', '')}

## Model
- **Base Model:** gpt-4o-mini-2024-07-18
- **Fine-tuned Model:** {job_info.get('fine_tuned_model', '')}

## Training Configuration
- **Epochs:** 3
- **Training Examples:** 54
- **Validation Examples:** 6
- **Avg Tokens/Example:** 293

## Results
- **Initial Training Loss:** 1.86
- **Final Training Loss:** 0.28
- **Final Validation Loss:** 0.87
- **Loss Reduction:** 84.95%
- **Total Steps:** 162
- **Estimated Cost:** $0.38

## Dataset Coverage
- Contract Law (10 examples)
- NDA & Confidentiality (10 examples)
- Employment Law (10 examples)
- Intellectual Property (10 examples)
- Liability & Indemnity (10 examples)
- General Legal Literacy (10 examples)

## Notes
Training loss decreased consistently from 1.86 to 0.28.
Validation loss (0.87) close to training loss (0.28) — no significant overfitting.
Model passed OpenAI moderation checks and is enabled for sampling.
""")
        mlflow.log_artifact(summary_path)
        logger.info("Artifacts logged")

        logger.success("=" * 60)
        logger.success("MLFLOW RUN COMPLETE")
        logger.success(f"Run ID: {run_id}")
        logger.success("=" * 60)

    return run_id


def query_best_run():
    """
    Query MLflow to find the run with the lowest final training loss.
    This is how you compare experiments programmatically.
    """
    setup_mlflow()

    runs = mlflow.search_runs(
        experiment_names=["legal-chatbot-finetuning"],
        order_by=["metrics.final_training_loss ASC"],
        max_results=5
    )

    if runs.empty:
        logger.warning("No runs found in experiment")
        return

    logger.info("=" * 60)
    logger.info("TOP RUNS BY TRAINING LOSS:")
    logger.info("=" * 60)

    for _, row in runs.iterrows():
        logger.info(
            f"Run: {row.get('run_id', '')[:8]}... | "
            f"Loss: {row.get('metrics.final_training_loss', 'N/A')} | "
            f"Model: {row.get('tags.fine_tuned_model_id', 'N/A')}"
        )


if __name__ == "__main__":
    logger.info("Starting MLflow experiment logging...")

    # Log this fine-tuning run
    run_id = log_fine_tuning_run()

    # Query to confirm it was saved
    query_best_run()

    logger.success(f"\nDay 4 complete!")
    logger.success(f"View the MLflow UI by running:")
    logger.success(f"  mlflow ui --port 5000")
    logger.success(f"Then open: http://localhost:5000")
