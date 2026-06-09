# phenodocs justfile
# VitePress federation hub with TypeScript and link checking

set shell := ["bash", "-uc"]

# List available recipes
default:
    @just --list

# Start VitePress dev server with hot reload
dev:
    bun run dev

# Build the VitePress static site
build:
    bun run build

# Preview the built site locally
preview:
    bun run preview

# Run the test suite
test:
    @echo "No test runner defined for phenodocs"

# Run all linters (markdownlint + oxlint + link check)
lint:
    bun run lint
    bun run lint:ts
    bun run check-links

# Apply formatter
fmt:
    bunx prettier --write "**/*.md" "**/*.ts" "**/*.vue" "**/*.json"
    bunx markdownlint-cli --fix "docs/**/*.md" 2>/dev/null || true

# Remove build artifacts
clean:
    rm -rf .vitepress/cache .vitepress/dist docs/.vitepress/cache docs/.vitepress/dist
    @echo "Cleaned VitePress build artifacts"
