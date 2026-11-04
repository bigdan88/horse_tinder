"""Purely static workflow tests — no network, npm, or subprocess required."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "deploy.yml"


def test_workflow_exists_non_empty():
    assert WORKFLOW.is_file()
    content = WORKFLOW.read_text()
    assert content.strip()


def test_workflow_uses_pages_actions():
    text = WORKFLOW.read_text()
    assert re.search(r"actions/upload-pages-artifact@", text)
    assert re.search(r"actions/deploy-pages@", text)


def test_workflow_trigger_push_main():
    text = WORKFLOW.read_text()
    assert re.search(r"^on:", text, re.MULTILINE)
    assert "push:" in text
    assert "main" in text
    on_idx = text.index("on:")
    push_idx = text.index("push:")
    assert on_idx < push_idx
    # 'main' must appear in the trigger region between 'push:' and 'permissions:'
    region = text[push_idx:text.index("permissions:")]
    assert "main" in region


def test_workflow_npm_install_not_ci():
    text = WORKFLOW.read_text()
    assert "npm install" in text
    assert "npm ci" not in text
    assert "npm install --no-audit --no-fund" in text


def test_workflow_build_after_install():
    text = WORKFLOW.read_text()
    assert "npm run build" in text
    assert text.index("npm install") < text.index("npm run build")


def test_workflow_artifact_path_dist():
    text = WORKFLOW.read_text()
    assert re.search(r"path:\s*dist", text)


def test_workflow_permissions():
    text = WORKFLOW.read_text()
    assert "contents: read" in text
    assert "pages: write" in text
    assert "id-token: write" in text


def test_workflow_node_setup():
    text = WORKFLOW.read_text()
    assert "setup-node" in text
    assert "node-version: 20" in text


def test_readme_live_section():
    text = (ROOT / "README.md").read_text()
    assert "## Live" in text
    assert "https://bigdan88.github.io/horse_tinder/" in text


def test_project_spec_unchanged():
    spec = ROOT / "docs" / "project-spec.md"
    assert spec.is_file()
    text = spec.read_text()
    fixed = text.split("## Living", 1)[0]
    assert fixed.startswith("# Horse Tinder Demo\n\n## Fixed\n")
    for heading in (
        "### Goal",
        "### Milestones",
        "#### 5. Polish & Live Deploy",
        "### Latitude",
    ):
        assert heading in fixed


def test_workflow_yaml_parses():
    text = WORKFLOW.read_text()
    assert "\t" not in text
    try:
        import yaml
    except ImportError:
        return
    data = yaml.safe_load(text)
    assert data["name"] == "Deploy to GitHub Pages"
    assert "push" in data[True]  # YAML 1.1 parses bare 'on' as boolean True
    assert data["permissions"] == {
        "contents": "read",
        "pages": "write",
        "id-token": "write",
    }
    job = data["jobs"]["build-and-deploy"]
    assert job["runs-on"] == "ubuntu-latest"
    steps = job["steps"]
    assert len(steps) == 7
    assert steps[0]["uses"] == "actions/checkout@v4"
    assert steps[1]["uses"] == "actions/setup-node@v4"
    assert steps[1]["with"] == {"node-version": 20}
    assert steps[2]["run"] == "npm install --no-audit --no-fund"
    assert steps[3]["run"] == "npm run build"
    assert steps[4]["uses"] == "actions/configure-pages@v5"
    assert steps[5]["uses"] == "actions/upload-pages-artifact@v3"
    assert steps[5]["with"] == {"path": "dist"}
    assert steps[6]["uses"] == "actions/deploy-pages@v4"
    assert steps[6]["id"] == "deployment"
