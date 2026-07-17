# ARCHITECTURE.md — Parpoura Canonical Architecture

**Date:** 2026-06-11  
**Status:** ACTIVE  
**Scope:** Parpoura planning workspace and Venture architecture alignment

## Executive Summary

Parpoura is the canonical planning and specification workspace for the Kush ecosystem. It
curates cross-track specs, traceability agreements, and execution governance for the
Venture autonomy platform and its CIV simulation dependency graph.

At runtime, `Venture` is a policy-governed control-plane ecosystem with:

- Event-sourced workflows (`workflow.*`, `task.*`, `artifact.*`, `money.*`, `compliance.*`).
- Authorization and allowlist enforcement before agent actions.
- Deterministic artifact compilation and treasury/compliance controls.
- Explicit governance checkpoints for freeze/unfreeze, policy changes, and audit evidence.

## Four-Layer Architecture

### 1. Planning Layer (Parpoura)

Parpoura maintains and governs the spec corpus:

- Spec registry and dependency index (`SPECS_INDEX.md`).
- Track specifications (`TECHNICAL_SPEC.md`, `TRACK_A...`, `TRACK_B...`, `TRACK_C...`).
- Governance and gate controls (`docs/governance/*`, `QUALITY_GATES`, `ADR`).
- Evidence and integration contracts (`docs/traceability/*`, `docs/reference/*`).

### 2. Control Plane Layer

Core runtime services and policy runtime:

- `control-plane-api` for founder intents and lifecycle control.
- `policy-engine` for policy bundle checks, validation, and allowlist enforcement.
- `venture-orchestrator` for workflow/task orchestration and dispatch control.
- `agent-runtime` for dispatch execution (L1/L2/L3 role model).

### 3. Domain Runtime Layer

- `artifact-compiler` — artifact IR compilation, cache/checksum/provenance path.
- `treasury-api` — authorization lifecycle, double-entry ledger writes, velocity checks.
- `compliance-engine` — policy evaluation outcomes, audit validation, evidence events.

### 4. Ledger + Integration Layer

- `event-bus` (NATS/Jets) as append-only operational event substrate.
- PostgreSQL-backed event store and ledger projections.
- Redis for cache, idempotency keys, and rate-control state.
- Cross-project contracts in `docs/reference/INTERFACE_CONTRACTS.md`.

## Principal Data Flows

### Workflow and Task Flow

1. Founder intent enters `control-plane-api`.
2. `policy-engine` validates policy and role constraints.
3. `venture-orchestrator` schedules task envelope and dispatches execution.
4. `agent-runtime` executes, producing events and artifact/ledger/compliance artifacts.
5. `control-plane` emits append-only events and emits governance actions (`freeze`, `unfreeze`).

### Event-to-State Flow

- Every mutating action emits typed events into the event bus.
- Ledger and audit projections materialize immutable state views for compliance and traceability.
- Evidence chains are constructed through linked event IDs and schema contracts.

## Cross-System Contract Boundaries

- Parpoura ↔ Venture: governance, architecture, and traceability source-of-truth.
- Venture ↔ CIV: integration contracts for ledger events, state synchronization, compliance evidence, and
  deterministic replay requirements.
- Evidence consumers consume `docs/traceability/*` and `docs/reference/INTERFACE_CONTRACTS.md`
  for strict contract boundaries.

## Quality and Traceability Controls

- Spec quality gates: `docs/governance/QUALITY_GATES.md`.
- Traceability matrix: `docs/traceability/CROSS_PROJECT_TRACEABILITY.md`,
  `VENTURE_TRACEABILITY_MATRIX.md`, `EVENT_TAXONOMY.md`.
- Planning gates: `PLAN.md`, `NEXT_STEPS.md`, `WORK_STREAM` status tracking.

## References

- `TECHNICAL_SPEC.md`
- `TRACK_A_ARTIFACT_DETERMINISM_SPEC.md`
- `TRACK_B_TREASURY_COMPLIANCE_SPEC.md`
- `TRACK_C_CONTROL_PLANE.md`
- `API_EVENTS_SPEC.md`
- `DATA_MODEL_DB_SPEC.md`
- `OPS_COMPLIANCE_SPEC.md`
- `docs/reference/ECOSYSTEM_MAP.md`
- `docs/reference/INTERFACE_CONTRACTS.md`

