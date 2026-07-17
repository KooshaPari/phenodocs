# SPEC.md — Parpoura Canonical Specification Index

**Date:** 2026-06-11  
**Status:** ACTIVE  
**Owner:** Parpoura Working Group  
**Scope:** Canonical navigation for the four core spec pillars:
`traceability`, `SDLC-PM`, `evidence-engine`, `org-intel`.

## Source of Truth

The canonical engineering source remains:

- `TECHNICAL_SPEC.md`
- `TRACK_A_ARTIFACT_DETERMINISM_SPEC.md`
- `TRACK_B_TREASURY_COMPLIANCE_SPEC.md`
- `TRACK_C_CONTROL_PLANE.md`
- `API_EVENTS_SPEC.md`
- `DATA_MODEL_DB_SPEC.md`
- `OPS_COMPLIANCE_SPEC.md`
- `USER_SPEC.md`
- `PRODUCT_MODEL.md`
- `SCHEMA_PACK.md`
- `IMPLEMENTATION_ROADMAP.md`

Operational context:

- `PRD.md`
- `FUNCTIONAL_REQUIREMENTS.md`
- `NEXT_STEPS.md`
- `SPECS_INDEX.md`
- `docs/operations/journey-traceability.md`

## 1) traceability

Purpose: keep cross-system dependencies and event semantics traceable.

- `SPECS_INDEX.md` — full spec index and integration map
- `docs/traceability/CROSS_PROJECT_TRACEABILITY.md` — CIV ↔ Venture mapping
- `docs/traceability/EVENT_TAXONOMY.md` — canonical event and lifecycle taxonomies
- `docs/traceability/VENTURE_TRACEABILITY_MATRIX.md` — internal venture mapping
- `docs/reference/INTERFACE_CONTRACTS.md` — 5 formal integration contracts
- `TECHNICAL_SPEC.md` and `API_EVENTS_SPEC.md` — architectural/event foundations
- `PLAN.md` — phased execution and dependency graph

## 2) SDLC-PM

Purpose: keep delivery, planning, and requirement traceability coherent.

- `PRD.md` — product requirements and acceptance criteria
- `FUNCTIONAL_REQUIREMENTS.md` — FR/NFR map for capability and testing
- `PLAN.md` — project DAG and dependencies
- `NEXT_STEPS.md` — implementation sequencing and owners
- `USER_JOURNEYS.md` — operational/user journey intent
- `USER_SPEC.md` — user lifecycle and role expectations
- `docs/ADR` — architecture and process decisions

## 3) evidence-engine

Purpose: define verifiable proof of behavior across compliance, audit, treasury, and event systems.

- `OPS_COMPLIANCE_SPEC.md` — compliance policy and evidence handling
- `TRACK_B_TREASURY_COMPLIANCE_SPEC.md` — money authorization and ledger controls
- `TRACK_A_ARTIFACT_DETERMINISM_SPEC.md` — build determinism and reproducibility
- `TRACK_C_CONTROL_PLANE.md` — dispatch, FSM, and execution guarantees
- `API_EVENTS_SPEC.md` — schema contracts and stream semantics
- `DATA_MODEL_DB_SPEC.md` — evidence artifacts, cases, audit logs, and projections
- `SCHEMA_PACK.md` — shared payload, event, and schema contracts
- `docs/governance/QUALITY_GATES.md` — spec completion criteria

## 4) org-intel

Purpose: capture governance, architecture intent, and ecosystem operating context.

- `README.md` — repository mission and structure
- `CLAUDE.md` / `AGENTS.md` — operational governance baseline
- `docs/adr/ADR-001-workspace-structure.md` — repository layout governance
- `docs/governance/GOVERNANCE_SUMMARY.md` — governance stack and targets
- `docs/governance/QUALITY_GATES.md` — governance and quality controls
- `docs/reference/ECOSYSTEM_MAP.md` — ecosystem architecture and ownership
- `docs/reference/WORK_STREAM.md` — execution status for org tracking
- `docs/reference/SERVICE_CATALOG.md` — system service inventory

## Canonical Update Rule

When canonical behavior changes:

1. Edit the owning spec first (`TECHNICAL_SPEC.md`, relevant track spec, or `PRD.md`).
2. Update downstream traceability indexes in this file and `SPECS_INDEX.md`.
3. Update `PLAN.md` and `NEXT_STEPS.md` for sequencing and ownership if scope changed.
4. Re-run quality checks documented in `docs/governance/QUALITY_GATES.md`.

