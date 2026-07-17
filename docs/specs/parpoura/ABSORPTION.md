# Parpoura Absorption

**Absorbed:** 2026-07-17
**Source:** KooshaPari/Parpoura (84KB remote / 27MB local)
**Target:** phenodocs/docs/specs/parpoura/
**Disposition:** ABSORB (per registry row id=repo-Parpoura)
**Wave:** 2026-07-17-absorption

## What was absorbed

Parpoura is a dormant (30% complete, last push 2026-02-23) "spec-first
planning/architecture" repository for the Phenotype control-plane design. The
local checkout is doc-heavy: ~5MB of Markdown spread across PRD, FR, ADR, PLAN,
USER_JOURNEYS, TECHNICAL_SPEC, three track specs (A/B/C), DATA_MODEL_DB_SPEC,
API_EVENTS_SPEC, ARTIFACT_COMPILER_SPEC, OPS_COMPLIANCE_SPEC, SCHEMA_PACK,
ROLE_TOOL_ALLOWLIST_MATRIX, USER_SPEC, plus a `docs/` tree with research,
traceability, reference, and guides subtrees. The 27MB local size is dominated
by rendered HTML mirrors (each `.md` has an `.html` sibling in many cases) and
provenance dumps.

After absorption this directory holds **80 files / 2.7MB** of pure spec
content. Source repo archived on GitHub via
`gh repo archive KooshaPari/Parpoura -y`.

## Layout

```
docs/specs/parpoura/
├── README.md                              # mission + structure overview
├── PRD.md                                 # product requirements
├── TECHNICAL_SPEC.md                      # low-level design (44KB)
├── FUNCTIONAL_REQUIREMENTS.md             # FR / NFR map (41KB)
├── USER_JOURNEYS.md                       # end-to-end flows (65KB)
├── USER_SPEC.md                           # user lifecycle + roles (45KB)
├── PLAN.md                                # phased WBS (40KB)
├── IMPLEMENTATION_ROADMAP.md              # delivery sequencing (37KB)
├── PRODUCT_MODEL.md                       # product model (34KB)
├── ARCHITECTURE.md                        # architecture overview
├── COMPARISON.md                          # alternatives analysis
├── NEXT_STEPS.md                          # implementation sequencing
├── QUICK_START.md                         # onboarding quickstart
├── SPEC.md                                # canonical spec index
├── SPECS_INDEX.md                         # full spec index
├── SPECS_DELIVERY_INDEX.md                # delivery index
├── GOVERNANCE_SCAFFOLD_SUMMARY.md         # governance scaffolding
├── SCHEMA_PACK.md                         # shared payload/event/schema contracts
├── DATA_MODEL_DB_SPEC.md                  # data model + DB (105KB)
├── API_EVENTS_SPEC.md                     # API + events (149KB)
├── ARTIFACT_COMPILER_SPEC.md              # artifact compiler (37KB)
├── TRACK_A_ARTIFACT_DETERMINISM_SPEC.md   # track A (309KB)
├── TRACK_B_TREASURY_COMPLIANCE_SPEC.md    # track B (304KB)
├── TRACK_C_CONTROL_PLANE.md               # track C (219KB)
├── INFRASTRUCTURE_AND_TEST_SPECS.md       # infra + test specs
├── OPS_COMPLIANCE_SPEC.md                 # ops compliance (91KB)
├── ROLE_TOOL_ALLOWLIST_MATRIX.md          # role × tool matrix (85KB)
├── CLAUDE.md                              # agent operating context (29KB)
├── ADR.md                                 # master ADR index (27KB)
├── adr-markdown/                          # 7 individual ADR markdown files
├── traceability/                          # CROSS_PROJECT_TRACEABILITY,
│                                          # EVENT_TAXONOMY,
│                                          # VENTURE_TRACEABILITY_MATRIX
├── research/                              # 6 RND notes (RND-008 → RND-014)
│                                          # + RESEARCH_INDEX
│                                          # + CONVERSATION_DUMP provenance
├── reference/                             # ECOSYSTEM_MAP, INTERFACE_CONTRACTS,
│                                          # INFRASTRUCTURE_SPEC,
│                                          # LIBRARY_MANIFEST, SERVICE_CATALOG,
│                                          # SECURITY_THREAT_MODEL,
│                                          # CIVLAB_GAME_DESIGN,
│                                          # VENTURE_SELF_FUNDING_MECHANICS,
│                                          # WORK_STREAM + status trackers
└── docs/                                  # deep tree from docs/
    ├── BACKLOG.md
    ├── IMPLEMENTATION_PLAN.md
    ├── STATUS_REPORT.md
    ├── traceability.md
    ├── RELEASE_CHECKLIST.md
    ├── SPEC.md
    ├── index.md
    ├── journey-traceability.md
    └── guides/                            # 7 guide docs (anti-patterns,
                                           # AGILE_WORKSTREAM, COPILOT_L3,
                                           # GIT_WORKTREE, TEST_FIRST,
                                           # agent-orchestration, index)
```

