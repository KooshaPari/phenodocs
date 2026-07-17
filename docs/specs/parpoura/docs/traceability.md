# traceability

**Date:** 2026-06-11  
**Status:** SKELETON  
**Owner:** Parpoura Documentation Workstream

This file is the canonical navigation spine for **traceability artifacts**.

## Four-Pillar Traceability Index

### traceability

- `SPECS_INDEX.md` — full specification index and cross-track inventory
- `docs/traceability/CROSS_PROJECT_TRACEABILITY.md` — CIV ↔ Venture integration map
- `docs/traceability/EVENT_TAXONOMY.md` — event types and lifecycle semantics
- `docs/traceability/VENTURE_TRACEABILITY_MATRIX.md` — venture domain mapping
- `docs/reference/INTERFACE_CONTRACTS.md` — formal interoperability contracts

### SDLC-PM

- `PRD.md` — requirements and acceptance criteria
- `PLAN.md` — phased roadmap and dependency DAG
- `FUNCTIONAL_REQUIREMENTS.md` — requirement-to-spec coverage baseline
- `NEXT_STEPS.md` — planned implementation sequencing
- `USER_JOURNEYS.md` — journey-level behavioral expectations

### evidence-engine

- `OPS_COMPLIANCE_SPEC.md` — evidence, violation, and policy enforcement flows
- `TRACK_B_TREASURY_COMPLIANCE_SPEC.md` — ledger/evidence controls
- `TRACK_A_ARTIFACT_DETERMINISM_SPEC.md` — build determinism and reproducibility evidence
- `TRACK_C_CONTROL_PLANE.md` — execution evidence and task FSM traces
- `API_EVENTS_SPEC.md` — canonical event schemas
- `DATA_MODEL_DB_SPEC.md` — evidence artifacts and persistence model
- `SCHEMA_PACK.md` — canonical schema library for events and envelopes

### org-intel

- `docs/governance/GOVERNANCE_SUMMARY.md` — governance model and targets
- `docs/governance/QUALITY_GATES.md` — doc/spec quality criteria
- `docs/reference/ECOSYSTEM_MAP.md` — ecosystem overview and ownership context
- `docs/reference/WORK_STREAM.md` — execution trace for ownership and status
- `docs/ADR/` — decision traces for architecture and structure
- `TECHNICAL_SPEC.md` — architecture baseline for long-term evidence interpretation

## Status and Next Actions

1. Fill each pillar with concrete artifact owners per quarter.
2. Keep each row synchronized with `SPECS_INDEX.md` and `PLAN.md`.
3. Add open questions with owner + due date to `NEXT_STEPS.md` or ADRs.
4. Regenerate any derived traceability artifacts using governance workflows in
   `docs/governance/QUALITY_GATES.md`.
