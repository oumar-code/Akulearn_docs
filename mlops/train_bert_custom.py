"""
Production BERT training script with MLflow experiment tracking.

Usage:
    python mlops/train_bert_custom.py \
        --dataset imdb \
        --model_name bert-base-uncased \
        --epochs 3 \
        --batch_size 8 \
        --learning_rate 2e-5 \
        --experiment_name "bert-imdb-v1"

Or with custom data:
    python mlops/train_bert_custom.py \
        --data_file path/to/data.csv \
        --text_column text \
        --label_column label \
        --model_name bert-base-uncased

Features:
  - MLflow experiment tracking (metrics, params, model artifacts)
  - Multi-GPU support (automatic with accelerate)
  - Checkpointing and early stopping
  - Comprehensive logging
"""

import argparse
import os
import json
import logging
from pathlib import Path
from datetime import datetime

import torch
import numpy as np
import mlflow
import mlflow.pytorch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    DataCollatorWithPadding,
)
from datasets import load_dataset, Dataset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(args):
    """Load dataset from HF Hub or local file."""
    logger.info(f"Loading dataset: {args.dataset or args.data_file}")
    
    if args.dataset:
        # Load from Hugging Face Hub
        dataset = load_dataset(args.dataset)
        if "test" not in dataset:
            # Split if no test set
            dataset = dataset["train"].train_test_split(test_size=0.1, seed=42)
        return dataset
    elif args.data_file:
        # Load from local CSV/JSON
        ext = Path(args.data_file).suffix
        if ext == ".csv":
            dataset = load_dataset("csv", data_files=args.data_file)
        elif ext == ".json":
            dataset = load_dataset("json", data_files=args.data_file)
        else:
            raise ValueError(f"Unsupported format: {ext}")
        
        # Rename columns if needed
        if args.text_column != "text":
            dataset = dataset.rename_column(args.text_column, "text")
        if args.label_column != "label":
            dataset = dataset.rename_column(args.label_column, "label")
        
        # Split if needed
        if "test" not in dataset:
            dataset = dataset["train"].train_test_split(test_size=0.1, seed=42)
        
        return dataset
    else:
        raise ValueError("Provide either --dataset or --data_file")


def preprocess_function(examples, tokenizer, args):
    """Tokenize text examples."""
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=args.max_seq_length,
    )


def compute_metrics(eval_preds):
    """Compute evaluation metrics (accuracy, precision, recall, F1)."""
    predictions, labels = eval_preds
    predictions = np.argmax(predictions, axis=1)
    
    return {
        "accuracy": accuracy_score(labels, predictions),
        "precision": precision_score(labels, predictions, average="weighted", zero_division=0),
        "recall": recall_score(labels, predictions, average="weighted", zero_division=0),
        "f1": f1_score(labels, predictions, average="weighted", zero_division=0),
    }


