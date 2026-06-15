# phenodocs scripts package
from .changelog_automation import (
    Commit,
    build as build_changelog,
)
from .check_docs_links import (
    LinkResult,
    check_link,
    check_links_concurrent,
    collect_all_links,
    extract_links_from_file,
    is_placeholder_url,
    print_report,
    KNOWN_PLACEHOLDERS,
)
from .generate_api_reference import (
    generate as generate_api_reference,
)
from .rfc_guard import main as run_rfc_guard

__all__ = [
    "Commit",
    "LinkResult",
    "build_changelog",
    "check_link",
    "check_links_concurrent",
    "collect_all_links",
    "extract_links_from_file",
    "generate_api_reference",
    "is_placeholder_url",
    "print_report",
    "run_rfc_guard",
    "KNOWN_PLACEHOLDERS",
]
