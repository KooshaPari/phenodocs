# Reconcile Sprint: CLIProxy++, thegent, agentapi++ (2026-02-26)

## Executive Status

- `cliproxyapi-plusplus`: enormous open-PR surface with stacked/cascading migration PRs and shared workflow failures (`CodeQL`, `Analyze (Go)`, `build`, `verify-required-check-names`, `CodeRabbit`, `Build Docs`).
- `thegent`: 8 open PRs with 7 blocked/dirty states and significant CI breakage concentrated in multi-platform/build/doc/gating jobs.
- `agentapi-plusplus`: 20+ open PRs, mostly `BLOCKED` or `DIRTY`, widespread check failures and many open review threads in #243 and #242.

## Repo-by-Repo Audit

### cliproxyapi-plusplus (open PRs observed: 60+ in this batch)

- Snapshot IDs checked: `616, 615, 614, 613, 612, 611, 610, 609, 608, 607` (same pattern continues through `557+`).
- Top sample check posture:
  - `616`: `Analyze (Go) (go)` failure, `build` failure, `verify-required-check-names` success.
  - `615-613`: same failing core checks + `verify-required-check-names` failures.
  - `612`: `Verify`/`build`/`Analyze` failures.
  - `611`: 6 failing checks with `CodeRabbit` success.
  - `610`: `Analyze` + `build` failures (Go lint/analyze area) plus neutral CodeQL.
  - `609/608`: `verify-required-check-names`, `Analyze`, `Build Docs` failures.
- Merge status spread:
  - Mostly `BLOCKED` or `DIRTY` with both `MERGEABLE` and `CONFLICTING`.
  - High churn means these are mostly wave-merged migration branches rather than isolated work.
- Review/action signal:
  - Many PRs have issue comments (`review_comments=0` for sampled IDs, with comments often attached as issue-level threads).
  - Several PRs show `verify-required-check-names` drift, indicating required check manifest and workflow naming mismatch.

### thegent

| PR | Branch | Merge state | Issue comments | Review comments | Failing checks | Key issue |
|---|---|---|---:|---:|---:|---|
| 498 | garden/release-framework | BLOCKED | 2 | 0 | 45 | Global infra stack fail (`Build wheels`, `Build Docs`, `Comprehensive Benchmark`, platform tests) |
| 497 | chore/cliproxyctl-auto-install | BLOCKED | 2 | 0 | 19 | Same infra stack as #498 |
| 496 | PR: fix/tests3 | DIRTY | 4 | 0 | 2 | Mergeability noise despite mostly green checks |
| 494 | fix/orjson-v2 | DIRTY | 11 | 1 | 1 | `CodeRabbit` only; comment debt |
| 493 | fix/tests-v4 | DIRTY | 2 | 0 | 0 | Mostly green, mergeability still dirty |
| 482 | no-litellm | BLOCKED | 2 | 2 | 26 | Unresolved review threads in PR body + infra gate failures |
| 480 | fix/cli-test-fixes | BLOCKED | 2 | 2 | 17 | Unresolved review threads + test infra failures |
| 478 | fix/remove-broken-dag-files | DIRTY | 2 | 6 | 2 | 5+ unresolved review threads |

Notes:
- branch audit shows mixed mergeability metadata; treat as a **batch-first stabilization** where shared CI is fixed before per-PR conflict repair.

### agentapi-plusplus

| PR | Branch | Merge state | Issue comments | Review comments | Failing checks | Key issue |
|---|---|---|---:|---:|---:|---|
| 263 | fix/test-msg-format | BLOCKED | 4 | 0 | 5 | CodeRabbit needed |
| 262 | fix/slash-commands | BLOCKED | 4 | 0 | 5 | CodeRabbit needed |
| 261 | garden/sdk-integration | DIRTY | 5 | 0 | 1 | Merge conflicts |
| 260 | fix/pr17 | DIRTY | 5 | 0 | 5 | CodeRabbit needed |
| 259 | fix/pr16 | DIRTY | 5 | 0 | 5 | CodeRabbit needed |
| 258 | fix/pr14 | DIRTY | 4 | 0 | 5 | CodeRabbit needed |
| 257 | fix/pr13 | DIRTY | 2 | 0 | 5 | CodeRabbit needed |
| 256 | garden/git-tightening | BLOCKED | 2 | 0 | 4 | Mix of infra and review queue |
| 255 | fix/pagination | DIRTY | 4 | 0 | 1 | CodeRabbit needed |
| 254 | fix/opencodescreen-diff | DIRTY | 5 | 0 | 5 | CodeRabbit needed |
| 253 | fix/initial-prompt-tests | DIRTY | 4 | 0 | 5 | CodeRabbit needed |
| 252 | fix/health-check | DIRTY | 5 | 0 | 5 | CodeRabbit needed |
| 251 | fix/first-line-trimmed | DIRTY | 5 | 0 | 1 | CodeRabbit needed |
| 250 | fix/feature18 | BLOCKED | 5 | 0 | 5 | CodeRabbit needed |
| 249 | fix/e2e-asciinema | BLOCKED | 4 | 0 | 5 | CodeRabbit needed |
| 248 | fix/askuser-input | DIRTY | 4 | 0 | 5 | CodeRabbit needed |
| 247 | fix/afero-walk | DIRTY | 4 | 0 | 5 | CodeRabbit needed |
| 246 | fix/add-agent-info | DIRTY | 2 | 0 | 5 | CodeRabbit needed |
| 243 | fix/voice-input | DIRTY | 4 | 3 | 1 | Unresolved threaded comments + bot review |
| 242 | chore/docs-scaffold-and-test-fix | DIRTY | 4 | 12 | 1 | Substantial threaded review backlog |

## Re-review Actions Executed

- `agentapi-plusplus`:
  - Posted `@coderabbitai full review` on PRs: `#263, #262, #260, #259, #258, #257, #256, #255, #254`.
- `thegent`:
  - Posted `@coderabbitai full review` on PR `#494`.
- `cliproxyapi-plusplus`:
  - Broad full-sweep trigger for all open PRs was attempted but API/CLI timed out during batch execution.

## Priority Plan

1. Run repo-wide workflow baseline fixes first (`verify-required-check-names`, `Build Docs`, `Build wheels`, shared `go analyze` failures).
2. For `thegent`, unblock infra gates then resolve threaded reviews in `#478 -> #480 -> #482`.
3. For `agentapi-plusplus`, clear `CodeRabbit`-failing PRs with targeted re-review then address `CONFLICTING` stacks in numeric order.
4. For `cliproxyapi-plusplus`, process as migration waves with root/replay branches (`fix-ci`, `migrated*`, `lane*`) and keep canonical `main` local branch clean.

## Immediate next commands

- `git -C /Users/kooshapari/CodeProjects/Phenotype/repos/cliproxyapi-plusplus status --short --branch`
- `git -C /Users/kooshapari/CodeProjects/Phenotype/repos/cliproxyapi-plusplus worktree list`
- `for n in $(gh pr list --repo KooshaPari/cliproxyapi-plusplus --state open --json number --jq '.[].number' --limit 60); do gh pr checks $n --repo KooshaPari/cliproxyapi-plusplus --json name,state; done` (chunked)
- `gh pr checks <PR> --repo KooshaPari/agentapi-plusplus --json name,state`
- `gh pr checks <PR> --repo KooshaPari/thegent --json name,state`
