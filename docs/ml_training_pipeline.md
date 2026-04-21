# ML Training Pipeline

## Objective
Provide a reproducible end-to-end pipeline for training, evaluating, and deploying multilingual models (English ↔ Hausa/Igbo/Yoruba) for Akulearn content and tutoring workflows.

## Scope
- Tasks: translation, classification, retrieval quality scoring.
- Data sources: curated curriculum data, approved public corpora, and multilingual news datasets.
- Outputs: versioned datasets, trained models, evaluation reports, deployable artifacts.

## Pipeline Stages

## 1) Data Ingestion
- Ingest raw documents from approved sources.
- Validate schema and metadata (source, language, timestamp, license).
- Store immutable raw snapshots for lineage.

## 2) Data Preparation
- Normalize text (encoding, punctuation, script handling).
- Remove duplicates and low-quality pairs.
- Segment into train/validation/test with leakage prevention.
- Export standardized formats (TSV/JSONL/HF datasets).

## 3) Dataset Quality Gates
- Language identification accuracy checks.
- Minimum alignment confidence for parallel corpora.
- Toxicity/safety screening.
- Coverage checks by subject and grade level.

## 4) Training
- Select baseline model per task and language pair.
- Run parameterized training jobs with tracked configs.
- Save checkpoints and model card metadata.

Recommended baseline translation models:
- `Helsinki-NLP/opus-mt-en-ha`
- `Helsinki-NLP/opus-mt-en-yo`
- `Helsinki-NLP/opus-mt-en-ig`

## 5) Evaluation
- Automated metrics: BLEU/chrF/COMET (for translation), accuracy/F1 (classification).
- Safety checks: harmful output and bias spot checks.
- Human review: linguistic quality and curriculum fidelity.

Promotion gate:
- Candidate model must outperform production baseline on agreed metrics and pass safety checks.

## 6) Packaging and Registry
- Package model + tokenizer + inference config.
- Register artifact with semantic version and lineage metadata.
- Store reproducibility details: dataset version, code commit, training config.

## 7) Deployment
- Deploy to staging first with shadow/canary traffic.
- Monitor latency, error rate, and output quality regressions.
- Promote to production after acceptance criteria are met.

## 8) Monitoring and Retraining
- Track live quality indicators and drift signals.
- Trigger retraining on drift, content expansion, or metric decay.
- Keep rollback-ready previous model versions.

## Suggested Repository Layout
```text
content/
  news_corpus/
  ml_datasets/
models/
  <task>/<lang-pair>/<version>/
reports/
  eval/
```

## Example Command Flow
```bash
# 1) Generate/collect corpus
python generate_news_corpus.py --count 100 --langs en ha yo ig

# 2) Prepare parallel dataset
python prepare_ml_dataset.py --corpus content/news_corpus --source-lang en --target-lang ha --output content/ml_datasets --format tsv

# 3) Dry-run training
python train_translation_model.py --data content/ml_datasets/en-ha.tsv --lang-pair en-ha --base-model Helsinki-NLP/opus-mt-en-ha --output models --dry-run

# 4) Train
python train_translation_model.py --data content/ml_datasets/en-ha.tsv --lang-pair en-ha --base-model Helsinki-NLP/opus-mt-en-ha --output models --max-steps 5000 --batch-size 16 --learning-rate 2e-5
```

## CI/CD Integration
- CI validates dataset schema and training config.
- Scheduled jobs run periodic evaluation against benchmark sets.
- Release pipeline blocks deployment when quality gates fail.

## Risks and Mitigations
- **Data drift**: continuous monitoring and periodic retraining.
- **Low-resource language quality**: expand corpus and increase human review.
- **Overfitting**: strict held-out test sets and early stopping.
- **Unsafe outputs**: content safety filters and moderation checks.

## Definition of Done
- Reproducible training run from raw data to deployable model.
- Quality and safety reports generated for each candidate.
- Versioned model promoted through staging to production with rollback plan.
