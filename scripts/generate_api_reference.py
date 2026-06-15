"""
API reference generator for PhenoDocs.

Reads OpenAPI 3.x specs (YAML or JSON) and emits a set of Markdown files
under docs/.generated/api/<spec-name>/. The output is consumed by the
VitePress site at /api/openapi/.

Usage:
    uv run python scripts/generate_api_reference.py \\
        --spec packages/thegent/api/openapi.yaml \\
        --out docs/.generated/api/thegent

The generator is intentionally dependency-light: it only needs PyYAML at
runtime (already in pyproject.toml). The output is plain Markdown that
the existing VitePress pipeline renders without further configuration.

The generator never fails the build on a missing spec — it logs a warning
and exits 0. This keeps `bun run build` green even when a federated
package hasn't published its spec yet.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    print("error: PyYAML is required (uv add pyyaml)", file=sys.stderr)
    sys.exit(2)


HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}


@dataclass(frozen=True)
class ResolvedRef:
    """A $ref resolved into its target dict and the path used to reach it."""

    target: Dict[str, Any]
    path: List[str]

    def get(self, key: str, default: Any = None) -> Any:
        return self.target.get(key, default)


def _load_spec(path: Path) -> Dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(raw)
    return json.loads(raw)


def _resolve_ref(ref: str, spec: Dict[str, Any]) -> ResolvedRef:
    """Resolve a $ref like '#/components/schemas/Foo' against the spec."""
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported external ref: {ref}")
    parts = ref[2:].split("/")
    cursor: Any = spec
    for part in parts:
        cursor = cursor[part]
    return ResolvedRef(target=cursor, path=parts)


def _md_escape(text: str) -> str:
    """Light Markdown escape for inline text."""
    return text.replace("|", "\\|").replace("\n", " ").strip()


def _render_schema(name: str, schema: Dict[str, Any], spec: Dict[str, Any], depth: int = 0) -> str:
    if depth > 4:
        return f"\n_{name}: (recursion limit reached)_\n"

    if "$ref" in schema:
        ref = _resolve_ref(schema["$ref"], spec)
        return _render_schema(name or ref.path[-1], ref.target, spec, depth + 1)

    if "oneOf" in schema:
        variants = schema["oneOf"]
        out = [f"\n##### `{name}` (oneOf)\n"]
        for i, variant in enumerate(variants, 1):
            out.append(_render_schema(f"variant_{i}", variant, spec, depth + 1))
        return "\n".join(out)

    if "anyOf" in schema:
        variants = schema["anyOf"]
        out = [f"\n##### `{name}` (anyOf)\n"]
        for i, variant in enumerate(variants, 1):
            out.append(_render_schema(f"variant_{i}", variant, spec, depth + 1))
        return "\n".join(out)

    if "allOf" in schema:
        out = [f"\n##### `{name}` (allOf)\n"]
        for i, part in enumerate(schema["allOf"], 1):
            out.append(_render_schema(f"part_{i}", part, spec, depth + 1))
        return "\n".join(out)

    typ = schema.get("type", "any")
    fmt = schema.get("format", "")
    desc = schema.get("description", "")
    enum = schema.get("enum")

    head = f"\n##### `{name}`: `{typ}{f' ({fmt})' if fmt else ''}`\n"
    body: List[str] = []
    if desc:
        body.append(f"\n{desc}\n")
    if enum:
        body.append("\n**Allowed values:**\n")
        body.extend(f"- `{e}`\n" for e in enum)

    if typ == "object" or "properties" in schema:
        props = schema.get("properties", {})
        required = set(schema.get("required", []))
        if props:
            body.append("\n| Field | Type | Required | Description |\n")
            body.append("| --- | --- | --- | --- |\n")
            for prop_name, prop_schema in props.items():
                if "$ref" in prop_schema:
                    ptype = _resolve_ref(prop_schema["$ref"], spec).path[-1]
                elif "type" in prop_schema:
                    ptype = prop_schema["type"]
                    if "format" in prop_schema:
                        ptype = f"{ptype} ({prop_schema['format']})"
                elif "$ref" not in prop_schema and "oneOf" in prop_schema:
                    ptype = "oneOf"
                else:
                    ptype = "any"
                req = "yes" if prop_name in required else "no"
                pdesc = _md_escape(prop_schema.get("description", ""))
                body.append(f"| `{prop_name}` | `{ptype}` | {req} | {pdesc} |\n")
    elif typ == "array":
        items = schema.get("items", {})
        if "$ref" in items:
            item_type = _resolve_ref(items["$ref"], spec).path[-1]
        elif "type" in items:
            item_type = items["type"]
        else:
            item_type = "any"
        body.append(f"\nArray of `{item_type}`.\n")

    return head + "".join(body)


def _render_operation(
    path: str,
    method: str,
    op: Dict[str, Any],
    spec: Dict[str, Any],
) -> str:
    summary = op.get("summary", "")
    desc = op.get("description", "")
    op_id = op.get("operationId", "")
    tags = op.get("tags", [])
    deprecated = op.get("deprecated", False)
    body_parts: List[str] = []

    badge = f"`{method.upper()}`"
    body_parts.append(f"### {badge} `{path}`\n")
    if op_id:
        body_parts.append(f"\n**Operation ID:** `{op_id}`\n")
    if tags:
        body_parts.append(f"\n**Tags:** {', '.join(f'`{t}`' for t in tags)}\n")
    if deprecated:
        body_parts.append("\n> **DEPRECATED** — do not use in new clients.\n")
    if summary:
        body_parts.append(f"\n{summary}\n")
    if desc:
        body_parts.append(f"\n{desc}\n")

    # Parameters
    params = op.get("parameters", [])
    if params:
        body_parts.append("\n#### Parameters\n")
        body_parts.append("\n| Name | In | Type | Required | Description |\n")
        body_parts.append("| --- | --- | --- | --- | --- |\n")
        for p in params:
            ptype = "any"
            if "schema" in p:
                s = p["schema"]
                if "$ref" in s:
                    ptype = _resolve_ref(s["$ref"], spec).path[-1]
                elif "type" in s:
                    ptype = s["type"]
                    if "format" in s:
                        ptype = f"{ptype} ({s['format']})"
            req = "yes" if p.get("required", False) else "no"
            body_parts.append(
                f"| `{p.get('name','')}` | `{p.get('in','')}` | `{ptype}` | {req} | "
                f"{_md_escape(p.get('description',''))} |\n"
            )

    # Request body
    rb = op.get("requestBody")
    if rb:
        body_parts.append("\n#### Request body\n")
        content = rb.get("content", {})
        for media_type, media in content.items():
            body_parts.append(f"\n**Media type:** `{media_type}`\n")
            schema = media.get("schema", {})
            body_parts.append(_render_schema("body", schema, spec))
            if rb.get("required"):
                body_parts.append("\n*Required.*\n")

    # Responses
    responses = op.get("responses", {})
    if responses:
        body_parts.append("\n#### Responses\n")
        for status, resp in responses.items():
            desc = _md_escape(resp.get("description", ""))
            body_parts.append(f"\n**`{status}`** — {desc}\n")
            content = resp.get("content", {})
            for media_type, media in content.items():
                body_parts.append(f"\n_Media type: `{media_type}`_\n")
                schema = media.get("schema", {})
                body_parts.append(_render_schema("response", schema, spec))

    return "\n".join(body_parts) + "\n"


def _render_paths(paths: Dict[str, Any], spec: Dict[str, Any]) -> str:
    out: List[str] = ["# API Endpoints\n"]
    grouped: Dict[str, List[Tuple[str, str, Dict[str, Any]]]] = {}
    for path, methods in paths.items():
        for method, op in methods.items():
            if method.lower() not in HTTP_METHODS:
                continue
            tag = (op.get("tags") or ["default"])[0]
            grouped.setdefault(tag, []).append((path, method, op))

    for tag in sorted(grouped):
        out.append(f"\n## Tag: `{tag}`\n")
        for path, method, op in grouped[tag]:
            out.append(_render_operation(path, method, op, spec))
    return "".join(out)


def _render_components(components: Dict[str, Any], spec: Dict[str, Any]) -> str:
    out: List[str] = ["# Components\n"]
    schemas = components.get("schemas", {})
    if schemas:
        out.append("\n## Schemas\n")
        for name in sorted(schemas):
            out.append(_render_schema(name, schemas[name], spec, depth=0))
    return "".join(out)


def _render_info(info: Dict[str, Any]) -> str:
    title = info.get("title", "API")
    version = info.get("version", "0.0.0")
    desc = info.get("description", "")
    contact = info.get("contact", {})
    license_ = info.get("license", {})
    out: List[str] = [
        f"# {title} — API Reference\n",
        f"\n**Version:** `{version}`\n",
    ]
    if desc:
        out.append(f"\n{desc}\n")
    if contact:
        out.append(f"\n**Contact:** {contact.get('name','?')} <{contact.get('email','')}>\n")
    if license_:
        out.append(f"\n**License:** {license_.get('name','')}\n")
    out.append("\n> Auto-generated by `scripts/generate_api_reference.py`. "
               "Do not edit the rendered files directly — re-run the generator.\n")
    return "".join(out)


def generate(spec_path: Path, out_dir: Path, *, force: bool = False) -> List[Path]:
    if not spec_path.exists():
        print(f"warn: spec not found: {spec_path} (skipping)", file=sys.stderr)
        return []

    spec = _load_spec(spec_path)
    info = spec.get("info", {})
    paths = spec.get("paths", {})
    components = spec.get("components", {})

    if force and out_dir.exists():
        for child in out_dir.iterdir():
            if child.is_file():
                child.unlink()

    out_dir.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []

    info_path = out_dir / "index.md"
    info_path.write_text(_render_info(info), encoding="utf-8")
    written.append(info_path)

    if paths:
        p = out_dir / "endpoints.md"
        p.write_text(_render_paths(paths, spec), encoding="utf-8")
        written.append(p)

    if components:
        p = out_dir / "components.md"
        p.write_text(_render_components(components, spec), encoding="utf-8")
        written.append(p)

    print(f"generated {len(written)} file(s) from {spec_path} -> {out_dir}")
    return written


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spec",
        action="append",
        type=Path,
        required=True,
        help="Path to an OpenAPI spec (YAML or JSON). Repeatable.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("docs/.generated/api"),
        help="Output root. One subdirectory per spec, named after the spec stem.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Clear existing files in each output dir before writing.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    total = 0
    for spec_path in args.spec:
        target = args.out / spec_path.stem
        written = generate(spec_path, target, force=args.force)
        total += len(written)

    print(f"done: {total} file(s) written under {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
