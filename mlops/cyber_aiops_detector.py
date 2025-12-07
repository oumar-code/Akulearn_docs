"""
Lightweight Cyber AIops anomaly detection prototype.

- Reads newline-delimited log file (structured JSON lines or simple text lines)
- Extracts basic features and vectorizes message text (TF-IDF)
- Trains or loads an IsolationForest to detect anomalous log lines
- Emits alerts to stdout and writes `runs/cyber_alerts.json`

Usage:
    python mlops/cyber_aiops_detector.py --log-file mlops/sample_logs.log --mode score --output runs/cyber_alerts.json

"""
import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import logging

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cyber_aiops")

MODEL_DIR = Path("runs/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "isoforest.joblib"
VEC_PATH = MODEL_DIR / "tfidf.joblib"


def parse_log_line(line: str):
    """Try parse JSON first; otherwise fallback to naive parsing."""
    try:
        obj = json.loads(line)
        # Expected keys: timestamp, level, service, message
        ts = obj.get("timestamp")
        level = obj.get("level")
        service = obj.get("service")
        message = obj.get("message") or obj.get("msg") or ""
        return {
            "timestamp": ts,
            "level": level,
            "service": service,
            "message": message,
            "raw": line.strip(),
        }
    except Exception:
        # fallback naive parse: assume "[ts] LEVEL service: message"
        raw = line.strip()
        ts = None
        level = None
        service = None
        message = raw
        return {
            "timestamp": ts,
            "level": level,
            "service": service,
            "message": message,
            "raw": raw,
        }


def load_logs(path: Path):
    data = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if not line.strip():
                continue
            data.append(parse_log_line(line))
    return pd.DataFrame(data)


def extract_features(df: pd.DataFrame):
    # Text features via TF-IDF
    messages = df["message"].fillna("")
    if len(messages) == 0:
        return None, None
    tfidf = TfidfVectorizer(max_features=512, ngram_range=(1,2))
    X_text = tfidf.fit_transform(messages)

    # Basic numeric features: message length, presence of ERROR/EXCEPTION, digit counts
    msg_len = messages.str.len().fillna(0).astype(float).values.reshape(-1, 1)
    has_error = messages.str.contains(r"error|exception|failed|traceback", case=False, regex=True).astype(float).values.reshape(-1,1)
    digits = messages.str.count(r"\d").fillna(0).astype(float).values.reshape(-1,1)

    # Combine sparse TF-IDF with small dense features
    from scipy.sparse import hstack
    X = hstack([X_text, msg_len, has_error, digits])
    return X, tfidf


def train_model(X):
    logger.info("Training IsolationForest on provided logs (assumes mostly normal data)...")
    model = IsolationForest(n_estimators=200, contamination=0.01, random_state=42)
    model.fit(X)
    joblib.dump(model, MODEL_PATH)
    logger.info(f"Saved model to {MODEL_PATH}")
    return model


def score_and_alert(df: pd.DataFrame, X, model, tfidf, output: Path, top_k=20):
    # Score anomaly (negative scores are more anomalous)
    scores = model.decision_function(X)  # higher is more normal
    anomaly_score = -scores  # flip so higher means more anomalous
    df = df.copy()
    df["anomaly_score"] = anomaly_score
    df_sorted = df.sort_values("anomaly_score", ascending=False)

    # Choose threshold: top_k or score threshold
    alerts = []
    for _, row in df_sorted.head(top_k).iterrows():
        alert = {
            "timestamp": row.get("timestamp") or str(datetime.utcnow().isoformat()),
            "service": row.get("service"),
            "message": row.get("message"),
            "raw": row.get("raw"),
            "anomaly_score": float(row.get("anomaly_score", 0.0)),
        }
        alerts.append(alert)

    # Write alerts
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump({"generated_at": datetime.utcnow().isoformat(), "alerts": alerts}, f, indent=2)

    # Print top alerts
    logger.info(f"Top {len(alerts)} alerts written to {output}")
    for a in alerts:
        print("--- ALERT ---")
        print(f"time: {a['timestamp']}")
        print(f"service: {a['service']}")
        print(f"score: {a['anomaly_score']:.4f}")
        print(f"message: {a['message']}")
        print()

    return alerts


def load_or_train(df: pd.DataFrame, force_train=False):
    X, tfidf = extract_features(df)
    if X is None:
        raise RuntimeError("No messages to analyze")

    if MODEL_PATH.exists() and VEC_PATH.exists() and not force_train:
        try:
            model = joblib.load(MODEL_PATH)
            tfidf = joblib.load(VEC_PATH)
            logger.info("Loaded existing model and vectorizer")
            return X, model, tfidf
        except Exception as e:
            logger.warning(f"Failed to load model/vectorizer: {e}, retraining...")

    # Train new
    model = train_model(X)
    joblib.dump(tfidf, VEC_PATH)
    logger.info(f"Saved vectorizer to {VEC_PATH}")
    return X, model, tfidf


def main():
    parser = argparse.ArgumentParser(description="Cyber AIops anomaly detection prototype")
    parser.add_argument("--log-file", required=True, help="Path to newline-delimited log file")
    parser.add_argument("--mode", choices=["train","score"], default="score", help="Train or score")
    parser.add_argument("--force-train", action="store_true", help="Force retrain model")
    parser.add_argument("--output", default="runs/cyber_alerts.json", help="Output alerts JSON")
    parser.add_argument("--top-k", type=int, default=20, help="Top K anomalies to emit")
    args = parser.parse_args()

    path = Path(args.log_file)
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    df = load_logs(path)
    logger.info(f"Loaded {len(df)} log lines from {path}")

    X, model, tfidf = load_or_train(df, force_train=args.force_train or args.mode=="train")

    if args.mode == "train":
        logger.info("Training completed (mode=train)")
        return

    alerts = score_and_alert(df, X, model, tfidf, Path(args.output), top_k=args.top_k)
    logger.info(f"Produced {len(alerts)} alerts")


if __name__ == "__main__":
    main()
