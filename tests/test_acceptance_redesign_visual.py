"""Supplementary acceptance tests for the issue "Visual redesign of Horse
Tinder".

Complements tests/test_redesign.py by covering the exact wording of the
criteria that the static suite leaves open:

- AC2: `npm run build` must not only exit 0 (already covered by
  tests/test_acceptance_scaffold.py) but the emitted dist/index.html must
  actually reference its assets under the GitHub Pages base path
  '/horse_tinder/', otherwise the deployed site would 404.
- AC4: the two big round buttons under the card must be the reject (✕) and
  accept (♥) buttons named in the issue, not anonymous buttons.
- AC6: the clean top bar must SHOW the app title (the header element must
  contain 'Horse Tinder'), in addition to the liked-nav-btn counter already
  asserted by test_redesign.py.

AC2 here is the only dynamic test (it shells out to the local `npm run
build`, exactly like tests/test_acceptance_scaffold.py); it needs no network.
The AC4/AC6 checks are pure file-content analysis.
"""

import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "src" / "App.jsx"
DECK = ROOT / "src" / "components" / "CardDeck.jsx"


# ---------------------------------------------------------------------------
# AC2 — the built dist must be rooted at the GitHub Pages base path
# ---------------------------------------------------------------------------


def test_ac2_built_dist_references_horse_tinder_base_assets():
    if shutil.which("npm") is None:
        pytest.skip("npm executable not available")
    assert (ROOT / "node_modules" / "vite").is_dir(), (
        "Run npm install before running the dynamic acceptance tests"
    )
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
    html = (dist / "index.html").read_text(encoding="utf-8")
    assert '<div id="root">' in html

    # Every local asset URL must be prefixed with the /horse_tinder/ base.
    refs = re.findall(r'(?:src|href)="(/[^"]+)"', html)
    assert refs, "dist/index.html must reference built assets"
    local = [r for r in refs if not r.startswith("http")]
    for ref in local:
        assert ref.startswith("/horse_tinder/"), (
            f"asset URL {ref!r} is not rooted at the GitHub Pages base path"
        )

    # The referenced JS bundle must really exist on disk (working dist).
    # Vite's base is a URL prefix: dist/ itself still lays assets out at
    # dist/assets/..., so strip the base before looking on disk.
    js_refs = [r for r in local if r.endswith(".js")]
    assert js_refs, "dist/index.html must reference a built JS bundle"
    for ref in js_refs:
        assert (dist / ref.removeprefix("/horse_tinder/")).is_file(), (
            f"missing {ref} in dist/"
        )


# ---------------------------------------------------------------------------
# AC4 — the round buttons are the ✕ reject and ♥ accept actions
# ---------------------------------------------------------------------------


def test_ac4_deck_renders_reject_and_accept_glyph_buttons():
    src = DECK.read_text(encoding="utf-8")
    # Buttons must exist and call the existing swipe logic (test_redesign.py
    # asserts the triggerSwipe wiring; here we assert the visible glyphs).
    assert re.search(r"triggerSwipe\(\s*'left'\s*\)", src), (
        "CardDeck.jsx must keep a reject action calling triggerSwipe('left')"
    )
    assert re.search(r"triggerSwipe\(\s*'right'\s*\)", src), (
        "CardDeck.jsx must keep an accept action calling triggerSwipe('right')"
    )
    # The issue names the buttons ✕ and ♥; accept the common glyph variants.
    assert re.search(r"[✕✖×]|&times;", src), (
        "CardDeck.jsx must render the ✕ reject glyph on the left button"
    )
    assert re.search(r"[♥❤]|&hearts;", src), (
        "CardDeck.jsx must render the ♥ accept glyph on the right button"
    )


def test_ac4_action_buttons_rendered_under_the_card():
    src = DECK.read_text(encoding="utf-8")
    # The button row must appear after the .card-deck container in the JSX
    # (i.e. under the card), not before it.
    deck_pos = src.find('className="card-deck"')
    assert deck_pos != -1, "CardDeck.jsx must render the .card-deck container"
    left = re.search(r"triggerSwipe\(\s*'left'\s*\)", src)
    right = re.search(r"triggerSwipe\(\s*'right'\s*\)", src)
    assert left and right
    assert left.start() > deck_pos and right.start() > deck_pos, (
        "the ✕/♥ buttons must be rendered under the card"
    )


# ---------------------------------------------------------------------------
# AC6 — the top bar shows the app title
# ---------------------------------------------------------------------------


def test_ac6_top_bar_shows_app_title():
    app = APP.read_text(encoding="utf-8")
    header = re.search(
        r"<header[^>]*className=\{?['\"][^'\"]*(?:topbar|top-bar|app-header)[^'\"]*['\"]"
        r"[^>]*>(.*?)</header>",
        app,
        re.DOTALL,
    )
    assert header, "App.jsx must render the app title inside a top-bar <header> element"
    assert "Horse Tinder" in header.group(1), (
        "the top bar must show the app title 'Horse Tinder'"
    )
