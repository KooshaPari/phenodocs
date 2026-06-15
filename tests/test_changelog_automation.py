"""Self-test for the changelog automation script.

Builds a small synthetic git repo inside a temp directory, creates two
conventional commits + a non-conventional one, and verifies that the
changelog builder renders the expected buckets and sections.

Run:
    uv run python tests/test_changelog_automation.py
or via pytest:
    uv run pytest tests/test_changelog_automation.py -q
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import changelog_automation as ca  # noqa: E402


def _git(cwd: Path, *args: str, env: dict | None = None) -> str:
    full_env = os.environ.copy()
    full_env.update(
        {
            "GIT_AUTHOR_NAME": "Tester",
            "GIT_AUTHOR_EMAIL": "t@example.com",
            "GIT_COMMITTER_NAME": "Tester",
            "GIT_COMMITTER_EMAIL": "t@example.com",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null",
        }
    )
    if env:
        full_env.update(env)
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
        env=full_env,
    )
    return result.stdout.strip()


class ChangelogAutomationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="ca-test-"))
        _git(self.tmp, "init", "-q", "--initial-branch=main")
        _git(self.tmp, "config", "user.email", "t@example.com")
        _git(self.tmp, "config", "user.name", "Tester")
        # Initial commit so HEAD exists.
        (self.tmp / "README.md").write_text("hi\n")
        _git(self.tmp, "add", ".")
        _git(self.tmp, "commit", "-q", "-m", "chore: bootstrap")
        self.base_sha = _git(self.tmp, "rev-parse", "HEAD")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _commit(self, msg: str, body: str = "", file: str = "f.txt") -> None:
        (self.tmp / file).write_text(msg + "\n")
        _git(self.tmp, "add", ".")
        if body:
            full = f"{msg}\n\n{body}"
        else:
            full = msg
        _git(self.tmp, "commit", "-q", "-m", full)

    def test_buckets_render(self) -> None:
        self._commit("feat(api): add /v1/widgets endpoint")
        self._commit("fix(router): reject empty slug", body="The slug must be non-empty.")
        self._commit("chore(deps): bump vitepress to 1.6.0")
        self._commit("misc cleanup", file="misc.txt")
        self._commit(
            "feat!: change response envelope",
            body="BREAKING CHANGE: response is now { data, error }.",
        )

        cl_path = self.tmp / "CHANGELOG.md"
        result = ca.build(
            repo=self.tmp,
            from_ref=self.base_sha,
            to_ref="HEAD",
            version="v0.2.0",
            date="2026-06-14",
            changelog_path=cl_path,
        )
        self.assertIsNotNone(result)
        text = cl_path.read_text(encoding="utf-8")
        self.assertIn("## [v0.2.0] — 2026-06-14", text)
        self.assertIn("### Added", text)
        self.assertIn("### Fixed", text)
        self.assertIn("### Dependencies", text)
        self.assertNotIn("### Governance", text)  # no RFC commits here
        self.assertIn("**api:**", text)
        self.assertIn("**deps:**", text)
        self.assertIn("BREAKING", text)
        # Non-conventional commit still appears under Changed.
        self.assertIn("misc cleanup", text)
        self.assertIn("### Changed", text)

    def test_no_commits_returns_none(self) -> None:
        cl_path = self.tmp / "CHANGELOG.md"
        result = ca.build(
            repo=self.tmp,
            from_ref="HEAD",
            to_ref="HEAD",
            version="v0.0.1",
            date="2026-06-14",
            changelog_path=cl_path,
        )
        self.assertIsNone(result)
        self.assertFalse(cl_path.exists())

    def test_dry_run_does_not_write(self) -> None:
        self._commit("feat(x): thing")
        cl_path = self.tmp / "CHANGELOG.md"
        out = ca.build(
            repo=self.tmp,
            from_ref=self.base_sha,
            to_ref="HEAD",
            version="v0.1.0",
            date="2026-06-14",
            changelog_path=cl_path,
            dry_run=True,
        )
        self.assertIsNotNone(out)
        self.assertFalse(cl_path.exists())
        self.assertIn("## [v0.1.0] — 2026-06-14", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
