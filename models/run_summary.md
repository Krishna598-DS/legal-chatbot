# Fine-tuning Run Summary

## Run Details
- **Run ID:** dab63b95fb6c48cb835e4680bf9c9dd7
- **Date:** 2026-05-08 04:02
- **Job ID:** ftjob-hLTXTU5SlIoZTmmD81YWlNhC
- **Status:** succeeded

## Model
- **Base Model:** gpt-4o-mini-2024-07-18
- **Fine-tuned Model:** ft:gpt-4o-mini-2024-07-18:personal:legal-chatbot:Dd52Ybnu

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
