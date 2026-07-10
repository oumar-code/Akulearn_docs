# Post-Remediation Runbook

**Created:** 2026-05-10  
**Purpose:** Exact, ordered steps to close out the cross-repo remediation phase and advance
the Aku Platform from scaffold-merged state to running GHCR images and declared operational steady state.

All Actions-tab triggers in this runbook target the `oumar-code/Akulearn_docs` repository
(the coordination hub) unless the step says otherwise.

---

## Prerequisites

Before starting, confirm the following are in place:

| Prerequisite | Where to check |
|---|---|
| `GH_PAT` repo secret exists | `Akulearn_docs` → Settings → Secrets and variables → Actions |
| `GH_PAT` has scopes: `repo`, `workflow`, `write:packages` | GitHub → Settings → Tokens — regenerate if `write:packages` is missing |
| `gh` CLI installed and authenticated on your local machine | `gh auth status` |
| Python 3.11+ installed locally | `python3 --version` |
| `ruff` installed locally | `pip install ruff` |
| `git-lfs` installed locally | `git lfs version` |

---

## Step 1 — Review and merge remediation PRs in service repos

The cross-repo fix scripts (`fix-lint.sh`, `fix-ci-git-credentials.sh`) opened PRs
against each of the 9 service repos. These must be merged so that:
- `ruff` lint passes in CI (fix-lint.sh PRs)
- `pip install` can fetch `aku-platform-contracts` in CI (fix-ci-git-credentials.sh PRs)

### 1a — Confirm the requirements.txt fix was applied first

Go to: **Actions → "Service — Fix requirements.txt" → Run workflow**

Leave all inputs at defaults and click **Run workflow**. This ensures every service repo
has the correct `aku-platform-contracts @ git+https://…aku-platform-contracts.git@v0.1.1`
line before the Docker build runs.

Review the summary output; services that report `SKIPPED (already correct)` are fine.

### 1b — Merge lint-remediation PRs in each service repo

For each repo in the list below, go to the open PR on branch `fix/ruff-lint-remediation`
and merge it to `main`:

- https://github.com/oumar-code/AkuAI/pulls
- https://github.com/oumar-code/Akudemy/pulls
- https://github.com/oumar-code/Aku-EdgeHub/pulls
- https://github.com/oumar-code/Aku-IGHub/pulls
- https://github.com/oumar-code/Aku-Telhone/pulls
- https://github.com/oumar-code/Aku-SuperHub/pulls
- https://github.com/oumar-code/AkuTutor/pulls
- https://github.com/oumar-code/AkuWorkspace/pulls
- https://github.com/oumar-code/Aku-DaaS/pulls

If no PR exists for a repo, the script found nothing to fix (already clean).

### 1c — Merge CI-credentials PRs in each service repo

For each repo above, also merge the open PR on branch `fix/ci-git-credentials-for-pip`.

---

## Step 2 — Unblock GH_PAT (add write:packages scope)

Docker image pushes to GHCR require `write:packages` on the PAT.

1. Go to https://github.com/settings/tokens
2. Click the token used as `GH_PAT`
3. Enable the `write:packages` checkbox
4. Click **Update token** and copy the new token value
5. Go to `Akulearn_docs` → **Settings → Secrets and variables → Actions**
6. Click **GH_PAT** → **Update secret** → paste the new token value → **Save**

---

## Step 3 — Re-run the Docker build/push pipeline

Go to: **Actions → "Service — Docker Build & Push" → Run workflow**

Inputs to use:

| Input | Value |
|---|---|
| services | *(leave empty — builds all 9)* |
| tag | `v0.1.1` |
| dry_run | `false` |

Click **Run workflow**. The job takes ~15–30 minutes. Watch for per-service `✓` or `✗` in
the step logs. Common failures and fixes:

| Symptom | Fix |
|---|---|
| `could not read Username` during pip install | Step 1c was not applied — merge the CI-credentials PR |
| `ruff` lint failure | Step 1b was not applied — merge the lint PR |
| `python-multipart` missing (Aku-DaaS) | Automatically patched by this workflow via scaffold fallback |
| `OutputFormat` NameError (AkuAI) | Automatically patched by this workflow via scaffold fallback |

---

## Step 4 — Confirm integration tests pass

The integration test workflow auto-triggers after a successful Docker build. You can also
trigger it manually:

Go to: **Actions → "Service — Integration Tests (Health Checks)" → Run workflow**

Inputs:

| Input | Value |
|---|---|
| tag | `v0.1.1` |
| fail_on_missing | `false` *(while images are being pushed incrementally)* |

A service showing `⚠ skipped — image not yet published to GHCR` is expected while its
build is still in progress. Once all 9 images are confirmed in GHCR, re-run with
`fail_on_missing=true` for a strict gate.

---

