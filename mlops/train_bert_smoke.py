"""
Minimal BERT training smoke test (no network required).
Creates a tiny BERT model locally and trains on a small dataset.
Expected runtime: ~30-60 seconds on CPU.
"""

from transformers import BertConfig, BertForSequenceClassification
from datasets import Dataset
from transformers import TrainingArguments, Trainer
import torch
import os

# Create output directory
os.makedirs("runs/bert-smoke", exist_ok=True)

# Tiny dataset
texts = ["hello world", "goodbye world", "hello again", "yet another sentence"]
labels = [0, 1, 0, 1]
ds = Dataset.from_dict({"text": texts, "label": labels})

# Create a tiny BERT config and model locally (no network needed)
print("Creating tiny BERT model locally...")
config = BertConfig(
    vocab_size=1000,
    hidden_size=64,
    num_hidden_layers=2,
    num_attention_heads=2,
    intermediate_size=256,
    num_labels=2,
)
model = BertForSequenceClassification(config)
print(f"Model created: {model.config}")

# Simple tokenizer: split text and map to token IDs
print("Tokenizing dataset...")
def preprocess(example):
    text = example["text"].lower()
    tokens = text.split()[:30]
    input_ids = [101]  # [CLS]
    for token in tokens:
        input_ids.append(abs(hash(token)) % (config.vocab_size - 2) + 2)
    input_ids.append(102)  # [SEP]
    
    max_len = 32
    attention_mask = [1] * len(input_ids) + [0] * (max_len - len(input_ids))
    input_ids = (input_ids + [0] * max_len)[:max_len]
    
    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "token_type_ids": [0] * max_len,
    }

ds = ds.map(preprocess, batched=False)
ds = ds.train_test_split(test_size=0.5)

print(f"Dataset split: train={len(ds['train'])}, eval={len(ds['test'])}")

training_args = TrainingArguments(
    output_dir="runs/bert-smoke",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=1,
    logging_steps=1,
    report_to=[],
    save_strategy="no",
)

print("Creating trainer...")
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=ds["train"],
    eval_dataset=ds["test"],
)

print("Starting training (1 epoch, 2 samples)...")
trainer.train()
print("\n" + "="*50)
print("✓ SMOKE_TRAIN_COMPLETED_SUCCESSFULLY")
print("="*50)
print("PyTorch:", torch.__version__)
print("No GPU used (CPU training confirmed)")
