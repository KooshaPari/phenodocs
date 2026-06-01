# Implementation Strategy

Use a fresh worktree rooted at the active `fix/tsconfig-strict-mode` head. This
avoids carrying stale `ci/add-mypy` branch deltas into the live checkout.

Keep the downstream change governance-only: README badge plus session docs.
