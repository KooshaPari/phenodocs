#!/usr/bin/env python3
"""Link checker for documentation files."""
from __future__ import annotations

import asyncio
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import httpx

KNOWN_PLACEHOLDERS = {"example.com", "example.org", "vendor.com"}


@dataclass
class LinkResult:
    """Result of checking a single link."""

    url: str
    file_path: str
    line_number: int
    status_code: int | None
    is_valid: bool
    error: str | None = None


def extract_links_from_file(file_path: Path) -> List[tuple[int, str]]:
    """Extract HTTP(S) links from a markdown file."""
    links = []
    if not file_path.exists():
        return links
    pattern = re.compile(r"\[([^\]]*)\]\((https?://[^\)]+)\)")
    try:
        content = file_path.read_text()
    except Exception:
        return links
    for i, line in enumerate(content.splitlines(), 1):
        for match in pattern.finditer(line):
            url = match.group(2)
            if url.startswith("http://") or url.startswith("https://"):
                links.append((i, url))
    return links


def is_placeholder_url(url: str) -> bool:
    """Check if a URL is a known placeholder."""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        if not domain:
            return False
        return domain in KNOWN_PLACEHOLDERS
    except Exception:
        return False


def collect_all_links(docs_dir: Path) -> List[tuple[Path, int, str]]:
    """Collect all HTTP(S) links from markdown files in a directory."""
    links = []
    if not docs_dir.exists():
        return links
    for path in docs_dir.rglob("*.md"):
        # Skip .generated directories
        if ".generated" in path.parts:
            continue
        for line_number, url in extract_links_from_file(path):
            links.append((path, line_number, url))
    return links


async def check_link(
    client: httpx.AsyncClient,
    url: str,
    file_path: Path,
    line_number: int,
    timeout: float = 10.0,
) -> LinkResult:
    """Check if a single link is valid."""
    if is_placeholder_url(url):
        return LinkResult(
            url=url,
            file_path=str(file_path),
            line_number=line_number,
            status_code=None,
            is_valid=True,
        )
    try:
        response = await client.head(url, timeout=timeout, follow_redirects=True)
        return LinkResult(
            url=url,
            file_path=str(file_path),
            line_number=line_number,
            status_code=response.status_code,
            is_valid=response.status_code < 400,
        )
    except httpx.TimeoutException:
        return LinkResult(
            url=url,
            file_path=str(file_path),
            line_number=line_number,
            status_code=None,
            is_valid=False,
            error="Timeout",
        )
    except httpx.HTTPStatusError as e:
        return LinkResult(
            url=url,
            file_path=str(file_path),
            line_number=line_number,
            status_code=e.response.status_code,
            is_valid=False,
            error=str(e),
        )
    except Exception as e:
        return LinkResult(
            url=url,
            file_path=str(file_path),
            line_number=line_number,
            status_code=None,
            is_valid=False,
            error=str(e),
        )


async def check_links_concurrent(
    links: List[tuple[Path, int, str]],
    timeout: float = 10.0,
) -> List[LinkResult]:
    """Check multiple links concurrently."""
    results = []
    async with httpx.AsyncClient() as client:
        tasks = [
            check_link(client, url, file_path, line_number, timeout)
            for file_path, line_number, url in links
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return [
        r if isinstance(r, LinkResult) else LinkResult(
            url="",
            file_path="",
            line_number=0,
            status_code=None,
            is_valid=False,
            error=str(r),
        )
        for r in results
    ]


def print_report(results: List[LinkResult]) -> None:
    """Print a report of link check results."""
    valid = [r for r in results if r.is_valid]
    invalid = [r for r in results if not r.is_valid]
    print(f"Valid links: {len(valid)}")
    print(f"Invalid links: {len(invalid)}")
    for r in invalid:
        print(f"  - {r.url} ({r.file_path}:{r.line_number}) - {r.error or r.status_code}")


def main() -> int:
    """Main entry point for the link checker."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        print("No docs directory found.")
        return 0
    links = collect_all_links(docs_dir)
    if not links:
        print("No links found.")
        return 0
    results = asyncio.run(check_links_concurrent(links))
    print_report(results)
    return 1 if any(not r.is_valid for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
