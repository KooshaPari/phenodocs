# Quillr Specification

> Type-Safe Documentation Generation System for the Phenotype Ecosystem

**Version**: 2.0  
**Status**: Draft  
**Last Updated**: 2026-04-04  
**Classification**: Technical Specification  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Charter and Tenets](#charter-and-tenets)
3. [System Overview](#system-overview)
4. [Architecture](#architecture)
5. [Core Components](#core-components)
6. [Data Model](#data-model)
7. [Build System](#build-system)
8. [Plugin System](#plugin-system)
9. [Development Server](#development-server)
10. [Output Formats](#output-formats)
11. [Performance Specification](#performance-specification)
12. [Security Model](#security-model)
13. [API Reference](#api-reference)
14. [CLI Interface](#cli-interface)
15. [Configuration](#configuration)
16. [Testing Strategy](#testing-strategy)
17. [Deployment](#deployment)
18. [Integration Points](#integration-points)
19. [Migration Guide](#migration-guide)
20. [Appendices](#appendices)

---

## Executive Summary

Quillr is a next-generation documentation generation system designed for the Phenotype ecosystem. Built in Rust with a focus on type safety, performance, and extensibility, Quillr addresses the limitations of existing documentation tools while providing a foundation for the future of technical documentation.

### Key Capabilities

| Capability | Description | Status |
|------------|-------------|--------|
| **Type-Safe Documentation** | Compile-time validation of documentation graph | Design |
| **Incremental Builds** | < 500ms rebuilds for single page changes | Design |
| **Multi-Format Output** | HTML, PDF, Markdown, IDE integration from single source | Design |
| **WebAssembly Plugins** | Safe, language-agnostic extensibility | Design |
| **Real-time Collaboration** | CRDT-based collaborative editing | Future |
| **Phenotype Integration** | Native AgilePlus, HexaKit, PhenoSpecs support | Design |

### Target Users

1. **Documentation Authors**: Technical writers, developers, product managers
2. **Platform Engineers**: Teams maintaining documentation infrastructure
3. **Open Source Maintainers**: Projects needing comprehensive documentation
4. **Enterprise Documentation Teams**: Organizations with complex documentation needs

### Success Metrics

| Metric | Target | Current SOTA |
|--------|--------|--------------|
| Build Time (10,000 pages) | < 5s | Hugo: 2.3s, Docusaurus: 90s |
| Incremental Build | < 500ms | VitePress: 3s, Gatsby: 60s |
| Memory Usage | < 200MB | Hugo: 180MB, Docusaurus: 800MB |
| Type Safety | Compile-time | None in existing tools |

---

## Charter and Tenets

### Mission

To create the fastest, most reliable, and most extensible documentation generation system for technical teams, enabling documentation that is as well-crafted as the code it describes.

### Tenets (Unless You Know Better Ones)

These tenets guide Quillr's development. They are guidelines and goals, not absolute rules.

#### Tenet 1: Performance First

Documentation builds should be instantaneous. A developer waiting for documentation to build is a developer not solving problems.

- Target: < 1 second for sites under 10,000 pages
- Target: < 500ms for incremental rebuilds
- Measure: Continuous benchmarking in CI

#### Tenet 2: Type Safety

Documentation should be as type-safe as the code it documents. Broken links, missing references, and invalid cross-references should be caught at build time, not by users.

- All internal links validated at compile time
- Required sections enforced by schema
- Cross-references verified against documentation graph

#### Tenet 3: Developer Experience

The best documentation tool is the one developers actually use. Quillr prioritizes:

- Instant feedback in development (HMR)
- Clear error messages with suggestions
- IDE integration with autocomplete
- Minimal configuration for common cases

#### Tenet 4: Extensibility Without Compromise

Users should be able to customize without forking. The plugin system must be:

- Safe (sandboxed execution)
- Fast (near-native performance)
- Flexible (any language via WASM)

#### Tenet 5: Phenotype Native

Quillr is built for the Phenotype ecosystem and integrates deeply with:

- AgilePlus specifications
- HexaKit templates
- PhenoSpecs standards
- CLI Proxy patterns

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                   Quillr System                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                              Input Layer                                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │   │
│  │  │  Markdown   │  │    MDX      │  │    YAML     │  │   Phenotype Sources     │  │   │
│  │  │   Files     │  │  Components │  │   Config    │  │  (AgilePlus, etc.)      │  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │   │
│  └─────────┼────────────────┼────────────────┼─────────────────────┼──────────────────┘   │
│            │                │                │                     │                      │
│            └────────────────┴────────────────┴─────────────────┘                      │
│                              │                                                          │
│                              v                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         Content Processing Layer                                 │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────────┐     │   │
│  │  │    Parser       │  │   Frontmatter   │  │   Type Extraction               │     │   │
│  │  │  (pulldown-     │  │   Processor     │  │   (from code comments)          │     │   │
│  │  │   cmark)        │  │                 │  │                                 │     │   │
│  │  └────────┬────────┘  └────────┬────────┘  └────────────────┬────────────────┘     │   │
│  └───────────┼────────────────────┼────────────────────────────┼──────────────────────┘   │
│              │                    │                            │                        │
│              └────────────────────┴────────────────────────────┘                        │
│                                    │                                                    │
│                                    v                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                         Documentation Graph                                      │   │
│  │  ┌─────────────────────────────────────────────────────────────────────────┐    │   │
│  │  │  Nodes: Pages, Sections, API References, Code Blocks, Cross-References   │    │   │
│  │  │  Edges: Includes, References, Version-of, Depends-on                      │    │   │
│  │  │  Index: Full-text search, Type index, Tag index                           │    │   │
│  │  └─────────────────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                    │                                                    │
│                                    v                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                           Build Pipeline                                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │   │
│  │  │   Plugin    │  │  Template   │  │   Render    │  │   Post-Processing       │  │   │
│  │  │   Pipeline  │  │   Engine    │  │   Engine    │  │   (optimization)        │  │   │
│  │  │             │  │             │  │             │  │                         │  │   │
│  │  │ • Transforms│  │ • Minijinja │  │ • HTML      │  │ • Minification          │  │   │
│  │  │ • Filters   │  │ • React/Vue│  │ • Markdown│  │ • Image optimization    │  │   │
│  │  │ • Hooks     │  │ • Custom   │  │ • PDF      │  │ • Asset hashing         │  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │   │
│  └─────────┼────────────────┼────────────────┼─────────────────────┼──────────────────┘   │
│            │                │                │                     │                      │
│            └────────────────┴────────────────┴─────────────────────┘                      │
│                              │                                                          │
│                              v                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                            Output Layer                                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │   │
│  │  │    HTML     │  │     PDF     │  │   Static    │  │    IDE Integration      │  │   │
│  │  │   Site      │  │   Output    │  │    Files    │  │      (LSP)              │  │   │
│  │  │             │  │             │  │             │  │                         │  │   │
│  │  │ • Optimized │  │ • LaTeX     │  │ • Images    │  │ • Autocomplete          │  │   │
│  │  │ • Search    │  │ • WeasyPrint│  │ • Fonts     │  │ • Hover docs            │  │   │
│  │  │ • SPA nav   │  │ • Paged.js  │  │ • Downloads │  │ • Go-to-definition      │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Component Interactions

```
                    ┌─────────────────┐
                    │   Source Files  │
                    │  (Markdown/    │
                    │   Code/Config)  │
                    └────────┬────────┘
                             │
                             v
┌─────────────────────────────────────────────────────────────┐
│                     Parse & Load                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Markdown  │  │    Code     │  │   Configuration     │  │
│  │   Parser    │  │   Parser    │  │      Loader         │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼───────────────┘
          │                │                    │
          └────────────────┴────────────────────┘
                             │
                             v
          ┌──────────────────────────────────────┐
          │      Documentation Graph               │
          │  ┌────────────┐    ┌────────────┐    │
          │  │   Nodes    │◄──►│   Edges    │    │
          │  │            │    │            │    │
          │  │ • Pages    │    │ • Links    │    │
          │  │ • Sections │    │ • Includes │    │
          │  │ • APIs     │    │ • Refs     │    │
          │  └────────────┘    └────────────┘    │
          └────────────────────┬─────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              v              v              v
        ┌─────────┐   ┌─────────┐   ┌─────────┐
        │ Validate│   │  Index  │   │  Build  │
        │  Graph  │   │  Search │   │ Pipeline│
        └────┬────┘   └────┬────┘   └────┬────┘
             │             │             │
             v             v             v
        ┌─────────┐   ┌─────────┐   ┌─────────┐
        │  Error  │   │  Search │   │  Render │
        │ Reports │   │  Index  │   │ Output  │
        └─────────┘   └─────────┘   └─────────┘
```

---

## Architecture

### Layered Architecture

Quillr follows a layered architecture with clear separation of concerns:

#### Layer 1: Foundation (Core Engine)

Responsible for:
- Documentation graph representation
- Incremental build coordination
- Cache management
- Plugin orchestration

```rust
// Core engine structure
pub struct QuillrEngine {
    graph: DocumentationGraph,
    cache: ContentAddressableCache,
    plugin_host: PluginHost,
    build_coordinator: BuildCoordinator,
}

impl QuillrEngine {
    pub async fn build(&mut self, config: BuildConfig) -> Result<BuildOutput> {
        // 1. Load configuration
        // 2. Scan for changes
        // 3. Update dependency graph
        // 4. Execute incremental build
        // 5. Generate output
    }
}
```

#### Layer 2: Processing (Transformations)

Responsible for:
- Content parsing (Markdown, MDX, YAML)
- Type extraction from source code
- Plugin transformations
- Template processing

#### Layer 3: Presentation (Output)

Responsible for:
- HTML generation
- Asset optimization
- Search index generation
- PDF/print rendering

### Architectural Patterns

#### Pattern 1: Documentation Graph

All documentation is modeled as a directed graph:

```rust
pub struct DocumentationGraph {
    nodes: HashMap<NodeId, DocNode>,
    edges: Vec<DocEdge>,
    index: DocIndex,
}

pub enum DocNode {
    Page(PageNode),
    Section(SectionNode),
    ApiReference(ApiNode),
    CodeExample(CodeNode),
    Navigation(NavNode),
}

pub struct DocEdge {
    from: NodeId,
    to: NodeId,
    kind: EdgeKind,
}

pub enum EdgeKind {
    LinksTo,        // Page A links to Page B
    Includes,       // Page includes partial content
    References,     // API doc references type definition
    VersionOf,      // This page is version X of page Y
    DependsOn,    // Build dependency
}
```

#### Pattern 2: Content-Addressable Storage

All build artifacts are stored and retrieved by content hash:

```rust
pub struct ContentAddressableCache {
    storage: Box<dyn CacheStorage>,
}

impl ContentAddressableCache {
    pub fn get(&self, hash: ContentHash) -> Option<Arc<[u8]>> {
        // Retrieve by BLAKE3 hash
    }
    
    pub fn put(&self, content: &[u8]) -> ContentHash {
        // Store and return hash
    }
}
```

#### Pattern 3: Plugin Pipeline

Content flows through a configurable plugin pipeline:

```rust
pub struct PluginPipeline {
    plugins: Vec<Box<dyn Plugin>>,
}

impl PluginPipeline {
    pub fn process(&self, node: DocNode) -> Result<DocNode> {
        let mut result = node;
        for plugin in &self.plugins {
            result = plugin.transform(result)?;
        }
        Ok(result)
    }
}
```

---

## Core Components

### Component 1: Content Parser

**Purpose**: Parse various input formats into the documentation graph.

**Supported Formats**:
| Format | Parser | Status |
|--------|--------|--------|
| CommonMark | pulldown-cmark | ✅ |
| GitHub Flavored Markdown | pulldown-cmark | ✅ |
| MDX | custom | Design |
| YAML Frontmatter | serde_yaml | ✅ |
| TOML Config | toml | ✅ |
| TypeScript | swc/tsc API | Design |
| Rust | rustdoc JSON | Design |
| Python | ast module | Future |

**Architecture**:
```rust
pub trait Parser: Send + Sync {
    fn parse(&self, input: &str, ctx: &ParseContext) -> Result<ParsedContent>;
    fn supported_extensions(&self) -> Vec<&str>;
}

pub struct MarkdownParser {
    options: Options,
}

impl Parser for MarkdownParser {
    fn parse(&self, input: &str, ctx: &ParseContext) -> Result<ParsedContent> {
        let parser = pulldown_cmark::Parser::new_ext(input, self.options);
        // Convert events to DocNodes
    }
}
```

### Component 2: Documentation Graph

**Purpose**: Represent and manage documentation structure and relationships.

**Key Features**:
- Immutable graph for reproducible builds
- Incremental updates for performance
- Query API for navigation generation
- Validation for broken links/references

**API**:
```rust
impl DocumentationGraph {
    /// Add a node to the graph
    pub fn add_node(&mut self, node: DocNode) -> NodeId;
    
    /// Create edge between nodes
    pub fn add_edge(&mut self, from: NodeId, to: NodeId, kind: EdgeKind);
    
    /// Get all nodes that depend on a given node
    pub fn get_dependents(&self, node: NodeId) -> Vec<NodeId>;
    
    /// Validate graph integrity
    pub fn validate(&self) -> Vec<ValidationError>;
    
    /// Topological sort for build ordering
    pub fn topological_sort(&self) -> Vec<NodeId>;
    
    /// Query nodes by type/tag/path
    pub fn query(&self, filter: QueryFilter) -> Vec<&DocNode>;
}
```

### Component 3: Incremental Builder

**Purpose**: Perform efficient incremental builds with dependency tracking.

**Algorithm**:
```
1. Compute content hash for each source file
2. Compare with cached hashes
3. Identify changed nodes
4. Find transitive dependents
5. Topologically sort affected nodes
6. Parallel render affected nodes
7. Update cache with new hashes
```

**Implementation**:
```rust
pub struct IncrementalBuilder {
    graph: DocumentationGraph,
    cache: ContentAddressableCache,
    render_engine: RenderEngine,
}

impl IncrementalBuilder {
    pub async fn build(&mut self, changes: Vec<Change>) -> Result<BuildResult> {
        // 1. Detect affected nodes
        let affected = self.graph.detect_affected_nodes(&changes);
        
        // 2. Check cache for unchanged outputs
        let to_render: Vec<_> = affected
            .into_iter()
            .filter(|node| !self.cache.is_fresh(node))
            .collect();
        
        // 3. Parallel render
        let results = self.render_parallel(to_render).await;
        
        // 4. Update cache
        for (node, output) in &results {
            self.cache.put(node.content_hash(), output);
        }
        
        Ok(BuildResult::from(results))
    }
}
```

### Component 4: Plugin Host

**Purpose**: Manage and execute plugins safely.

**Plugin Types**:
1. **Native Plugins**: Rust shared libraries (performance-critical)
2. **WASI Plugins**: WebAssembly modules (safe, language-agnostic)
3. **Script Plugins**: JavaScript/Lua for quick scripts

**Architecture**:
```rust
pub struct PluginHost {
    native_plugins: Vec<NativePlugin>,
    wasi_host: WasiPluginHost,
    script_engine: ScriptEngine,
}

impl PluginHost {
    pub fn load_plugin(&mut self, manifest: PluginManifest) -> Result<PluginId>;
    
    pub fn execute_hook(&self, hook: Hook, ctx: &HookContext) -> Result<()> {
        for plugin in self.plugins_for_hook(hook) {
            plugin.execute(ctx)?;
        }
        Ok(())
    }
}
```

### Component 5: Template Engine

**Purpose**: Render documentation nodes to output formats.

**Engine**: MiniJinja (Jinja2-compatible)

**Features**:
- Template inheritance
- Macros and includes
- Custom filters and functions
- Hot reload in dev mode

```rust
pub struct TemplateEngine {
    env: Environment,
    loaders: Vec<Box<dyn TemplateLoader>>,
}

impl TemplateEngine {
    pub fn render(&self, template: &str, context: &Context) -> Result<String> {
        self.env.get_template(template)?.render(context)
    }
}
```

### Component 6: Development Server

**Purpose**: Provide instant feedback during development.

**Features**:
- File watching with notify
- Hot Module Replacement
- Source maps for debugging
- WebSocket-based refresh

```rust
pub struct DevServer {
    engine: QuillrEngine,
    watcher: FileWatcher,
    websocket: WebSocketServer,
}

impl DevServer {
    pub async fn run(&mut self, config: ServerConfig) -> Result<()> {
        // 1. Initial build
        self.engine.build(BuildConfig::default()).await?;
        
        // 2. Start HTTP server
        let app = self.create_router();
        
        // 3. Start file watcher
        let mut rx = self.watcher.watch(&config.content_dir)?;
        
        // 4. Handle changes
        while let Some(changes) = rx.recv().await {
            let result = self.engine.build_incremental(changes).await?;
            self.websocket.broadcast_reload(result).await?;
        }
        
        Ok(())
    }
}
```

---

## Data Model

### Core Types

```rust
/// Unique identifier for any document entity
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct NodeId(u64);

/// Cryptographic hash of content (BLAKE3)
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ContentHash([u8; 32]);

/// File system location
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SourceLocation {
    pub path: PathBuf,
    pub line: Option<usize>,
    pub column: Option<usize>,
}

/// Document metadata
#[derive(Debug, Clone, Default)]
pub struct Metadata {
    pub title: Option<String>,
    pub description: Option<String>,
    pub author: Option<String>,
    pub date: Option<DateTime<Utc>>,
    pub tags: Vec<String>,
    pub draft: bool,
    pub weight: i32,
    pub custom: HashMap<String, Value>,
}
```

### Document Nodes

```rust
/// The main node types in the documentation graph
pub enum DocNode {
    Page(PageNode),
    Section(SectionNode),
    ApiReference(ApiNode),
    CodeExample(CodeNode),
    Partial(PartialNode),
    Asset(AssetNode),
}

/// A documentation page
pub struct PageNode {
    pub id: NodeId,
    pub path: String,
    pub source: SourceLocation,
    pub metadata: Metadata,
    pub content: NodeContent,
    pub template: Option<String>,
    pub layout: Option<String>,
}

/// A section within a page
pub struct SectionNode {
    pub id: NodeId,
    pub parent: NodeId,
    pub level: u8,
    pub title: String,
    pub anchor: String,
    pub content: Vec<ContentBlock>,
}

/// API documentation extracted from code
pub struct ApiNode {
    pub id: NodeId,
    pub kind: ApiKind,
    pub name: String,
    pub signature: String,
    pub description: String,
    pub parameters: Vec<Parameter>,
    pub returns: Option<ReturnInfo>,
    pub examples: Vec<CodeExample>,
    pub source: SourceLocation,
}

pub enum ApiKind {
    Function,
    Struct,
    Enum,
    Trait,
    Type,
    Module,
    Constant,
    Macro,
}

/// A code example with metadata
pub struct CodeNode {
    pub id: NodeId,
    pub language: String,
    pub code: String,
    pub filename: Option<String>,
    pub runnable: bool,
    pub output: Option<String>,
}
```

### Content Model

```rust
/// Parsed content blocks
pub enum ContentBlock {
    Paragraph(Vec<InlineContent>),
    Heading {
        level: u8,
        content: Vec<InlineContent>,
        anchor: String,
    },
    CodeBlock {
        language: Option<String>,
        code: String,
        metadata: CodeMetadata,
    },
    List {
        ordered: bool,
        items: Vec<ListItem>,
    },
    Blockquote(Vec<ContentBlock>),
    Table {
        headers: Vec<Vec<InlineContent>>,
        rows: Vec<Vec<Vec<InlineContent>>>,
    },
    Image {
        src: String,
        alt: String,
        title: Option<String>,
    },
    Admonition {
        kind: AdmonitionKind,
        title: Option<String>,
        content: Vec<ContentBlock>,
    },
    MdxComponent {
        name: String,
        props: HashMap<String, Value>,
        children: Vec<ContentBlock>,
    },
}

pub enum InlineContent {
    Text(String),
    Emphasis(Vec<InlineContent>),
    Strong(Vec<InlineContent>),
    Code(String),
    Link {
        text: Vec<InlineContent>,
        url: String,
        title: Option<String>,
    },
    Image {
        src: String,
        alt: String,
    },
    Break,
}

pub enum AdmonitionKind {
    Note,
    Tip,
    Important,
    Warning,
    Caution,
}
```

### Graph Relationships

```rust
/// Edge types in the documentation graph
pub enum EdgeKind {
    /// Page A links to Page B
    LinksTo { text: String },
    
    /// Page includes partial content
    Includes { variable: Option<String> },
    
    /// Page references API documentation
    ReferencesApi { symbol: String },
    
    /// This is version X of another page
    VersionOf { version: String },
    
    /// Build dependency
    DependsOn,
    
    /// Navigation parent-child
    NavChild,
    
    /// Related content
    RelatedTo { reason: String },
}

/// An edge in the documentation graph
pub struct DocEdge {
    pub from: NodeId,
    pub to: NodeId,
    pub kind: EdgeKind,
}
```

---

## Build System

### Build Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Build Pipeline                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Phase 1: Discovery                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  Scan       │  │  Parse      │  │  Extract    │                 │
│  │  Filesystem │──│  Frontmatter│──│  Metadata   │                 │
│  │             │  │             │  │             │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                                                                      │
│  Phase 2: Graph Construction                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  Create     │  │  Resolve    │  │  Validate   │                 │
│  │  Nodes      │──│  Links      │──│  Graph      │                 │
│  │             │  │             │  │             │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                                                                      │
│  Phase 3: Processing                                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  Plugin     │  │  Template   │  │  Index      │                 │
│  │  Pipeline   │──│  Processing │──│  Search     │                 │
│  │             │  │             │  │             │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                                                                      │
│  Phase 4: Output                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │  Render     │  │  Optimize   │  │  Write      │                 │
│  │  HTML       │──│  Assets     │──│  Files      │                 │
│  │             │  │             │  │             │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Incremental Build Algorithm

```rust
pub async fn incremental_build(&mut self) -> Result<BuildReport> {
    let start = Instant::now();
    
    // 1. Detect file system changes
    let changes = self.watcher.detect_changes().await?;
    
    // 2. Compute content hashes
    let hashed_changes: Vec<_> = changes
        .into_iter()
        .map(|c| (c.path, blake3::hash(&c.content)))
        .collect();
    
    // 3. Find affected nodes in graph
    let mut affected = HashSet::new();
    for (path, hash) in &hashed_changes {
        if let Some(node_id) = self.graph.get_node_by_path(path) {
            let node = self.graph.get_node(node_id)?;
            if node.content_hash() != *hash {
                affected.insert(node_id);
                // Add all dependents
                affected.extend(self.graph.get_transitive_dependents(node_id));
            }
        }
    }
    
    // 4. Topological sort for correct build order
    let build_order = self.graph.topological_sort(&affected);
    
    // 5. Parallel processing with work-stealing
    let results = self.render_parallel(build_order).await?;
    
    // 6. Update cache
    for (node_id, output) in &results {
        let node = self.graph.get_node(*node_id)?;
        self.cache.put(node.content_hash(), output.serialize()?);
    }
    
    // 7. Generate report
    Ok(BuildReport {
        duration: start.elapsed(),
        nodes_rendered: results.len(),
        nodes_cached: affected.len() - results.len(),
        errors: results.iter().filter(|r| r.is_err()).count(),
    })
}
```

### Parallel Rendering

```rust
async fn render_parallel(&self, nodes: Vec<NodeId>) -> Vec<RenderResult> {
    // Create a stream of render tasks
    let tasks = nodes.into_iter().map(|node_id| {
        let engine = self.clone();
        async move {
            engine.render_node(node_id).await
        }
    });
    
    // Execute with controlled parallelism
    let stream = futures::stream::iter(tasks)
        .buffer_unordered(self.concurrency_limit);
    
    // Collect results
    stream.collect::<Vec<_>>().await
}
```

### Cache Strategy

**Content-Addressable Cache**:
```rust
pub struct ContentAddressableCache {
    /// Memory cache for hot items
    lru: LruCache<ContentHash, Arc<[u8]>>,
    
    /// Disk cache for persistence
    disk: PathBuf,
    
    /// Remote cache for CI/CD sharing
    remote: Option<RemoteCache>,
}

impl ContentAddressableCache {
    pub async fn get(&self, hash: ContentHash) -> Option<Arc<[u8]>> {
        // 1. Check memory cache
        if let Some(data) = self.lru.get(&hash) {
            return Some(data.clone());
        }
        
        // 2. Check disk cache
        let path = self.disk.join(format!("{:x}", hash));
        if let Ok(data) = fs::read(&path).await {
            let arc = Arc::from(data.into_boxed_slice());
            self.lru.put(hash, arc.clone());
            return Some(arc);
        }
        
        // 3. Check remote cache
        if let Some(remote) = &self.remote {
            if let Some(data) = remote.get(hash).await {
                fs::write(&path, &data).await.ok();
                let arc = Arc::from(data.into_boxed_slice());
                self.lru.put(hash, arc.clone());
                return Some(arc);
            }
        }
        
        None
    }
}
```

---

## Plugin System

### Plugin Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Plugin Architecture                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Plugin Types                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │   │
│  │  │   Native    │  │    WASI     │  │      Script       │   │   │
│  │  │   (Rust)    │  │    (Any)    │  │   (JS/Lua)        │   │   │
│  │  │             │  │             │  │                   │   │   │
│  │  │ • Fastest   │  │ • Sandboxed │  │ • Quick scripts   │   │   │
│  │  │ • Unsafe    │  │ • Portable  │  │ • Hot reload      │   │   │
│  │  │ • Native API│  │ • Any lang  │  │ • Limited API     │   │   │
│  │  └──────┬──────┘  └──────┬──────┘  └─────────┬─────────┘   │   │
│  └─────────┼────────────────┼──────────────────┼─────────────┘   │
│            │                │                  │                  │
│            └────────────────┴──────────────────┘                  │
│                           │                                       │
│                           v                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Plugin Host                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐   │   │
│  │  │  Native API │  │ wasmtime    │  │  QuickJS/Rhai     │   │   │
│  │  │  (dynamic)  │  │  WASI host  │  │   script engine   │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                           │                                       │
│                           v                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Core Engine                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Plugin Interface

```rust
/// The plugin trait - all plugins implement this
pub trait Plugin: Send + Sync {
    /// Plugin metadata
    fn metadata(&self) -> PluginMetadata;
    
    /// Initialize the plugin with configuration
    fn init(&mut self, config: &Config) -> Result<(), PluginError>;
    
    /// Transform a document node
    fn transform(&self, node: DocNode, ctx: &PluginContext) 
        -> Result<DocNode, PluginError>;
    
    /// Hook: Build starting
    fn on_build_start(&self, ctx: &BuildContext) -> Result<(), PluginError> {
        Ok(())
    }
    
    /// Hook: Build completed
    fn on_build_end(&self, ctx: &BuildContext) -> Result<(), PluginError> {
        Ok(())
    }
}

/// Metadata for a plugin
#[derive(Debug, Clone)]
pub struct PluginMetadata {
    pub name: String,
    pub version: Version,
    pub author: String,
    pub description: String,
    pub capabilities: Vec<Capability>,
}

/// Capabilities that a plugin can request
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Capability {
    FileRead(PathPattern),
    FileWrite(PathPattern),
    NetworkHttp,
    NetworkHttps,
    EnvRead(EnvPattern),
    ExecCommand,
}
```

### WASI Plugin Implementation

```rust
use wasmtime::{Engine, Module, Store, Instance, TypedFunc};
use wasmtime_wasi::WasiCtxBuilder;

pub struct WasiPlugin {
    engine: Engine,
    module: Module,
    store: Store<WasiCtx>,
    instance: Instance,
    transform_fn: TypedFunc<(i32, i32), (i32, i32)>,
}

impl WasiPlugin {
    pub fn new(wasm_bytes: &[u8], caps: Vec<Capability>) -> Result<Self> {
        let engine = Engine::default();
        let module = Module::new(&engine, wasm_bytes)?;
        
        // Build WASI context with restricted capabilities
        let mut wasi_builder = WasiCtxBuilder::new();
        for cap in caps {
            match cap {
                Capability::FileRead(pattern) => {
                    wasi_builder.preopened_dir(
                        pattern.base_path(), 
                        pattern.virtual_path(),
                        DirPerms::READ
                    );
                }
                Capability::NetworkHttps => {
                    wasi_builder.inherit_network();
                }
                _ => {}
            }
        }
        
        let wasi = wasi_builder.build();
        let mut store = Store::new(&engine, wasi);
        let instance = Instance::new(&mut store, &module, &[])?;
        
        let transform_fn = instance
            .get_typed_func::<(i32, i32), (i32, i32)>(&mut store, "transform")?;
        
        Ok(Self { engine, module, store, instance, transform_fn })
    }
    
    pub fn transform(&mut self, input: DocNode) -> Result<DocNode> {
        // Serialize input to JSON
        let input_json = serde_json::to_vec(&input)?;
        
        // Allocate memory in WASM
        let ptr = self.alloc(input_json.len() as i32)?;
        
        // Write input to WASM memory
        self.write_memory(ptr, &input_json)?;
        
        // Call transform function
        let (out_ptr, out_len) = self.transform_fn.call(&mut self.store, (ptr, input_json.len() as i32))?;
        
        // Read output from WASM memory
        let output_json = self.read_memory(out_ptr, out_len)?;
        
        // Deserialize result
        let output: DocNode = serde_json::from_slice(&output_json)?;
        
        // Free WASM memory
        self.free(ptr)?;
        self.free(out_ptr)?;
        
        Ok(output)
    }
}
```

### Example Plugins

#### 1. Analytics Plugin (WASI)

```rust
// analytics.rs (compiled to WASM)
use quillr_plugin_sdk::*;

#[derive(Default)]
struct AnalyticsPlugin {
    tracking_id: String,
}

impl Plugin for AnalyticsPlugin {
    fn metadata(&self) -> PluginMetadata {
        PluginMetadata {
            name: "analytics".to_string(),
            version: "1.0.0".parse().unwrap(),
            author: "Quillr".to_string(),
            description: "Add Google Analytics tracking".to_string(),
            capabilities: vec![
                Capability::EnvRead("GA_TRACKING_ID".into())
            ],
        }
    }
    
    fn transform(&self, mut node: DocNode, _ctx: &PluginContext) -> Result<DocNode> {
        if let DocNode::Page(ref mut page) = node {
            let script = format!(
                r#"<script async src="https://www.googletagmanager.com/gtag/js?id={}"></script>
                <script>
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){{dataLayer.push(arguments);}}
                  gtag('js', new Date());
                  gtag('config', '{}');
                </script>"#,
                self.tracking_id, self.tracking_id
            );
            page.head.push_str(&script);
        }
        Ok(node)
    }
}

plugin_export!(AnalyticsPlugin);
```

#### 2. Image Optimization Plugin (Native)

```rust
use image::{ImageFormat, ImageReader};

pub struct ImageOptimizationPlugin {
    quality: u8,
    max_width: Option<u32>,
}

impl Plugin for ImageOptimizationPlugin {
    fn transform(&self, node: DocNode, ctx: &PluginContext) -> Result<DocNode> {
        if let DocNode::Asset(AssetNode::Image(ref mut img)) = node {
            let path = ctx.resolve_path(&img.src)?;
            let img_data = fs::read(&path)?;
            
            // Decode image
            let reader = ImageReader::new(Cursor::new(&img_data))
                .with_guessed_format()?
                .decode()?;
            
            // Resize if needed
            let processed = if let Some(max_w) = self.max_width {
                if reader.width() > max_w {
                    reader.resize(max_w, max_w * reader.height() / reader.width(), FilterType::Lanczos3)
                } else {
                    reader
                }
            } else {
                reader
            };
            
            // Re-encode with quality setting
            let mut output = Vec::new();
            processed.write_to(&mut Cursor::new(&mut output), ImageFormat::WebP)?;
            
            // Update asset
            img.optimized_data = Some(output);
            img.src = img.src.with_extension("webp");
        }
        
        Ok(node)
    }
}
```

---

## Development Server

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Development Server                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    File Watcher                               │   │
│  │  notify crate with debouncing and recursive watching          │   │
│  └──────────────────────┬────────────────────────────────────────┘   │
│                        │                                             │
│                        v                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 Incremental Builder                           │   │
│  │  Content-addressable cache for instant rebuilds               │   │
│  └──────────────────────┬────────────────────────────────────────┘   │
│                        │                                             │
│                        v                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    HTTP Server (Axum)                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │   │
│  │  │   Static    │  │   Route     │  │    API            │     │   │
│  │  │   Files     │  │   Handler   │  │   Endpoints       │     │   │
│  │  │             │  │             │  │                   │     │   │
│  │  │ • Assets    │  │ • Pages     │  │ • Search          │     │   │
│  │  │ • Generated │  │ • 404       │  │ • Validation      │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘     │   │
│  └──────────────────────┬────────────────────────────────────────┘   │
│                        │                                             │
│                        v                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 WebSocket Server                              │   │
│  │  Live reload with granular updates                           │   │
│  │  • Full page refresh on structural changes                   │   │
│  │  • HMR for style changes                                     │   │
│  │  • Hot content updates for text changes                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Hot Module Replacement

```rust
pub struct HmrEngine {
    engine: QuillrEngine,
    websocket: WebSocketManager,
    connected_clients: Vec<ClientId>,
}

impl HmrEngine {
    pub async fn handle_change(&mut self, change: FileChange) -> Result<()> {
        // Determine change type
        let change_type = self.classify_change(&change);
        
        match change_type {
            ChangeType::Content => {
                // Rebuild just this file
                let result = self.engine.build_incremental(vec![change]).await?;
                
                // Send granular update
                self.websocket.broadcast(Message::ContentUpdate {
                    path: change.path,
                    html: result.html,
                }).await?;
            }
            
            ChangeType::Style => {
                // Extract CSS changes
                let css = self.engine.extract_css_changes(&change).await?;
                
                self.websocket.broadcast(Message::StyleUpdate {
                    css,
                }).await?;
            }
            
            ChangeType::Structure => {
                // Full rebuild needed
                let result = self.engine.build().await?;
                
                self.websocket.broadcast(Message::FullReload).await?;
            }
        }
        
        Ok(())
    }
}
```

### WebSocket Protocol

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum ServerMessage {
    #[serde(rename = "connected")]
    Connected { version: String },
    
    #[serde(rename = "content_update")]
    ContentUpdate { 
        path: String, 
        html: String,
        scroll_position: Option<(f64, f64)>,
    },
    
    #[serde(rename = "style_update")]
    StyleUpdate { 
        css: String,
        selector: Option<String>,
    },
    
    #[serde(rename = "full_reload")]
    FullReload,
    
    #[serde(rename = "build_error")]
    BuildError { 
        message: String,
        location: Option<ErrorLocation>,
    },
}
```

---

## Output Formats

### HTML Output

```rust
pub struct HtmlRenderer {
    templates: TemplateEngine,
    head_injections: Vec<String>,
    body_injections: Vec<String>,
}

impl HtmlRenderer {
    pub fn render_page(&self, page: &PageNode, ctx: &RenderContext) -> Result<String> {
        let mut html = String::new();
        
        // HTML5 boilerplate
        html.push_str("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n");
        
        // Meta tags
        html.push_str(&format!("<meta charset=\"UTF-8\">\n"));
        html.push_str(&format!("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"));
        html.push_str(&format!("<title>{}</title>\n", page.metadata.title.as_deref().unwrap_or("Untitled")));
        
        // Injected head content (analytics, etc.)
        for injection in &self.head_injections {
            html.push_str(injection);
        }
        
        // Styles
        html.push_str(&format!("<link rel=\"stylesheet\" href=\"{}\">\n", ctx.asset_url("styles.css")));
        
        html.push_str("</head>\n<body>\n");
        
        // Navigation
        html.push_str(&self.render_nav(ctx)?);
        
        // Main content
        html.push_str("<main>\n");
        html.push_str(&self.render_content(&page.content, ctx)?);
        html.push_str("</main>\n");
        
        // Sidebar/TOC
        html.push_str(&self.render_toc(page, ctx)?);
        
        // Footer
        html.push_str(&self.render_footer(ctx)?);
        
        // Scripts
        html.push_str(&format!("<script src=\"{}\"></script>\n", ctx.asset_url("app.js")));
        
        // Injected body content
        for injection in &self.body_injections {
            html.push_str(injection);
        }
        
        html.push_str("</body>\n</html>");
        
        Ok(html)
    }
}
```

### Search Index Generation

```rust
pub struct SearchIndexBuilder {
    documents: Vec<SearchDocument>,
}

impl SearchIndexBuilder {
    pub fn add_page(&mut self, page: &PageNode) {
        let doc = SearchDocument {
            id: page.id.to_string(),
            title: page.metadata.title.clone().unwrap_or_default(),
            content: self.extract_searchable_text(&page.content),
            path: page.path.clone(),
            headings: self.extract_headings(&page.content),
            tags: page.metadata.tags.clone(),
        };
        self.documents.push(doc);
    }
    
    pub fn build_index(&self) -> SearchIndex {
        // Build inverted index
        let mut index: HashMap<String, Vec<(String, f32)>> = HashMap::new();
        
        for doc in &self.documents {
            let tokens = self.tokenize(&doc.content);
            for (token, freq) in tokens {
                let tf = 1.0 + freq.log10();
                let idf = (self.documents.len() as f32 / index.get(&token).map(|v| v.len()).unwrap_or(1) as f32).log10();
                let score = tf * idf;
                
                index.entry(token).or_default().push((doc.id.clone(), score));
            }
        }
        
        SearchIndex { documents: self.documents.clone(), index }
    }
}
```

### PDF Output (Future)

```rust
pub struct PdfRenderer {
    options: PdfOptions,
}

impl PdfRenderer {
    pub async fn render(&self, pages: Vec<&PageNode>) -> Result<PdfDocument> {
        // Option 1: LaTeX intermediate
        let latex = self.to_latex(pages)?;
        let pdf = self.compile_latex(&latex).await?;
        
        // Option 2: Direct PDF generation (print CSS + headless)
        let html = self.to_print_html(pages)?;
        let pdf = self.render_with_chrome(&html).await?;
        
        // Option 3: WeasyPrint/Paged.js
        let pdf = self.render_with_weasyprint(&html).await?;
        
        Ok(pdf)
    }
}
```

---

## Performance Specification

### Build Performance Targets

| Scenario | Target | Measurement |
|----------|--------|-------------|
| Cold build (1,000 pages) | < 3s | From scratch, no cache |
| Cold build (10,000 pages) | < 10s | From scratch, no cache |
| Incremental build (1 page) | < 200ms | Single file change |
| Incremental build (10 pages) | < 500ms | Multiple related changes |
| Dev server startup | < 1s | First render |
| Hot reload | < 100ms | Change to browser update |

### Resource Usage Targets

| Resource | Target | Limit |
|----------|--------|-------|
| Memory (cold build) | < 200MB | Peak RSS |
| Memory (dev server) | < 100MB | Steady state |
| Disk cache | < 1GB | LRU eviction |
| Binary size | < 15MB | Release build |

### Benchmarking

```rust
#[cfg(test)]
mod benchmarks {
    use criterion::{black_box, criterion_group, criterion_main, Criterion};
    
    fn benchmark_full_build(c: &mut Criterion) {
        c.bench_function("build_1000_pages", |b| {
            let engine = create_test_engine(1000);
            b.iter(|| {
                black_box(engine.build().unwrap());
            });
        });
    }
    
    fn benchmark_incremental_build(c: &mut Criterion) {
        c.bench_function("incremental_1_page", |b| {
            let mut engine = create_test_engine(1000);
            engine.build().unwrap(); // Initial build
            
            b.iter(|| {
                let changes = vec![create_single_change()];
                black_box(engine.build_incremental(changes).unwrap());
            });
        });
    }
    
    criterion_group!(benches, benchmark_full_build, benchmark_incremental_build);
    criterion_main!(benches);
}
```

---

## Security Model

### Threat Model

| Threat | Severity | Mitigation |
|--------|----------|------------|
| Malicious plugin execution | Critical | WASI sandbox, capability-based access |
| XSS via user content | High | Content sanitization, CSP headers |
| Path traversal | High | Input validation, canonical paths |
| SSRF via plugin | Medium | Network capability restrictions |
| Information disclosure | Medium | Secret scanning, access controls |
| Supply chain attacks | Medium | Dependency auditing, signed releases |

### Content Security Policy

```rust
pub fn default_security_headers() -> HeaderMap {
    let mut headers = HeaderMap::new();
    
    // Strict CSP for documentation sites
    headers.insert(
        "Content-Security-Policy",
        "default-src 'self'; \\
         script-src 'self' 'unsafe-inline' 'unsafe-eval'; \\
         style-src 'self' 'unsafe-inline'; \\
         img-src 'self' data: https:; \\
         font-src 'self'; \\
         connect-src 'self'; \\
         frame-ancestors 'none'; \\
         base-uri 'self'; \\
         form-action 'self';".parse().unwrap()
    );
    
    headers.insert("X-Frame-Options", "DENY".parse().unwrap());
    headers.insert("X-Content-Type-Options", "nosniff".parse().unwrap());
    headers.insert("Referrer-Policy", "strict-origin-when-cross-origin".parse().unwrap());
    
    headers
}
```

### Secret Detection

```rust
pub struct SecretScanner {
    patterns: Vec<Regex>,
}

impl SecretScanner {
    pub fn new() -> Self {
        let patterns = vec![
            // AWS Access Key ID
            Regex::new(r"AKIA[0-9A-Z]{16}").unwrap(),
            // GitHub Personal Access Token
            Regex::new(r"ghp_[a-zA-Z0-9]{36}").unwrap(),
            // Generic API key patterns
            Regex::new(r"(?i)(api[_-]?key|apikey)\s*[=:]\s*[\"']?[a-zA-Z0-9]{16,}[\"']?").unwrap(),
            // Private keys
            Regex::new(r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----").unwrap(),
        ];
        
        Self { patterns }
    }
    
    pub fn scan(&self, content: &str) -> Vec<SecretFinding> {
        let mut findings = Vec::new();
        
        for (i, pattern) in self.patterns.iter().enumerate() {
            for mat in pattern.find_iter(content) {
                findings.push(SecretFinding {
                    pattern_id: i,
                    position: mat.start()..mat.end(),
                    snippet: mat.as_str().to_string(),
                });
            }
        }
        
        findings
    }
}
```

---

## API Reference

### Rust API (Core Library)

```rust
//! Quillr Core Library
//!
//! The primary API for programmatic documentation generation.

use std::path::Path;

/// Main entry point for Quillr
pub struct Quillr;

impl Quillr {
    /// Create a new builder with default configuration
    pub fn builder() -> QuillrBuilder {
        QuillrBuilder::default()
    }
}

/// Builder for Quillr configuration
pub struct QuillrBuilder {
    config: Config,
}

impl QuillrBuilder {
    /// Set the content directory
    pub fn content_dir(mut self, path: impl AsRef<Path>) -> Self {
        self.config.content_dir = path.as_ref().to_path_buf();
        self
    }
    
    /// Set the output directory
    pub fn output_dir(mut self, path: impl AsRef<Path>) -> Self {
        self.config.output_dir = path.as_ref().to_path_buf();
        self
    }
    
    /// Add a plugin
    pub fn with_plugin(mut self, plugin: impl Plugin) -> Self {
        self.config.plugins.push(Box::new(plugin));
        self
    }
    
    /// Set cache directory
    pub fn cache_dir(mut self, path: impl AsRef<Path>) -> Self {
        self.config.cache_dir = path.as_ref().to_path_buf();
        self
    }
    
    /// Build the engine
    pub async fn build(self) -> Result<QuillrEngine, BuildError> {
        QuillrEngine::new(self.config).await
    }
}

/// The main engine for building documentation
pub struct QuillrEngine {
    config: Config,
    graph: DocumentationGraph,
    cache: ContentAddressableCache,
    plugins: PluginHost,
}

impl QuillrEngine {
    /// Perform a full build
    pub async fn build(&mut self) -> Result<BuildOutput, BuildError> {
        // Implementation
    }
    
    /// Perform an incremental build
    pub async fn build_incremental(
        &mut self, 
        changes: Vec<FileChange>
    ) -> Result<BuildOutput, BuildError> {
        // Implementation
    }
    
    /// Start the development server
    pub async fn serve(self, config: ServerConfig) -> Result<(), ServerError> {
        // Implementation
    }
}
```

### JavaScript/TypeScript API (Node.js bindings)

```typescript
// quillr.d.ts

export interface QuillrConfig {
  contentDir: string;
  outputDir: string;
  cacheDir?: string;
  plugins?: Plugin[];
}

export interface BuildOptions {
  incremental?: boolean;
  watch?: boolean;
  strict?: boolean;
}

export interface BuildResult {
  success: boolean;
  pages: number;
  errors: BuildError[];
  warnings: BuildWarning[];
  duration: number;
}

export class Quillr {
  constructor(config: QuillrConfig);
  
  build(options?: BuildOptions): Promise<BuildResult>;
  serve(port?: number): Promise<Server>;
  watch(callback: (event: WatchEvent) => void): Promise<Watcher>;
}

export interface Server {
  url: string;
  close(): Promise<void>;
}

export interface Watcher {
  close(): Promise<void>;
}
```

### CLI API

See [CLI Interface](#cli-interface) section.

---

## CLI Interface

### Command Structure

```
quillr [OPTIONS] <COMMAND>

Commands:
  build     Build documentation
  serve     Start development server
  init      Initialize new project
  plugin    Manage plugins
  validate  Validate documentation
  search    Search content
  help      Print help

Options:
  -c, --config <FILE>    Configuration file [default: quillr.toml]
  -v, --verbose          Verbose output
  -q, --quiet            Suppress output
  -V, --version          Print version
  -h, --help             Print help
```

### Build Command

```
quillr build [OPTIONS]

Build documentation for production

Options:
  -i, --incremental    Perform incremental build
  -o, --output <DIR>   Output directory
      --base-url <URL> Base URL for links
      --strict         Fail on warnings
      --no-cache       Disable cache
  -j, --jobs <N>      Parallel jobs [default: CPU count]
  
Examples:
  quillr build                    # Full build with defaults
  quillr build -i                 # Incremental build
  quillr build -o ./dist          # Custom output directory
  quillr build --strict           # Fail on any warning
```

### Serve Command

```
quillr serve [OPTIONS]

Start development server with hot reload

Options:
  -p, --port <PORT>    Port to listen on [default: 3000]
  -h, --host <HOST>    Host to bind to [default: localhost]
      --no-open        Don't open browser
      --no-hmr         Disable hot module replacement
      --https          Use HTTPS with self-signed cert
  
Examples:
  quillr serve                    # Start on localhost:3000
  quillr serve -p 8080            # Start on port 8080
  quillr serve -h 0.0.0.0         # Bind to all interfaces
```

### Init Command

```
quillr init [OPTIONS] [NAME]

Initialize a new Quillr project

Arguments:
  [NAME]  Project name (defaults to current directory name)

Options:
  -t, --template <NAME>  Project template [default: default]
      --git             Initialize git repository
      --install         Install dependencies
  
Templates:
  default     Basic documentation site
  blog        Blog with posts and tags
  api         API documentation with OpenAPI
  book        Multi-chapter book structure
  pheno       Phenotype ecosystem integration
  
Examples:
  quillr init my-docs             # Create my-docs/ with default template
  quillr init -t api api-docs     # Create API documentation project
```

### Plugin Command

```
quillr plugin <SUBCOMMAND>

Manage Quillr plugins

Subcommands:
  list        List installed plugins
  install     Install a plugin
  uninstall   Remove a plugin
  update      Update plugins
  create      Scaffold a new plugin
  
Examples:
  quillr plugin list                    # Show installed plugins
  quillr plugin install analytics       # Install from registry
  quillr plugin install ./my-plugin   # Install from path
  quillr plugin create my-plugin        # Create plugin template
```

### Validate Command

```
quillr validate [OPTIONS] [PATH]

Validate documentation without building

Arguments:
  [PATH]  Path to validate [default: .]

Options:
      --fix            Auto-fix issues where possible
      --format <FMT>   Output format [default: pretty] [possible: json, junit]
  
Checks:
  • Internal link validity
  • Required frontmatter fields
  • Image/asset existence
  • Code block syntax
  • Accessibility (headings, alt text)
  
Examples:
  quillr validate               # Validate current directory
  quillr validate ./docs        # Validate specific path
  quillr validate --fix         # Auto-fix issues
  quillr validate --format json > report.json
```

---

## Configuration

### Configuration File (quillr.toml)

```toml
# quillr.toml - Quillr Configuration

# Project metadata
[project]
name = "My Documentation"
description = "Comprehensive documentation for My Project"
version = "1.0.0"
author = "Documentation Team"
license = "MIT"

# Content settings
[content]
# Source directory (relative to config)
dir = "./content"

# File extensions to process
extensions = ["md", "mdx"]

# Files/directories to ignore
exclude = ["drafts/**", "private/**"]

# Default frontmatter for new pages
default_frontmatter = { draft = false, toc = true }

# Build settings
[build]
# Output directory
output_dir = "./dist"

# Base URL for links (required for sitemap/rss)
base_url = "https://docs.example.com"

# Cache directory
cache_dir = "./.quillr/cache"

# Clean URLs (/page instead of /page.html)
clean_urls = true

# Generate sitemap.xml
sitemap = true

# Generate RSS/Atom feeds
feed = { format = "rss", path = "feed.xml" }

# Build environments
[build.environments]
production = { 
    minify = true, 
    analytics = true,
    base_url = "https://docs.example.com"
}
development = { 
    minify = false, 
    analytics = false,
    base_url = "http://localhost:3000"
}

# Server settings
[server]
port = 3000
host = "localhost"
open_browser = true
hot_reload = true

# Watch settings
watch = { 
    debounce_ms = 100,
    poll_interval_ms = 500,
    ignore = ["*.tmp", ".git/**"]
}

# Search configuration
[search]
enabled = true
placeholder = "Search documentation..."
min_query_length = 2
max_results = 20
ranking = ["title", "headings", "content", "tags"]

# Theme settings
[theme]
name = "default"
color_scheme = "auto"  # auto, light, dark
primary_color = "#3b82f6"
logo = "./assets/logo.svg"
favicon = "./assets/favicon.ico"

[theme.fonts]
heading = "Inter"
body = "Inter"
code = "JetBrains Mono"

# Navigation structure
[[nav]]
label = "Getting Started"
items = [
    { label = "Introduction", path = "/intro" },
    { label = "Installation", path = "/install" },
    { label = "Quick Start", path = "/quickstart" },
]

[[nav]]
label = "API Reference"
path = "/api"
collapsed = false

# Sidebar configuration
[sidebar]
auto_generate = true
depth = 3
collapsible = true

# Plugin configuration
[plugins.analytics]
enabled = true
source = "https://plugins.quillr.dev/analytics@v1.2.0"
tracking_id = "${GA_TRACKING_ID}"
anonymize_ip = true

[plugins.analytics.capabilities]
network = ["https://*.google-analytics.com"]
env = ["GA_TRACKING_ID"]

[plugins.search-enhanced]
enabled = true
source = "./local-plugins/search-enhanced"
synonyms = [
    ["config", "configuration"],
    ["api", "interface"],
]

# Markdown processing
[markdown]
# Enable GFM (tables, strikethrough, tasklists)
gfm = true

# Syntax highlighting
syntax_highlighting = { theme = "github-dark", line_numbers = true }

# Heading anchors
heading_anchors = true

# External link handling
external_links = { 
    target = "_blank", 
    rel = "noopener noreferrer",
    icon = true 
}

# Smart typography
smart_punctuation = true

# Custom components (MDX)
[[markdown.components]]
name = "Alert"
path = "./components/Alert.tsx"
props = ["type", "title"]

[[markdown.components]]
name = "CodeSandbox"
path = "./components/CodeSandbox.tsx"

# Asset processing
[assets]
# Image optimization
optimize_images = { quality = 85, format = "webp" }

# Responsive images
responsive_images = { widths = [480, 800, 1200] }

# Fingerprint assets for cache busting
fingerprint = true

# Internationalization
[i18n]
default_locale = "en"
locales = [
    { code = "en", name = "English", flag = "🇺🇸" },
    { code = "es", name = "Español", flag = "🇪🇸" },
    { code = "fr", name = "Français", flag = "🇫🇷" },
]

# API documentation generation
[api]
enabled = true
source_dirs = ["./src"]
output_path = "/api"

[api.typescript]
enabled = true
tsconfig_path = "./tsconfig.json"
entry_points = ["./src/index.ts"]

[api.rust]
enabled = false  # Use rustdoc directly

# Versioning
[versions]
current = "2.0"
default = "2.0"
versions = [
    { version = "2.0", path = "/2.0", label = "v2.0 (latest)" },
    { version = "1.0", path = "/1.0", label = "v1.0", deprecated = true },
]

# Phenotype ecosystem integration
[phenotype]
agileplus_enabled = true
agileplus_spec_path = "../AgilePlus/kitty-specs"

hexakit_enabled = true
hexakit_template_path = "../HexaKit/templates"

phenospecs_enabled = true
phenospecs_adr_path = "../PhenoSpecs/ADRs"

# Advanced settings
[advanced]
# Parallel jobs
parallel_jobs = 8

# Memory limit (MB)
memory_limit = 512

# Timeout for external operations (seconds)
timeout = 30

# Debug mode
debug = false

# Experimental features
experimental = { 
    wasm_plugins = true,
    incremental_search_index = true 
}
```

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `QUILLR_ENV` | Build environment | `production`, `development` |
| `QUILLR_CONFIG` | Config file path | `./config/quillr.toml` |
| `QUILLR_CACHE_DIR` | Cache directory | `/tmp/quillr-cache` |
| `QUILLR_LOG` | Log level | `debug`, `info`, `warn`, `error` |
| `QUILLR_BASE_URL` | Base URL override | `https://docs.example.com` |

---

## Testing Strategy

### Test Pyramid

```
                    ┌─────────────┐
                    │   E2E       │  10% - Full integration
                    │  (Playwright)│
                    ├─────────────┤
                    │  Integration │  20% - Component interaction
                    │   Tests      │
                    ├─────────────┤
                    │    Unit      │  70% - Individual components
                    │   Tests      │
                    └─────────────┘
```

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_markdown_parsing() {
        let input = "# Hello\n\nWorld";
        let parser = MarkdownParser::new(Options::default());
        let result = parser.parse(input, &ParseContext::default()).unwrap();
        
        assert_eq!(result.nodes.len(), 2);
        assert!(matches!(result.nodes[0], DocNode::Heading { .. }));
    }
    
    #[test]
    fn test_graph_validation() {
        let mut graph = DocumentationGraph::new();
        
        let page_a = graph.add_node(create_page("/a"));
        let page_b = graph.add_node(create_page("/b"));
        
        // Create broken link
        graph.add_edge(page_a, page_b, EdgeKind::LinksTo);
        
        // Remove page_b
        graph.remove_node(page_b);
        
        // Validation should detect broken link
        let errors = graph.validate();
        assert_eq!(errors.len(), 1);
        assert!(matches!(errors[0], ValidationError::BrokenLink { .. }));
    }
    
    #[test]
    fn test_incremental_build() {
        let mut builder = IncrementalBuilder::new();
        
        // Initial build
        let result1 = builder.build().unwrap();
        assert_eq!(result1.rendered.len(), 10);
        
        // Incremental build (no changes)
        let result2 = builder.build_incremental(vec![]).unwrap();
        assert_eq!(result2.rendered.len(), 0);  // All cached
        
        // Change one file
        let changes = vec![FileChange::modified("page1.md")];
        let result3 = builder.build_incremental(changes).unwrap();
        assert_eq!(result3.rendered.len(), 1);
    }
}
```

### Integration Tests

```rust
#[tokio::test]
async fn test_full_build_pipeline() {
    let temp_dir = tempfile::tempdir().unwrap();
    
    // Create test content
    fs::write(
        temp_dir.path().join("quillr.toml"),
        r#"
[project]
name = "Test"

[content]
dir = "./content"

[build]
output_dir = "./dist"
"#
    ).unwrap();
    
    fs::create_dir(temp_dir.path().join("content")).unwrap();
    fs::write(
        temp_dir.path().join("content/index.md"),
        "# Test\n\nHello World"
    ).unwrap();
    
    // Run build
    let engine = Quillr::builder()
        .config_file(temp_dir.path().join("quillr.toml"))
        .build()
        .await
        .unwrap();
    
    let output = engine.build().await.unwrap();
    
    // Verify output
    assert!(temp_dir.path().join("dist/index.html").exists());
    let html = fs::read_to_string(temp_dir.path().join("dist/index.html")).unwrap();
    assert!(html.contains("Test"));
    assert!(html.contains("Hello World"));
}
```

### E2E Tests

```typescript
// tests/e2e/build.spec.ts
import { test, expect } from '@playwright/test';

test('full site build', async ({ page }) => {
  // Build site
  await execa('quillr', ['build'], { cwd: './test-site' });
  
  // Start static server
  const server = await startStaticServer('./test-site/dist');
  
  // Navigate to home
  await page.goto(server.url);
  
  // Verify content
  await expect(page.locator('h1')).toContainText('Test Documentation');
  await expect(page.locator('nav')).toBeVisible();
  
  // Test navigation
  await page.click('text=Getting Started');
  await expect(page.url()).toContain('/getting-started');
  
  // Test search
  await page.fill('[data-testid="search"]', 'installation');
  await expect(page.locator('.search-results')).toContainText('Installation');
  
  await server.close();
});

test('hot reload', async ({ page }) => {
  const quillr = spawn('quillr', ['serve'], { cwd: './test-site' });
  
  // Wait for server
  await waitForServer('http://localhost:3000');
  await page.goto('http://localhost:3000');
  
  const initialContent = await page.locator('h1').textContent();
  
  // Modify file
  const filePath = './test-site/content/index.md';
  const originalContent = fs.readFileSync(filePath, 'utf-8');
  fs.writeFileSync(filePath, '# Updated Title\n\nUpdated content');
  
  // Wait for hot reload
  await page.waitForEvent('websocket');
  await expect(page.locator('h1')).toContainText('Updated Title');
  
  // Restore original
  fs.writeFileSync(filePath, originalContent);
  
  quillr.kill();
});
```

### Performance Tests

```rust
#[cfg(test)]
mod benchmarks {
    use criterion::{criterion_group, criterion_main, Criterion, BenchmarkId};
    
    fn bench_build_scaling(c: &mut Criterion) {
        let mut group = c.benchmark_group("build_scaling");
        
        for page_count in [100, 1_000, 10_000] {
            group.bench_with_input(
                BenchmarkId::from_parameter(page_count),
                &page_count,
                |b, &n| {
                    let engine = create_engine_with_pages(n);
                    b.iter(|| {
                        engine.build().unwrap();
                    });
                },
            );
        }
        
        group.finish();
    }
    
    criterion_group!(benches, bench_build_scaling);
    criterion_main!(benches);
}
```

---

## Deployment

### Static Hosting

Quillr generates static files suitable for any static host:

| Platform | Setup | Performance |
|----------|-------|-------------|
| Vercel | `vercel.json` config | Edge-cached |
| Netlify | `netlify.toml` config | Edge-cached |
| GitHub Pages | GitHub Actions | CDN-backed |
| Cloudflare Pages | Git integration | Edge-cached |
| AWS S3 + CloudFront | S3 sync | Highly scalable |
| Self-hosted | Any web server | Configurable |

### Vercel Configuration

```json
// vercel.json
{
  "buildCommand": "quillr build",
  "outputDirectory": "dist",
  "framework": null,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, must-revalidate"
        }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/search",
      "destination": "https://search.example.com/api"
    }
  ]
}
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM rust:1.75 as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates
COPY --from=builder /app/target/release/quillr /usr/local/bin/quillr

WORKDIR /site
COPY quillr.toml .
COPY content ./content

EXPOSE 3000
CMD ["quillr", "serve", "-h", "0.0.0.0"]
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quillr-docs
spec:
  replicas: 3
  selector:
    matchLabels:
      app: quillr-docs
  template:
    metadata:
      labels:
        app: quillr-docs
    spec:
      containers:
        - name: quillr
          image: registry.example.com/quillr-docs:latest
          ports:
            - containerPort: 3000
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: quillr-docs
spec:
  selector:
    app: quillr-docs
  ports:
    - port: 80
      targetPort: 3000
```

---

## Integration Points

### Phenotype Ecosystem

#### AgilePlus Integration

```rust
pub struct AgilePlusIntegration {
    spec_path: PathBuf,
}

impl Plugin for AgilePlusIntegration {
    fn on_build_start(&self, ctx: &BuildContext) -> Result<(), PluginError> {
        // Load AgilePlus specs
        let specs = self.load_specs()?;
        
        // Generate feature documentation
        for spec in specs {
            let doc_page = self.spec_to_page(&spec)?;
            ctx.graph.add_node(DocNode::Page(doc_page));
        }
        
        // Create traceability links
        self.create_traceability_links(ctx)?;
        
        Ok(())
    }
    
    fn load_specs(&self) -> Result<Vec<AgileSpec>> {
        let pattern = self.spec_path.join("**/spec.md");
        glob(&pattern)?
            .map(|path| self.parse_spec(&path))
            .collect()
    }
}
```

#### HexaKit Integration

```rust
pub struct HexaKitIntegration {
    template_path: PathBuf,
}

impl HexaKitIntegration {
    pub fn register_templates(&self, engine: &mut TemplateEngine) -> Result<()> {
        for entry in fs::read_dir(&self.template_path)? {
            let path = entry?.path();
            if path.extension() == Some("html".as_ref()) {
                let name = path.file_stem().unwrap().to_string_lossy();
                let content = fs::read_to_string(&path)?;
                engine.register_template(&name, content)?;
            }
        }
        Ok(())
    }
}
```

#### PhenoSpecs Integration

```rust
pub struct PhenoSpecsIntegration;

impl Plugin for PhenoSpecsIntegration {
    fn transform(&self, node: DocNode, ctx: &PluginContext) -> Result<DocNode> {
        // Link ADR references to PhenoSpecs
        if let DocNode::Page(ref mut page) = node {
            for block in &mut page.content {
                if let ContentBlock::Paragraph(inlines) = block {
                    for inline in inlines {
                        if let InlineContent::Link { ref mut url, .. } = inline {
                            if url.starts_with("ADR-") {
                                *url = format!(
                                    "https://github.com/KooshaPari/PhenoSpecs/tree/main/ADRs/{}",
                                    url
                                );
                            }
                        }
                    }
                }
            }
        }
        Ok(node)
    }
}
```

### CI/CD Integration

#### GitHub Actions

```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Quillr
        run: cargo install quillr
        
      - name: Restore cache
        uses: actions/cache@v3
        with:
          path: .quillr/cache
          key: quillr-${{ hashFiles('**/Cargo.lock') }}
          restore-keys: quillr-
          
      - name: Validate
        run: quillr validate --strict
        
      - name: Build
        run: quillr build
        
      - name: Deploy
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### IDE Integration

#### Language Server Protocol (LSP)

```rust
pub struct QuillrLsp {
    engine: QuillrEngine,
    client: Client,
}

#[tower_lsp::async_trait]
impl LanguageServer for QuillrLsp {
    async fn initialize(&self, _: InitializeParams) -> Result<InitializeResult> {
        Ok(InitializeResult {
            capabilities: ServerCapabilities {
                text_document_sync: Some(TextDocumentSyncCapability::Kind(
                    TextDocumentSyncKind::INCREMENTAL,
                )),
                completion_provider: Some(CompletionOptions::default()),
                hover_provider: Some(HoverProviderCapability::Simple(true)),
                definition_provider: Some(OneOf::Left(true)),
                ..Default::default()
            },
            ..Default::default()
        })
    }
    
    async fn completion(&self, params: CompletionParams) -> Result<Option<CompletionResponse>> {
        let position = params.text_document_position.position;
        let document = self.engine.get_document(&params.text_document_position.text_document.uri)?;
        
        // Provide completions for:
        // - Internal page links [[...]]
        // - Frontmatter keys
        // - Component names
        // - Shortcodes
        
        let completions = self.generate_completions(&document, position)?;
        Ok(Some(CompletionResponse::Array(completions)))
    }
    
    async fn hover(&self, params: HoverParams) -> Result<Option<Hover>> {
        let position = params.text_document_position_params.position;
        let document = self.engine.get_document(&params.text_document_position_params.text_document.uri)?;
        
        // Show hover information for:
        // - Internal links (page preview)
        // - Code symbols
        // - Abbreviations
        
        let hover_info = self.get_hover_info(&document, position)?;
        Ok(Some(Hover {
            contents: HoverContents::Markup(MarkupContent {
                kind: MarkupKind::Markdown,
                value: hover_info,
            }),
            range: None,
        }))
    }
}
```

---

## Migration Guide

### From Docusaurus

```bash
# 1. Create new Quillr project
quillr init my-docs --template docusaurus-compat

# 2. Copy content
cp -r old-docs/docs/* my-docs/content/
cp -r old-docs/blog/* my-docs/content/blog/
cp -r old-docs/static/* my-docs/public/

# 3. Migrate config
cat old-docs/docusaurus.config.js | quillr migrate-config > my-docs/quillr.toml

# 4. Update imports
cd my-docs
quillr migrate-mdx ./content/**/*.mdx

# 5. Build and verify
quillr build
quillr serve
```

### From VitePress

```bash
# 1. Create new project
quillr init my-docs --template vitepress-compat

# 2. Copy content
cp -r old-docs/* my-docs/content/

# 3. Migrate config
cat old-docs/.vitepress/config.ts | quillr migrate-config > my-docs/quillr.toml

# 4. Build and verify
quillr build
```

### From Hugo

```bash
# 1. Create new project
quillr init my-docs

# 2. Copy content (structure differs)
# Hugo: content/posts/my-post.md
# Quillr: content/posts/my-post/index.md
cp -r old-docs/content/* my-docs/content/

# 3. Migrate frontmatter
quillr migrate-frontmatter my-docs/content/**/*.md --from hugo

# 4. Migrate templates
quillr migrate-templates old-docs/layouts/ my-docs/templates/
```

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Documentation Graph** | Directed graph representing documentation structure and relationships |
| **Content-Addressable Storage** | Storage system indexed by content hash rather than location |
| **Incremental Build** | Build process that only recompiles changed content |
| **Hot Module Replacement** | Live update of changed modules without full page reload |
| **CRDT** | Conflict-free Replicated Data Type for collaborative editing |
| **WASI** | WebAssembly System Interface for sandboxed execution |
| **Island Architecture** | Partial hydration pattern for performance |
| **HMR** | Hot Module Replacement |

### Appendix B: File Structure

```
my-docs/
├── quillr.toml              # Configuration
├── content/                 # Documentation content
│   ├── index.md            # Home page
│   ├── getting-started/
│   │   ├── index.md
│   │   ├── installation.md
│   │   └── quickstart.md
│   ├── api/
│   │   ├── index.md
│   │   └── reference.md
│   └── blog/
│       ├── index.md
│       └── 2024-01-01-hello.md
├── templates/              # Custom templates (optional)
├── public/               # Static assets
│   ├── logo.svg
│   └── favicon.ico
├── plugins/              # Local plugins
│   └── my-plugin/
├── components/           # MDX components
│   ├── Alert.tsx
│   └── CodeSandbox.tsx
├── styles/               # Custom CSS
│   └── custom.css
└── .quillr/              # Generated (gitignored)
    ├── cache/
    └── temp/
```

### Appendix C: Environment Compatibility

| Environment | Version | Status |
|-------------|---------|--------|
| Linux (glibc) | 2.31+ | ✅ Supported |
| Linux (musl) | Latest | ✅ Supported |
| macOS (Intel) | 11+ | ✅ Supported |
| macOS (Apple Silicon) | 11+ | ✅ Supported |
| Windows | 10+ | ✅ Supported |
| FreeBSD | 13+ | ⚠️ Experimental |
| WebAssembly | WASI | ⚠️ Experimental |

### Appendix D: Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- PR process

---

## Document Information

**Specification Version**: 2.0  
**Last Updated**: 2026-04-04  
**Status**: Draft  
**Maintainer**: Quillr Core Team  
**Review Schedule**: Monthly  

### Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-04-04 | Complete rewrite with nanovms-level detail |
| 1.0 | 2026-04-02 | Initial specification |

---

*This specification is a living document and will be updated as the project evolves.*
