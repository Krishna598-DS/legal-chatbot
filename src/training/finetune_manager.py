"""
Day 3: OpenAI Fine-tuning Manager
This script handles the complete fine-tuning lifecycle:
1. Upload training and validation files to OpenAI
2. Create the fine-tuning job
3. Monitor job progress
4. Save the fine-tuned model ID for later use

The model ID produced here is used in every subsequent day.
"""

import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger

load_dotenv()


class FineTuningManager:
    """
    Manages the complete OpenAI fine-tuning lifecycle.
    Encapsulating this in a class is a design pattern
    interviewers look for — it shows you think in systems.
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_config_path = "models/fine_tuned_model.json"
        Path("models").mkdir(exist_ok=True)

    # ----------------------------------------------------------
    # STEP 1: UPLOAD FILES
    # ----------------------------------------------------------
    def upload_file(self, filepath: str, purpose: str = "fine-tune") -> str:
        """
        Upload a JSONL file to OpenAI's servers.
        'purpose' must be 'fine-tune' for training files.
        Returns the file_id OpenAI assigns.
        """
        logger.info(f"Uploading {filepath} to OpenAI...")

        with open(filepath, "rb") as f:
            response = self.client.files.create(
                file=f,
                purpose=purpose
            )

        file_id = response.id
        logger.success(f"Uploaded: {filepath} -> file_id: {file_id}")
        return file_id

    # ----------------------------------------------------------
    # STEP 2: CREATE FINE-TUNING JOB
    # ----------------------------------------------------------
    def create_fine_tuning_job(
        self,
        train_file_id: str,
        val_file_id: str,
        base_model: str = "gpt-4o-mini-2024-07-18",
        n_epochs: int = 3,
        suffix: str = "legal-chatbot"
    ) -> str:
        """
        Create the fine-tuning job on OpenAI.

        Parameters:
        - base_model: The model we start from. gpt-4o-mini is cheapest.
        - n_epochs: How many full passes through the training data.
                    More epochs = more training = higher cost + risk of overfitting.
        - suffix: A label appended to your model name so you can identify it.
        Returns the job_id.
        """
        logger.info(f"Creating fine-tuning job on base model: {base_model}")
        logger.info(f"Training for {n_epochs} epochs")

        job = self.client.fine_tuning.jobs.create(
            training_file=train_file_id,
            validation_file=val_file_id,
            model=base_model,
            hyperparameters={
                "n_epochs": n_epochs
            },
            suffix=suffix
        )

        job_id = job.id
        logger.success(f"Fine-tuning job created: {job_id}")
        logger.info(f"Status: {job.status}")

        # Save job info immediately
        self._save_job_info({
            "job_id": job_id,
            "base_model": base_model,
            "train_file_id": train_file_id,
            "val_file_id": val_file_id,
            "status": job.status,
            "created_at": job.created_at,
            "fine_tuned_model": None
        })

        return job_id

    # ----------------------------------------------------------
    # STEP 3: MONITOR JOB
    # ----------------------------------------------------------
    def monitor_job(self, job_id: str, poll_interval_seconds: int = 60) -> str:
        """
        Poll the fine-tuning job status until completion.
        Fine-tuning typically takes 10-30 minutes for small datasets.

        Returns the fine-tuned model ID when complete.
        """
        logger.info(f"Monitoring job {job_id}...")
        logger.info(f"Polling every {poll_interval_seconds} seconds.")
        logger.info("Fine-tuning typically takes 10-30 minutes. You can also")
        logger.info("check status at: https://platform.openai.com/finetune")

        terminal_states = {"succeeded", "failed", "cancelled"}

        while True:
            job = self.client.fine_tuning.jobs.retrieve(job_id)
            status = job.status

            logger.info(f"Status: {status} | Job: {job_id}")

            # Print recent events (training loss updates)
            events = self.client.fine_tuning.jobs.list_events(
                fine_tuning_job_id=job_id,
                limit=3
            )
            for event in reversed(events.data):
                logger.info(f"  Event: {event.message}")

            if status in terminal_states:
                break

            time.sleep(poll_interval_seconds)

        if status == "succeeded":
            model_id = job.fine_tuned_model
            logger.success("=" * 60)
            logger.success("FINE-TUNING SUCCEEDED!")
            logger.success(f"Fine-tuned model ID: {model_id}")
            logger.success("=" * 60)

            # Save the model ID — this is used in Day 7
            self._save_job_info({
                "job_id": job_id,
                "status": "succeeded",
                "fine_tuned_model": model_id,
                "finished_at": job.finished_at
            })

            return model_id

        else:
            logger.error(f"Fine-tuning {status}.")
            logger.error(f"Check details at: https://platform.openai.com/finetune/{job_id}")
            raise RuntimeError(f"Fine-tuning job {status}")

    # ----------------------------------------------------------
    # STEP 4: TEST THE FINE-TUNED MODEL
    # ----------------------------------------------------------
    def test_fine_tuned_model(self, model_id: str) -> str:
        """
        Send a test legal question to the fine-tuned model
        to verify it responds correctly.
        """
        logger.info(f"Testing fine-tuned model: {model_id}")

        response = self.client.chat.completions.create(
            model=model_id,
            messages=[
                {
                    "role": "user",
                    "content": "What is the difference between a void and voidable contract?"
                }
            ],
            max_tokens=300,
            temperature=0.3
        )

        reply = response.choices[0].message.content
        logger.success("Test response received:")
        logger.info(f"\n{reply}")
        return reply

    # ----------------------------------------------------------
    # UTILITY: SAVE/LOAD JOB INFO
    # ----------------------------------------------------------
    def _save_job_info(self, data: dict):
        """Save job info to disk so we can resume if script restarts."""
        existing = {}
        if Path(self.model_config_path).exists():
            with open(self.model_config_path, 'r') as f:
                existing = json.load(f)
        existing.update(data)
        with open(self.model_config_path, 'w') as f:
            json.dump(existing, f, indent=2)
        logger.info(f"Job info saved to {self.model_config_path}")

    def load_job_info(self) -> dict:
        """Load previously saved job info."""
        if Path(self.model_config_path).exists():
            with open(self.model_config_path, 'r') as f:
                return json.load(f)
        return {}

    def list_my_models(self):
        """List all fine-tuned models in your OpenAI account."""
        logger.info("Your fine-tuned models:")
        jobs = self.client.fine_tuning.jobs.list(limit=10)
        for job in jobs.data:
            logger.info(
                f"  Job: {job.id} | "
                f"Status: {job.status} | "
                f"Model: {job.fine_tuned_model or 'pending'}"
            )


# ----------------------------------------------------------
# RESUME MONITOR (if you need to reconnect to a running job)
# ----------------------------------------------------------
def resume_monitoring(job_id: str):
    """
    Use this if your terminal closed while a job was running.
    Just call: python src/training/finetune_manager.py resume <job_id>
    """
    manager = FineTuningManager()
    logger.info(f"Resuming monitoring for job: {job_id}")
    model_id = manager.monitor_job(job_id, poll_interval_seconds=30)
    manager.test_fine_tuned_model(model_id)


# ----------------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------------
if __name__ == "__main__":
    import sys

    manager = FineTuningManager()

    # If called with 'resume <job_id>', resume monitoring
    if len(sys.argv) == 3 and sys.argv[1] == "resume":
        resume_monitoring(sys.argv[2])
        sys.exit(0)

    # If called with 'list', show existing models
    if len(sys.argv) == 2 and sys.argv[1] == "list":
        manager.list_my_models()
        sys.exit(0)

    # Otherwise run the full pipeline
    logger.info("Starting full fine-tuning pipeline...")

    # Step 1: Upload files
    train_file_id = manager.upload_file("data/fine_tune/legal_qa_train.jsonl")
    val_file_id = manager.upload_file("data/fine_tune/legal_qa_val.jsonl")

    # Step 2: Create job
    job_id = manager.create_fine_tuning_job(
        train_file_id=train_file_id,
        val_file_id=val_file_id,
        n_epochs=3,
        suffix="legal-chatbot"
    )

    logger.info(f"\nJob ID saved. If this terminal closes, resume with:")
    logger.info(f"python src/training/finetune_manager.py resume {job_id}")

    # Step 3: Monitor until done
    model_id = manager.monitor_job(job_id, poll_interval_seconds=60)

    # Step 4: Test it
    manager.test_fine_tuned_model(model_id)

    logger.success(f"\nDay 3 complete! Your fine-tuned model ID: {model_id}")
    logger.success(f"This ID is saved at: models/fine_tuned_model.json")
    logger.success("Keep this ID — you will use it every day from Day 7 onwards.")
