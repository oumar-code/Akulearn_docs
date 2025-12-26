# ML Training Pipeline for Nigerian Language Translation

## Overview
Generate news articles, build parallel corpora, and fine-tune translation models for English ↔ Hausa/Igbo/Yoruba.

## Workflow

### 1. Generate News Corpus
```bash
# Synthetic articles in English + automatic translation (requires HF model)
python generate_news_corpus.py \
  --count 100 \
  --langs en ha yo ig \
  --pairs en-ha en-yo en-ig \
  --models Helsinki-NLP/opus-mt-en-ha Helsinki-NLP/opus-mt-en-yo Helsinki-NLP/opus-mt-en-ig

# Output: content/news_corpus/
#   en/YYYY/MM/DD/*.json      (English articles)
#   ha/YYYY/MM/DD/*.json      (Hausa articles)
#   yo/YYYY/MM/DD/*.json      (Yoruba articles)
#   ig/YYYY/MM/DD/*.json      (Igbo articles)
```

### 2. Prepare Dataset for Training
```bash
# Build parallel corpus (document-level pairs)
python prepare_ml_dataset.py \
  --corpus content/news_corpus \
  --source-lang en \
  --target-lang ha \
  --output content/ml_datasets \
  --format tsv

# Or split into sentences for finer-grained training
python prepare_ml_dataset.py \
  --corpus content/news_corpus \
  --source-lang en \
  --target-lang ha \
  --output content/ml_datasets \
  --format tsv \
  --sentence-level

# Output: content/ml_datasets/en-ha.tsv
#   Format: source_text \t target_text (one pair per line)
```

### 3. Fine-Tune Translation Model
```bash
# Test setup first
python train_translation_model.py \
  --data content/ml_datasets/en-ha.tsv \
  --lang-pair en-ha \
  --base-model Helsinki-NLP/opus-mt-en-ha \
  --output models \
  --dry-run

# Train (requires GPU recommended for speed)
python train_translation_model.py \
  --data content/ml_datasets/en-ha.tsv \
  --lang-pair en-ha \
  --base-model Helsinki-NLP/opus-mt-en-ha \
  --output models \
  --max-steps 5000 \
  --batch-size 16 \
  --learning-rate 2e-5

# Output: models/en-ha/
#   pytorch_model.bin      (fine-tuned weights)
#   config.json            (model config)
#   tokenizer.json         (tokenizer)
```

### 4. Use Fine-Tuned Model in Akulearn
```bash
# Update .env
export HUGGINGFACE_TRANSLATION_MODEL=models/en-ha

# Translate lessons
python translate_lessons.py \
  content/ai_generated/textbooks/Computer\ Science/SS1/lesson_01_computer_hardware_and_software.json \
  --lang ha

# Output: content/ai_generated_translated/ha/lesson_01_...json
```

## Dataset Formats

**TSV (Tab-Separated Values):**
```
source_text	target_text
The school is green.	Makaranta ita gida.
```

**JSONL (JSON Lines):**
```json
{"source": "The school is green.", "target": "Makaranta ita gida."}
```

**HF Datasets Format:**
```json
{
  "translation": [
    {"en": "The school is green.", "ha": "Makaranta ita gida."},
    ...
  ]
}
```

## Parallel Datasets to Combine (Future)
- **MAFAND-MT**: News parallel corpus (Hausa, Yoruba, Pidgin)
- **JW300**: Bible (13+ Nigerian languages)
- **MENYO-20k**: Yoruba-English multi-domain

## Base Models (Hugging Face)
| Language Pair | Model |
|---|---|
| en-ha | `Helsinki-NLP/opus-mt-en-ha` |
| en-yo | `Helsinki-NLP/opus-mt-en-yo` |
| en-ig | `Helsinki-NLP/opus-mt-en-ig` |
| ha-en | `Helsinki-NLP/opus-mt-ha-en` |

## Environment Variables
```bash
# .env
HUGGINGFACE_TOKEN=your_hf_token_if_using_private_models
HUGGINGFACE_TRANSLATION_MODEL=models/en-ha  # Path to fine-tuned model
```

## Metrics & Evaluation
- **BLEU Score**: Automatic metric for translation quality
- **Training curves**: Logged via HF Trainer (view in `models/en-ha/`)
- **Manual review**: Spot-check translated lessons for accuracy

## Tips
1. **Start small**: 100-500 articles for initial fine-tuning
2. **Use GPU**: Training on CPU is slow; consider Colab/Lambda Labs
3. **Monitor**: Check `models/<pair>/training_args.bin` for convergence
4. **Iterate**: Collect more domain-specific news to improve
5. **Combine**: Merge Akulearn corpus with MAFAND-MT for larger dataset

## Next: Multi-Modal Training
Once translation is working, add:
- Image-to-caption pairs (BBC News articles + images)
- Audio-to-text (VOA podcasts + transcripts)
- Cross-lingual image-text alignment
