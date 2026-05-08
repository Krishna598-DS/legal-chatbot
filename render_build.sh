#!/bin/bash
pip install -r requirements.txt
mkdir -p models
cat > models/fine_tuned_model.json << 'JSONEOF'
{
  "job_id": "ftjob-hLTXTU5SlIoZTmmD81YWlNhC",
  "base_model": "gpt-4o-mini-2024-07-18",
  "train_file_id": "file-YK7V41zQ7SmTrffxNaet3d",
  "val_file_id": "file-Pon9jKGEdpgURFG3v6efEk",
  "status": "succeeded",
  "fine_tuned_model": "ft:gpt-4o-mini-2024-07-18:personal:legal-chatbot:Dd52Ybnu"
}
JSONEOF
echo "Build complete. Model config written."
