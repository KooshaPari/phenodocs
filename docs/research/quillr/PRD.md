# Product Requirements Document — Quillr

**Version**: 2.0  
**Status**: Design  
**Last Updated**: 2026-04-05

---

## Overview

Quillr is a **next-generation documentation generation system** for the Phenotype ecosystem, built in Rust with a focus on type safety, performance, and extensibility. It addresses the limitations of existing documentation tools while providing a foundation for the future of technical documentation.

### What Quillr Is

- **Type-Safe Documentation**: Compile-time validation of documentation graph
- **Incremental Builds**: Sub-500ms rebuilds for single page changes
- **Multi-Format Output**: HTML, PDF, Markdown from single source
- **WASM Plugin System**: Safe, language-agnostic extensibility
- **Phenotype Native**: AgilePlus, HexaKit, PhenoSpecs integration

### What Quillr Is Not

- Not a CMS (content managed externally)
- Not a static site generator (for general websites)
- Not a wiki (no built-in editing UI)
- Not a documentation hosting platform (generates output only)

---

## Problem Statement

Current documentation tools have fundamental limitations:

| Problem | Impact | Current Solutions |
|---------|--------|-------------------|
| Build Speed | Developers wait minutes for changes | Hugo (fast but limited) |
| Type Safety | Broken links caught at runtime | None |
| Scalability | Large sites (10K+ pages) slow | Gatsby, Docusaurus (slow) |
| Extensibility | Fork or plugin limitations | Docusaurus plugins |
| Ecosystem | Phenotype integration missing | Custom scripts |

Quillr addresses these by combining Rust performance with type-safe documentation validation and a modern plugin architecture.

---

## Goals

| Goal | Description | Success Metric |
|------|-------------|----------------|
| Build Performance | < 5s for 10K pages | Benchmark verified |
| Incremental Builds | < 500ms for single page | Benchmark verified |
| Type Safety | Compile-time validation | Zero runtime errors |
| Memory Efficiency | < 200MB peak | Profiling verified |
| Plugin System | WASM-based extensibility | Working examples |
| Phenotype Integration | AgilePlus, HexaKit native | Full support |

---

## Non-Goals

- **Full CMS functionality**: Quillr generates from source files
- **WYSIWYG editing**: Authors use their preferred editors
- **User authentication**: Hosting platform handles this
- **Analytics collection**: Integrate with external tools
- **Multi-language content**: English-only initially

---

## Epics & User Stories

### E1 — Core Documentation Generation

**Goal**: Parse Markdown, code comments, and config into a documentation graph.

| Story | As a... | I want... | So that... |
|-------|---------|----------|------------|
| E1.1 | Author | Write in Markdown | I use familiar syntax |
| E1.2 | Author | Include code examples | I show how things work |
| E1.3 | Author | Reference other pages | I create linked docs |
| E1.4 | Author | Add frontmatter metadata | I can categorize content |
| E1.5 | Developer | Extract API docs from code | Docs stay in sync |

**Acceptance Criteria**:
- Markdown files are parsed correctly
- Code blocks are syntax highlighted
- Internal links are validated
- Frontmatter is extracted

---

### E2 — Incremental Build System

**Goal**: Only rebuild changed pages and their dependents.

| Story | As a... | I want... | So that... |
|-------|---------|----------|------------|
| E2.1 | Developer | Sub-500ms rebuild | I get instant feedback |
| E2.2 | Developer | Dependency tracking | Related pages update |
| E2.3 | Developer | Cache invalidation | Only stale content rebuilds |
| E2.4 | Developer | Parallel rendering | Builds utilize all cores |
| E2.5 | DevOps | Deterministic builds | Reproducible output |

**Acceptance Criteria**:
- Single page change triggers < 500ms rebuild
- Content-addressable cache for outputs
- Transitive dependency updates
- Parallel rendering with work-stealing

---

### E3 — Plugin System

**Goal**: Extensible architecture via WASM plugins.

| Story | As a... | I want... | So that... |
|-------|---------|----------|------------|
| E3.1 | Developer | Write plugins in any language | I use familiar tools |
| E3.2 | Developer | Sandboxed execution | Plugins can't break builds |
| E3.3 | Developer | Access to content AST | I transform docs |
| E3.4 | Developer | Custom output formats | I generate specialized output |
| E3.5 | Developer | Plugin hooks | I integrate at build stages |

**Acceptance Criteria**:
- Plugins compiled to WASM run safely
- Plugin manifest declares capabilities
- Transform, filter, and hook APIs available
- Official plugins for analytics, SEO, i18n

---

### E4 — Template Engine

**Goal**: Flexible, performant template rendering.

| Story | As a... | I want... | So that... |
|-------|---------|----------|------------|
| E4.1 | Developer | Template inheritance | I share layouts |
| E4.2 | Developer | Custom filters | I format data |
| E4.3 | Developer | Hot reload | I see changes instantly |
| E4.4 | Designer | CSS variables | I theme easily |
| E4.5 | Author | Shortcodes | I embed complex content |

