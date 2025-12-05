# MLflow + BERT Training Guide

## Quick Start: Train BERT on IMDB Dataset

```bash
python mlops/train_bert_custom.py \
    --dataset imdb \
    --model_name bert-base-uncased \
    --epochs 3 \
    --batch_size 8 \
    --learning_rate 2e-5 \
    --experiment_name "bert-imdb-baseline"
```

Expected output:
```
Loading dataset: imdb
Loading and preprocessing dataset...
Tokenizing...
Loading model: bert-base-uncased
Starting training...
Training completed. Model saved to runs/bert-custom
MLflow run: bert-imdb-baseline-20241204_120000
```

## Using Your Own Data

### CSV Format

Create a CSV file with text and label columns:

```csv
text,label
"This movie was great",1
"I did not like it",0
"Amazing performance!",1
```

Train:

```bash
python mlops/train_bert_custom.py \
    --data_file path/to/your_data.csv \
    --text_column text \
    --label_column label \
    --model_name bert-base-uncased \
    --epochs 5 \
    --batch_size 16 \
    --experiment_name "bert-custom-data"
```

### JSON Format

```json
[
  {"text": "This movie was great", "label": 1},
  {"text": "I did not like it", "label": 0}
]
```

Train:

```bash
python mlops/train_bert_custom.py \
    --data_file path/to/your_data.json \
    --text_column text \
    --label_column label \
    --num_labels 2 \
    --experiment_name "bert-json-data"
```

## Advanced Configuration

### Multi-GPU Training

```bash
python mlops/train_bert_custom.py \
    --dataset imdb \
    --model_name bert-base-uncased \
    --batch_size 16 \
    --gradient_accumulation_steps 2 \
    --device cuda \
    --experiment_name "bert-multi-gpu"
```

### Different Models

```bash
# RoBERTa (more robust)
python mlops/train_bert_custom.py \
    --dataset glue \
    --model_name roberta-base \
    --epochs 3 \
    --experiment_name "roberta-glue"

# DistilBERT (faster, smaller)
python mlops/train_bert_custom.py \
    --dataset imdb \
    --model_name distilbert-base-uncased \
    --batch_size 32 \
    --epochs 3 \
    --experiment_name "distilbert-imdb"

# BERT Large (better quality, slower)
python mlops/train_bert_custom.py \
    --dataset glue \
    --model_name bert-large-uncased \
    --batch_size 4 \
    --learning_rate 1e-5 \
    --epochs 2 \
    --experiment_name "bert-large-glue"
```

### Fine-tune on Custom Tasks

```bash
# Multi-class classification (5 classes)
python mlops/train_bert_custom.py \
    --data_file sentiment_5class.json \
    --num_labels 5 \
    --model_name bert-base-uncased \
    --learning_rate 2e-5 \
    --epochs 4 \
    --experiment_name "bert-5class-sentiment"

# With early stopping and checkpointing
python mlops/train_bert_custom.py \
    --data_file your_data.csv \
    --model_name bert-base-uncased \
    --epochs 10 \
    --eval_steps 100 \
    --save_steps 100 \
    --patience 2 \
    --experiment_name "bert-early-stopping"
```

## View MLflow Experiments

### Start MLflow UI

```bash
mlflow ui --backend-store-uri runs/mlflow
```

Then open `http://localhost:5000` in your browser.

### Or use command line to query

```bash
# List experiments
mlflow experiments list --backend-store-uri runs/mlflow

# List runs in an experiment
mlflow runs list --experiment-name "bert-imdb-baseline" --backend-store-uri runs/mlflow

# Get run details
mlflow runs show <RUN_ID> --backend-store-uri runs/mlflow
```

## Logged Metrics & Parameters

Each MLflow run automatically logs:

**Parameters:**
- `model_name` — pretrained model
- `dataset` — dataset source
- `epochs`, `batch_size`, `learning_rate` — hyperparameters
- `warmup_steps`, `weight_decay` — training settings

**Metrics (logged per epoch):**
- `train_loss` — training loss
- `eval_loss` — validation loss
- `eval_accuracy` — validation accuracy
- `eval_precision`, `eval_recall`, `eval_f1` — precision, recall, F1 score

**Artifacts:**
- `model/` — trained model files (pytorch_model.bin, config.json, tokenizer files)
- `training_results.json` — final training metrics

## Comparing Runs

### Via MLflow UI

1. Open MLflow UI (`mlflow ui ...`)
2. Click "Experiments" → select experiment
3. Check boxes on runs to compare
4. View side-by-side metrics and parameters

### Via Python Script

```python
import mlflow
from mlflow.entities import ViewType

mlflow.set_tracking_uri("runs/mlflow")
client = mlflow.tracking.MlflowClient()

# Get experiment
exp = client.get_experiment_by_name("bert-imdb-baseline")
runs = client.search_runs(
    experiment_ids=[exp.experiment_id],
    order_by=["metrics.eval_f1 DESC"],
    max_results=10
)

for run in runs:
    print(f"Run: {run.info.run_name}")
    print(f"  F1: {run.data.metrics.get('eval_f1', 'N/A')}")
    print(f"  LR: {run.data.params.get('learning_rate', 'N/A')}")
```

## Using the Trained Model

After training, use your model:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load model
model_path = "runs/bert-custom"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Inference
text = "This movie was amazing!"
inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=512)
with torch.no_grad():
    logits = model(**inputs).logits
    prediction = torch.argmax(logits, dim=-1).item()

print(f"Predicted label: {prediction}")
```

## Troubleshooting

### Out of Memory (OOM)

Reduce batch size:

```bash
python mlops/train_bert_custom.py \
    --dataset imdb \
    --batch_size 4 \
    --gradient_accumulation_steps 4
```

### Slow Training on CPU

Use GPU or reduce dataset size:

```bash
python mlops/train_bert_custom.py \
    --dataset imdb \
    --device cuda
```

### Model Not Converging

Increase learning rate or epochs:

```bash
python mlops/train_bert_custom.py \
    --dataset imdb \
    --learning_rate 5e-5 \
    --epochs 5
```

### Dataset Not Found

Ensure internet connection (for HF Hub) or correct file path (for local data):

```bash
# For HF Hub datasets
python mlops/train_bert_custom.py --dataset glue --data_dir sst2

# For local files
python mlops/train_bert_custom.py --data_file /absolute/path/to/data.csv
```

## Next Steps

1. **Prepare your dataset** — format as CSV/JSON.
2. **Run training** — use `train_bert_custom.py` with your hyperparameters.
3. **Monitor in MLflow** — check metrics and compare runs.
4. **Deploy** — save the model and use it in production.
5. **Iterate** — adjust hyperparameters, try different models, log experiments.

## Common Datasets

```bash
# Sentiment analysis
python mlops/train_bert_custom.py --dataset imdb
python mlops/train_bert_custom.py --dataset rotten_tomatoes

# Text classification (GLUE benchmark)
python mlops/train_bert_custom.py --dataset glue --data_dir sst2
python mlops/train_bert_custom.py --dataset glue --data_dir cola

# Toxic comments
python mlops/train_bert_custom.py --dataset jigsaw_toxic_comment_classification
```

See https://huggingface.co/datasets for full list of available datasets.
