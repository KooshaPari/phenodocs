"""Changelog section builder for PhenoDocs.

Reads conventional commits between two git refs, groups them by type,
and appends a Markdown section to `CHANGELOG.md` (or a dedicated
`docs/changelog/index.md` if present).

Usage:
    # Build the unreleased section from main..HEAD
    uv run python scripts/changelog_automation.py --from-ref origin/main --to-ref HEAD

    # Build a release section
    uv run python scripts/changelog_automation.py \\
        --from-ref v0.0.5 --to-ref v0.1.0 --version v0.1.0 --release-date 2026-06-14

    # Print a summary to stdout without modifying any file
    uv run python scripts/changelog_automation.py --from-ref HEAD~5 --to-ref HEAD --dry-run

The script is a no-op on repos with no conventional commits in the
range. The output format mirrors the [Keep a Changelog](https://keepachangelog.com)
convention (Added / Changed / Fixed / Removed / Security / Performance
/ Documentation) plus a `Governance` bucket for merged RFCs.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


CONVENTIONAL_TYPES = {
    "feat": "Added",
    "fix": "Fixed",
    "refactor": "Changed",
    "perf": "Performance",
    "docs": "Documentation",
    "chore": "Changed",
    "test": "Changed",
    "build": "Changed",
    "ci": "Changed",
    "style": "Changed",
    "revert": "Removed",
}

# Recognized scopes that get their own bucket.
SCOPES: Dict[str, str] = {
    "deps": "Dependencies",
    "security": "Security",
    "rfc": "Governance",
    "rfcs": "Governance",
    "release": "Release",
}

BREAKING_RE = re.compile(r"^BREAKING[ -]CHANGE:\s*(.+)$", re.MULTILINE)
SUBJECT_RE = re.compile(
    r"^(?P<type>[a-zA-Z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s*(?P<subject>.+)$"
)


@dataclass(frozen=True)
class Commit:
    sha: str
    type_: str
    scope: Optional[str]
    subject: str
    body: str
    breaking: bool

    @property
    def bucket(self) -> str:
        if self.scope in SCOPES:
            return SCOPES[self.scope]
        return CONVENTIONAL_TYPES.get(self.type_, "Changed")

    def render(self) -> str:
        scope = f"**{self.scope}:** " if self.scope else ""
        breaking = "  ⚠️ **BREAKING**" if self.breaking else ""
        return f"- {scope}{self.subject} ({self.sha[:7]}){breaking}"


def _run_git(args: List[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def _list_commits(repo: Path, from_ref: str, to_ref: str) -> List[str]:
    fmt = "%H%x1f%h%x1f%s%x1f%b%x1e"
    out = _run_git(
        ["log", f"--format={fmt}", f"{from_ref}..{to_ref}"],
        cwd=repo,
    )
    return [c for c in out.split("\x1e") if c.strip()]


def _parse_commit(raw: str) -> Optional[Commit]:
    parts = raw.split("\x1f")
    if len(parts) < 4:
        return None
    sha, short, subject, body = parts[0], parts[1], parts[2], parts[3]
    subject = subject.strip()
    match = SUBJECT_RE.match(subject)
    if not match:
        # Non-conventional commit; surface as "Changed" with the original subject.
        return Commit(
            sha=sha,
            type_="other",
            scope=None,
            subject=subject,
            body=body.strip(),
            breaking=bool(BREAKING_RE.search(body)),
        )
    type_ = match.group("type").lower()
    scope = match.group("scope")
    bang = match.group("bang") == "!"
    body_text = body.strip()
    breaking = bang or bool(BREAKING_RE.search(body_text))
    subject_text = match.group("subject").strip()
    return Commit(
        sha=sha,
        type_=type_,
        scope=scope,
        subject=subject_text,
        body=body_text,
        breaking=breaking,
    )


def _bucket(commits: Iterable[Commit]) -> Dict[str, List[Commit]]:
    buckets: Dict[str, List[Commit]] = defaultdict(list)
    for c in commits:
        buckets[c.bucket].append(c)
    return buckets


def _render_section(version: str, date: str, commits: List[Commit]) -> str:
    if not commits:
        return ""
    buckets = _bucket(commits)
    lines = [f"## [{version}] — {date}", ""]
    for name in [
        "Added",
        "Changed",
        "Fixed",
        "Performance",
        "Documentation",
        "Security",
        "Dependencies",
        "Governance",
        "Release",
        "Removed",
    ]:
        items = buckets.get(name, [])
        if not items:
            continue
        lines.append(f"### {name}")
        lines.append("")
        for c in items:
            lines.append(c.render())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _split_existing(text: str) -> Tuple[str, str]:
    """Split CHANGELOG.md into (header, body)."""
    if not text:
        return "# Changelog\n\n", ""
    lines = text.splitlines(keepends=True)
    # Find the first H2 (`## [` or `## Unreleased` or `## `)
    body_start = 0
    for i, line in enumerate(lines):
        if i > 0 and line.startswith("## "):
            body_start = i
            break
    return "".join(lines[:body_start]), "".join(lines[body_start:])


def build(
    repo: Path,
    from_ref: str,
    to_ref: str,
    version: str,
    date: str,
    changelog_path: Path,
    *,
    dry_run: bool = False,
) -> Optional[str]:
    raw_commits = _list_commits(repo, from_ref, to_ref)
    commits = [c for c in (_parse_commit(r) for r in raw_commits) if c is not None]
    if not commits:
        print(f"no conventional commits between {from_ref} and {to_ref}")
        return None

    section = _render_section(version, date, commits)
    existing = changelog_path.read_text(encoding="utf-8") if changelog_path.exists() else ""
    header, body = _split_existing(existing)
    new_body = f"{section}\n{body}".rstrip() + "\n"
    new_text = f"{header}{new_body}"

    if dry_run:
        print(new_text)
        return new_text

    changelog_path.write_text(new_text, encoding="utf-8")
    print(f"wrote {changelog_path} ({len(commits)} commits, {len(new_text)} bytes)")
    return new_text


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."), help="Path to the git repo")
    parser.add_argument("--from-ref", required=True, help="Older ref (exclusive)")
    parser.add_argument("--to-ref", required=True, help="Newer ref (inclusive)")
    parser.add_argument("--version", required=True, help="Release version, e.g. v0.1.0")
    parser.add_argument("--release-date", required=True, help="ISO date, e.g. 2026-06-14")
    parser.add_argument(
        "--changelog",
        type=Path,
        default=Path("CHANGELOG.md"),
        help="Path to the changelog file (will be created if missing).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the rendered changelog to stdout instead of writing the file.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    result = build(
        repo=args.repo,
        from_ref=args.from_ref,
        to_ref=args.to_ref,
        version=args.version,
        date=args.release_date,
        changelog_path=args.changelog,
        dry_run=args.dry_run,
    )
    return 0 if result is not None or args.dry_run else 0


if __name__ == "__main__":
    sys.exit(main())
