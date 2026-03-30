# Frontend Archive Notices

Three frontend repos are redundant now that `akulearn-dashboard/` (inside `Akulearn_docs`) is the canonical frontend.

**Decision recorded in:** [`docs/ecosystem-map.md — Frontend Consolidation Decision`](../ecosystem-map.md)

---

## Repos to Archive

| Repo | URL | Action |
|------|-----|--------|
| `Akudemy-frontend` | https://github.com/oumar-code/Akudemy-frontend | Archive + redirect README |
| `akulearn-dashB` | https://github.com/oumar-code/akulearn-dashB | Archive + redirect README |
| `Akulearn-dashboard` | https://github.com/oumar-code/Akulearn-dashboard | Archive + redirect README |

---

## How to Archive a Repo

1. Go to the repo on GitHub → **Settings** → scroll to **Danger Zone**
2. Click **Archive this repository** → confirm
3. Before archiving, push the redirect README below so visitors know where to go

---

## README Content: Akudemy-frontend

Copy this into `Akudemy-frontend/README.md` before archiving:

```markdown
# ⚠️ Archived — Redirected to Canonical Frontend

This repository has been archived. It was a minimal student-facing landing page stub.

**Active frontend:** All dashboard and marketing pages are now maintained in the canonical frontend:

> [`akulearn-dashboard/` inside oumar-code/Akulearn_docs](https://github.com/oumar-code/Akulearn_docs/tree/main/akulearn-dashboard)

**Platform decisions:** [Aku Platform Ecosystem Map](https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md#frontend-consolidation-decision)

No new work should go into this repo. Please direct all frontend contributions to `Akulearn_docs`.
```

---

## README Content: akulearn-dashB

Copy this into `akulearn-dashB/README.md` before archiving:

```markdown
# ⚠️ Archived — Redirected to Canonical Frontend

This repository has been archived. It was a bootstrapped Next.js 15 stub with no active development.

**Active frontend:** All dashboard and marketing pages are now maintained in the canonical frontend:

> [`akulearn-dashboard/` inside oumar-code/Akulearn_docs](https://github.com/oumar-code/Akulearn_docs/tree/main/akulearn-dashboard)

**Platform decisions:** [Aku Platform Ecosystem Map](https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md#frontend-consolidation-decision)

No new work should go into this repo. Please direct all frontend contributions to `Akulearn_docs`.
```

---

## README Content: Akulearn-dashboard

Copy this into `Akulearn-dashboard/README.md` before archiving:

```markdown
# ⚠️ Archived — Redirected to Canonical Frontend

This repository has been archived. It was an empty shell.

**Active frontend:** All dashboard and marketing pages are now maintained in the canonical frontend:

> [`akulearn-dashboard/` inside oumar-code/Akulearn_docs](https://github.com/oumar-code/Akulearn_docs/tree/main/akulearn-dashboard)

**Platform decisions:** [Aku Platform Ecosystem Map](https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md#frontend-consolidation-decision)

No new work should go into this repo. Please direct all frontend contributions to `Akulearn_docs`.
```

---

## After Archiving

Update the status in [`automation_progress.md`](../../automation_progress.md):
- Mark `Archive Akudemy-frontend` ✅
- Mark `Archive akulearn-dashB` ✅
- Mark `Archive Akulearn-dashboard` ✅

And update the Frontend table in [`docs/ecosystem-map.md`](../ecosystem-map.md) to show **Archived** status.
