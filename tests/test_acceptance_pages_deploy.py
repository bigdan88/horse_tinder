"""Acceptance tests for the GitHub Pages deploy workflow task.

Maps to acceptance criteria AC1-AC6 of the issue "Add GitHub Actions Pages
deploy workflow".  Everything here is purely static: file-content analysis
only, no network, no npm, no git subprocess, no pytest.skip.

- AC1: deploy.yml exists, triggers on push to main, uses
       actions/upload-pages-artifact and actions/deploy-pages
- AC2: workflow YAML is syntactically valid (2-space indentation, no
       malformed keys) -- checked statically and, when PyYAML is available,
       by a real parse
- AC3: runs `npm install` (never `npm ci`) then `npm run build` and publishes
       dist/ via the Pages actions
- AC4: README.md gained a '## Live' section with the Pages URL while the
       pre-existing content is untouched
- AC5: docs/project-spec.md Fixed section is byte-for-byte unchanged
       (sha256-pinned)
- AC6: the committed tests/test_workflow.py verifies deploy.yml statically
"""

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "deploy.yml"

# sha256 of everything in docs/project-spec.md before the '## Living' heading,
# as committed at the base of this run (git diff confirms no edits this run).
SPEC_FIXED_SHA256 = "c97978fe1452c59fa673287b7d0cdf17197fefd7b4e778ec323417510e3b71e1"

# The README content that existed before this task (from the merged scaffold).
README_PREEXISTING = """\
# Horse Tinder Demo

A React + Vite single-page demo where you swipe through 14 fictional horse profiles.

## Getting started

```
npm install
npm run dev   # http://localhost:5173
npm run build # produces dist/
npm test      # placeholder
```
"""


def _workflow_text() -> str:
    assert WORKFLOW.is_file(), f"missing workflow file: {WORKFLOW}"
    return WORKFLOW.read_text(encoding="utf-8")


# --------------------------------------------------------------------------
# AC1: file exists, triggers on push to main, uses the Pages actions
# --------------------------------------------------------------------------


def test_ac1_deploy_yml_exists_non_empty():
    text = _workflow_text()
    assert text.strip(), "deploy.yml is empty"
    assert "name: Deploy to GitHub Pages" in text


def test_ac1_triggers_on_push_to_main():
    lines = _workflow_text().splitlines()
    assert lines[0].strip() == "name: Deploy to GitHub Pages"
    on_idx = lines.index("on:")
    # 'push:' is indented directly under 'on:', and 'main' is in the
    # branches list of that push trigger.
    push_idx = lines.index("  push:", on_idx)
    region = lines[push_idx + 1 :]
    branch_line = next(
        ln for ln in region if ln.startswith("    branches:")
    )
    assert "main" in branch_line
    # trigger region ends before the next top-level key
    next_top = next(i for i, ln in enumerate(lines[on_idx + 1 :], on_idx + 1) if ln and not ln[0].isspace())
    assert push_idx < next_top


def test_ac1_uses_pages_artifact_and_deploy_actions():
    text = _workflow_text()
    assert re.search(r"uses:\s*actions/upload-pages-artifact@", text)
    assert re.search(r"uses:\s*actions/deploy-pages@", text)
    assert re.search(r"uses:\s*actions/checkout@v4", text)
    assert re.search(r"uses:\s*actions/setup-node@v4", text)


# --------------------------------------------------------------------------
# AC2: YAML is syntactically valid (static lint + real parse when possible)
# --------------------------------------------------------------------------

_KEY_OR_ITEM = re.compile(
    r"^(?:(?:[A-Za-z_][A-Za-z0-9_-]*:(?:\s+\S.*)?)|(?:- .*)|(?:-)|(#.*))$"
)


def test_ac2_no_tabs_and_two_space_indentation():
    text = _workflow_text()
    assert "\t" not in text, "tabs are invalid indentation in YAML"
    prev_indent = 0
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        assert indent % 2 == 0, f"line {n}: indentation not a multiple of 2"
        assert indent - prev_indent <= 2 or prev_indent >= indent, (
            f"line {n}: indentation jumps by more than 2 spaces"
        )
        prev_indent = indent


