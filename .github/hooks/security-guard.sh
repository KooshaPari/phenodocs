#!/usr/bin/env bash
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$HOOK_DIR/../.." && pwd)"

<<<<<<< HEAD
=======
if command -v uv >/dev/null 2>&1; then
  cd "$PROJECT_ROOT"
  uv sync --group dev
  uv run pre-commit run --hook-stage pre-commit --config "$PROJECT_ROOT/.pre-commit-config.yaml" --show-diff-on-failure
  exit $?
fi

>>>>>>> upstream/main
if [ -x "$PROJECT_ROOT/.venv/bin/pre-commit" ]; then
  PRE_COMMIT="$PROJECT_ROOT/.venv/bin/pre-commit"
elif command -v pre-commit >/dev/null 2>&1; then
  PRE_COMMIT="pre-commit"
else
<<<<<<< HEAD
  echo "pre-commit executable not found; trying to install via pip"
  python -m pip install --quiet pre-commit
  PRE_COMMIT="pre-commit"
=======
  echo "pre-commit executable not found; install uv (https://docs.astral.sh/uv/) or: pip install pre-commit"
  exit 1
>>>>>>> upstream/main
fi

"$PRE_COMMIT" run --hook-stage pre-commit --config "$PROJECT_ROOT/.pre-commit-config.yaml" --show-diff-on-failure
