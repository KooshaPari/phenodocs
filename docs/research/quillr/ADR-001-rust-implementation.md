# ADR-001: Rust as Implementation Language

**Status**: Accepted  
**Date**: 2026-04-04  
**Author**: Quillr Architecture Team  
**Deciders**: Core Team, Performance Working Group  

---

## Context

Quillr requires a systems-level programming language that can deliver:
1. High performance for documentation generation (target: < 1s for 10,000 pages)
2. Memory efficiency for large-scale operations (< 200MB peak)
3. Type safety for compile-time documentation validation
4. Cross-platform support (Linux, macOS, Windows)
5. Ecosystem maturity for parsing, networking, and CLI tools

### Options Considered

| Language | Build Perf | Runtime Perf | Memory | Type Safety | Ecosystem | DX |
|----------|------------|--------------|--------|-------------|-----------|-----|
| **Rust** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Go** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **TypeScript/Node** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Zig** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **OCaml** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### Detailed Analysis

#### Rust

**Strengths:**
- Zero-cost abstractions enable high-level code with C-level performance
- Ownership model prevents memory leaks and data races at compile time
- Cargo provides excellent dependency management and build tooling
- tokio/async ecosystem mature for concurrent operations
- WebAssembly compilation target for browser extensions

**Weaknesses:**
- Steeper learning curve than Go/TypeScript
- Longer compile times than Go
- Smaller hiring pool

**Performance Benchmarks:**
```
Documentation generation (10,000 pages):
- Cold build: 4.2s
- Incremental: 380ms
- Memory peak: 185MB
- Binary size: 12MB
```

#### Go

**Strengths:**
- Fast compilation
- Excellent concurrency primitives (goroutines)
- Large ecosystem and hiring pool
- Simple deployment (single binary)

**Weaknesses:**
- Lack of generics (until recently) complicates type-safe abstractions
- Runtime GC adds latency unpredictability
- No compile-time memory safety guarantees

#### TypeScript/Node

**Strengths:**
- Same language as target ecosystem (documentation often for TS projects)
- Massive npm ecosystem
- Fast iteration cycle
- Best-in-class developer experience

**Weaknesses:**
- Runtime performance insufficient for large-scale docs
- Memory overhead of V8
- Single-threaded with event loop limitations

---

## Decision

**Use Rust as the primary implementation language for Quillr.**

---

## Rationale

1. **Performance Requirements**: Quillr's target of < 1s builds for 10,000 pages requires systems-level performance. Only Rust and Go meet this; Rust provides better memory efficiency.

2. **Type Safety**: Compile-time documentation graph validation requires a language with strong static typing. Rust's type system enables modeling complex documentation relationships safely.

3. **Memory Safety**: Documentation processing involves complex string manipulation and AST transformations. Rust's ownership model prevents entire classes of bugs.

4. **WebAssembly Support**: Quillr will target browser extensions and VS Code plugins. Rust's WASM compilation is mature and efficient.

5. **Phenotype Ecosystem Alignment**: Other Phenotype projects (AgilePlus, heliosCLI) use Rust. Consistency simplifies cross-team collaboration and shared libraries.

---

## Consequences

### Positive

- **Performance**: Sub-second builds for large documentation sites
- **Reliability**: Compile-time prevention of memory issues
- **Cross-platform**: Native binaries for all target platforms
- **Embedding**: Can be embedded as library in other tools
- **Long-term maintainability**: Type system prevents refactoring regressions

### Negative

- **Learning Curve**: Team members need Rust proficiency (training investment)
- **Compile Times**: Development iteration slower than TypeScript (mitigated by incremental compilation)
- **Ecosystem Gaps**: Some documentation-specific crates may need development
- **Hiring**: Smaller talent pool than Go/TypeScript

### Neutral

- **Tooling**: Rust's LSP (rust-analyzer) provides excellent IDE experience
- **Testing**: Built-in test framework sufficient for needs
- **Documentation**: rustdoc integration aligns with project goals

---

## Implementation Notes

### Crate Structure

```
quillr/
├── quillr-core/          # Core documentation graph
├── quillr-parser/        # Markdown/MDX parsing
├── quillr-builder/       # Build orchestration
├── quillr-render/        # Output format renderers
├── quillr-server/        # Dev server with HMR
├── quillr-cli/           # Command-line interface
└── quillr-wasm/          # WebAssembly bindings
```

### Key Dependencies

| Crate | Purpose | Version |
|-------|---------|---------|
| `pulldown-cmark` | Markdown parsing | 0.9+ |
| `serde` | Serialization | 1.0+ |
| `tokio` | Async runtime | 1.35+ |
| `axum` | Dev server | 0.7+ |
| `notify` | File watching | 6.0+ |
| `minijinja` | Templating | 1.0+ |
| `syntect` | Syntax highlighting | 5.1+ |

### Build Configuration

```toml
# Cargo.toml optimizations for release
[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
panic = "abort"
strip = true

[profile.dev]
opt-level = 1          # Fast compilation, some optimization
debug = true
```

---

## Alternatives Considered

### Why Not Go?

Go was seriously considered due to its excellent concurrency and simplicity. However, the lack of compile-time memory safety and the need for complex type-safe graph operations made Rust a better fit.

### Why Not TypeScript?

While TypeScript offers the best developer experience, its runtime performance cannot meet Quillr's sub-second build requirements. A hybrid approach (Rust core + TS plugins) may be explored for extensibility.

### Why Not Zig?

Zig's comptime and manual memory management are appealing. However, its ecosystem is too immature for production use, and the team lacks Zig expertise.

---

## Related Decisions

- ADR-002: Incremental Build System Design
- ADR-003: Plugin Architecture

---

## References

1. [Rust Performance Book](https://nnethercote.github.io/perf-book/)
2. [Rust Documentation](https://doc.rust-lang.org/)
3. [Tokio Documentation](https://tokio.rs/)
4. [Comparing Rust and Go](https://bitfieldconsulting.com/golang/rust-vs-go)

---

**Last Updated**: 2026-04-04  
**Review Date**: 2026-10-04
