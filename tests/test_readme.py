"""Static README and unchanged-file tests for Milestone 5 part 2: testing and
capabilities documentation.

Maps to the acceptance criteria of the issue
"README testing and capabilities documentation with static README tests":

- AC1: README.md keeps its pinned prefix byte-for-byte (title, description
       line, '## Getting started' block including "npm test      # placeholder")
       and the '## Live' heading followed by
       https://bigdan88.github.io/horse_tinder/.
- AC2: README.md contains a '## Testing' section documenting
       `python -m pytest -q` as the real test command and stating that
       `npm test` is a placeholder, plus a '## Capabilities' section describing
       all five demo capabilities: the swipe deck with left/right
       slide-and-fade removal and a remaining-cards counter, the tap-to-open
       full profile modal with a close action, the 33% "It's a Match!"
       overlay on right-swipe, the Liked Horses grid with a thumbnail and name
       per liked horse, and 'Reset & Shuffle' restoring all 14 horses in a new
       random order.  The '## Live' block must precede '## Testing', which must
       precede '## Capabilities'.
- AC3: the six stylesheets keep the palette, media-query, button and fluid
       declarations pinned by tests/test_polish.py.
- AC4: the .jsx/.ts sources, package.json (including the `npm test`
       placeholder), vite.config.js and .github/workflows/deploy.yml are
       unchanged.
- AC5: docs/project-spec.md's Fixed section keeps its pinned FNV-1a digest,
       no package-lock.json exists, and this suite stays purely static.

Purely static: file-content analysis only, no shelling out, no remote
services, no conditional bypasses.  (Dynamic build self-verification is the
developer's step; the gate evidence is these static checks plus the
pre-existing suite.)
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
INDEX_CSS = SRC / "index.css"
APP_CSS = SRC / "App.css"
SWIPE_CSS = SRC / "components" / "SwipeDeck.css"
MODAL_CSS = SRC / "components" / "ProfileModal.css"
MATCH_CSS = SRC / "components" / "MatchOverlay.css"
LIKED_CSS = SRC / "components" / "LikedHorses.css"
CSS_FILES = (INDEX_CSS, APP_CSS, SWIPE_CSS, MODAL_CSS, MATCH_CSS, LIKED_CSS)
APP = SRC / "App.jsx"
DECK = SRC / "components" / "CardDeck.jsx"
CARD = SRC / "components" / "Card.jsx"
MODAL = SRC / "components" / "ProfileModal.jsx"
MATCH = SRC / "components" / "MatchOverlay.jsx"
LIKED = SRC / "components" / "LikedHorses.jsx"
HORSES = SRC / "data" / "horses.ts"
MAIN = SRC / "main.jsx"
PACKAGE = ROOT / "package.json"
VITE_CONFIG = ROOT / "vite.config.js"
WORKFLOW = ROOT / ".github" / "workflows" / "deploy.yml"
README = ROOT / "README.md"
SPEC = ROOT / "docs" / "project-spec.md"

# Hex literals the pre-existing suites pin inside component stylesheets.
PINNED_HEXES = {"#fff", "#c0392b", "#e74c3c"}
# Ad-hoc colours the polish pass replaced with shared tokens.
AD_HOC_HEXES = ("#333", "#555", "#777", "#34495e", "#faf7f2")

# FNV-1a 64-bit digest and character length of the Fixed section exactly as
# merged on main.  The Fixed part of the spec must be committed unchanged, so
# any byte or length change must break this pinned digest.
FIXED_FNV1A64 = 0x706BE30ACF599D9E
FIXED_LEN = 3544


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rule(css: str, selector: str) -> str:
    """Body of a top-level CSS rule for `selector` (exact match), or ''."""
    m = re.search(
        r"^" + re.escape(selector) + r"\s*\{(.*?)\n\}", css, re.DOTALL | re.MULTILINE
    )
    return m.group(1) if m else ""


def _json_block(raw: str, key: str) -> str:
    """Body of a flat JSON object value in package.json, or ''."""
    m = re.search(r'"' + re.escape(key) + r'"\s*:\s*\{(.*?)\}', raw, re.DOTALL)
    return m.group(1) if m else ""


def _fnv1a_64(data: bytes) -> int:
    h = 0xCBF29CE484222325
    for byte in data:
        h = ((h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF) ^ byte
    return h


def _fixed_section() -> str:
    spec = _read(SPEC)
    assert spec.count("## Fixed") == 1, (
        "project-spec.md must carry exactly one Fixed heading"
    )
    assert spec.count("## Living") == 1, (
        "project-spec.md must carry exactly one Living heading"
    )
    start = spec.index("## Fixed")
    end = spec.index("## Living")
    assert start < end, "the Fixed section must precede the Living section"
    return spec[start:end]


# ---------------------------------------------------------------------------
# AC1 — pinned README prefix, Getting started block and Live URL
# ---------------------------------------------------------------------------


def test_readme_prefix_unchanged():
    content = _read(README)
    prefix = (
        "# Horse Tinder Demo\n\n"
        "A React + Vite single-page demo where you swipe through 14 fictional "
        "horse profiles."
    )
    assert content.startswith(prefix), "README.md must keep its pinned prefix"


def test_readme_getting_started_commands_unchanged():
    content = _read(README)
    assert "## Getting started" in content, "README.md must keep '## Getting started'"
    for command in (
        "npm install",
        "npm run dev   # http://localhost:5173",
        "npm run build # produces dist/",
        "npm test      # placeholder",
    ):
        assert command in content, f"README.md must keep the command {command!r}"


def test_readme_live_block_unchanged():
    content = _read(README)
    assert "## Live\n\nhttps://bigdan88.github.io/horse_tinder/" in content, (
        "README.md must keep the '## Live' heading and Pages URL"
    )


# ---------------------------------------------------------------------------
# AC2 — new Testing and Capabilities sections
# ---------------------------------------------------------------------------


def test_readme_testing_section():
    content = _read(README)
    assert "## Testing" in content, "README.md must contain a '## Testing' section"
    start = content.index("## Testing")
    end = content.index("## Capabilities")
    section = content[start:end]
    assert "python -m pytest -q" in section, (
        "the Testing section must document `python -m pytest -q` as the real command"
    )
    assert "placeholder" in section, (
        "the Testing section must state that `npm test` is a placeholder"
    )
    assert "npm test" in section, (
        "the Testing section must name the `npm test` placeholder"
    )


def test_readme_capabilities_section():
    content = _read(README)
    assert "## Capabilities" in content, (
        "README.md must contain a '## Capabilities' section"
    )
    section = content[content.index("## Capabilities") :]
    for marker in (
        "slide-and-fade",
        "counter",
        "modal",
        "close",
        "It's a Match!",
        "33%",
        "Liked Horses",
        "thumbnail",
        "Reset & Shuffle",
        "14",
        "random order",
    ):
        assert marker in section, f"the Capabilities section must describe {marker!r}"


def test_readme_section_order():
    content = _read(README)
    live = content.index("## Live")
    testing = content.index("## Testing")
    capabilities = content.index("## Capabilities")
    assert live < testing < capabilities, (
        "README.md must order '## Live' before '## Testing' before '## Capabilities'"
    )


# ---------------------------------------------------------------------------
# AC3 — six stylesheets keep their pinned declarations
# ---------------------------------------------------------------------------


def test_index_css_palette_and_typography():
    css = _read(INDEX_CSS)
    root = _rule(css, ":root")
    assert root, "src/index.css must define a :root block"
    for token in (
        "--background",
        "--surface",
        "--text",
        "--muted",
        "--accent",
        "--accent-dark",
        "--radius",
        "--shadow",
    ):
        assert re.search(re.escape(token) + r"\s*:", root), (
            f":root must define the {token} custom property"
        )
    family = re.search(r"font-family:\s*([^;]+);", root)
    assert family, ":root must declare a font-family stack"
    assert len([part for part in family.group(1).split(",") if part.strip()]) >= 2, (
        "the font-family stack must have at least two entries"
    )
    assert re.search(r"font-size:\s*16px", root), ":root must set a 16px base font-size"
    assert re.search(r"line-height:\s*1\.5", root), ":root must set line-height: 1.5"
    for tag in ("h1", "h2", "h3"):
        rule = _rule(css, tag)
        assert rule, f"src/index.css must define a {tag} rule"
        assert re.search(r"font-size:\s*[^;]+;", rule), f"{tag} must set a font-size"

    reset = _rule(css, "*, *::before, *::after")
    assert reset, "src/index.css must define the universal reset rule"
    assert re.search(r"box-sizing:\s*border-box", reset), (
        "the universal reset must set box-sizing: border-box"
    )
    assert re.search(r"margin:\s*0", reset), "the universal reset must set margin: 0"


def test_app_css_media_queries_and_container():
    css = _read(APP_CSS)
    assert css.count("var(--") >= 3, "src/App.css must use at least three tokens"
    app = _rule(css, ".app")
    assert app, "src/App.css must define the .app shell"
    assert re.search(r"min-height:\s*100vh", app), ".app must keep min-height: 100vh"
    assert "center" in app, ".app must keep its centering declarations"
    assert re.search(r"max-width:\s*(var\(--container\)|min\(|100%)", css), (
        "src/App.css must define a max-width container"
    )
    for query in ("@media (max-width: 480px)", "@media (min-width: 1024px)"):
        assert query in css, f"src/App.css must contain the literal {query}"
        block = re.search(re.escape(query) + r"\s*\{(.*?)\n\}", css, re.DOTALL)
        assert block, f"{query} must open a block closed at column 0"
        declarations = re.findall(r":\s*[^;]+;", block.group(1))
        assert len(declarations) >= 2, f"{query} must contain at least two declarations"


def test_swipe_deck_css_fluid_and_keyframes():
    css = _read(SWIPE_CSS)
    deck = _rule(css, ".card-deck")
    assert deck, ".card-deck rule must exist"
    assert re.search(r"width:\s*min\(\s*340px\s*,\s*90vw\s*\)", deck), (
        ".card-deck width must stay min(340px, 90vw)"
    )
    assert re.search(r"max-width:\s*100%", deck), (
        ".card-deck must cap at max-width: 100%"
    )

    card = _rule(css, ".card")
    assert card, ".card rule must exist"
    assert re.search(r"position:\s*absolute", card), (
        ".card must stay position: absolute"
    )
    assert re.search(r"inset:\s*0", card), ".card must keep inset: 0"

    for cls, keyframe in (
        ("swipe-right", "slideRightFade"),
        ("swipe-left", "slideLeftFade"),
    ):
        rule = _rule(css, ".card." + cls)
        assert rule, f".card.{cls} rule must exist"
        anim = re.search(r"animation:\s*([^;]+);", rule)
        assert anim, f".card.{cls} must declare an animation"
        assert keyframe in anim.group(1), f".card.{cls} must use {keyframe}"
        assert "300ms" in anim.group(1), f".card.{cls} animation must stay 300ms"
        assert "forwards" in anim.group(1), f".card.{cls} must keep forwards fill"

        block = re.search(
            r"@keyframes\s+" + keyframe + r"\s*\{(.*?)\n\}", css, re.DOTALL
        )
        assert block, f"@keyframes {keyframe} must exist"
        body = block.group(1)
        assert "transform" in body and "opacity" in body, (
            f"@keyframes {keyframe} must animate transform and opacity"
        )
        assert re.search(r"from\s*\{[^}]*transform", body, re.DOTALL), (
            f"@keyframes {keyframe} from block must set transform"
        )
        assert re.search(r"to\s*\{[^}]*opacity", body, re.DOTALL), (
            f"@keyframes {keyframe} to block must set opacity"
        )

    assert _rule(css, ".reset-btn:hover"), ".reset-btn:hover rule must exist"


def test_profile_modal_css_rules():
    css = _read(MODAL_CSS)
    overlay = _rule(css, ".profile-overlay")
    assert overlay, ".profile-overlay rule must exist"
    assert re.search(r"position:\s*fixed", overlay), "overlay must be position: fixed"
    assert re.search(r"inset:\s*0", overlay), "overlay must set inset: 0"
    assert re.search(r"background:\s*rgba\(\s*0,\s*0,\s*0,\s*0?\.6\s*\)", overlay), (
        "overlay backdrop must stay rgba(0, 0, 0, 0.6)"
    )
    assert re.search(r"display:\s*flex", overlay), "overlay must be flex"
    assert re.search(r"align-items:\s*center", overlay), (
        "overlay must center vertically"
    )
    assert re.search(r"justify-content:\s*center", overlay), (
        "overlay must center horizontally"
    )
    assert re.search(r"z-index:\s*100", overlay), "overlay must keep z-index: 100"

    modal = _rule(css, ".profile-modal")
    assert modal, ".profile-modal rule must exist"
    assert re.search(r"background:\s*#fff", modal), "modal background must stay #fff"
    assert re.search(r"border-radius:\s*16px", modal), "modal radius must stay 16px"
    assert re.search(r"max-width:\s*400px", modal), "modal max-width must stay 400px"
    assert re.search(r"width:\s*90vw", modal), "modal width must stay 90vw"
    assert re.search(r"max-height:\s*85vh", modal), "modal max-height must stay 85vh"
    assert re.search(r"box-shadow:", modal), "modal must keep a box-shadow"
    assert re.search(r"position:\s*relative", modal), (
        "modal must stay position: relative"
    )
    assert "min(" in modal, ".profile-modal must use a min() width"
    assert re.search(r"max-width:\s*100%", modal), (
        ".profile-modal must cap at max-width: 100%"
    )

    photo = _rule(css, ".profile-photo")
    assert photo, ".profile-photo rule must exist"
    assert re.search(r"width:\s*100%", photo), "photo must span the modal"
    assert re.search(r"height:\s*280px", photo), "photo height must stay 280px"
    assert re.search(r"object-fit:\s*cover", photo), "photo must use object-fit: cover"

    h2 = _rule(css, ".profile-modal h2")
    assert h2, ".profile-modal h2 rule must exist"
    assert re.search(r"color:\s*#c0392b", h2), "modal heading must stay #c0392b"
    assert re.search(r"font-size:\s*1\.6rem", h2), "modal heading must stay 1.6rem"

    bio = _rule(css, ".profile-bio")
    assert bio, ".profile-bio rule must exist"
    assert re.search(r"line-height:\s*1\.5", bio), "bio must keep line-height: 1.5"

    close = _rule(css, ".profile-close")
    assert close, ".profile-close rule must exist"
    assert re.search(r"background:\s*#e74c3c", close), "close button must stay #e74c3c"
    assert re.search(r"border-radius:\s*50%", close), "close button must stay circular"

    hover = _rule(css, ".profile-close:hover")
    assert hover, ".profile-close:hover rule must exist"
    assert re.search(r"background:\s*#c0392b", hover), "close hover must stay #c0392b"


def test_match_overlay_css_rules():
    css = _read(MATCH_CSS)
    overlay = _rule(css, ".match-overlay")
    assert overlay, ".match-overlay rule must exist"
    assert re.search(r"position:\s*fixed", overlay), "overlay must be position: fixed"
    assert re.search(r"inset:\s*0", overlay), "overlay must set inset: 0"
    assert re.search(r"background:\s*rgba\(\s*0,\s*0,\s*0,\s*0\.65\s*\)", overlay), (
        "overlay backdrop must stay rgba(0, 0, 0, 0.65)"
    )
    assert re.search(r"display:\s*flex", overlay), "overlay must be flex"
    assert re.search(r"align-items:\s*center", overlay), (
        "overlay must center vertically"
    )
    assert re.search(r"justify-content:\s*center", overlay), (
        "overlay must center horizontally"
    )
    z = re.search(r"z-index:\s*(\d+)", overlay)
    assert z, "overlay must declare a numeric z-index"
    assert int(z.group(1)) >= 200, "overlay z-index must be >= 200"

    card = _rule(css, ".match-card")
    assert card, ".match-card rule must exist"
    assert "min(" in card, ".match-card must use a min() width"
    anim = re.search(r"animation:\s*([A-Za-z0-9_-]+)", card)
    assert anim, ".match-card must declare an entrance animation"
    name = anim.group(1)
    keyframes = re.search(
        r"@keyframes\s+" + re.escape(name) + r"\s*\{(.*?)\n\}", css, re.DOTALL
    )
    assert keyframes, f"@keyframes {name} must define the .match-card animation"
    body = keyframes.group(1)
    assert "transform" in body and "opacity" in body, (
        f"@keyframes {name} must animate transform and opacity"
    )
    assert re.search(r"from\s*\{[^}]*transform", body, re.DOTALL), (
        f"@keyframes {name} from block must set transform"
    )
    assert re.search(r"to\s*\{[^}]*opacity", body, re.DOTALL), (
        f"@keyframes {name} to block must set opacity"
    )

    photo = _rule(css, ".match-photo")
    assert photo, ".match-photo rule must exist"
    assert re.search(r"width:\s*100%", photo), ".match-photo must span the card"
    assert re.search(r"height:\s*260px", photo), ".match-photo height must stay 260px"
    assert re.search(r"object-fit:\s*cover", photo), (
        ".match-photo must use object-fit: cover"
    )

    h2 = _rule(css, ".match-card h2")
    assert h2, ".match-card h2 rule must exist"
    assert re.search(r"color:\s*#e74c3c", h2), ".match-card h2 must stay #e74c3c"
    assert re.search(r"font-size:\s*1\.8rem", h2), ".match-card h2 must stay 1.8rem"

    hover = _rule(css, ".match-close:hover")
    assert hover, ".match-close:hover rule must exist"
    assert re.search(r"background:\s*#c0392b", hover), (
        ".match-close:hover must stay #c0392b"
    )


def test_liked_horses_css_rules():
    css = _read(LIKED_CSS)
    nav = _rule(css, ".liked-nav-btn")
    assert nav, ".liked-nav-btn rule must exist"
    assert re.search(r"position:\s*fixed", nav), (
        ".liked-nav-btn must stay position: fixed"
    )

    grid = _rule(css, ".liked-grid")
    assert grid, ".liked-grid rule must exist"
    assert re.search(r"display:\s*grid", grid), ".liked-grid must stay display: grid"
    assert re.search(r"repeat\(\s*auto-fill", grid), (
        ".liked-grid must keep repeat(auto-fill, ...)"
    )
    assert "minmax(min(" in grid, ".liked-grid must use minmax(min(...), ...)"
    assert re.search(r"max-width:", grid), ".liked-grid must declare a max-width"

    item = _rule(css, ".liked-item")
    assert item, ".liked-item rule must exist"
    assert re.search(r"background:\s*#fff", item), (
        ".liked-item background must stay #fff"
    )
    assert re.search(r"border-radius:", item), ".liked-item must keep border-radius"
    assert re.search(r"padding:", item), ".liked-item must keep padding"
    assert re.search(r"box-shadow:", item), ".liked-item must keep box-shadow"
    assert re.search(r"text-align:\s*center", item), ".liked-item must stay centered"

    thumb = _rule(css, ".liked-thumb")
    assert thumb, ".liked-thumb rule must exist"
    assert re.search(r"width:\s*100%", thumb), ".liked-thumb must span the item"
    assert re.search(r"height:\s*100px", thumb), ".liked-thumb height must stay 100px"
    assert re.search(r"object-fit:\s*cover", thumb), (
        ".liked-thumb must use object-fit: cover"
    )
    assert re.search(r"border-radius:", thumb), ".liked-thumb must keep border-radius"

    paragraph = _rule(css, ".liked-item p")
    assert paragraph, ".liked-item p rule must exist"
    assert re.search(r"margin:", paragraph), ".liked-item p must keep margin"
    assert re.search(r"font-weight:\s*600", paragraph), (
        ".liked-item p must keep font-weight: 600"
    )

    empty = _rule(css, ".liked-empty")
    assert empty, ".liked-empty rule must exist"
    assert re.search(r"text-align:\s*center", empty), ".liked-empty must stay centered"
    assert re.search(r"padding:\s*24px", empty), ".liked-empty padding must stay 24px"


def test_buttons_declare_six_properties():
    for path, selector in (
        (SWIPE_CSS, ".reset-btn"),
        (MODAL_CSS, ".profile-close"),
        (MATCH_CSS, ".match-close"),
        (LIKED_CSS, ".liked-nav-btn"),
    ):
        rule = _rule(_read(path), selector)
        assert rule, f"{selector} rule must exist in {path.name}"
        for prop in (
            "background",
            "color",
            "border",
            "border-radius",
            "padding",
            "cursor",
        ):
            assert re.search(rf"(?m)^\s*{re.escape(prop)}:\s*[^;]+;", rule), (
                f"{selector} must explicitly declare {prop}"
            )


def test_component_css_uses_tokens_and_no_ad_hoc_hexes():
    for path in (SWIPE_CSS, MODAL_CSS, MATCH_CSS, LIKED_CSS):
        css = _read(path)
        assert css.count("var(--") >= 2, (
            f"{path.name} must reference at least two shared tokens"
        )
        hexes = set(re.findall(r"#[0-9a-fA-F]{3,8}\b", css))
        assert hexes <= PINNED_HEXES, (
            f"{path.name} contains ad-hoc hex colours: {sorted(hexes - PINNED_HEXES)}"
        )
        for bad in AD_HOC_HEXES:
            assert bad not in css, (
                f"{path.name} must not contain the ad-hoc colour {bad}"
            )


def test_css_formatting_one_declaration_per_line():
    for path in CSS_FILES:
        css = _read(path)
        for lineno, line in enumerate(css.splitlines(), 1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped == "}":
                assert line == "}" or line.startswith("  "), (
                    f"{path.name}:{lineno}: closing brace must be at column 0 "
                    "or indented inside a nested block"
                )
            elif stripped.endswith("{"):
                assert stripped.endswith("{"), (
                    f"{path.name}:{lineno}: rule opener must end with '{{'"
                )
            else:
                assert stripped.endswith(";"), (
                    f"{path.name}:{lineno}: declaration must end with ';' "
                    f"(one declaration per line): {line!r}"
                )


# ---------------------------------------------------------------------------
# AC4 — source and config files unchanged
# ---------------------------------------------------------------------------


def test_app_jsx_unchanged():
    src = _read(APP)
    assert "Horse Tinder Demo" in src, "src/App.jsx must keep 'Horse Tinder Demo'"
    assert "./data/horses" in src, "src/App.jsx must keep './data/horses'"
    assert re.search(
        r"import\s+CardDeck\s+from\s+['\"]\./components/CardDeck['\"]", src
    ), "src/App.jsx must keep the CardDeck import"
    assert "<CardDeck" in src, "src/App.jsx must keep rendering <CardDeck />"
    assert "horses.map(" not in src, "the placeholder list view must stay removed"
    assert re.search(r"export\s+default\s+function\s+App\s*\(\s*\)", src), (
        "App.jsx must keep export default function App()"
    )
    assert "<h1>Horse Tinder Demo</h1>" in src, (
        "src/App.jsx must keep its <h1>Horse Tinder Demo</h1> header"
    )
    assert (
        '<p className="tagline">{horses.length} horses looking for love</p>' in src
    ), "src/App.jsx must keep its tagline"


def test_card_deck_unchanged_wiring():
    src = _read(DECK)
    assert "import { useRef, useState } from 'react';" in src, (
        "CardDeck.jsx must keep its React import"
    )
    for name in ("LikedHorses", "MatchOverlay", "ProfileModal"):
        assert re.search(
            r"import\s+" + name + r"\s+from\s+['\"]\./" + name + r"['\"]", src
        ), f"CardDeck.jsx must keep the {name} import"
    assert "Math.random() < 0.33" in src, "CardDeck.jsx must keep the 33% match roll"
    assert "const SWIPE_THRESHOLD = 100;" in src, (
        "CardDeck.jsx must keep SWIPE_THRESHOLD = 100"
    )
    assert "Math.abs(deltaX.current) > SWIPE_THRESHOLD" in src, (
        "CardDeck.jsx must keep the swipe threshold comparison"
    )
    assert "animating === 'right' ? 'swipe-right' : 'swipe-left'" in src, (
        "CardDeck.jsx must keep the swipe animation class ternary"
    )
    assert "setTimeout(finishSwipe, 300)" in src, (
        "CardDeck.jsx must keep the 300ms finishSwipe timeout"
    )
    assert "deck.length === 0 && !leavingCard && !animating" in src, (
        "CardDeck.jsx must keep the isEmpty guard"
    )
    assert "cards remaining" in src, "CardDeck.jsx must keep the remaining counter"
    assert "Reset &amp; Shuffle" in src, (
        "CardDeck.jsx must keep the Reset & Shuffle label"
    )
    assert "Math.abs(deltaX.current) < 10" in src, (
        "CardDeck.jsx must keep the tap detection threshold"
    )
    assert "const [showLiked, setShowLiked] = useState(false);" in src, (
        "CardDeck.jsx must keep the showLiked state"
    )
    assert "setShowLiked((s) => !s)" in src, (
        "CardDeck.jsx must keep the liked nav toggle"
    )
    assert "Liked ({liked.length})" in src, (
        "CardDeck.jsx must keep the liked count label"
    )
    assert re.search(r"export\s+default\s+function\s+CardDeck\s*\(\s*\)", src), (
        "CardDeck.jsx must keep export default function CardDeck()"
    )


def test_component_export_signatures_unchanged():
    assert re.search(
        r"export\s+default\s+function\s+Card\s*\(\s*\{\s*horse\s*,\s*"
        r"zIndex\s*=\s*1\s*,\s*style\s*=\s*\{\s*\}\s*,\s*className\s*=\s*''\s*\}\s*\)",
        _read(CARD),
    ), "Card.jsx must keep its export signature"
    assert re.search(
        r"export\s+default\s+function\s+ProfileModal\s*\(\s*\{\s*horse\s*,\s*onClose\s*\}\s*\)",
        _read(MODAL),
    ), "ProfileModal.jsx must keep its export signature"
    assert re.search(
        r"export\s+default\s+function\s+MatchOverlay\s*\(\s*\{\s*horse\s*,\s*onClose\s*\}\s*\)",
        _read(MATCH),
    ), "MatchOverlay.jsx must keep its export signature"
    assert re.search(
        r"export\s+default\s+function\s+LikedHorses\s*\(\s*\{\s*horses\s*\}\s*\)",
        _read(LIKED),
    ), "LikedHorses.jsx must keep its export signature"


def test_card_jsx_structure_unchanged():
    src = _read(CARD)
    for marker in (
        "className={'card ' + className}",
        "<img src={horse.imageUrl} alt={horse.name} />",
        'className="card-info"',
        "<h2>{horse.name}</h2>",
        'className="breed"',
        'className="age"',
    ):
        assert marker in src, f"Card.jsx must keep {marker!r}"


def test_profile_modal_jsx_structure_unchanged():
    src = _read(MODAL)
    for marker in (
        "import './ProfileModal.css';",
        "if (!horse) return null;",
        'className="profile-overlay"',
        'className="profile-modal"',
        'className="profile-photo"',
        'className="profile-breed"',
        'className="profile-age"',
        'className="profile-bio"',
        'className="profile-close"',
    ):
        assert marker in src, f"ProfileModal.jsx must keep {marker!r}"


def test_match_overlay_jsx_structure_unchanged():
    src = _read(MATCH)
    for marker in (
        "import './MatchOverlay.css';",
        "if (!horse) return null;",
        'className="match-overlay"',
        'className="match-card"',
        "<h2>It's a Match!</h2>",
        'className="match-photo"',
        'className="match-name"',
        'className="match-close"',
    ):
        assert marker in src, f"MatchOverlay.jsx must keep {marker!r}"


def test_liked_horses_jsx_structure_unchanged():
    src = _read(LIKED)
    for marker in (
        "import './LikedHorses.css';",
        "if (!horses || horses.length === 0)",
        'className="liked-empty"',
        'className="liked-grid"',
        'className="liked-item"',
        'className="liked-thumb"',
        "<p>{horse.name}</p>",
    ):
        assert marker in src, f"LikedHorses.jsx must keep {marker!r}"


def test_main_jsx_unchanged():
    main = _read(MAIN)
    for marker in (
        "import React from 'react';",
        "import { createRoot } from 'react-dom/client';",
        "import App from './App.jsx'",
        "import './index.css'",
        "createRoot",
        "getElementById('root')",
        "<React.StrictMode>",
    ):
        assert marker in main, f"src/main.jsx must keep {marker!r}"


def test_horses_data_unchanged():
    data = _read(HORSES)
    assert "export const horses" in data, "horses.ts must keep the named export"
    assert "export default horses" in data, "horses.ts must keep the default export"
    assert len(re.findall(r"name:\s*'([^']+)'", data)) == 14, (
        "horses.ts must keep 14 named profiles"
    )
    assert len(re.findall(r"breed:\s*'[^']+'", data)) == 14, (
        "horses.ts must keep 14 breeds"
    )
    assert len(re.findall(r"age:\s*\d+", data)) == 14, "horses.ts must keep 14 ages"
    assert len(re.findall(r"bio:\s*'[^']+'", data)) == 14, "horses.ts must keep 14 bios"
    assert len(re.findall(r"""imageUrl:\s*["']""", data)) == 14, (
        "horses.ts must keep 14 image URLs"
    )