## Step 5 — Trigger the three pending migration workflows

These three workflows create stub PRs in external repos entirely within CI
(no local files needed). Trigger them in the order below.

### 5a — Aku-Content stub

Go to: **Actions → "Aku-Content — Initialise Stub" → Run workflow**

- Leave `dry_run` as `false`
- After it completes: review and merge the PR in https://github.com/oumar-code/Aku-Content/pulls

### 5b — Akudemy exam papers stub

Go to: **Actions → "Akudemy — Exam Papers Stub" → Run workflow**

- Leave `dry_run` as `false`
- After it completes: review and merge the PR in https://github.com/oumar-code/Akudemy/pulls

### 5c — Aku-SmartBoard CI scaffold

Go to: **Actions → "Aku-Smartboard — Apply CI/Release Scaffold" → Run workflow**

- Leave `dry_run` as `false`
- After it completes: review and merge the PR in https://github.com/oumar-code/Aku-Smartboard/pulls

---

## Step 6 — Execute local-machine migrations (full content copy)

These steps require your local machine because the source directories are gitignored
in `Akulearn_docs` and not present in CI.

### Prerequisites for local steps

```bash
# From your local Akulearn_docs clone
brew install gh git-lfs     # macOS; use apt on Linux
git lfs install
gh auth login
```

### 6a — Migrate content/ to Aku-Content

```bash
ls content/           # must exist — textbooks, AR, VR, simulations, etc.
ls content_templates/ # must exist — 8 WAEC/NERDC CSV templates

./docs/service-migrations/migrate-to-aku-content.sh
# For a dry-run preview first:
./docs/service-migrations/migrate-to-aku-content.sh --dry-run
```

After the PR is merged in Aku-Content, remove the source dirs:

```bash
git rm -r content/ content_templates/
git commit -m "chore: remove content/ and content_templates/ after migration to Aku-Content"
git push
```

### 6b — Migrate exam papers to Akudemy

```bash
# Option A — restore from local drive
ls data/exam_papers/           # 1,350 JSON/CSV questions
ls mlops/exam_paper_scraper.py

# Option B — regenerate from scratch
pip install -r requirements.txt
python mlops/exam_paper_scraper.py --output data/exam_papers/

./docs/service-migrations/migrate-exam-papers.sh
```

After the PR is merged in Akudemy, remove from Akulearn_docs:

```bash
git rm -r data/exam_papers/
git commit -m "chore: remove data/exam_papers/ after migration to Akudemy"
git push
```

### 6c — Migrate akulearn-linux-app/ to Aku-SmartBoard

```bash
ls akulearn-linux-app/   # must exist — KMP Compose Desktop source

./docs/service-migrations/migrate-to-aku-smartboard.sh
```

After the PR is merged in Aku-SmartBoard, remove from Akulearn_docs:

```bash
git rm -r akulearn-linux-app/
git commit -m "chore: remove akulearn-linux-app/ after migration to Aku-SmartBoard"
git push
```

---

## Step 7 — Pin contracts version and sync OpenAPI specs

After Docker images are validated:

Go to: **Actions → "Service — Lint, Format & Tag"** and confirm all 9 services are on `v0.1.1`.

The OpenAPI sync workflow auto-triggers after lint/format/tag succeeds (via `workflow_run`).
You can also trigger it manually:

Go to: **Actions → "Service — Sync OpenAPI to Contracts"**

---

## Step 8 — Declare operational steady state

Once all steps above are done, update `internal operations tracker`:

1. Mark the Docker Build & Push line: `⬜ Pending first run` → `✅ Done`
2. Mark the OpenAPI sync line: `⬜ Pending lint/format/tag re-run` → `✅ Done`
3. Mark the Integration tests line: `⬜ Pending Docker images` → `✅ Done`
4. Mark the three stub workflow trigger lines → `✅ Done`
5. Mark the three local migration lines → `✅ Done` (after confirmation)
6. Add a new session log entry with date and summary

Optional next phase — Kubernetes staging:

```
Apply manifests to staging cluster:
  kubectl apply -f docs/deployment/k8s/namespace.yaml
  kubectl apply -f docs/deployment/k8s/

Create GHCR pull secret first (see docs/deployment/k8s/README.md).
```

---

## Quick reference — workflow trigger URLs

All workflows are in `oumar-code/Akulearn_docs`. Go to the Actions tab there.

| Step | Workflow name |
|---|---|
| 1a | Service — Fix requirements.txt |
| 3 | Service — Docker Build & Push |
| 4 | Service — Integration Tests (Health Checks) |
| 5a | Aku-Content — Initialise Stub |
| 5b | Akudemy — Exam Papers Stub |
| 5c | Aku-Smartboard — Apply CI/Release Scaffold |
| 7 | Service — Sync OpenAPI to Contracts |
