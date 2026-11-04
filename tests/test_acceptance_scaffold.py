"""Acceptance tests for Milestone 1 (Vite+React scaffold, 14 horses).

Maps to the issue's acceptance criteria AC1–AC8.

Environment notes:
- Static checks (config files, data shape, gitignore semantics, README, spec)
  run anywhere with only Python.
- `npm test` (AC4) is genuinely executed here; it needs no node_modules.
- AC1/AC3 dynamic checks (dev server, production build) self-provision
  preinstalled node_modules and fail if dependencies are missing.
- AC2 is verified semantically by importing horses.ts with Node's built-in
  TypeScript type-stripping (Node >= 22.6), not by regex alone.
"""

import fnmatch
import json
import re
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

EXPECTED_COMMITTED_FILES = (
    ".gitignore",
    "package.json",
    "vite.config.js",
    "index.html",
    "src/main.jsx",
    "src/App.jsx",
    "src/index.css",
    "src/App.css",
    "src/data/horses.ts",
    "README.md",
    "docs/project-spec.md",
)

# The exact approved Fixed section of docs/project-spec.md (everything before
# the "## Living" header), transcribed from the approved spec in the issue.
# AC5 requires this to be byte-for-byte unchanged.
EXPECTED_FIXED_SECTION = """\
# Horse Tinder Demo

## Fixed

### Goal
A React single-page demo where the user swipes through ~14 fictional AI-generated horse profiles, taps cards for full bios, triggers a 33% random match animation on right-swipe, revisits a Liked Horses collection, and can reset/shuffle the deck. Static site, no backend, no social network.

### Users
Just the creator (solo demo, no multi-user)

### Milestones
#### 1. Scaffold & Horse Data
Initialize React+Vite project, author 14 fictional horse profiles with AI-generated images, and wire GitHub Pages auto-deploy on push to main.
- [ ] `npm run dev` serves a blank React app at localhost:5173
- [ ] A data file contains 14+ horse objects each with name, breed, age, bio, and an image URL
- [ ] `npm run build` produces a static dist/ folder with no server dependencies
- [ ] A GitHub Actions workflow deploys dist/ to GitHub Pages on every push to main
Estimate: $5.0 · 3.0 hours

#### 2. Swipe Deck UI
Render a stacked card deck with left/right swipe gestures, animated card removal, and a reset/shuffle button when the deck is empty.
- [ ] Swiping right on the top card removes it with a rightward slide-and-fade animation
- [ ] Swiping left removes it with a leftward slide-and-fade animation
- [ ] A visible counter shows remaining cards in the deck
- [ ] When the deck is empty a 'Reset & Shuffle' button appears; clicking it restores all 14 cards in a new random order
Estimate: $7.0 · 5.0 hours

#### 3. Full Profile View
Tapping the top card expands into a detail view showing all horse fields and a larger photo, with a close/back action.
- [ ] Tapping the top card opens a modal or overlay showing name, breed, age, bio, and photo
- [ ] A close/back button dismisses the detail view and returns to the swipe deck
- [ ] At least 14 distinct profiles are viewable this way with unique content
Estimate: $3.0 · 2.0 hours

#### 4. Match Animation & Liked Collection
On right-swipe a 33% random chance triggers a celebratory 'It's a Match!' overlay; liked/matched horses are saved and viewable in a grid.
- [ ] Right-swiping across 10+ horses produces at least one 'It's a Match!' overlay with the horse's photo (verifies ~33% rate)
- [ ] Every right-swiped horse is added to a 'Liked Horses' collection
- [ ] A nav button opens a grid view showing thumbnail + name for each liked horse; count matches number of right-swipes performed
Estimate: $4.0 · 3.0 hours

#### 5. Polish & Live Deploy
Apply a cohesive visual style, ensure responsive layout, and confirm the full app is live on GitHub Pages with no errors.
- [ ] App uses a consistent color palette, readable typography, and no raw/unstyled elements
- [ ] Layout is usable at 375px mobile width and 1280px desktop width
- [ ] The live GitHub Pages URL loads the app and all five capabilities work end-to-end
- [ ] Browser console shows zero errors on load and during a full swipe session
Estimate: $1.0 · 2.0 hours

### Out of scope
No real user accounts, no backend/API, no push notifications, no payments, no social network, no real horse data, no multi-user matchmaking

### Constraints
Repository: bigdan88/horse_tinder (existing)
Stack: React + Vite (static SPA build)
Hosting: GitHub Pages
Budget: $20.0
Deadline: 3 days from approval

### Latitude
Free rein on horse names, breeds, ages, bios, AI-generated photos, visual style, color palette, deck size (~14 profiles), and the 33% match probability. No need to ask before choosing any creative or UI detail.
Ask before: Nothing — user granted full creative and technical latitude on all listed items

"""


def _package_json() -> dict:
    return json.loads((ROOT / "package.json").read_text(encoding="utf-8"))


def _gitignore_patterns() -> list[str]:
    lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]


