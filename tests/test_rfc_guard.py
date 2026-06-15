"""Self-test for the RFC guard.

Builds a temporary RFCs directory, writes a few RFCs with valid and
invalid frontmatter, and asserts the guard catches the right errors.

Run:
    uv run python tests/test_rfc_guard.py
or via pytest:
    uv run pytest tests/test_rfc_guard.py -q
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Re-point the module's constants to a temp directory for hermetic tests.
import rfc_guard  # noqa: E402


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class RfcGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="rfcguard-"))
        rfc_guard.RFCS_DIR = self.tmp
        rfc_guard.INDEX_PATH = self.tmp / "README.md"
        rfc_guard.TEMPLATE_PATH = self.tmp / "template.md"
        rfc_guard.README_PATH = self.tmp / "README.md"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _valid_rfc(self, number: int, slug: str, title: str, status: str) -> str:
        return (
            f"---\n"
            f"status: {status}\n"
            f"number: {number}\n"
            f"title: \"RFC {number:04d} — {title}\"\n"
            f"---\n\n"
            f"# RFC {number:04d} — {title}\n\n"
            f"body\n"
        )

    def _index(self, lines: list[str]) -> str:
        header = "# RFCs\n\n## Index\n\n"
        return header + "\n".join(lines) + "\n"

    def test_valid_set_passes(self) -> None:
        _write(self.tmp / "0001-foo.md", self._valid_rfc(1, "foo", "Foo proposal", "proposed"))
        _write(self.tmp / "0002-bar.md", self._valid_rfc(2, "bar", "Bar proposal", "accepted"))
        _write(
            self.tmp / "README.md",
            self._index(
                [
                    "### Proposed",
                    "- [RFC 0001 — Foo proposal](./0001-foo.md)",
                    "",
                    "### Accepted",
                    "- [RFC 0002 — Bar proposal](./0002-bar.md)",
                ]
            ),
        )
        rfcs, errors = rfc_guard._collect()
        self.assertEqual(errors, [])
        self.assertEqual(len(rfcs), 2)
        self.assertEqual(rfc_guard._check_index(rfcs), [])

    def test_bad_filename_caught(self) -> None:
        _write(self.tmp / "foo.md", self._valid_rfc(1, "foo", "Foo", "proposed"))
        _write(self.tmp / "README.md", self._index(["### Proposed"]))
        _, errors = rfc_guard._collect()
        self.assertTrue(any("filename must match" in e for e in errors))

    def test_missing_frontmatter_caught(self) -> None:
        _write(self.tmp / "0001-foo.md", "# Just a doc, no frontmatter\n")
        _write(self.tmp / "README.md", self._index(["### Proposed"]))
        _, errors = rfc_guard._collect()
        self.assertTrue(any("missing or invalid frontmatter" in e for e in errors))

    def test_invalid_status_caught(self) -> None:
        _write(self.tmp / "0001-foo.md", self._valid_rfc(1, "foo", "Foo", "in-progress"))
        _write(self.tmp / "README.md", self._index(["### Proposed"]))
        _, errors = rfc_guard._collect()
        self.assertTrue(any("invalid status" in e for e in errors))

    def test_index_link_required(self) -> None:
        _write(self.tmp / "0001-foo.md", self._valid_rfc(1, "foo", "Foo", "proposed"))
        _write(
            self.tmp / "README.md",
            self._index(["### Proposed", "_no link here_"]),
        )
        rfcs, errors = rfc_guard._collect()
        self.assertEqual(errors, [])
        index_errors = rfc_guard._check_index(rfcs)
        self.assertTrue(any("missing link" in e for e in index_errors))

    def test_duplicate_number_caught(self) -> None:
        _write(self.tmp / "0001-foo.md", self._valid_rfc(1, "foo", "Foo", "proposed"))
        _write(self.tmp / "0001-bar.md", self._valid_rfc(1, "bar", "Bar", "proposed"))
        _write(self.tmp / "README.md", self._index(["### Proposed"]))
        rfcs, errors = rfc_guard._collect()
        self.assertEqual(errors, [])
        dup = rfc_guard._check_duplicate_numbers(rfcs)
        self.assertTrue(any("duplicate RFC number" in e for e in dup))


if __name__ == "__main__":
    unittest.main(verbosity=2)
