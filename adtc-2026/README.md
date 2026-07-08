# ADTC 2026 — Submission Files

Completed submission files for `oumar-code/adtc-2026-submission-template`.

## How to apply these files

Copy all three files into the root of your forked repo and push:

```bash
# From the Akulearn_docs root
cp adtc-2026/metadata.json   ../adtc-2026-submission-template/metadata.json
cp adtc-2026/download_model.sh ../adtc-2026-submission-template/download_model.sh
cp adtc-2026/REPORT.md       ../adtc-2026-submission-template/REPORT.md
```

Or copy them manually one by one via GitHub's web editor.

## Before you push — fill in the 3 TODOs in `metadata.json`

Open `metadata.json` and replace every value that starts with `TODO:`:

| Field | Where to find your value |
|---|---|
| `team_id` | Your ADTF / 3MTT portal registration page |
| `submitter.name` | Your full legal name as registered |
| `submitter.email` | The email address linked to your team registration |

Everything else is already filled in and contest-ready.

## Pre-submission smoke test

Run this from inside your forked repo after copying the files:

```bash
bash download_model.sh
pip install "git+https://github.com/Africa-Deep-Tech-Foundation/adtc-profiler.git"
adtc-profiler run --submission . --mode participant --output submission.json --skip-accuracy
cat submission.json   # must show "measured_on": "participant_laptop"
```

## Submission checklist

- [ ] `metadata.json` — no `TODO:` values remain
- [ ] `metadata.json` — exactly 2 prompts in `test_prompts`
- [ ] `download_model.sh` — runs clean end-to-end (`bash download_model.sh`)
- [ ] `model/*.gguf` is listed in `.gitignore` (already in template)
- [ ] Repository is **public** on GitHub
- [ ] Smoke test passes (`submission.json` produced with no errors)
- [ ] Submitted at **adtc-2026.devpost.com**