def _is_ignored(relpath: str) -> bool:
    """Minimal gitignore matcher for the simple patterns this repo uses.

    Directory patterns (trailing slash) match any path component; bare-name
    and glob patterns match the basename (gitignore semantics for patterns
    without a slash).
    """
    parts = relpath.split("/")
    for pat in _gitignore_patterns():
        dir_only = pat.endswith("/")
        base = pat.rstrip("/")
        if dir_only:
            if base in parts[:-1]:
                return True
        elif fnmatch.fnmatch(parts[-1], base):
            return True
    return False


# ---------------------------------------------------------------------------
# AC1 — npm run dev starts Vite dev server at localhost:5173 serving the app
# ---------------------------------------------------------------------------


def test_ac1_dev_is_vite_with_default_port_5173():
    """Static half of AC1: dev script is bare `vite` (default port 5173) and
    vite.config.js does not override the port."""
    pkg = _package_json()
    assert pkg["scripts"]["dev"] == "vite"
    cfg = (ROOT / "vite.config.js").read_text(encoding="utf-8")
    assert "defineConfig" in cfg and "@vitejs/plugin-react" in cfg
    assert "plugins: [react()]" in cfg
    assert not re.search(r"\bport\b", cfg), "config must not change the 5173 default"


def test_ac1_entrypoint_renders_app_into_root_div():
    """Static half of AC1: the served document contains #root and mounts App."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert '<div id="root">' in html
    assert 'type="module" src="/src/main.jsx"' in html
    main = (ROOT / "src/main.jsx").read_text(encoding="utf-8")
    assert "createRoot" in main and "getElementById('root')" in main
    app = (ROOT / "src/App.jsx").read_text(encoding="utf-8")
    assert "Horse Tinder Demo" in app


def _require_deps() -> None:
    assert (ROOT / "node_modules" / "vite").is_dir(), "Run npm install before running the acceptance tests"


def _wait_for_port(port: int, proc: subprocess.Popen, timeout: float = 30.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise AssertionError(f"dev server exited with {proc.returncode}")
        with socket.socket() as sock:
            sock.settimeout(0.5)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.25)
    raise AssertionError(f"nothing listening on port {port} after {timeout}s")


def test_ac1_npm_run_dev_serves_root_div_over_http():
    """Dynamic half of AC1: curl-equivalent GET http://localhost:5173 must
    return HTTP 200 with the #root div."""
    _require_deps()
    proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--host", "127.0.0.1", "--strictPort"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_port(5173, proc)
        with urllib.request.urlopen("http://127.0.0.1:5173/", timeout=10) as resp:
            assert resp.status == 200
            body = resp.read().decode("utf-8")
        assert '<div id="root">' in body
        assert "/src/main.jsx" in body
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)


# ---------------------------------------------------------------------------
# AC2 — horses.ts exports exactly 14 complete horse objects
# ---------------------------------------------------------------------------

_NODE_LOAD_SCRIPT = (
    "const m = await import({uri});"
    "if (m.default !== m.horses) {{ console.error('default export is not horses'); "
    "process.exit(3); }}"
    "if (!Array.isArray(m.horses)) {{ console.error('horses is not an array'); "
    "process.exit(4); }}"
    "console.log(JSON.stringify(m.horses));"
)


def _load_horses_via_node() -> list[dict]:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node executable not available")
    uri = json.dumps((ROOT / "src" / "data" / "horses.ts").as_uri())
    script = _NODE_LOAD_SCRIPT.format(uri=uri)
    runs = [
        [node, "--input-type=module", "-e", script],
        [node, "--experimental-strip-types", "--input-type=module", "-e", script],
    ]
    last_stderr = ""
    for cmd in runs:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60, check=False
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip().splitlines()[-1])
        last_stderr = result.stderr
        if "strip-types" not in result.stderr and "Type Stripping" not in result.stderr:
            break  # a real module error, not a missing-flag issue
    pytest.fail(f"could not import horses.ts via node: {last_stderr[-500:]}")


def test_ac2_horse_array_is_semantically_valid():
    horses = _load_horses_via_node()
    assert len(horses) == 14, f"expected exactly 14 horses, got {len(horses)}"
    assert [h["id"] for h in horses] == list(range(1, 15))
    for h in horses:
        assert isinstance(h["name"], str) and h["name"].strip()
        assert isinstance(h["breed"], str) and h["breed"].strip()
        assert isinstance(h["age"], int) and 0 < h["age"] < 40
        assert isinstance(h["bio"], str) and len(h["bio"]) >= 20
        assert h["imageUrl"].startswith("data:"), h["imageUrl"][:30]
    # 14 distinct profiles (unique names and bios)
    assert len({h["name"] for h in horses}) == 14
    assert len({h["bio"] for h in horses}) == 14


def test_ac2_named_and_default_exports_declared():
    content = (ROOT / "src" / "data" / "horses.ts").read_text(encoding="utf-8")
    assert re.search(r"export\s+(const|interface)\s+Horse\b", content)
    assert "export const horses" in content
    assert "export default horses" in content


# ---------------------------------------------------------------------------
# AC3 — npm run build exits 0, emits dist/index.html + hashed assets
# ---------------------------------------------------------------------------