## Excluded from absorption

The following categories were intentionally **not** copied because they either
duplicate phenodocs/Parpoura's own governance layer, are rendered HTML
duplicates of the Markdown sources, or are build/tooling artifacts that have no
place in a documentation site.

- **Rendered HTML**: `index.html`, `404.html`, `CHANGELOG.html`, `PRD.html`,
  `SPEC.html`, `QUALITY_GATES.html`, `WORKLOG.html`,
  `Joule-based Technocratic Economy.html`, plus all `.html` siblings under
  `adr/`, `docs/`, `governance/`, `guides/`, `reference/`, `research/`,
  `specs/`, `worklogs/`, `reports/`. The Markdown sources are canonical.
- **ChatGPT provenance dumps**: `ChatGPT_Conversation_2026-02-21.md` (550KB at
  root) and the 88 `docs/context/conv2/chunk_*.md` /
  `docs/context/conv2/chunk_*_parts/part_*__ChatGPT.md` files. These are
  LLM-conversation artifacts, not spec content. The
  `research/CONVERSATION_DUMP_2026-02-21.md` summary is retained as
  provenance metadata (it explains where the spec expansion came from).
- **Governance boilerplate**: `AGENTS.md`, `CODE_OF_CONDUCT.md`,
  `CODEOWNERS`, `CONTRIBUTING.md`, `CHANGELOG.md`, `FUNDING.yml`,
  `SECURITY.md`, `SUPPORT.md`, `LICENSE`, `LICENSE-APACHE`, `LICENSE-MIT`,
  `CITATION.cff`, `.env.example`, `SECURITY.md`. The canonical governance
  layer lives in `phenotype-registry/` and `phenodocs/`.
- **Build / tooling / lockfiles**: `package.json`, `package-lock.json`,
  `bun.lock`, `uv.lock`, `process-compose.yaml`, `pyproject.toml`,
  `Taskfile.yml`, `justfile`, `quality-gate.yml`, `qa-config.json`,
  `trufflehog.yml`, `ruff.toml`, `.pre-commit-config.yaml`, `.shellcheckrc`,
  `hashmap.json`, `vp-icons.css`, `VERSION`.
- **CI / IDE / dotfile configs**: `.github/`, `.airlock/`, `.devcontainer/`,
  `.gemini/`, `.gitattributes`, `.gitignore`, `.editorconfig`,
  `.coderabbit.yaml`.
- **Localization stubs**: `fa/`, `fa-Latn/`, `zh-CN/`, `zh-TW/` — empty
  placeholders.
- **Scripts / hooks / checks**: `scripts/`, `hooks/`, `checks/`,
  `worklogs/`, `tests/`, `traceability/`-related Python tests at root.
- **Duplicates under `docs/fragemented/`** (typo for "fragmented") — these
  are stale snapshots of guides/governance that mirror content already
  preserved in `docs/guides/` and the root files.
- **Assets**: `assets/` (diagrams/images) and `Joule-based Technocratic
  Economy_files/` — binary artifacts tied to the rendered HTML which is
  itself excluded.

## Runtime code (skipped, not absorbed)

Parpoura ships a small Python runtime under `venture/` (~6 stub modules:
`auth.py`, `database.py`, `eventbus/schema.py`, `ledger/schema.py`,
`api/main.py`, `__init__.py`) and `tests/` (~11 stub pytest files). These
are skeleton scaffolds tied to a venture concept that never reached
implementation (the README marks the project 30% complete and DORMANT).

This absorption is **docs-only**. The `venture/` Python stubs are not
copied because:

1. They are dormant stubs with no proven behavior — copying them would
   create dead code in phenodocs.
2. They are runtime code, not documentation. If revived, they belong in
   `phenotype-apps` or a dedicated repo, not in a docs site.
3. The repository was archived as-is; the runtime can be revived
   independently from this absorption if the venture concept is picked up.

The `venture/` and `tests/` trees remain in the (now archived) source repo
for forensic reference.

## Related registry entries

- Registry row: `repo-Parpoura` in
  `phenotype-registry/registry/disposition-index.json`
- Absorption audit: `phenotype-registry/audits/absorption-justifications/Parpoura-2026-07-17.md`
- Boundary doc: `phenotype-registry/docs/boundary/Parpoura.md` (created during
  absorption)
- Source repo: `KooshaPari/Parpoura` — archived 2026-07-17

## Provenance

This directory is byte-for-byte identical to the corresponding paths in
`KooshaPari/Parpoura` at commit `50976ab` (main HEAD at absorption time).
No content has been edited, reorganized, or rewritten during absorption
except for the addition of this `ABSORPTION.md` provenance note.
