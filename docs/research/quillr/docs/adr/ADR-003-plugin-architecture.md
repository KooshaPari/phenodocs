# ADR-003: Plugin Architecture with WebAssembly Extensions

**Status**: Accepted  
**Date**: 2026-04-04  
**Author**: Quillr Architecture Team  
**Deciders**: Core Team, Extensibility Working Group  

---

## Context

Quillr must support diverse documentation needs across the Phenotype ecosystem and beyond. A plugin architecture is essential for:

1. **Custom transformations**: Organization-specific formatting requirements
2. **New output formats**: PDF, ePub, man pages, custom formats
3. **Integration**: CI/CD systems, external tools, proprietary workflows
4. **Community contributions**: Third-party extensions without core changes
5. **Gradual migration**: Incremental adoption from existing tools

### Requirements

| Requirement | Priority | Description |
|-------------|----------|-------------|
| **Sandboxed execution** | P1 | Plugins must not compromise build system |
| **Language agnostic** | P1 | Support plugins in multiple languages |
| **Performance** | P1 | Plugin overhead < 10% of total build |
| **Hot reload** | P2 | Dev server plugin updates without restart |
| **Discovery** | P2 | Registry/directory for community plugins |
| **Versioning** | P2 | Plugin API versioning for stability |

### Options Considered

| Approach | Sandboxing | Language Support | Performance | Complexity |
|----------|------------|------------------|-------------|------------|
| **WebAssembly (WASI)** | ⭐⭐⭐⭐⭐ | Any (compiled) | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Native Dynamic Libraries** | ❌ | Rust/C only | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **JavaScript/Node.js** | ❌ | JS only | ⭐⭐ | ⭐⭐ |
| **Lua/JIT** | Partial | Lua only | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **gRPC/Process IPC** | ⭐⭐⭐⭐ | Any | ⭐⭐ | ⭐⭐⭐⭐ |

---

## Decision

**Implement a hybrid plugin architecture:**

1. **Core plugins**: Native Rust for performance-critical paths
2. **Standard plugins**: WebAssembly (WASI) for safe, language-agnostic extensions
3. **Script plugins**: Quick JavaScript/Lua scripts for simple transformations

**Primary interface: WebAssembly with WASI snapshot1**

---

## Rationale

### Why WebAssembly?

**Security**: WASI provides capability-based sandboxing. Plugins cannot:
- Access filesystem outside designated paths
- Make network requests without permission
- Access environment variables
- Execute arbitrary system commands

**Performance**: Near-native speed (within 10-20% of native)

**Language Support**: Any language compiling to WASM:
- Rust (wasm32-wasi target)
- Go (TinyGo)
- AssemblyScript
- C/C++ (Emscripten)
- Grain, AssemblyScript, etc.

**Ecosystem**: Mature tooling (wasmtime, wasmer, wasm3)

### Why Hybrid?

Not all plugins need sandboxing or language flexibility:

| Plugin Type | Implementation | Use Case |
|-------------|----------------|----------|
| Core renderer | Native Rust | Markdown → HTML |
| Search indexer | Native Rust | Full-text indexing |
| Custom theme | WASI | Organization branding |
| Analytics integration | WASI | Google Analytics, Plausible |
| Syntax highlighter | Native Rust | Code block processing |
| Content filter | JavaScript | Simple text replacement |

---

## Consequences

### Positive

- **Security**: Sandboxed execution prevents malicious plugins
- **Flexibility**: Plugins in any WASM-compilable language
- **Performance**: Near-native execution speed
- **Isolation**: Plugin crashes don't affect core system
- **Distribution**: WASM binaries are portable and versioned

### Negative

- **Complexity**: Multiple plugin runtime systems to maintain
- **Debugging**: WASM debugging more complex than native
- **Bundle size**: WASM binaries larger than source
- **Startup**: Initial compilation overhead for JIT

### Neutral

- **Learning**: Developers need to understand WASM toolchain
- **Tooling**: wasmtime provides good debugging support

---

## Architecture

### Plugin System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Plugin Architecture                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                     Plugin Registry                           │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │  │
│  │  │   Native    │  │    WASI     │  │       Script        │  │  │
│  │  │   Plugins   │  │   Plugins   │  │      Plugins        │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              v                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    Plugin Host Interface                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │  │
│  │  │  Native API │  │  WASI Host  │  │  Script Engine      │  │  │
│  │  │  (direct)   │  │  (wasmtime) │  │  (QuickJS/Rhai)     │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              v                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                       Core Engine                            │  │
│  │              (Document Graph + Build Pipeline)               │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Plugin Interface Definition

