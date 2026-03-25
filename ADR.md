# Architecture Decision Records -- phenodocs

## ADR-001: VitePress as Documentation Engine

**Status:** Accepted
**Context:** Need a fast, Markdown-first static site generator with search, theming, and Vue component support.
**Decision:** Use VitePress for documentation federation.
**Alternatives:** Docusaurus (heavier, React-based), MkDocs (Python, less customizable).
**Consequences:** Vue-based theming; Node.js build dependency; excellent Markdown and search support.

## ADR-002: Federation via Git Subtree/Clone

**Status:** Accepted
**Context:** Docs from multiple repos need to be aggregated at build time without requiring manual copy.
**Decision:** Pull docs from source repos via git clone/sparse-checkout at build time into the VitePress `docs/` tree.
**Alternatives:** Git submodules (complex UX), manual copy (drift risk), monorepo (too coupled).
**Consequences:** Build script manages repo fetching; build depends on network access to source repos.

## ADR-003: Layered Content Organization

**Status:** Accepted
**Context:** Different audiences (developers, auditors, researchers) need different views of the same content.
**Decision:** Organize content into layers (lab, docs, audit, kb) via directory structure and frontmatter tags.
**Alternatives:** Single flat structure (harder to navigate), separate sites per audience (fragmented).
**Consequences:** Navigation auto-generated per layer; content can be tagged into multiple layers.

## ADR-004: .llms.txt for AI Context

**Status:** Accepted
**Context:** AI agents need structured project context without parsing raw HTML or Markdown.
**Decision:** Generate `.llms.txt` files at build time containing structured summaries per project section.
**Alternatives:** Raw Markdown (too verbose), custom API (overkill for static content).
**Consequences:** Build step added for llms.txt generation; agents can consume via file:// or HTTPS.