def test_package_json_unchanged():
    raw = _read(PACKAGE)
    assert '"name": "horse-tinder"' in raw, "package.json name must stay horse-tinder"
    assert '"version": "0.1.0"' in raw, "package.json version must stay 0.1.0"
    assert '"private": true' in raw, "package.json must stay private"
    assert '"type": "module"' in raw, "package.json must stay an ES module"
    assert '"dev": "vite"' in raw, "package.json dev script must stay 'vite'"
    assert '"build": "vite build"' in raw, (
        "package.json build script must stay 'vite build'"
    )
    assert '"preview": "vite preview"' in raw, (
        "package.json preview script must stay 'vite preview'"
    )
    assert '"test": "echo \'scaffold ok\'"' in raw, (
        "package.json must keep the npm test placeholder"
    )
    deps = _json_block(raw, "dependencies")
    assert deps, "package.json must keep a dependencies block"
    assert set(re.findall(r'"([^"]+)"\s*:', deps)) == {"react", "react-dom"}, (
        "dependencies must stay exactly react and react-dom"
    )
    devdeps = _json_block(raw, "devDependencies")
    assert devdeps, "package.json must keep a devDependencies block"
    assert set(re.findall(r'"([^"]+)"\s*:', devdeps)) == {
        "@vitejs/plugin-react",
        "vite",
    }, "devDependencies must stay exactly @vitejs/plugin-react and vite"