```rust
/// The plugin capability interface
pub trait Plugin: Send + Sync {
    /// Plugin metadata
    fn metadata(&self) -> PluginMetadata;
    
    /// Initialize with configuration
    fn init(&mut self, config: &Config) -> Result<(), PluginError>;
    
    /// Transform a document node
    fn transform(&self, node: DocNode, ctx: &PluginContext) -> Result<DocNode, PluginError>;
    
    /// Hook for build start
    fn on_build_start(&self, ctx: &BuildContext) -> Result<(), PluginError> {
        Ok(())
    }
    
    /// Hook for build end
    fn on_build_end(&self, ctx: &BuildContext) -> Result<(), PluginError> {
        Ok(())
    }
}

#[derive(Debug, Clone)]
pub struct PluginMetadata {
    pub name: String,
    pub version: String,
    pub author: String,
    pub description: String,
    pub capabilities: Vec<Capability>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Capability {
    FileRead,
    FileWrite,
    NetworkHttp,
    NetworkHttps,
    EnvRead,
}
```

### WASI Plugin Host

```rust
use wasmtime::{Engine, Module, Store, Instance};
use wasmtime_wasi::{WasiCtx, WasiCtxBuilder};

pub struct WasiPluginHost {
    engine: Engine,
    module: Module,
    wasi: WasiCtx,
}

impl WasiPluginHost {
    pub fn new(wasm_bytes: &[u8], capabilities: Vec<Capability>) -> Result<Self> {
        let engine = Engine::default();
        let module = Module::new(&engine, wasm_bytes)?;
        
        // Build WASI context with restricted capabilities
        let mut wasi_builder = WasiCtxBuilder::new();
        
        for cap in capabilities {
            match cap {
                Capability::FileRead => {
                    wasi_builder.preopened_dir("/content", "/content", DirPerms::READ);
                }
                Capability::FileWrite => {
                    wasi_builder.preopened_dir("/output", "/output", DirPerms::READ | DirPerms::WRITE);
                }
                Capability::NetworkHttp | Capability::NetworkHttps => {
                    // Enable HTTP capability (wasmtime-wasi-http)
                }
                Capability::EnvRead => {
                    wasi_builder.envs(&[("QUILLR_VERSION", env!("CARGO_PKG_VERSION"))]);
                }
            }
        }
        
        let wasi = wasi_builder.build();
        
        Ok(Self { engine, module, wasi })
    }
    
    pub fn transform(&mut self, input: DocNode) -> Result<DocNode> {
        // Serialize input to WASM memory
        let input_bytes = serde_json::to_vec(&input)?;
        
        // Call WASM exported function
        let mut store = Store::new(&self.engine, self.wasi.clone());
        let instance = Instance::new(&mut store, &self.module, &[])?;
        
        let transform = instance
            .get_typed_func::<(i32, i32), (i32, i32)>(&mut store, "transform")?;
        
        // Allocate memory in WASM, write input, call function
        // ... (memory management details)
        
        // Deserialize result
        let result: DocNode = serde_json::from_slice(&output_bytes)?;
        Ok(result)
    }
}
```

### Script Plugin Engine

```rust
use rhai::{Engine, Scope, AST};

pub struct ScriptPluginHost {
    engine: Engine,
    ast: AST,
}

impl ScriptPluginHost {
    pub fn new(script: &str) -> Result<Self> {
        let engine = Engine::new();
        
        // Register Quillr-specific functions
        engine.register_fn("slugify", |s: &str| slug::slugify(s));
        engine.register_fn("format_date", |ts: i64| {
            let dt = DateTime::from_timestamp(ts, 0)?;
            dt.format("%Y-%m-%d").to_string()
        });
        
        let ast = engine.compile(script)?;
        
        Ok(Self { engine, ast })
    }
    
    pub fn transform(&self, node: DocNode) -> Result<DocNode> {
        let mut scope = Scope::new();
        scope.push("node", node);
        
        let result: DocNode = self.engine.eval_ast_with_scope(&mut scope, &self.ast)?;
        Ok(result)
    }
}
```

### Plugin Manifest Format

```toml
# quillr-plugin.toml
[plugin]
name = "analytics-integration"
version = "1.2.0"
author = "Quillr Team"
description = "Add analytics tracking to generated pages"
type = "wasi"  # "native", "wasi", or "script"

[capabilities]
file_read = ["/templates"]
file_write = ["/output"]
network = ["https://www.google-analytics.com"]
env = ["GA_TRACKING_ID"]

[config]
enabled = { type = "boolean", default = true }
tracking_id = { type = "string", required = true }
anonymize_ip = { type = "boolean", default = true }

[hooks]
on_build_start = true
on_page_render = true
on_build_end = false
```

---

## Plugin Development

### Rust Plugin Example

