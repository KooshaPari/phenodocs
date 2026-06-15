# Changelog

This page is the **rendered** changelog. It is rebuilt by
`scripts/changelog_automation.py` for every release.

The raw data lives in `CHANGELOG.md` (the same Markdown, kept for
tooling that expects the conventional location). On a release, the
script:

1. Reads conventional commits between the previous tag and `HEAD`.
2. Buckets them by type (`feat:` / `fix:` / `chore:` / etc.) and scope.
3. Inserts a new section at the top of the changelog file.
4. Tags the merge as `vX.Y.Z` according to the conventional bump rules
   (see [Release Matrix](/templates/release-matrix-template)).

The rendered page below mirrors the file.

---

_This index is generated. The rendered content appears below as it
exists in `CHANGELOG.md`._