def test_ac3_build_script_and_no_server_runtime_dependency():
    """Static half of AC3: build is `vite build` and runtime dependencies are
    browser-only (react/react-dom) — no server framework anywhere in the
    manifest."""
    pkg = _package_json()
    assert pkg["scripts"]["build"] == "vite build"
    assert set(pkg.get("dependencies", {})) <= {"react", "react-dom"}
    raw = (ROOT / "package.json").read_text(encoding="utf-8")
    for server in ("express", "fastify", "koa", "hapi", "next"):
        assert server not in raw


def test_ac3_npm_run_build_emits_hashed_static_dist():
    """Dynamic half of AC3: `npm run build` must exit 0 and emit a static
    dist/ with hashed assets referenced by dist/index.html."""
    _require_deps()
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    dist = ROOT / "dist"
    assert dist.is_dir()
    html = (dist / "index.html").read_text(encoding="utf-8")
    assert '<div id="root">' in html
    assets = [p for p in (dist / "assets").iterdir() if p.is_file()]
    assert assets, "dist/assets/ is empty"
    js = [p.name for p in assets if p.name.endswith(".js")]
    assert any(re.fullmatch(r"[\w-]+-[A-Za-z0-9_-]{8,}\.js", n) for n in js), js
    for name in js:
        assert name in html, "index.html must reference the hashed bundle"


# ---------------------------------------------------------------------------
# AC4 — npm test exits 0 via the placeholder echo script
# ---------------------------------------------------------------------------


def test_ac4_npm_test_placeholder_exits_zero():
    if shutil.which("npm") is None:
        pytest.skip("npm executable not available")
    assert _package_json()["scripts"]["test"].startswith("echo ")
    result = subprocess.run(
        ["npm", "test"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "scaffold ok" in result.stdout


# ---------------------------------------------------------------------------
# AC5 — docs/project-spec.md present and Fixed section byte-for-byte approved
# ---------------------------------------------------------------------------


def test_ac5_project_spec_fixed_section_is_byte_for_byte_approved():
    spec = ROOT / "docs" / "project-spec.md"
    assert spec.is_file()
    content = spec.read_text(encoding="utf-8")
    assert "## Living" in content, "Living section header must exist"
    fixed_part = content.split("## Living", 1)[0]
    assert fixed_part == EXPECTED_FIXED_SECTION


# ---------------------------------------------------------------------------
# AC6 — README heading, one-line description, getting-started commands
# ---------------------------------------------------------------------------


def test_ac6_readme_heading_and_description():
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    assert content.startswith("# Horse Tinder Demo\n")
    assert (
        "A React + Vite single-page demo where you swipe through 14 fictional "
        "horse profiles." in content
    )


def test_ac6_readme_getting_started_commands():
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    for cmd in ("npm install", "npm run dev", "npm run build", "npm test"):
        assert cmd in content, cmd


# ---------------------------------------------------------------------------
# AC7 — .gitignore covers build artifacts; git add -A cannot stage them
# ---------------------------------------------------------------------------


def test_ac7_gitignore_contains_all_required_entries():
    patterns = _gitignore_patterns()
    for entry in ("node_modules/", "dist/", "package-lock.json", ".vite/", "*.local"):
        assert entry in patterns, entry


@pytest.mark.parametrize(
    "artifact",
    [
        "node_modules/vite/index.js",
        "node_modules/.bin/vite",
        "package-lock.json",
        "dist/index.html",
        "dist/assets/index-a1b2c3d4.js",
        ".vite/deps/react.js",
        "src/vite-env.local",
    ],
)
def test_ac7_artifact_paths_are_gitignored(artifact):
    assert _is_ignored(artifact), f"{artifact} would be staged by git add -A"


def test_ac7_source_files_are_not_gitignored():
    for rel in EXPECTED_COMMITTED_FILES:
        assert not _is_ignored(rel), f"{rel} must be stageable"


# ---------------------------------------------------------------------------
# AC8 — lockfile never committed/hand-authored; committed files exist
# ---------------------------------------------------------------------------


def test_ac8_package_lock_is_gitignored_not_committed():
    """The lockfile can never enter the index: it is gitignored. (Attempt 1 of
    this milestone failed because a hand-authored lockfile was committed.)"""
    assert "package-lock.json" in _gitignore_patterns()
    assert _is_ignored("package-lock.json")


def test_ac8_all_expected_committed_files_exist():
    """Every file that should be committed is a hand-written source/config
    file that actually exists in the tree."""
    for rel in EXPECTED_COMMITTED_FILES:
        assert (ROOT / rel).is_file(), rel


def test_ac8_no_typescript_or_vitest_dependency_smuggling():
    raw = (ROOT / "package.json").read_text(encoding="utf-8")
    manifest = json.loads(raw)
    all_deps = {
        **manifest.get("dependencies", {}),
        **manifest.get("devDependencies", {}),
    }
    assert "typescript" not in all_deps
    assert "vitest" not in all_deps
    assert "jsdom" not in all_deps
    assert not (ROOT / "tsconfig.json").exists(), "esbuild handles .ts in Vite"
