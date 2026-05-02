#!/usr/bin/env python3
"""Check all external links in documentation for validity."""
from __future__ import annotations

import asyncio
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from collections.abc import Sequence

DOCS_DIR = Path(__file__).parent.parent / "docs"
MARKDOWN_EXTENSIONS = {".md", ".mdx"}

# URLs known to be placeholders (intentionally broken for examples)
KNOWN_PLACEHOLDERS = {
    "https://example.com",
    "https://example.org",
    "https://vendor.com",
}

# Timeout for HTTP requests in seconds
REQUEST_TIMEOUT = 10.0


@dataclass
class LinkResult:
    """Result of checking a single link."""
    url: str
    file_path: str
    line_number: int
    status_code: int | None
    is_valid: bool
    error: str | None = None


def extract_links_from_file(file_path: Path) -> list[tuple[int, str]]:
    """Extract all markdown links from a file.

    Returns:
        List of (line_number, url) tuples for HTTP(S) links.
    """
    links: list[tuple[int, str]] = []
    http_link_pattern = re.compile(r"\]\((https?://[^)]+)\)")

    try:
        content = file_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"  Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return links

    for line_num, line in enumerate(content.splitlines(), start=1):
        for match in http_link_pattern.finditer(line):
            url = match.group(1)
            links.append((line_num, url))

    return links


def collect_all_links(docs_dir: Path) -> list[tuple[Path, int, str]]:
    """Collect all HTTP links from all markdown files in docs directory.

    Returns:
        List of (file_path, line_number, url) tuples.
    """
    all_links: list[tuple[Path, int, str]] = []

    for md_file in docs_dir.rglob("*.md"):
        # Skip generated content
        if ".generated" in md_file.parts:
            continue
        file_links = extract_links_from_file(md_file)
        all_links.extend((md_file, line_num, url) for line_num, url in file_links)

    return all_links


def is_placeholder_url(url: str) -> bool:
    """Check if URL is a known placeholder/example URL."""
    for placeholder in KNOWN_PLACEHOLDERS:
        if url == placeholder or url.startswith(placeholder + "/"):
            return True
    return False


async def check_link(
    client: httpx.AsyncClient,
    url: str,
    file_path: Path,
    line_number: int,
) -> LinkResult:
    """Check if a single URL is accessible.

    Args:
        client: HTTP client to use for requests.
        url: URL to check.
        file_path: Path to the file containing the link.
        line_number: Line number where the link appears.

    Returns:
        LinkResult with the check outcome.
    """
    try:
        response = await client.head(url, follow_redirects=True, timeout=REQUEST_TIMEOUT)
        is_valid = 200 <= response.status_code < 400
        # Try to get relative path, fall back to absolute
        try:
            rel_path = str(file_path.relative_to(Path.cwd()))
        except ValueError:
            rel_path = str(file_path)
        return LinkResult(
            url=url,
            file_path=rel_path,
            line_number=line_number,
            status_code=response.status_code,
            is_valid=is_valid,
            error=None if is_valid else f"HTTP {response.status_code}",
        )
    except httpx.TimeoutException:
        try:
            rel_path = str(file_path.relative_to(Path.cwd()))
        except ValueError:
            rel_path = str(file_path)
        return LinkResult(
            url=url,
            file_path=rel_path,
            line_number=line_number,
            status_code=None,
            is_valid=False,
            error="Timeout",
        )
    except httpx.RequestError as e:
        try:
            rel_path = str(file_path.relative_to(Path.cwd()))
        except ValueError:
            rel_path = str(file_path)
        return LinkResult(
            url=url,
            file_path=rel_path,
            line_number=line_number,
            status_code=None,
            is_valid=False,
            error=str(e),
        )


async def check_links_concurrent(links: Sequence[tuple[Path, int, str]]) -> list[LinkResult]:
    """Check all links concurrently with rate limiting.

    Args:
        links: Sequence of (file_path, line_number, url) tuples.

    Returns:
        List of LinkResult for each link checked.
    """
    results: list[LinkResult] = []
    semaphore = asyncio.Semaphore(10)  # Limit concurrent requests

    async def check_with_semaphore(file_path: Path, line_number: int, url: str) -> LinkResult:
        async with semaphore:
            async with httpx.AsyncClient(
                headers={"User-Agent": "PhenoDocs-LinkChecker/1.0"}
            ) as client:
                return await check_link(client, url, file_path, line_number)

    tasks = [
        check_with_semaphore(file_path, line_num, url)
        for file_path, line_num, url in links
    ]

    # Process in batches to show progress
    batch_size = 50
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        batch_results = await asyncio.gather(*batch)
        results.extend(batch_results)
        print(f"  Checked {len(results)}/{len(links)} links...")

    return results


def print_report(results: Sequence[LinkResult]) -> None:
    """Print a formatted report of link check results."""
    valid_links = [r for r in results if r.is_valid]
    invalid_links = [r for r in results if not r.is_valid]
    skipped_placeholders = [r for r in results if is_placeholder_url(r.url)]

    print("\n" + "=" * 70)
    print("LINK CHECK REPORT")
    print("=" * 70)

    print(f"\nTotal links found:  {len(results)}")
    print(f"Valid links:        {len(valid_links)}")
    print(f"Skipped (placeholders): {len(skipped_placeholders)}")
    print(f"Invalid links:      {len(invalid_links)}")

    if invalid_links:
        print("\n" + "-" * 70)
        print("INVALID LINKS:")
        print("-" * 70)
        for result in sorted(invalid_links, key=lambda r: (r.file_path, r.line_number)):
            print(f"\n  File: {result.file_path}:{result.line_number}")
            print(f"  URL:  {result.url}")
            print(f"  Error: {result.error or f'HTTP {result.status_code}'}")


def main() -> int:
    """Main entry point for the link checker."""
    print("PhenoDocs Link Checker")
    print("=" * 50)

    # Collect all links
    print(f"\nScanning documentation in: {DOCS_DIR}")
    links = collect_all_links(DOCS_DIR)

    if not links:
        print("No external links found.")
        return 0

    print(f"Found {len(links)} external links")

    # Filter out placeholders
    real_links = [(fp, ln, url) for fp, ln, url in links if not is_placeholder_url(url)]
    placeholders = [(fp, ln, url) for fp, ln, url in links if is_placeholder_url(url)]

    if placeholders:
        print(f"Skipping {len(placeholders)} placeholder/example URLs")

    if not real_links:
        print("No real links to check (only placeholders found).")
        return 0

    # Check all real links
    print("\nChecking links...")
    results = asyncio.run(check_links_concurrent(real_links))

    # Print report
    print_report(results)

    # Return exit code based on results
    invalid_count = sum(1 for r in results if not r.is_valid)
    return 1 if invalid_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