**Acceptance Criteria**:
- MiniJinja-based rendering
- Template inheritance with blocks
- Custom filter registration
- Development server with HMR

---

### E5 — Multi-Format Output

**Goal**: Generate HTML, PDF, Markdown, and IDE integration.

| Story | As a... | I want... | So that... |
|-------|---------|----------|------------|
| E5.1 | Author | HTML output | I publish to web |
| E5.2 | Author | PDF generation | I create printable docs |
| E5.3 | Developer | Markdown output | I integrate with other tools |
| E5.4 | Developer | LSP integration | I get docs in IDE |
| E5.5 | Developer | CLI help generation | I auto-document commands |

**Acceptance Criteria**:
- Static HTML site with search
- PDF via LaTeX/WeasyPrint
- Markdown export preserves structure
- Language Server for hover docs

---

### E6 — Search and Navigation

**Goal**: Fast, relevant search with structured navigation.

| Story | As a... | I want... | So that... |
|-------|---------|----------|------------|
| E6.1 | Author | Full-text search | Readers find content |
| E6.2 | Author | Search ranking tuning | Best results first |
| E6.3 | Author | Navigation structure | Readers browse easily |
| E6.4 | Author | Previous/Next links | Readers follow linearly |
| E6.5 | Author | Breadcrumbs | Readers know location |

**Acceptance Criteria**:
- Index built at build time
- Sub-50ms query latency
- Configurable result ranking
- Auto-generated navigation

---

### E7 — Performance Engineering

**Goal**: Sub-1s builds for 10K pages, minimal memory.

| Story | As a... | I want... | So that... |
|-------|---------|----------|------------|
| E7.1 | Developer | Parallel processing | Builds use all cores |
| E7.2 | Developer | Content hashing | Cache works correctly |
| E7.3 | Developer | Streaming output | Memory is bounded |
| E7.4 | DevOps | Incremental CI | Deployments are fast |
| E7.5 | Developer | Bundle analysis | I find size issues |

**Performance Targets**:
| Metric | Target | SOTA (Docusaurus) |
|--------|--------|-------------------|
| 10K page build | < 5s | 90s |
| Incremental (1 page) | < 500ms | 12s |
| Memory peak | < 200MB | 800MB |
| Output size | < 50MB | 180MB |

---

### E8 — Phenotype Ecosystem Integration

**Goal**: Deep integration with Phenotype tools.

| Story | As a... | I want... | So that... |
|-------|---------|----------|------------|
| E8.1 | Developer | AgilePlus specs | Feature docs auto-generate |
| E8.2 | Developer | HexaKit templates | I use consistent layouts |
| E8.3 | Developer | PhenoSpecs linking | ADRs are traceable |
| E8.4 | Developer | CLI Proxy docs | Commands are documented |
| E8.5 | Author | Worklog integration | I track decisions |

**Acceptance Criteria**:
- AgilePlus feature parsing
- HexaKit template support
- PhenoSpecs reference resolution
- CLI Proxy command extraction

---

## Acceptance Criteria Matrix

| Epic | Criterion | Verification |
|------|-----------|--------------|
| E1 | Markdown parsing | Unit test |
| E1 | Code extraction | Integration test |
| E1 | Link validation | Unit test |
| E2 | < 500ms incremental | Benchmark |
| E2 | Dependency tracking | Unit test |
| E2 | Cache correctness | Integration test |
| E3 | WASM plugins run | Integration test |
| E3 | Sandboxed execution | Security test |
| E4 | Template rendering | Unit test |
| E4 | HMR in dev server | Manual test |
| E5 | HTML output | Visual inspection |
| E5 | PDF generation | Manual test |
| E6 | Search index | Performance test |
| E6 | Navigation generation | Unit test |
| E7 | Benchmarks meet targets | CI benchmark |
| E8 | AgilePlus integration | Integration test |

---

## Dependencies

| Dependency | Purpose | Version |
|------------|---------|---------|
| Rust | Primary language | 1.85+ |
| tokio | Async runtime | 1.x |
| MiniJinja | Template engine | 2.x |
| pulldown-cmark | Markdown parsing | 0.12.x |
| blake3 | Content hashing | 0.10.x |
| wasmtime | WASM runtime | 28.x |
| serde | Serialization | 1.x |
| notify | File watching | 6.x |

---

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Build time (10K pages) | < 5s | TBD |
| Incremental build | < 500ms | TBD |
| Memory usage | < 200MB | TBD |
| Test coverage | > 80% | TBD |
| Type safety | 100% | TBD |

---

## Future Considerations

- **AI-Powered Search**: Semantic understanding of content
- **Real-Time Collaboration**: CRDT-based multi-user editing
- **Interactive Code Sandboxes**: Runnable examples
- **Visual Editing**: Hybrid WYSIWYG for non-technical authors
- **Voice Navigation**: Voice-controlled documentation

---

**Document Owner**: Platform Architecture Team  
**Reviewers**: Engineering, Design, Product  
**Last Updated**: 2026-04-05
