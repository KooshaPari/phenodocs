# ADR-002: Incremental Build System with Content-Addressable Storage

**Status**: Accepted  
**Date**: 2026-04-04  
**Author**: Quillr Architecture Team  
**Deciders**: Core Team, Performance Working Group  

---

## Context

Documentation sites often contain thousands of pages. Full rebuilds on every change are unacceptable for developer experience. Quillr must support:

1. **Sub-second incremental builds**: Single page changes should rebuild in < 500ms
2. **Dependency tracking**: Changes to templates, partials, or styles should cascade correctly
3. **Deterministic builds**: Same inputs must produce identical outputs
4. **Distributed caching**: Build artifacts should be shareable across CI runners
5. **Local development**: File watching with instant browser refresh

### State of the Art Analysis

| Tool | Incremental Strategy | Cache Strategy | Dependency Tracking | Performance |
|------|---------------------|----------------|---------------------|-------------|
| **Hugo** | Partial rebuilds | File mtime | Limited | Excellent |
| **Gatsby** | webpack HMR | Filesystem | Graph-based | Poor |
| **VitePress** | Vite HMR | Module graph | ES imports | Good |
| **Astro** | Partial hydration | Content hashes | File-based | Good |
| **Eleventy** | Template caching | Filesystem | Manual | Fair |

### Problems with Existing Approaches

1. **Hugo**: Uses file modification times, which can miss dependency changes in includes/partials
2. **Gatsby**: Webpack-based incremental builds are slow and memory-intensive
3. **VitePress**: Good for dev, but production builds still regenerate entire site
4. **Astro**: Content-based but limited granularity for documentation relationships

---

## Decision

**Implement a content-addressable incremental build system with fine-grained dependency tracking.**

Key components:
1. **Content-addressable storage**: All artifacts indexed by content hash (BLAKE3)
2. **Dependency graph**: Complete graph of content relationships
3. **Granular invalidation**: Per-node change detection
4. **Parallel pipeline**: Multi-threaded rendering with work-stealing
5. **Persistent cache**: Disk-based cache shareable across CI runs

---

## Rationale

### Why Content-Addressable?

Traditional build systems use file paths and modification times:
```python
# Traditional approach
if file.mtime > cache.mtime:
    rebuild(file)
```

Content-addressable storage uses content hashes:
```rust
// Content-addressable approach
let hash = blake3::hash(content);
if let Some(cached) = cache.get(hash) {
    return cached;
}
let result = build(content);
cache.put(hash, result);
```

**Benefits:**
1. **Deterministic**: Same content always produces same hash
2. **Shareable**: Cache entries can be shared across machines
3. **Collision-free**: Content changes always detected
4. **Immutable**: Cache entries never change (simplifies concurrency)

### Why Fine-Grained Dependencies?

Documentation has complex relationships:
- Pages include partials/templates
- API docs reference source code
- Cross-links between pages
- Shared navigation structures

A change to a template should only rebuild pages using that template, not the entire site.

---

## Consequences

### Positive

- **Performance**: 100x faster incremental builds vs full rebuilds
- **Correctness**: Never miss a dependency change
- **Scalability**: Handles 100,000+ page sites
- **CI/CD**: Shared caches reduce build times from minutes to seconds
- **Reliability**: Content hashing prevents stale cache issues

### Negative

- **Complexity**: More complex than file-mtime approaches
- **Storage**: Cache can grow large (mitigated by LRU eviction)
- **Initial build**: Slightly slower due to graph construction
- **Memory**: Dependency graph kept in memory during builds

### Neutral

- **Debugging**: Cache inspection tools needed for troubleshooting
- **Migration**: Existing projects get full initial build

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Incremental Build System                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
│  │   File Watcher  │───>│ Change Detector │───>│   Build Queue   │ │
│  │   (notify)      │    │   (hash-based)  │    │   (priority)    │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘ │
│                                                          │          │
│  ┌─────────────────┐    ┌─────────────────┐              │          │
│  │ Content-Addr    │<───│  Render Engine  │<─────────────┘          │
│  │ Cache (BLAKE3)  │    │  (parallel)     │                       │
│  └─────────────────┘    └─────────────────┘                       │
│           │                                                          │
│           v                                                          │
│  ┌─────────────────┐    ┌─────────────────┐                         │
│  │  Dependency     │───>│   Output Writer │                         │
│  │  Graph Update   │    │   (atomic)      │                         │
│  └─────────────────┘    └─────────────────┘                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Structures

```rust
/// Unique identifier for any document node
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct NodeId(u64);

/// Content hash for cache addressing
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ContentHash([u8; 32]);

/// A node in the documentation graph
pub struct DocNode {
    id: NodeId,
    content_hash: ContentHash,
    node_type: NodeType,
    dependencies: Vec<NodeId>,
    dependents: Vec<NodeId>,
    last_rendered: Option<ContentHash>,
}

/// The complete documentation graph
pub struct DocGraph {
    nodes: HashMap<NodeId, DocNode>,
    index: DocIndex,
    cache: ContentAddressableCache,
}

/// Content-addressable cache storage
pub struct ContentAddressableCache {
    storage: Box<dyn CacheStorage>,
    hasher: blake3::Hasher,
    max_size: usize,
    current_size: usize,
}
```

### Build Pipeline

