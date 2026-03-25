# SPEC.md — xDD Methodologies & Best Practices

## Overview

This document specifies the xDD methodologies and best practices enforced in phenodocs.

## Development Methodologies (50+)

### TDD Family

| Method | Status | Description |
|--------|--------|-------------|
| TDD | ✅ Required | Test-Driven Development - Red/Green/Refactor cycle |
| BDD | ✅ | Behavior-Driven Development - Gherkin scenarios |
| DDD | ✅ | Domain-Driven Design - bounded contexts |
| ATDD | 🟡 | Acceptance Test-Driven Development |
| SDD | 🟡 | Specification-Driven Development - doc tests |
| FDD | 🔴 | Feature-Driven Development |
| CDD | ✅ | Context-Driven Development |
| IDD | 🔴 | Intent-Driven Development |
| MDD | 🟡 | Model-Driven Development |
| RDD | 🔴 | README-Driven Development |
| Property-Based Testing | 🔴 | Generate inputs, verify invariants |
| Mutation Testing | 🔴 | Verify test quality |
| Contract Testing | 🔴 | Consumer-Driven Contracts |

### Design Principles

| Principle | Status | Description |
|-----------|--------|-------------|
| DRY | ✅ | Don't Repeat Yourself |
| KISS | ✅ | Keep It Simple, Stupid |
| YAGNI | ✅ | You Aren't Gonna Need It |
| SOLID | ✅ | Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion |
| GRASP | ✅ | General Responsibility Assignment Software Patterns |
| LoD | 🟡 | Law of Demeter |
| SoC | ✅ | Separation of Concerns |
| PoLA | 🟡 | Principle of Least Astonishment |

### Architecture Patterns

| Pattern | Status | Description |
|---------|--------|-------------|
| Clean Architecture | ✅ | Entities, Use Cases, Controllers, Frameworks |
| Hexagonal/Ports&Adapters | ✅ | Ports, Adapters, Domain Core |
| Onion Architecture | ✅ | Domain, Application, Infrastructure |
| CQRS | 🟡 | Command Query Responsibility Segregation |
| Event Sourcing | 🔴 | Immutable event log |
| EDA | 🟡 | Event-Driven Architecture |
| Reactive | 🔴 | Non-blocking, async message-passing |

### Quality Gates

| Gate | Status |
|------|--------|
| cargo fmt | ✅ |
| cargo clippy | ✅ |
| cargo test | ✅ |
| cargo doc | 🟡 |
| codespell | ✅ |
| cargo-deny | ✅ |
| fuzz tests | 🔴 |
| Mutation testing | 🔴 |

## File Structure

```
phenodocs/
├── SPEC.md
├── Cargo.toml
├── src/
│   └── lib.rs
├── tests/
└── benches/
```

## CI/CD Pipeline

1. Format check
2. Lint/clippy
3. Test
4. Doc generation
5. Spell check
6. Security audit

## References

- TDD: Test-Driven Development by Example (Beck)
- BDD: Cucumber/Gherkin
- DDD: Domain-Driven Design (Evans)
- Clean Architecture: Uncle Bob
- Hexagonal: Ports & Adapters (Cockburn)
