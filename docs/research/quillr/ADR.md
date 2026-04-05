# Architecture Decision Records

> Quillr Documentation System Architecture Decisions

**Project**: Quillr  
**Version**: 2.0  
**Status**: Active  
**Last Updated**: 2026-04-04  

---

## Active ADRs

| ADR | Title | Status | Date | Impact |
|-----|-------|--------|------|--------|
| [ADR-001](docs/adr/ADR-001-rust-implementation.md) | Rust as Implementation Language | Accepted | 2026-04-04 | High |
| [ADR-002](docs/adr/ADR-002-incremental-build-system.md) | Incremental Build System with Content-Addressable Storage | Accepted | 2026-04-04 | High |
| [ADR-003](docs/adr/ADR-003-plugin-architecture.md) | Plugin Architecture with WebAssembly Extensions | Accepted | 2026-04-04 | High |

---

## ADR Status Definitions

| Status | Description |
|--------|-------------|
| **Proposed** | Under discussion, not yet approved |
| **Accepted** | Approved and being implemented |
| **Deprecated** | No longer recommended, superseded by newer ADR |
| **Rejected** | Considered and explicitly rejected |
| **Superseded** | Replaced by a newer ADR (link provided) |

---

## Quick Reference

### ADR-001: Rust as Implementation Language
**Decision**: Use Rust as the primary implementation language for Quillr.

**Key Points**:
- Performance: < 1s builds for 10,000 pages
- Type safety: Compile-time documentation validation
- Memory safety: Ownership model prevents leaks
- WASM support: Native browser/IDE extension compilation
- Ecosystem alignment: Other Phenotype projects use Rust

**Consequences**:
- Steeper learning curve than Go/TypeScript
- Longer compile times (mitigated by incremental compilation)
- Exceptional runtime performance and reliability

---

### ADR-002: Incremental Build System with Content-Addressable Storage
**Decision**: Implement content-addressable incremental build system.

**Key Points**:
- BLAKE3 content hashing for cache keys
- Fine-grained dependency graph tracking
- Sub-second incremental builds (< 500ms for single page)
- Distributed cache support for CI/CD
- Deterministic, reproducible builds

**Consequences**:
- 100x faster incremental builds
- Never miss dependency changes
- More complex than simple mtime approaches
- Cache storage overhead (mitigated by LRU)

---

### ADR-003: Plugin Architecture with WebAssembly Extensions
**Decision**: Hybrid plugin architecture: Native + WASI + Scripts.

**Key Points**:
- Core plugins: Native Rust for performance
- Standard plugins: WebAssembly (WASI) for security + flexibility
- Script plugins: QuickJS for simple transformations
- Capability-based sandboxing
- Near-native WASM performance (within 10-20%)

**Consequences**:
- Sandboxed execution prevents malicious plugins
- Plugins in any WASM-compilable language
- Multiple runtime systems to maintain
- Slightly more complex debugging

---

## ADR Process

### Creating a New ADR

1. **Copy template** from `docs/adr/template.md`
2. **Fill in context**, options considered, and decision
3. **Submit PR** for discussion
4. **Address feedback** and update
5. **Merge** when accepted

### ADR Template

```markdown
# ADR-XXX: Title

**Status**: Proposed
**Date**: YYYY-MM-DD
**Author**: Name
**Deciders**: Team

## Context
What is the issue we're deciding?

## Options Considered
| Option | Pros | Cons |
|--------|------|------|
| Option A | ... | ... |
| Option B | ... | ... |

## Decision
What was decided?

## Rationale
Why this decision?

## Consequences
What are the positive/negative impacts?

## Related Decisions
Links to related ADRs

## References
External resources
```

---

## Decision Log

### 2026-04-04
- ✅ Accepted: ADR-001, ADR-002, ADR-003
- Project foundation established

---

**Maintained by**: Quillr Architecture Team  
**Review Cycle**: Quarterly  
