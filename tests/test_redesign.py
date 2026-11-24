"""Static acceptance tests for the Horse Tinder visual redesign.

Maps to the acceptance criteria of the issue "Visual redesign of Horse
Tinder":

- AC1: swarmforge.project.yml gains a `preview:` section that runs the Vite
       dev server on 127.0.0.1:5173 and exposes the "/" page, while keeping
       the sandbox/install/test commands.
- AC2: vite.config.js sets the GitHub Pages base path to '/horse_tinder/'
       without overriding the dev-server port.
- AC3: the card is a full-bleed photo card with rounded corners, a soft
       shadow and a gradient name/age overlay.
- AC4: CardDeck.jsx renders big round reject/accept buttons that call
       triggerSwipe('left') / triggerSwipe('right').
- AC5: the design system uses one named font, warm palette tokens, and the
       swipe keyframes keep the 120vw slide plus a tilt; dragging the card
       applies a rotate transform.
- AC6: the app shell has a clean top bar and the liked counter is preserved.
- AC7: the responsive layout keeps both pinned media queries and fluid deck
       sizing so it works at 375px and 1280px.
- AC8: package.json keeps its dependency/script invariants and no lockfile
       is committed.

Purely static: file-content analysis only, no shelling out, no remote
services, no conditional bypasses.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "swarmforge.project.yml"
VITE_CONFIG = ROOT / "vite.config.js"
INDEX_CSS = ROOT / "src" / "index.css"
APP_CSS = ROOT / "src" / "App.css"
APP = ROOT / "src" / "App.jsx"
SWIPE_CSS = ROOT / "src" / "components" / "SwipeDeck.css"
LIKED_CSS = ROOT / "src" / "components" / "LikedHorses.css"
DECK = ROOT / "src" / "components" / "CardDeck.jsx"
CARD = ROOT / "src" / "components" / "Card.jsx"
PACKAGE = ROOT / "package.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rule(css: str, selector: str) -> str:
    """Body of a top-level CSS rule for `selector` (exact match), or ''."""
    m = re.search(
        r"^" + re.escape(selector) + r"\s*\{(.*?)\n\}",
        css,
        re.DOTALL | re.MULTILINE,
    )
    return m.group(1) if m else ""


# ---------------------------------------------------------------------------
# AC1 — preview section for the designer's screenshots
# ---------------------------------------------------------------------------


def test_ac1_preview_section_configured():
    text = _read(PROJECT)
    assert "preview:" in text, "swarmforge.project.yml must add a preview: section"
    assert re.search(
        r"command:\s*['\"]?npm run dev -- --host 127\.0\.0\.1 --port 5173['\"]?",
        text,
    ), "preview.command must run the Vite dev server on 127.0.0.1:5173"
    assert re.search(r"^\s*port:\s*['\"]?5173['\"]?\s*$", text, re.MULTILINE), (
        "preview.port must be 5173"
    )
    pages_list = re.search(r"pages:\s*\[([^\]]*)\]", text)
    pages_block = re.search(r"pages:\s*\n((?:\s*-\s*[^\n]+\n)+)", text)
    assert (pages_list and "/" in pages_list.group(1)) or (
        pages_block and re.search(r"-\s*['\"]?/['\"]?", pages_block.group(1))
    ), "preview.pages must contain the '/' page"
    for key in ("sandbox_image:", "install_command:", "test_command:"):
        assert re.search(r"^\s*" + re.escape(key), text, re.MULTILINE), (
            f"swarmforge.project.yml must keep the {key} line"
        )


# ---------------------------------------------------------------------------
# AC2 — GitHub Pages base path without changing the dev port
# ---------------------------------------------------------------------------


def test_ac2_github_pages_base_path():
    cfg = _read(VITE_CONFIG)
    assert re.search(r"base:\s*['\"]/horse_tinder/['\"]", cfg), (
        "vite.config.js must set base: '/horse_tinder/'"
    )
    assert "import { defineConfig } from 'vite'" in cfg, (
        "vite.config.js must keep the defineConfig import"
    )
    assert "import react from '@vitejs/plugin-react'" in cfg, (
        "vite.config.js must keep the react plugin import"
    )
    assert "plugins: [react()]" in cfg, "vite.config.js must keep plugins: [react()]"
    assert not re.search(r"\bport\b", cfg), (
        "vite.config.js must not override the 5173 dev-server port"
    )


# ---------------------------------------------------------------------------
# AC3 — full-bleed photo card with rounded corners, shadow and gradient
# ---------------------------------------------------------------------------


def test_ac3_full_bleed_card_visuals():
    css = _read(SWIPE_CSS)
    card = _rule(css, ".card")
    assert card, ".card rule must exist in SwipeDeck.css"
    assert re.search(r"border-radius:\s*var\(--", card), (
        ".card must use a tokenised border-radius"
    )
    assert re.search(r"box-shadow:\s*[^;]+;", card), ".card must keep a soft shadow"

    info = _rule(css, ".card-info")
    assert info, ".card-info rule must exist in SwipeDeck.css"
    assert re.search(r"background:\s*linear-gradient\(", info), (
        ".card-info must use a linear-gradient overlay"
    )

    card_jsx = _read(CARD)
    assert re.search(
        r"<img\s+src=\{horse\.imageUrl\}\s+alt=\{horse\.name\}", card_jsx
    ), "Card.jsx must keep the full-bleed horse image"
    img_rule = re.search(r"\.card[^{]*\bimg\b[^{]*\{([^}]*)\}", css, re.DOTALL)
    assert img_rule, "SwipeDeck.css must style the card image"
    img_body = img_rule.group(1)
    assert re.search(r"width:\s*100%", img_body), "the card image must span the card"
    assert re.search(r"height:\s*100%", img_body), "the card image must fill the card"
    assert re.search(r"object-fit:\s*cover", img_body), (
        "the card image must use object-fit: cover"
    )


# ---------------------------------------------------------------------------
# AC4 — big round reject/accept action buttons
# ---------------------------------------------------------------------------


def test_ac4_round_action_buttons():
    src = _read(DECK)
    left = re.search(
        r"<button[^>]*onClick=\{\s*\(\s*\)\s*=>\s*triggerSwipe\(\s*['\"]left['\"]\s*\)\s*\}",
        src,
    )
    right = re.search(
        r"<button[^>]*onClick=\{\s*\(\s*\)\s*=>\s*triggerSwipe\(\s*['\"]right['\"]\s*\)\s*\}",
        src,
    )
    assert left, "CardDeck.jsx must render a reject button calling triggerSwipe('left')"
    assert right, (
        "CardDeck.jsx must render an accept button calling triggerSwipe('right')"
    )

    css = _read(SWIPE_CSS)
    btn = _rule(css, ".swipe-btn")
    assert btn, ".swipe-btn rule must exist in SwipeDeck.css"
    width = re.search(r"width:\s*([^;]+);", btn)
    height = re.search(r"height:\s*([^;]+);", btn)
    assert width and height, ".swipe-btn must declare both width and height"
    assert width.group(1).strip() == height.group(1).strip(), (
        ".swipe-btn must be square (width == height)"
    )
    assert re.search(r"border-radius:\s*50%", btn), (
        ".swipe-btn must be round (border-radius: 50%)"
    )


# ---------------------------------------------------------------------------
# AC5 — warm design system, named font, swipe tilt
# ---------------------------------------------------------------------------


def test_ac5_warm_palette_and_named_font():
    css = _read(INDEX_CSS)
    root = _rule(css, ":root")
    assert root, "src/index.css must define a :root block"
    family = re.search(r"font-family:\s*([^;]+);", root)
    assert family, ":root must declare a font-family stack"
    first = family.group(1).split(",")[0].strip().strip("'\"")
    generic = {
        "system-ui",
        "-apple-system",
        "sans-serif",
        "serif",
        "monospace",
        "inherit",
    }
    assert first and first.lower() not in generic, (
        ":root font-family must name the chosen font first"
    )
    assert re.search(r"--[a-z-]*(reject|nope|dislike)[a-z-]*\s*:", root), (
        ":root must define a warm reject-button token"
    )
    assert re.search(r"--[a-z-]*(accept|like|heart)[a-z-]*\s*:", root), (
        ":root must define a warm accept-button token"
    )
    assert re.search(r"--[a-z-]*(topbar|top-bar|header)[a-z-]*\s*:", root), (
        ":root must define a top-bar background token"
    )


def test_ac5_swipe_tilt_and_drag_rotation():
    css = _read(SWIPE_CSS)
    for name in ("slideRightFade", "slideLeftFade"):
        block = re.search(r"@keyframes\s+" + name + r"\s*\{(.*?)\n\}", css, re.DOTALL)
        assert block, f"@keyframes {name} must exist"
        body = block.group(1)
        assert re.search(r"translateX\([^)]*120vw", body), (
            f"{name} must slide the card fully off-screen with 120vw"
        )
        assert "rotate(" in body, f"{name} must add a slight tilt"

    deck = _read(DECK)
    assert re.search(r"rotate\([^)]*(deltaX|drag|offset|tilt)", deck) or re.search(
        r"(deltaX|drag|offset|tilt)[^;]{0,200}rotate\(", deck
    ), "CardDeck.jsx must apply a rotate transform tied to the drag state"


# ---------------------------------------------------------------------------
# AC6 — clean top bar and preserved liked counter
# ---------------------------------------------------------------------------


def test_ac6_top_bar_and_liked_counter():
    app = _read(APP)
    app_css = _read(APP_CSS)
    header = re.search(
        r"<header[^>]*className=\{?['\"][^'\"]*(topbar|top-bar|app-header)",
        app,
    )
    rule = (
        _rule(app_css, ".topbar")
        or _rule(app_css, ".top-bar")
        or _rule(app_css, ".app-header")
    )
    assert header or rule, (
        "App.jsx must render a top bar header or App.css must style .topbar/.app-header"
    )

    deck = _read(DECK)
    assert re.search(r'<button[^>]*className="liked-nav-btn"', deck), (
        "CardDeck.jsx must keep the liked-nav-btn counter"
    )
    assert "Liked ({liked.length})" in deck, (
        "CardDeck.jsx must keep the Liked ({liked.length}) label"
    )


def test_ac6_liked_counter_docked_into_topbar():
    """The Liked counter must sit inside the fixed top-bar band.

    The counter is rendered by CardDeck.jsx as a fixed-position button, so it
    only reads as part of the top bar when it is pinned near the top-right
    corner, stacks above the bar itself, and the bar reserves horizontal room
    for it instead of letting the title run underneath.
    """
    liked_css = _read(LIKED_CSS)
    app_css = _read(APP_CSS)

    counter = _rule(liked_css, ".liked-nav-btn")
    assert counter, f".liked-nav-btn rule must exist in {LIKED_CSS.relative_to(ROOT)}"
    assert re.search(r"position:\s*fixed", counter), (
        ".liked-nav-btn must be position: fixed so it docks into the top bar"
    )

    def _px(body: str, prop: str) -> float:
        m = re.search(r"(?<![\w-])" + prop + r":\s*(-?\d+(?:\.\d+)?)px", body)
        assert m, f".liked-nav-btn must declare a px {prop} offset"
        return float(m.group(1))

    top = _px(counter, "top")
    right = _px(counter, "right")
    assert top <= 24, f".liked-nav-btn top must be <= 24px, got {top}px"
    assert right <= 24, f".liked-nav-btn right must be <= 24px, got {right}px"

    topbar = _rule(app_css, ".topbar")
    assert topbar, f".topbar rule must exist in {APP_CSS.relative_to(ROOT)}"

    def _z_index(body: str, selector: str) -> int:
        m = re.search(r"z-index:\s*(-?\d+)", body)
        assert m, f"{selector} must declare a numeric z-index"
        return int(m.group(1))

    counter_z = _z_index(counter, ".liked-nav-btn")
    topbar_z = _z_index(topbar, ".topbar")
    assert counter_z >= topbar_z, (
        f".liked-nav-btn z-index ({counter_z}) must be >= the .topbar "
        f"z-index ({topbar_z}) so the counter stays visible in the bar"
    )

    reserve = re.search(r"(?<![\w-])padding-right:\s*([^;]+);", topbar)
    assert reserve, (
        ".topbar must declare a standalone padding-right reserving room for the "
        "Liked counter (a padding shorthand is not enough)"
    )
    rems = [float(v) for v in re.findall(r"(\d+(?:\.\d+)?)rem", reserve.group(1))]
    assert rems and max(rems) >= 7, (
        ".topbar padding-right must reserve at least 7rem for the Liked counter, "
        f"got {reserve.group(1).strip()}"
    )


# ---------------------------------------------------------------------------
# AC7 — responsive layout at 375px and 1280px
# ---------------------------------------------------------------------------


def test_ac7_responsive_layout():
    app_css = _read(APP_CSS)
    for query in ("@media (max-width: 480px)", "@media (min-width: 1024px)"):
        assert query in app_css, f"App.css must keep the literal {query}"
    assert re.search(r"min\(|clamp\(|vw", app_css), (
        "App.css must use fluid sizing for the responsive shell"
    )

    deck = _rule(_read(SWIPE_CSS), ".card-deck")
    assert deck, ".card-deck rule must exist"
    assert "min(" in deck, ".card-deck must use a min() width"
    assert "vw" in deck, ".card-deck must use viewport-relative sizing"


# ---------------------------------------------------------------------------
# AC8 — package invariants and no lockfile
# ---------------------------------------------------------------------------


def test_ac8_package_invariants_and_no_lockfile():
    raw = _read(PACKAGE)
    assert '"dev": "vite"' in raw, "package.json dev script must stay 'vite'"
    deps = re.search(r'"dependencies"\s*:\s*\{(.*?)\}', raw, re.DOTALL)
    assert deps, "package.json must keep a dependencies block"
    keys = set(re.findall(r'"([^"]+)"\s*:', deps.group(1)))
    assert keys == {"react", "react-dom"}, (
        f"dependencies must stay exactly react and react-dom, got {sorted(keys)}"
    )
    assert not (ROOT / "package-lock.json").exists(), (
        "package-lock.json must not be created"
    )


# ---------------------------------------------------------------------------
# Purity guard — this suite stays purely static
# ---------------------------------------------------------------------------


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
