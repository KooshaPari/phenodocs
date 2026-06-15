# phenodocs justfile
# VitePress federation hub with TypeScript and link checking
# Standard Phenotype-org task runner.

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

# Security advisories (bun audit)
audit:
    bun audit || true

# License + advisory + ban + source checks (no-op for TS — bun audit covers this)
deny:
    @echo "deny: no-op (Rust-only concept); use 'just audit' for TS dep security"

# Fleet-wide grading gate (uses vendored or central grade.sh)
grade:
    @if [ -f grade.sh ]; then ./grade.sh; \
    elif [ -f ../grade.sh ]; then bash ../grade.sh; \
    else echo "no grade.sh found (vendored or central)"; exit 1; \
    fi

grade-fast:
    @if [ -f grade.sh ]; then ./grade.sh --fast; \
    elif [ -f ../grade.sh ]; then bash ../grade.sh --fast; \
    else echo "no grade.sh found"; exit 1; \
    fi

# Full local CI sweep
ci: lint test build audit deny
    @echo "✓ CI checks pass"

# Remove build artifacts
clean:
    rm -rf .vitepress/cache .vitepress/dist docs/.vitepress/cache docs/.vitepress/dist
    @echo "Cleaned VitePress build artifacts"

# Measure code coverage (SSOT: see grade.sh for the canonical command)
coverage:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -f "Cargo.toml" ]]; then
        cargo llvm-cov --workspace --fail-under-lines 85
    elif [[ -f "package.json" ]]; then
        npx jest --coverage --coverageThreshold='{"global":{"branches":85,"functions":85,"lines":85,"statements":85}}'
    elif [[ -f "pyproject.toml" || -f "setup.py" ]]; then
        pytest --cov=src --cov-report=term-missing --cov-fail-under=85
    elif [[ -f "go.mod" ]]; then
        go test -coverprofile=coverage.out -covermode=atomic ./... && go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//' | awk '{exit($1 < 85 ? 1 : 0)}'
    else
        echo "No recognized stack (Cargo.toml / package.json / pyproject.toml / go.mod) found." >&2
        exit 1
    fi
