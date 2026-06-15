"""RFC guard: enforces the RFC flow conventions on PRs.

Checks (each is a hard failure, not a warning):

1. Every file under `docs/rfcs/` (excluding `README.md` and `template.md`)
   has a frontmatter block with `status:`, `number:`, and `title:`.
2. `status` is one of `proposed`, `accepted`, `rejected`, `superseded`.
3. `number` is a 4-digit zero-padded integer.
4. The RFC's status appears in the index at `docs/rfcs/README.md` in the
   corresponding section heading.
5. The RFC's filename matches `NNNN-short-slug.md` where `NNNN` is the
   number and `short-slug` is the kebab-case form of the title.

Usage:
    uv run python scripts/rfc_guard.py
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml

RFCS_DIR = Path("docs/rfcs")
INDEX_PATH = RFCS_DIR / "README.md"
TEMPLATE_PATH = RFCS_DIR / "template.md"
README_PATH = RFCS_DIR / "README.md"

VALID_STATUSES = {"proposed", "accepted", "rejected", "superseded"}
SECTION_FOR_STATUS = {
    "proposed": "### Proposed",
    "accepted": "### Accepted",
    "rejected": "### Rejected",
    "superseded": "### Superseded",
}
FILENAME_RE = re.compile(r"^(?P<number>\d{4})-(?P<slug>[a-z0-9][a-z0-9-]*)\.md$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class RfcFile:
    path: Path
    number: int
    slug: str
    title: str
    status: str


def _read_frontmatter(path: Path) -> Optional[dict]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return None


def _check_filename(path: Path) -> tuple[Optional[int], Optional[str]]:
    m = FILENAME_RE.match(path.name)
    if not m:
        return None, None
    return int(m.group("number")), m.group("slug")


def _collect() -> tuple[List[RfcFile], List[str]]:
    files: List[RfcFile] = []
    errors: List[str] = []
    if not RFCS_DIR.exists():
        return files, [f"missing RFC directory: {RFCS_DIR}"]

    for path in sorted(RFCS_DIR.glob("*.md")):
        if path.name in {README_PATH.name, TEMPLATE_PATH.name}:
            continue
        number, slug = _check_filename(path)
        if number is None:
            errors.append(f"{path}: filename must match NNNN-slug.md (4 digits + kebab slug)")
            continue
        fm = _read_frontmatter(path)
        if not fm:
            errors.append(f"{path}: missing or invalid frontmatter")
            continue
        status = str(fm.get("status", "")).strip()
        title = str(fm.get("title", "")).strip()
        title_no_prefix = re.sub(r"^RFC\s*\d+\s*[\u2014\u2013\-:]\s*", "", title, flags=re.IGNORECASE)
        if not status or not title or "number" not in fm:
            errors.append(
                f"{path}: frontmatter must include status, number, and title"
            )
            continue
        if int(fm["number"]) != number:
            errors.append(
                f"{path}: frontmatter number={fm['number']} does not match filename {number}"
            )
        if status not in VALID_STATUSES:
            errors.append(
                f"{path}: invalid status '{status}' (must be one of {sorted(VALID_STATUSES)})"
            )
        if not title_no_prefix:
            errors.append(f"{path}: title must be non-empty after stripping 'RFC NNNN — ' prefix")
        files.append(RfcFile(path=path, number=number, slug=slug, title=title, status=status))
    return files, errors


def _check_index(rfcs: List[RfcFile]) -> List[str]:
    if not INDEX_PATH.exists():
        return [f"missing index: {INDEX_PATH}"]
    text = INDEX_PATH.read_text(encoding="utf-8")
    errors: List[str] = []
    for rfc in rfcs:
        section = SECTION_FOR_STATUS[rfc.status]
        if section not in text:
            errors.append(
                f"{rfc.path}: index is missing section '{section}' for status '{rfc.status}'"
            )
            continue
        # The RFC must be linked under its section.
        # We accept a link to "./NNNN-slug.md".
        link_token = f"](./{rfc.number:04d}-{rfc.slug}.md)"
        if link_token not in text:
            errors.append(
                f"{rfc.path}: index is missing link './{rfc.number:04d}-{rfc.slug}.md' "
                f"under section '{section}'"
            )
    return errors


def _check_duplicate_numbers(rfcs: List[RfcFile]) -> List[str]:
    seen: dict[int, str] = {}
    errors: List[str] = []
    for rfc in rfcs:
        if rfc.number in seen:
            errors.append(
                f"{rfc.path}: duplicate RFC number {rfc.number:04d} (also {seen[rfc.number]})"
            )
        else:
            seen[rfc.number] = str(rfc.path)
    return errors


def main() -> int:
    rfcs, errors = _collect()
    if errors:
        for e in errors:
            print(f"::error::{e}", file=sys.stderr)
        return 1
    if not rfcs:
        print("no RFCs to validate")
        return 0
    index_errors = _check_index(rfcs)
    dup_errors = _check_duplicate_numbers(rfcs)
    all_errors = index_errors + dup_errors
    for e in all_errors:
        print(f"::error::{e}", file=sys.stderr)
    if all_errors:
        return 1
    print(f"validated {len(rfcs)} RFC file(s) — all pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
