---
title: Full-turn delivery
---

# Full-turn delivery (PhenoDocs)

A **full turn** finishes when work is **merged** to **`main`** or an approved **release branch**, is **visible on GitHub** (PR URLs), and ships **changelog**, **version** (when applicable), and **docs** updates.

## Requirements

1. **≥1 merged PR** per turn to `main` or `release/*` (several PRs per turn are fine for stacked work).
2. **GitHub visibility:** record PR link(s) in the PR body and optionally in `CHANGELOG.md` under **[Unreleased]**.
3. **Changelog:** update root **`CHANGELOG.md`** for user-facing doc site or workflow changes.
4. **Version:** bump **`package.json`** `version` when releasing a tagged docs build or publishing a semver story; otherwise state **“version: N/A”** in the PR.
5. **Docs:** run **`pnpm run build`** before merge when `docs/` or `.vitepress/` changed.

## Commands

```bash
gh pr create --fill   # or explicit title/body with changelog + version note
gh pr merge             # after CI green
gh pr list --state merged --limit 5
```

## Batch planning (Next 50)

Large planning batches use **five parallel lanes (A–E)** and **ten waves (W1–W10)** — **50 tasks** with explicit **Depends** edges so work is **DAGified**: never more than five concurrent tasks, but independent tasks within the same wave can run together. See **[Full-turn Next 50](/planning/full-turn-next50-20260326)**.

## Related

- [Full-turn Next 50](/planning/full-turn-next50-20260326) — 50-item DAG batch (5 agents × 10 waves)
- [Rich workspace views](/planning/rich-workspace-views) — product roadmap for views
- [Workspace views](/views/) — changelog, commit log, WBS hubs