def test_ac2_no_malformed_keys():
    for n, line in enumerate(_workflow_text().splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        assert _KEY_OR_ITEM.match(stripped), f"line {n}: malformed YAML line: {line!r}"


def test_ac2_top_level_keys_unique_and_known():
    top = [
        ln.split(":", 1)[0]
        for ln in _workflow_text().splitlines()
        if ln and not ln[0].isspace() and ":" in ln
    ]
    assert len(top) == len(set(top)), f"duplicate top-level keys: {top}"
    assert set(top) <= {
        "name",
        "on",
        "permissions",
        "concurrency",
        "jobs",
    }


def test_ac2_parses_as_yaml_with_expected_shape():
    """Full parse when PyYAML is present; the static assertions below always
    run so this test is meaningful (and passing) in either environment."""
    text = _workflow_text()
    # Order of steps is asserted statically regardless of PyYAML availability.
    order = [
        "actions/checkout@v4",
        "actions/setup-node@v4",
        "npm install --no-audit --no-fund",
        "npm run build",
        "actions/configure-pages@v5",
        "actions/upload-pages-artifact@v3",
        "actions/deploy-pages@v4",
    ]
    positions = [text.index(item) for item in order]
    assert positions == sorted(positions), "workflow steps are out of order"

    try:
        import yaml
    except ImportError:
        return
    data = yaml.safe_load(text)
    assert isinstance(data, dict)
    assert data["name"] == "Deploy to GitHub Pages"
    # YAML 1.1 parses the bare key 'on' as boolean True; GitHub parses it as
    # the string 'on'.  Accept either spelling.
    trigger = data.get("on", data.get(True))
    assert isinstance(trigger, dict) and "push" in trigger
    assert trigger["push"]["branches"] == ["main"]
    job = data["jobs"]["build-and-deploy"]
    assert job["runs-on"] == "ubuntu-latest"
    assert job["steps"][5] == {
        "uses": "actions/upload-pages-artifact@v3",
        "with": {"path": "dist"},
    }


# --------------------------------------------------------------------------
# AC3: npm install (never npm ci) then npm run build; publishes dist/
# --------------------------------------------------------------------------


def test_ac3_npm_install_then_build_never_ci():
    text = _workflow_text()
    assert "npm ci" not in text, "workflow must not use npm ci (lockfile is gitignored)"
    assert "- run: npm install --no-audit --no-fund" in text
    assert "- run: npm run build" in text
    assert text.index("npm install") < text.index("npm run build")


def test_ac3_publishes_dist_to_pages():
    text = _workflow_text()
    upload_idx = text.index("actions/upload-pages-artifact@")
    deploy_idx = text.index("actions/deploy-pages@")
    # 'path: dist' belongs to the upload step, before the deploy step.
    between = text[upload_idx:deploy_idx]
    assert re.search(r"path:\s*dist\s*$", between, re.MULTILINE), (
        "upload-pages-artifact must publish the dist/ directory"
    )


# --------------------------------------------------------------------------
# AC4: README gained '## Live' + URL, existing content unchanged
# --------------------------------------------------------------------------


def test_ac4_readme_live_section_appended_after_existing_content():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert text.startswith(README_PREEXISTING), (
        "pre-existing README content was altered"
    )
    live_idx = text.index("## Live")
    assert live_idx > text.index("```", text.index("## Getting started"))
    tail = text[live_idx:]
    assert tail.splitlines()[0].strip() == "## Live"
    assert "https://bigdan88.github.io/horse_tinder/" in tail


# --------------------------------------------------------------------------
# AC5: docs/project-spec.md Fixed section byte-for-byte unchanged
# --------------------------------------------------------------------------


def test_ac5_spec_fixed_section_unchanged():
    spec = ROOT / "docs" / "project-spec.md"
    assert spec.is_file()
    text = spec.read_text(encoding="utf-8")
    fixed = text.split("## Living", 1)[0]
    assert fixed.startswith("# Horse Tinder Demo\n\n## Fixed\n")
    digest = hashlib.sha256(fixed.encode("utf-8")).hexdigest()
    assert digest == SPEC_FIXED_SHA256, "Fixed section of project-spec.md changed"


# --------------------------------------------------------------------------
# AC6: committed static pytest test for deploy.yml exists and covers the
#      required assertions
# --------------------------------------------------------------------------


def test_ac6_committed_workflow_test_file():
    f = ROOT / "tests" / "test_workflow.py"
    assert f.is_file(), "tests/test_workflow.py must be committed"
    src = f.read_text(encoding="utf-8")
    for needle in (
        "deploy-pages",
        "upload-pages-artifact",
        "on:",
        "push:",
        "main",
        "npm install",
        "npm ci",
    ):
        assert needle in src, f"committed workflow test missing check for {needle!r}"
    # It must be static: no network/npm/subprocess imports (docstrings may
    # mention those words, so only inspect import statements).
    imports = re.findall(r"^\s*(?:import|from)\s+\S+", src, re.MULTILINE)
    for forbidden in ("urllib", "requests", "subprocess", "socket", "http"):
        assert not any(forbidden in imp for imp in imports), (
            f"workflow test should not import {forbidden}"
        )