```rust
impl DocGraph {
    /// Process changes and return affected nodes
    pub async fn process_changes(&mut self, changes: Vec<FileChange>) -> Result<Vec<NodeId>> {
        let mut affected = Vec::new();
        
        for change in changes {
            // Compute content hash
            let new_hash = self.compute_hash(&change.content);
            
            // Find or create node
            let node_id = self.get_or_create_node(&change.path);
            let node = self.nodes.get_mut(&node_id).unwrap();
            
            // Check if content actually changed
            if node.content_hash != new_hash {
                node.content_hash = new_hash;
                affected.push(node_id);
                
                // Add transitive dependents
                affected.extend(self.get_dependents(node_id));
            }
        }
        
        Ok(affected)
    }
    
    /// Render only changed nodes
    pub async fn incremental_build(&mut self, affected: Vec<NodeId>) -> Result<BuildResult> {
        let mut results = Vec::new();
        
        // Sort by dependency order (topological)
        let ordered = self.topological_sort(&affected);
        
        // Parallel rendering with work-stealing
        let render_tasks: Vec<_> = ordered
            .into_iter()
            .map(|node_id| async move {
                self.render_node(node_id).await
            })
            .collect();
        
        let rendered = futures::future::join_all(render_tasks).await;
        
        for (node_id, result) in rendered {
            // Update cache
            let output_hash = blake3::hash(&result.output);
            self.cache.put(output_hash, result.output.clone());
            
            // Update node state
            if let Some(node) = self.nodes.get_mut(&node_id) {
                node.last_rendered = Some(output_hash);
            }
            
            results.push((node_id, result));
        }
        
        Ok(BuildResult::from(results))
    }
}
```

### Cache Storage Strategy

```rust
/// Cache storage backend trait
#[async_trait]
pub trait CacheStorage: Send + Sync {
    async fn get(&self, hash: ContentHash) -> Option<Vec<u8>>;
    async fn put(&self, hash: ContentHash, content: Vec<u8>) -> Result<()>;
    async fn exists(&self, hash: ContentHash) -> bool;
    async fn remove(&self, hash: ContentHash) -> Result<()>;
}

/// Local filesystem cache
pub struct FileSystemCache {
    root: PathBuf,
    max_size: usize,
}

impl CacheStorage for FileSystemCache {
    async fn get(&self, hash: ContentHash) -> Option<Vec<u8>> {
        let path = self.root.join(format!("{:x}", hash));
        fs::read(path).await.ok()
    }
    
    async fn put(&self, hash: ContentHash, content: Vec<u8>) -> Result<()> {
        let path = self.root.join(format!("{:x}", hash));
        fs::write(path, content).await?;
        Ok(())
    }
}

/// Remote cache (S3/R2 compatible)
pub struct RemoteCache {
    client: s3::Client,
    bucket: String,
}
```

---

## Implementation Phases

### Phase 1: Core Infrastructure (Weeks 1-4)

- [x] Content hash computation (BLAKE3)
- [x] In-memory dependency graph
- [x] Local filesystem cache
- [x] Basic incremental rendering

### Phase 2: Advanced Features (Weeks 5-8)

- [ ] Parallel rendering with tokio
- [ ] File watching integration (notify)
- [ ] Hot Module Replacement for dev server
- [ ] Cache compression (zstd)

### Phase 3: Production Hardening (Weeks 9-12)

- [ ] Remote cache backends (S3, R2)
- [ ] Cache eviction policies (LRU/TTL)
- [ ] Build metrics and profiling
- [ ] Distributed build coordination

---

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Incremental build (1 page) | < 200ms | Time from change to output |
| Full build (10,000 pages) | < 5s | Clean build on CI |
| Cache hit retrieval | < 10ms | Time to read from cache |
| Dependency graph update | < 50ms | Time to update relationships |
| Memory overhead | < 100MB | Graph + cache metadata |

---

## Testing Strategy

### Unit Tests

```rust
#[tokio::test]
async fn test_incremental_build() {
    let mut graph = DocGraph::new();
    
    // Add initial content
    let page1 = graph.add_node("page1.md", "# Hello").await;
    let page2 = graph.add_node("page2.md", "# World").await;
    
    // Full build
    let result1 = graph.build_all().await.unwrap();
    assert_eq!(result1.rendered.len(), 2);
    
    // Incremental change to page1 only
    graph.update_node(page1, "# Hello Updated").await;
    let result2 = graph.incremental_build(vec![page1]).await.unwrap();
    assert_eq!(result2.rendered.len(), 1);
    assert_eq!(result2.rendered[0].id, page1);
}
```

### Integration Tests

- Large site simulation (10,000 pages)
- Concurrent change handling
- Cache persistence across restarts
- Memory usage profiling

---

## Migration Path

### From Existing Tools

| From | Migration Strategy | Timeline |
|------|-------------------|----------|
| Hugo | Import content, rebuild templates | 1-2 weeks |
| Docusaurus | MDX compatibility layer | 2-3 weeks |
| VitePress | Vue SFC compilation | 2-3 weeks |
| MkDocs | Python macro translation | 3-4 weeks |

---

## Related Decisions

- ADR-001: Rust as Implementation Language
- ADR-003: Plugin Architecture
- ADR-004: Real-time Collaboration (future)

---

## References

1. [BLAKE3 Spec](https://github.com/BLAKE3-team/BLAKE3-specs/)
2. [Content-Defined Chunking](https://moinakg.wordpress.com/2013/06/22/high-performance-content-defined-chunking/)
3. [Ninja Build System](https://ninja-build.org/manual.html)
4. [Bazel Incremental Builds](https://bazel.build/basics/artifact-based-builds)

---

**Last Updated**: 2026-04-04  
**Review Date**: 2026-07-04
