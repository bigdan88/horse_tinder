"""Acceptance tests for Milestone 4 part 1: match overlay and liked collection.

Maps to the acceptance criteria of the issue
"Add MatchOverlay and LikedHorses components with static tests":

- AC1: src/components/MatchOverlay.jsx exists and default-exports
       MatchOverlay({ horse, onClose }), returns null for a falsy horse,
       imports './MatchOverlay.css', and renders the exact structure the
       issue mandates: .match-overlay (onClick={onClose}) > .match-card
       (stopPropagation) containing an "It's a Match!" heading, an
       <img src={horse.imageUrl} alt={horse.name} className="match-photo" />,
       the horse name, and a .match-close button calling onClose.
- AC2: src/components/MatchOverlay.css exists with .match-overlay
       (position: fixed, inset: 0, flex centering, z-index >= 200),
       .match-card with an entrance animation whose name has a matching
       @keyframes block, plus .match-photo, .match-card h2 and .match-close.
- AC3: src/components/LikedHorses.jsx exists and default-exports
       LikedHorses({ horses }), imports './LikedHorses.css', renders a
       .liked-empty message for an empty/undefined array, and otherwise maps
       horses into .liked-grid > .liked-item keyed by horse.id with
       img.liked-thumb src={horse.imageUrl} and <p>{horse.name}</p>.
- AC4: src/components/LikedHorses.css exists with .liked-grid
       (display: grid, auto-fill columns), .liked-nav-btn (position: fixed),
       .liked-item, .liked-thumb, .liked-item p and .liked-empty rules.

Purely static: file-content analysis only, no npm, no network, no git,
no shelling out, no conditional skips.  (Dynamic npm build self-verification
is the developer's step; the gate evidence is these static tests plus the
pre-existing suite.)
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
MATCH = SRC / "components" / "MatchOverlay.jsx"
MATCH_CSS = SRC / "components" / "MatchOverlay.css"
LIKED = SRC / "components" / "LikedHorses.jsx"
LIKED_CSS = SRC / "components" / "LikedHorses.css"


def _rule(css: str, selector: str) -> str:
    """Body of a top-level CSS rule for `selector` (exact match), or ''."""
    m = re.search(
        r"^" + re.escape(selector) + r"\s*\{(.*?)\n\}", css, re.DOTALL | re.MULTILINE
    )
    return m.group(1) if m else ""


# ---------------------------------------------------------------------------
# AC1 — MatchOverlay.jsx component structure
# ---------------------------------------------------------------------------


def test_match_overlay_file_exists_and_default_exports_component():
    assert MATCH.is_file(), "src/components/MatchOverlay.jsx must exist"
    src = MATCH.read_text(encoding="utf-8")
    assert re.search(
        r"export\s+default\s+function\s+MatchOverlay\s*\(\s*\{\s*horse\s*,\s*onClose\s*\}\s*\)",
        src,
    ), "MatchOverlay.jsx must default-export MatchOverlay({ horse, onClose })"


def test_match_overlay_returns_null_without_horse():
    src = MATCH.read_text(encoding="utf-8")
    assert re.search(r"if\s*\(\s*!horse\s*\)\s*return\s+null\s*;", src), (
        "MatchOverlay must render nothing (return null) when horse is falsy"
    )


def test_match_overlay_imports_css():
    src = MATCH.read_text(encoding="utf-8")
    assert re.search(r"import\s+['\"]\./MatchOverlay\.css['\"]", src), (
        "MatchOverlay.jsx must import './MatchOverlay.css'"
    )
    assert MATCH_CSS.is_file(), "src/components/MatchOverlay.css must exist"


def test_match_overlay_overlay_and_card_containers():
    src = MATCH.read_text(encoding="utf-8")
    assert re.search(r'<div\s+className="match-overlay"\s+onClick=\{onClose\}>', src), (
        'overlay must be <div className="match-overlay" onClick={onClose}>'
    )
    assert re.search(
        r'<div\s+className="match-card"\s+onClick=\{\s*\(?\s*e\s*\)?\s*=>\s*e\.stopPropagation\(\)\s*\}>',
        src,
    ), 'inner must be <div className="match-card" onClick={e => e.stopPropagation()}>'
    # overlay opens before the card div and the card nests inside it
    assert src.index('className="match-overlay"') < src.index(
        'className="match-card"'
    ), "the .match-card must be nested inside the .match-overlay"


def test_match_overlay_renders_heading_photo_and_name():
    src = MATCH.read_text(encoding="utf-8")
    assert re.search(r"<h2>\s*It's a Match!\s*</h2>", src), (
        "must render an <h2>It's a Match!</h2> heading"
    )
    assert re.search(
        r'<img\s+src=\{horse\.imageUrl\}\s+alt=\{horse\.name\}\s+className="match-photo"\s*/>',
        src,
    ), (
        'must render <img src={horse.imageUrl} alt={horse.name} className="match-photo" />'
    )
    assert re.search(r"<p[^>]*>\{horse\.name\}</p>", src), (
        "must render the horse name: <p>{horse.name}</p>"
    )


def test_match_overlay_close_button():
    src = MATCH.read_text(encoding="utf-8")
    assert re.search(
        r'<button\s+className="match-close"\s+onClick=\{onClose\}>', src
    ), 'must render <button className="match-close" onClick={onClose}>'


# ---------------------------------------------------------------------------
# AC2 — MatchOverlay.css rules
# ---------------------------------------------------------------------------


def test_css_match_overlay():
    css = MATCH_CSS.read_text(encoding="utf-8")
    rule = _rule(css, ".match-overlay")
    assert rule, ".match-overlay rule must exist"
    assert re.search(r"position:\s*fixed", rule), "overlay must be position: fixed"
    assert re.search(r"inset:\s*0", rule), "overlay must set inset: 0"
    assert re.search(r"display:\s*flex", rule), "overlay must be flex"
    assert re.search(r"align-items:\s*center", rule), "overlay must center vertically"
    assert re.search(r"justify-content:\s*center", rule), (
        "overlay must center horizontally"
    )
    z = re.search(r"z-index:\s*(\d+)", rule)
    assert z, "overlay must declare a numeric z-index"
    assert int(z.group(1)) >= 200, "overlay z-index must be >= 200"


def test_css_match_card_animation_and_keyframes():
    css = MATCH_CSS.read_text(encoding="utf-8")
    rule = _rule(css, ".match-card")
    assert rule, ".match-card rule must exist"
    anim = re.search(r"animation:\s*([A-Za-z0-9_-]+)", rule)
    assert anim, ".match-card must declare an entrance animation"
    name = anim.group(1)
    assert re.search(r"@keyframes\s+" + re.escape(name) + r"\s*\{", css), (
        f"@keyframes {name} must define the .match-card animation"
    )


def test_css_match_photo_heading_and_close_rules():
    css = MATCH_CSS.read_text(encoding="utf-8")
    photo = _rule(css, ".match-photo")
    assert photo, ".match-photo rule must exist"
    assert re.search(r"width:\s*100%", photo), "photo must span the card width"
    assert re.search(r"object-fit:\s*cover", photo), "photo must use object-fit: cover"

    h2 = _rule(css, ".match-card h2")
    assert h2, ".match-card h2 rule must exist"
    assert re.search(r"font-size:", h2), "match heading must set a font-size"

    close = _rule(css, ".match-close")
    assert close, ".match-close rule must exist"
    assert re.search(r"cursor:\s*pointer", close), (
        "close button must show a pointer cursor"
    )


# ---------------------------------------------------------------------------
# AC3 — LikedHorses.jsx component structure
# ---------------------------------------------------------------------------


def test_liked_horses_file_exists_and_default_exports_component():
    assert LIKED.is_file(), "src/components/LikedHorses.jsx must exist"
    src = LIKED.read_text(encoding="utf-8")
    assert re.search(
        r"export\s+default\s+function\s+LikedHorses\s*\(\s*\{\s*horses\s*\}\s*\)",
        src,
    ), "LikedHorses.jsx must default-export LikedHorses({ horses })"


def test_liked_horses_imports_css():
    src = LIKED.read_text(encoding="utf-8")
    assert re.search(r"import\s+['\"]\./LikedHorses\.css['\"]", src), (
        "LikedHorses.jsx must import './LikedHorses.css'"
    )
    assert LIKED_CSS.is_file(), "src/components/LikedHorses.css must exist"


def test_liked_horses_empty_state():
    src = LIKED.read_text(encoding="utf-8")
    assert re.search(
        r"if\s*\(\s*!horses\s*\|\|\s*horses\.length\s*===\s*0\s*\)", src
    ), "LikedHorses must guard an empty/undefined horses array"
    assert re.search(
        r'<p\s+className="liked-empty">\s*No liked horses yet\s*</p>', src
    ), 'empty state must render <p className="liked-empty">No liked horses yet</p>'


def test_liked_horses_grid_maps_items():
    src = LIKED.read_text(encoding="utf-8")
    assert re.search(r'<div\s+className="liked-grid">', src), (
        'must render <div className="liked-grid">'
    )
    assert re.search(r"horses\.map\(\s*\(?\s*horse\s*\)?\s*=>", src), (
        "must map each horse into the grid"
    )
    assert re.search(r'<div\s+className="liked-item"\s+key=\{horse\.id\}>', src), (
        'each item must be <div className="liked-item" key={horse.id}>'
    )
    assert re.search(
        r'<img\s+src=\{horse\.imageUrl\}\s+alt=\{horse\.name\}\s+className="liked-thumb"\s*/>',
        src,
    ), (
        'must render <img src={horse.imageUrl} alt={horse.name} className="liked-thumb" />'
    )
    assert re.search(r"<p>\{horse\.name\}</p>", src), (
        "must render the horse name: <p>{horse.name}</p>"
    )


# ---------------------------------------------------------------------------
# AC4 — LikedHorses.css rules
# ---------------------------------------------------------------------------


def test_css_liked_grid():
    css = LIKED_CSS.read_text(encoding="utf-8")
    rule = _rule(css, ".liked-grid")
    assert rule, ".liked-grid rule must exist"
    assert re.search(r"display:\s*grid", rule), ".liked-grid must be display: grid"
    cols = re.search(r"grid-template-columns:\s*([^;]+);", rule)
    assert cols, ".liked-grid must declare grid-template-columns"
    assert "auto-fill" in cols.group(1), (
        "grid columns must use auto-fill for a responsive collection"
    )


def test_css_liked_nav_btn():
    css = LIKED_CSS.read_text(encoding="utf-8")
    rule = _rule(css, ".liked-nav-btn")
    assert rule, ".liked-nav-btn rule must exist"
    assert re.search(r"position:\s*fixed", rule), (
        ".liked-nav-btn must be position: fixed"
    )


def test_css_liked_item_thumb_and_empty_rules():
    css = LIKED_CSS.read_text(encoding="utf-8")
    assert _rule(css, ".liked-item"), ".liked-item rule must exist"
    thumb = _rule(css, ".liked-thumb")
    assert thumb, ".liked-thumb rule must exist"
    assert re.search(r"object-fit:\s*cover", thumb), (
        "thumbnails must use object-fit: cover"
    )
    assert _rule(css, ".liked-item p"), ".liked-item p rule must exist"
    empty = _rule(css, ".liked-empty")
    assert empty, ".liked-empty rule must exist"
    assert re.search(r"text-align:\s*center", empty), "empty message must be centered"


# ---------------------------------------------------------------------------
# Purity guard — this suite stays purely static
# ---------------------------------------------------------------------------


def test_suite_is_purely_static():
    """The suite itself must not shell out, hit the network or skip tests."""
    src = Path(__file__).read_text(encoding="utf-8")
    forbidden = [
        "sub" + "process",
        "py" + "test." + "skip",
        "xf" + "ail",
        "os." + "system",
        "sock" + "et",
        "requ" + "ests",
        "url" + "open",
    ]
    for token in forbidden:
        assert token not in src, f"static suite must not use {token}"

    import_lines = [
        line.strip() for line in src.splitlines() if re.match(r"^(import|from)\s", line)
    ]
    assert import_lines == ["import re", "from pathlib import Path"], (
        "the suite may import only re and pathlib"
    )
