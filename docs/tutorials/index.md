# Tutorials

Step-by-step walkthroughs for working with the PhenoDocs federation hub.
Each tutorial is **task-oriented**: you should be able to copy a snippet
and have it work, not just read about it.

## Index

1. [First-time setup](./01-first-time-setup) — clone, install, run `bun run dev`.
2. [Adding a project to the hub](./02-adding-a-project) — wire a new project into the federation.
3. [Generating the API reference](./03-generating-api-reference) — run the OpenAPI → Markdown pipeline.
4. [Writing an RFC](./04-writing-an-rfc) — propose a change using the RFC flow.
5. [Cutting a release](./05-cutting-a-release) — run the changelog automation and publish a tag.

## Conventions for tutorials

- Use shell snippets that are copy-pasteable from the doc site.
- Prefer `bun` and `uv` (the repo's toolchains) over `npm` / `pip`.
- Each tutorial ends with a "Verify" section that confirms success.
- Link to the relevant governance doc instead of restating rules.

## Adding a new tutorial

1. Create `docs/tutorials/NN-short-title.md` (next sequential number).
2. Frontmatter:

   ```yaml
   ---
   title: NN — Short title
   ---
   ```

3. First heading must match the file name (kebab-case).
4. Add the entry to this index and to the VitePress sidebar (see
   `/.vitepress/config.mts`).
5. Open a PR — the doc-links CI job will validate internal references.