```rust
// lib.rs
use quillr_plugin_sdk::*;

#[derive(Default)]
pub struct AnalyticsPlugin {
    config: AnalyticsConfig,
}

impl Plugin for AnalyticsPlugin {
    fn metadata(&self) -> PluginMetadata {
        PluginMetadata {
            name: "analytics".to_string(),
            version: "1.0.0".to_string(),
            author: "Quillr".to_string(),
            description: "Add Google Analytics".to_string(),
            capabilities: vec![Capability::NetworkHttps, Capability::EnvRead],
        }
    }
    
    fn init(&mut self, config: &Config) -> Result<(), PluginError> {
        self.config = config.deserialize()?;
        Ok(())
    }
    
    fn transform(&self, mut node: DocNode, _ctx: &PluginContext) -> Result<DocNode, PluginError> {
        if let DocNode::Page(ref mut page) = node {
            let script = format!(
                r#"<script async src="https://www.googletagmanager.com/gtag/js?id={}"></script>
                <script>
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){{dataLayer.push(arguments);}}
                  gtag('js', new Date());
                  gtag('config', '{}', {{ 'anonymize_ip': true }});
                </script>"#,
                self.config.tracking_id,
                self.config.tracking_id
            );
            page.head.push_str(&script);
        }
        Ok(node)
    }
}

// Register the plugin
plugin_export!(AnalyticsPlugin);
```

### JavaScript Plugin Example (via QuickJS)

```javascript
// analytics.js
export function transform(node, ctx) {
    if (node.type === 'page') {
        const trackingId = config.get('tracking_id');
        const script = `
            <script async src="https://www.googletagmanager.com/gtag/js?id=${trackingId}"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', '${trackingId}');
            </script>
        `;
        node.head += script;
    }
    return node;
}

export function metadata() {
    return {
        name: 'analytics-js',
        version: '1.0.0',
        capabilities: ['network_https', 'env_read']
    };
}
```

---

## Implementation Phases

### Phase 1: Native Plugin System (Weeks 1-4)

- [x] Plugin trait definition
- [x] Plugin registry
- [x] Configuration loading
- [x] Hook system (transform, build_start, build_end)

### Phase 2: WASI Integration (Weeks 5-8)

- [ ] wasmtime integration
- [ ] Capability-based sandboxing
- [ ] WASM plugin SDK
- [ ] Memory management

### Phase 3: Script Engine (Weeks 9-10)

- [ ] QuickJS integration
- [ ] Plugin SDK bindings
- [ ] Hot reload for dev server

### Phase 4: Ecosystem (Weeks 11-12)

- [ ] Plugin registry/directory
- [ ] CLI plugin management (install, list, update)
- [ ] Documentation and examples

---

## Security Model

### Capability System

Plugins declare required capabilities; users grant them explicitly:

```toml
# quillr.toml
[plugins.analytics]
enabled = true
source = "https://plugins.quillr.dev/analytics@v1.2.0"

[plugins.analytics.capabilities]
# Explicit grant (defaults to false)
network = ["https://*.google-analytics.com"]
env = ["GA_TRACKING_ID"]
```

### Threat Mitigation

| Threat | Mitigation |
|--------|------------|
| Malicious code execution | WASI sandbox prevents system access |
| Resource exhaustion | CPU time limits, memory quotas |
| Data exfiltration | No network without explicit grant |
| Privilege escalation | Capability-based access control |
| Supply chain attacks | Plugin signing and verification |

---

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Plugins loaded only when needed for current content
2. **Caching**: WASM modules precompiled and cached
3. **Pooling**: Reuse plugin instances across multiple nodes
4. **Batching**: Group multiple transformations into single WASM call

### Benchmarks

| Operation | Native | WASI | Script | Target |
|-----------|--------|------|--------|--------|
| Simple transform | 0.1ms | 0.5ms | 2ms | < 1ms |
| Complex transform | 1ms | 3ms | 10ms | < 5ms |
| Cold start | 0ms | 50ms | 5ms | < 100ms |

---

## Related Decisions

- ADR-001: Rust as Implementation Language
- ADR-002: Incremental Build System with Content-Addressable Storage
- ADR-004: Real-time Collaboration (future)

---

## References

1. [WebAssembly System Interface](https://github.com/WebAssembly/WASI)
2. [wasmtime Documentation](https://docs.wasmtime.dev/)
3. [Capability-Based Security](https://en.wikipedia.org/wiki/Capability-based_security)
4. [Rhai Scripting Engine](https://rhai.rs/)
5. [QuickJS Documentation](https://bellard.org/quickjs/)

---

**Last Updated**: 2026-04-04  
**Review Date**: 2026-10-04