def test_vite_config_unchanged():
    cfg = _read(VITE_CONFIG)
    assert "import { defineConfig } from 'vite'" in cfg, (
        "vite.config.js must keep the defineConfig import"
    )
    assert "import react from '@vitejs/plugin-react'" in cfg, (
        "vite.config.js must keep the react plugin import"
    )
    assert "plugins: [react()]" in cfg, "vite.config.js must keep plugins: [react()]"


def test_deploy_workflow_unchanged():
    workflow = _read(WORKFLOW)
    for marker in (
        "name: Deploy to GitHub Pages",
        "branches: [main]",
        "runs-on: ubuntu-latest",
        "npm install",
        "npm run build",
        "actions/upload-pages-artifact@v3",
        "actions/deploy-pages@v4",
        "path: dist",
    ):
        assert marker in workflow, f"deploy.yml must keep {marker!r}"


# ---------------------------------------------------------------------------
# AC5 — spec digest, repo hygiene and purity
# ---------------------------------------------------------------------------


def test_project_spec_fixed_section_digest_unchanged():
    fixed = _fixed_section()
    assert len(fixed) == FIXED_LEN, (
        "the Fixed section of docs/project-spec.md changed length; it must be "
        "committed byte-for-byte unchanged"
    )
    assert _fnv1a_64(fixed.encode("utf-8")) == FIXED_FNV1A64, (
        "the Fixed section of docs/project-spec.md changed content; it must be "
        "committed byte-for-byte unchanged"
    )
    for marker in (
        "## Fixed",
        "### Goal",
        "#### 1. Scaffold & Horse Data",
        "Estimate: $5.0 · 3.0 hours",
    ):
        assert marker in fixed, (
            f"Fixed section of docs/project-spec.md lost marker {marker!r}"
        )
    assert _read(SPEC).startswith("# Horse Tinder Demo"), (
        "docs/project-spec.md must keep its title"
    )


def test_repo_hygiene_no_lockfile():
    assert not (ROOT / "package-lock.json").exists(), (
        "package-lock.json must not be created"
    )


def test_suite_is_purely_static():
    """The suite itself must not shell out, hit remote services or bypass tests."""
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