def main():
    parser = argparse.ArgumentParser(description="Train BERT with MLflow tracking")
    
    # Dataset
    parser.add_argument("--dataset", default="imdb", help="HF Hub dataset name (e.g., 'imdb', 'glue')")
    parser.add_argument("--data_file", default=None, help="Path to local CSV/JSON data")
    parser.add_argument("--text_column", default="text", help="Text column name")
    parser.add_argument("--label_column", default="label", help="Label column name")
    
    # Model
    parser.add_argument("--model_name", default="bert-base-uncased", help="Model name from HF Hub")
    parser.add_argument("--num_labels", type=int, default=2, help="Number of classification labels")
    parser.add_argument("--max_seq_length", type=int, default=512, help="Max sequence length")
    
    # Training
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Training batch size")
    parser.add_argument("--eval_batch_size", type=int, default=16, help="Evaluation batch size")
    parser.add_argument("--learning_rate", type=float, default=2e-5, help="Learning rate")
    parser.add_argument("--warmup_steps", type=int, default=500, help="Warmup steps")
    parser.add_argument("--weight_decay", type=float, default=0.01, help="Weight decay")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=1, help="Gradient accumulation steps")
    parser.add_argument("--max_grad_norm", type=float, default=1.0, help="Max gradient norm")
    
    # Checkpointing and early stopping
    parser.add_argument("--save_steps", type=int, default=500, help="Save checkpoint every N steps")
    parser.add_argument("--eval_steps", type=int, default=500, help="Eval every N steps")
    parser.add_argument("--patience", type=int, default=3, help="Early stopping patience")
    
    # MLflow
    parser.add_argument("--experiment_name", default="bert-training", help="MLflow experiment name")
    parser.add_argument("--run_name", default=None, help="MLflow run name (auto-generated if not set)")
    parser.add_argument("--tracking_uri", default="runs/mlflow", help="MLflow tracking URI")
    
    # Hardware
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu", help="Device (cuda/cpu)")
    
    # Output
    parser.add_argument("--output_dir", default="runs/bert-custom", help="Output directory")
    
    args = parser.parse_args()
    
    # Setup MLflow
    mlflow.set_tracking_uri(args.tracking_uri)
    mlflow.set_experiment(args.experiment_name)
    
    run_name = args.run_name or f"bert-{args.dataset or 'custom'}-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    with mlflow.start_run(run_name=run_name):
        logger.info(f"Started MLflow run: {run_name}")
        
        # Log parameters
        mlflow.log_param("model_name", args.model_name)
        mlflow.log_param("dataset", args.dataset or args.data_file)
        mlflow.log_param("epochs", args.epochs)
        mlflow.log_param("batch_size", args.batch_size)
        mlflow.log_param("learning_rate", args.learning_rate)
        mlflow.log_param("warmup_steps", args.warmup_steps)
        
        # Load data
        logger.info("Loading and preprocessing dataset...")
        dataset = load_data(args)
        train_dataset = dataset["train"]
        eval_dataset = dataset.get("test", dataset.get("validation"))
        
        # Sample logging for large datasets
        if len(train_dataset) > 10000:
            logger.info(f"Large dataset detected ({len(train_dataset)} samples). Using 10k for training demo.")
            train_dataset = train_dataset.select(range(min(10000, len(train_dataset))))
        
        # Rename label to labels (required by transformers Trainer)
        if "label" in train_dataset.column_names:
            train_dataset = train_dataset.rename_column("label", "labels")
        if eval_dataset and "label" in eval_dataset.column_names:
            eval_dataset = eval_dataset.rename_column("label", "labels")
        
        # Tokenize
        logger.info("Tokenizing dataset...")
        tokenizer = AutoTokenizer.from_pretrained(args.model_name)
        train_dataset = train_dataset.map(
            lambda x: preprocess_function(x, tokenizer, args),
            batched=True,
            remove_columns=["text"] if "text" in train_dataset.column_names else [],
        )
        
        if eval_dataset:
            eval_dataset = eval_dataset.map(
                lambda x: preprocess_function(x, tokenizer, args),
                batched=True,
                remove_columns=["text"] if "text" in eval_dataset.column_names else [],
            )
        
        # Model
        logger.info(f"Loading model: {args.model_name}")
        model = AutoModelForSequenceClassification.from_pretrained(
            args.model_name,
            num_labels=args.num_labels,
        )
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=args.output_dir,
            num_train_epochs=args.epochs,
            per_device_train_batch_size=args.batch_size,
            per_device_eval_batch_size=args.eval_batch_size,
            learning_rate=args.learning_rate,
            warmup_steps=args.warmup_steps,
            weight_decay=args.weight_decay,
            gradient_accumulation_steps=args.gradient_accumulation_steps,
            max_grad_norm=args.max_grad_norm,
            logging_steps=100,
            logging_dir="runs/logs",
            eval_strategy="steps" if eval_dataset else "no",
            eval_steps=args.eval_steps if eval_dataset else None,
            save_strategy="steps",
            save_steps=args.save_steps,
            save_total_limit=3,
            load_best_model_at_end=True if eval_dataset else False,
            metric_for_best_model="f1" if eval_dataset else None,
            report_to=["mlflow"],
        )
        
        # Trainer with early stopping
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            processing_class=tokenizer,
            compute_metrics=compute_metrics if eval_dataset else None,
            callbacks=[
                EarlyStoppingCallback(
                    early_stopping_patience=args.patience,
                    early_stopping_threshold=0.0,
                ) if eval_dataset else None
            ],
            data_collator=DataCollatorWithPadding(tokenizer),
        )
        
        # Train
        logger.info("Starting training...")
        train_result = trainer.train()
        
        # Evaluate
        if eval_dataset:
            logger.info("Evaluating...")
            eval_result = trainer.evaluate()
            mlflow.log_metrics(eval_result, step=0)
        
        # Save model
        logger.info(f"Saving model to {args.output_dir}")
        model.save_pretrained(args.output_dir)
        tokenizer.save_pretrained(args.output_dir)
        
        # Log model artifact
        mlflow.pytorch.log_model(model, "model")
        
        # Log training results
        with open(f"{args.output_dir}/training_results.json", "w") as f:
            json.dump(train_result.metrics, f, indent=2)
        mlflow.log_artifact(f"{args.output_dir}/training_results.json")
        
        logger.info(f"Training completed. Model saved to {args.output_dir}")
        logger.info(f"MLflow run: {run_name}")
        logger.info(f"Tracking URI: {args.tracking_uri}")


if __name__ == "__main__":
    main()
