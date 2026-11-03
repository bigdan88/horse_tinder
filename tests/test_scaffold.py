"""Purely static scaffold tests — no node_modules, npm, or network required."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_gitignore_entries():
    content = (ROOT / ".gitignore").read_text()
    for entry in ("node_modules/", "dist/", "package-lock.json"):
        assert entry in content


def test_package_json():
    pkg = json.loads((ROOT / "package.json").read_text())
    assert pkg["name"] == "horse-tinder"
    assert pkg["type"] == "module"
    for script in ("dev", "build", "preview", "test"):
        assert script in pkg["scripts"]
    assert "react" in pkg["dependencies"]
    assert "react-dom" in pkg["dependencies"]
    assert "vite" in pkg["devDependencies"]
    assert "@vitejs/plugin-react" in pkg["devDependencies"]
    raw = (ROOT / "package.json").read_text()
    assert "typescript" not in raw
    assert "vitest" not in raw


def test_horses_data():
    content = (ROOT / "src" / "data" / "horses.ts").read_text()
    ids = re.findall(r"^\s*id:\s*(\d+)\s*,\s*$", content, re.MULTILINE)
    assert len(ids) == 14
    assert sorted(int(i) for i in ids) == list(range(1, 15))
    array = content.split("export const horses", 1)[1]
    for field in ("name:", "breed:", "age:", "bio:", "imageUrl:"):
        assert len(re.findall(rf"^\s*{field}", array, re.MULTILINE)) == 14
    urls = re.findall(r"imageUrl:\s*\n?\s*\"(data:image/svg\+xml,[^\"]+)\"", array)
    assert len(urls) == 14
    assert all(u.startswith("data:image/svg+xml,") for u in urls)
    assert "export const horses" in content
    assert "export default horses" in content


def test_index_html():
    content = (ROOT / "index.html").read_text()
    assert '<div id="root"' in content
    assert "/src/main.jsx" in content
    assert "Horse Tinder Demo" in content


def test_source_files_exist():
    for rel in (
        "src/main.jsx",
        "src/App.jsx",
        "src/index.css",
        "src/App.css",
        "vite.config.js",
    ):
        assert (ROOT / rel).is_file(), rel
    app = (ROOT / "src" / "App.jsx").read_text()
    assert "./data/horses" in app


def test_readme():
    content = (ROOT / "README.md").read_text()
    assert "# Horse Tinder Demo" in content
    assert "A React + Vite single-page demo where you swipe through 14 fictional horse profiles." in content


def test_project_spec_unchanged():
    content = (ROOT / "docs" / "project-spec.md").read_text()
    for marker in (
        "### Goal",
        "#### 1. Scaffold & Horse Data",
        "Estimate: $5.0 · 3.0 hours",
        "## Fixed",
    ):
        assert marker in content
