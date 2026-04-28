# phenodocs generated temp cleanup

## Problem
phenodocs currently tracks VitePress generated .vitepress/.temp artifacts, which creates dirty worktrees after docs generation and pollutes source diffs.

## Scope
- Add .vitepress/.temp/ to .gitignore.
- Remove tracked .vitepress/.temp generated files from the git index only.
- Verify docs build/check commands after cleanup.

## Acceptance Criteria
- .vitepress/.temp files are no longer tracked.
- Generated temp artifacts remain ignored after build.
- bun run build and bun run check pass or blockers are documented.
