"""Self-test for the OpenAPI reference generator.

Runs the generator against the bundled phenodocs spec and asserts the
expected output structure. The test is intentionally self-contained: it
never reads the network and never writes outside the temp directory it
creates.

Run:
    uv run python tests/test_generate_api_reference.py
or via pytest:
    uv run pytest tests/test_generate_api_reference.py -q
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
SPEC_PATH = REPO_ROOT / "docs" / "api" / "openapi" / "phenodocs.yaml"

sys.path.insert(0, str(SCRIPTS_DIR))

import generate_api_reference as gar  # noqa: E402


class GenerateApiReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="gar-test-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_renders_index_endpoints_components(self) -> None:
        written = gar.generate(SPEC_PATH, self.tmp / "phenodocs", force=True)
        names = sorted(p.name for p in written)
        self.assertIn("index.md", names)
        self.assertIn("endpoints.md", names)
        self.assertIn("components.md", names)

        index_md = (self.tmp / "phenodocs" / "index.md").read_text(encoding="utf-8")
        self.assertIn("Phenotype Federation", index_md)
        self.assertIn("Version:", index_md)
        self.assertIn("Auto-generated", index_md)

        endpoints_md = (self.tmp / "phenodocs" / "endpoints.md").read_text(encoding="utf-8")
        self.assertIn("`GET` `/guide/{slug}`", endpoints_md)
        self.assertIn("`/api/openapi/{name}`", endpoints_md)

        comp_md = (self.tmp / "phenodocs" / "components.md").read_text(encoding="utf-8")
        self.assertIn("## Schemas", comp_md)
        self.assertIn("`Guide`", comp_md)
        self.assertIn("`Rfc`", comp_md)

    def test_missing_spec_does_not_raise(self) -> None:
        bogus = self.tmp / "nope.yaml"
        written = gar.generate(bogus, self.tmp / "out")
        self.assertEqual(written, [])

    def test_render_schema_object_table(self) -> None:
        spec = {
            "components": {
                "schemas": {
                    "Pet": {
                        "type": "object",
                        "required": ["id", "name"],
                        "properties": {
                            "id": {"type": "integer", "format": "int64"},
                            "name": {"type": "string", "description": "Pet name"},
                            "tag": {"type": "string", "description": "Optional tag"},
                        },
                    }
                }
            }
        }
        md = gar._render_schema("Pet", spec["components"]["schemas"]["Pet"], spec)  # noqa: SLF001
        self.assertIn("| Field | Type | Required | Description |", md)
        self.assertIn("`id`", md)
        self.assertIn("`name`", md)
        self.assertIn("yes", md)
        self.assertIn("no", md)

    def test_render_operation_deprecated_banner(self) -> None:
        spec = {
            "paths": {
                "/x": {
                    "get": {
                        "tags": ["t"],
                        "summary": "X",
                        "deprecated": True,
                        "responses": {"200": {"description": "ok"}},
                    }
                }
            }
        }
        md = gar._render_operation("/x", "get", spec["paths"]["/x"]["get"], spec)  # noqa: SLF001
        self.assertIn("DEPRECATED", md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
