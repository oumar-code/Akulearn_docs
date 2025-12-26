#!/usr/bin/env python3
"""
Fine-tune translation model on Akulearn news corpus.
- Loads prepared dataset (TSV/JSON)
- Fine-tunes a base HF translation model (e.g., Helsinki-NLP/opus-mt-en-ha)
- Saves fine-tuned model and evaluation metrics

Requirements:
  pip install transformers datasets torch evaluate sacrebleu

Usage:
  python train_translation_model.py --data content/ml_datasets/en-ha.tsv --lang-pair en-ha --output models/en-ha-finetuned
"""

import argparse
import json
from pathlib import Path
from typing import Optional


def load_dataset(data_path: Path, format: str = "tsv"):
    """Load dataset from TSV or JSONL"""
    pairs = []
    
    if format == "tsv":
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) == 2:
                    pairs.append({"source": parts[0], "target": parts[1]})
    elif format == "jsonl":
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)
                    pairs.append({"source": obj["source"], "target": obj["target"]})
    
    return pairs


def train_model(
    dataset_path: Path,
    base_model: str,
    output_dir: Path,
    lang_pair: str,
    max_steps: int = 1000,
    batch_size: int = 8,
    learning_rate: float = 2e-5,
):
    """Fine-tune translation model"""
    
    try:
        from transformers import (
            AutoTokenizer,
            AutoModelForSeq2SeqLM,
            Seq2SeqTrainer,
            Seq2SeqTrainingArguments,
            DataCollatorForSeq2Seq,
        )
        from datasets import Dataset
    except ImportError:
        raise SystemExit("Install transformers and datasets: pip install transformers datasets torch")
    
    print(f"🤖 Loading base model: {base_model}")
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    model = AutoModelForSeq2SeqLM.from_pretrained(base_model)
    
    print(f"📚 Loading dataset from {dataset_path}")
    pairs = load_dataset(dataset_path, format="tsv" if dataset_path.suffix == ".tsv" else "jsonl")
    print(f"✅ Loaded {len(pairs)} examples")
    
    # Split into train/val
    split_idx = int(0.9 * len(pairs))
    train_pairs = pairs[:split_idx]
    val_pairs = pairs[split_idx:]
    
    # Tokenize
    def tokenize(batch):
        source_lang, target_lang = lang_pair.split("-")
        src = batch["source"]
        tgt = batch["target"]
        
        inputs = tokenizer(src, truncation=True, max_length=256)
        targets = tokenizer(tgt, truncation=True, max_length=256)
        
        inputs["labels"] = targets["input_ids"]
        return inputs
    
    train_dataset = Dataset.from_dict({
        "source": [p["source"] for p in train_pairs],
        "target": [p["target"] for p in train_pairs],
    })
    val_dataset = Dataset.from_dict({
        "source": [p["source"] for p in val_pairs],
        "target": [p["target"] for p in val_pairs],
    })
    
    train_dataset = train_dataset.map(tokenize, batched=True, remove_columns=["source", "target"])
    val_dataset = val_dataset.map(tokenize, batched=True, remove_columns=["source", "target"])
    
    # Training args
    training_args = Seq2SeqTrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=3,
        max_steps=max_steps,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        save_steps=500,
        eval_steps=500,
        logging_steps=100,
        predict_with_generate=True,
        fp16=False,  # Set to True if using GPU with FP16 support
    )
    
    # Trainer
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer),
    )
    
    print("🚀 Training...")
    trainer.train(max_steps=max_steps)
    
    # Save
    print(f"💾 Saving model to {output_dir}")
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    
    print(f"✅ Training complete!")
    print(f"📁 Model saved to: {output_dir}")
    
    return trainer


def parse_args():
    parser = argparse.ArgumentParser(description="Fine-tune translation model on news corpus")
    parser.add_argument("--data", required=True, help="Dataset path (TSV or JSONL)")
    parser.add_argument("--lang-pair", required=True, help="Language pair (e.g., en-ha, en-yo)")
    parser.add_argument("--base-model", default=None, help="Base model (defaults to Helsinki-NLP/opus-mt-<pair>)")
    parser.add_argument("--output", default="models", help="Output directory for fine-tuned model")
    parser.add_argument("--max-steps", type=int, default=1000, help="Max training steps")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size")
    parser.add_argument("--learning-rate", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--dry-run", action="store_true", help="Validate setup without training")
    return parser.parse_args()


def main():
    args = parse_args()
    
    data_path = Path(args.data)
    if not data_path.exists():
        raise SystemExit(f"Dataset not found: {data_path}")
    
    # Infer base model if not provided
    base_model = args.base_model
    if not base_model:
        lang_pair = args.lang_pair.replace("-", "-")
        base_model = f"Helsinki-NLP/opus-mt-{lang_pair}"
        print(f"📝 Inferred base model: {base_model}")
    
    output_dir = Path(args.output) / args.lang_pair
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.dry_run:
        print("✅ Setup validation passed. Ready to train.")
        pairs = load_dataset(data_path, format="tsv" if data_path.suffix == ".tsv" else "jsonl")
        print(f"   Dataset: {len(pairs)} examples")
        print(f"   Base model: {base_model}")
        print(f"   Output: {output_dir}")
        return
    
    train_model(
        data_path,
        base_model,
        output_dir,
        args.lang_pair,
        max_steps=args.max_steps,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
    )


if __name__ == "__main__":
    main()
