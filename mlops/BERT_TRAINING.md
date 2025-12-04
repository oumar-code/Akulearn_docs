# BERT Training Setup for Akulearn Platform

## Overview

This guide provides step-by-step instructions for training BERT and other transformer models on your local Windows machine or scaling to GPUs/cloud.

## Quick Start (Windows + CPU)

### 1. Install MSVC Redistributable (Required for PyTorch)

Run as Administrator (PowerShell):

```powershell
$vcUrl = 'https://aka.ms/vs/17/release/vc_redist.x64.exe'
$dest = "$env:TEMP\vc_redist.x64.exe"
Invoke-WebRequest -Uri $vcUrl -OutFile $dest
Start-Process -FilePath $dest -ArgumentList '/install','/quiet','/norestart' -Verb RunAs -Wait
```

If prompted to reboot, do so before proceeding.

### 2. Install PyTorch + Hugging Face Stack

```powershell
cd C:\Users\<your-username>\Documents\Akulearn_docs

# Install to system Python or create a venv
python -m pip install --upgrade pip setuptools wheel

# Install PyTorch (CPU) + Transformers
python -m pip install torch transformers datasets accelerate huggingface-hub --only-binary :all: --upgrade
```

### 3. Verify Installation

```powershell
python -c "import torch, transformers; print('torch:', torch.__version__); print('cuda:', torch.cuda.is_available())"
```

Expected output:
```
torch: 2.9.1+cpu
cuda: False
```

### 4. Run Smoke Training Test

```powershell
python mlops/train_bert_smoke.py
```

Expected output (should complete in ~8 seconds on CPU):
```
Creating tiny BERT model locally...
Tokenizing dataset...
Dataset split: train=2, eval=2
Starting training (1 epoch, 2 samples)...
...
✓ SMOKE_TRAIN_COMPLETED_SUCCESSFULLY
PyTorch: 2.9.1+cpu
No GPU used (CPU training confirmed)
```

## Training BERT for Production

### Create a Training Script

Create `mlops/train_bert_custom.py` with your own dataset and hyperparameters:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import load_dataset, Dataset
import numpy as np

# Load your data
train_data = load_dataset("your_dataset", split="train")
eval_data = load_dataset("your_dataset", split="validation")

# Tokenize
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

train_data = train_data.map(preprocess, batched=True)
eval_data = eval_data.map(preprocess, batched=True)

# Model
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Training
training_args = TrainingArguments(
    output_dir="runs/bert-custom",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="runs/logs",
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=500,
    save_steps=500,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=eval_data,
)

trainer.train()
trainer.evaluate()
```

Run it:
```powershell
python mlops/train_bert_custom.py
```

## GPU Training (NVIDIA)

If you have an NVIDIA GPU:

1. Install NVIDIA GPU drivers and CUDA Toolkit 11.8+.
2. Reinstall PyTorch with CUDA support:

```powershell
python -m pip uninstall torch -y
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

3. Verify:

```powershell
python -c "import torch; print('cuda:', torch.cuda.is_available()); print('devices:', torch.cuda.device_count())"
```

4. Update your training script to use GPU (usually automatic with Trainer):

```python
training_args = TrainingArguments(
    ...
    device_map="auto",  # uses GPU if available
)
```

## Distributed Training (Multi-GPU or Multi-Node)

Use `accelerate` for multi-GPU training:

```powershell
# Configure
accelerate config

# Run
accelerate launch --multi_gpu mlops/train_bert_custom.py
```

## Cloud Training (Recommended for Large Models)

### Google Colab (Free GPU)

1. Upload your training script to Colab.
2. Install dependencies:

```python
!pip install torch transformers datasets accelerate
```

3. Run training in the cloud with free GPU access.

### AWS SageMaker

1. Create a SageMaker notebook instance.
2. Upload your training script.
3. Use the SageMaker SDK to launch training jobs with managed infrastructure.

## Known Issues

### Windows DLL Errors (OSError WinError 182)

**Problem**: `fbgemm.dll failed to load` or similar.

**Solution**: Install Microsoft Visual C++ Redistributable (x64) as shown in Step 1 above. If already installed, try:

```powershell
# Reinstall VC++ redistributable
$vcUrl = 'https://aka.ms/vs/17/release/vc_redist.x64.exe'
$dest = "$env:TEMP\vc_redist.x64.exe"
Invoke-WebRequest -Uri $vcUrl -OutFile $dest
Start-Process -FilePath $dest -ArgumentList '/repair','/quiet' -Verb RunAs -Wait
```

### Slow Training on CPU

BERT training on CPU is very slow for large datasets. Use GPU or cloud services for production workloads.

### Network Issues Loading Models

If models fail to download from Hugging Face Hub:

1. Check internet connection.
2. Use offline mode (download model once, cache locally):

```python
# First time (online)
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")

# Later (offline)
model = AutoModelForSequenceClassification.from_pretrained("./local-cache")
```

## Files

- `mlops/train_bert_smoke.py` — Minimal smoke test (no network required).
- `mlops/train_bert_custom.py` — Template for custom training (create this yourself).
- `mlops/requirements.txt` — Core dependencies (fastapi, uvicorn, mlflow, etc.).

## Next Steps

1. Collect or prepare your training dataset.
2. Adapt the training script to your task (classification, NER, QA, etc.).
3. Start with smoke test, then scale to GPU.
4. Log experiments with MLflow (`mlflow` is pre-installed).

## References

- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)
- [PyTorch Documentation](https://pytorch.org/docs)
- [Hugging Face Course (Free)](https://huggingface.co/course)
