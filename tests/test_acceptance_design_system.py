"""Supplementary acceptance tests for "Visual redesign of Horse Tinder".

Complements tests/test_redesign.py and tests/test_acceptance_redesign_visual.py
by pinning the exact numbers and names the issue wording demands but the
existing suites leave loose:

- AC4: the round ✕/♥ buttons must be 64px (not merely square) and must carry
  the .swipe-btn class that the 64px/50% rule styles.
- AC5: the named font must be Poppins, linked in index.html, and first in the
  :root stack; the card-info gradient must use the tokenised warm overlay.
- AC6: the top bar must paint itself with the warm --topbar-bg token.
- AC7: .card-deck must use exactly min(340px, 90vw).

Purely static: file-content analysis only — no shelling out, no network, no
conditional skips (same discipline as tests/test_redesign.py).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT / "index.html"
INDEX_CSS = ROOT / "src" / "index.css"
APP_CSS = ROOT / "src" / "App.css"
SWIPE_CSS = ROOT / "src" / "components" / "SwipeDeck.css"
DECK = ROOT / "src" / "components" / "CardDeck.jsx"


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
# AC5 — Poppins: linked in index.html and first in the :root stack
# ---------------------------------------------------------------------------


def test_ac5_poppins_linked_in_index_html():
    html = _read(INDEX_HTML)
    links = re.findall(r"<link\b[^>]*>", html, re.DOTALL)
    stylesheet_links = [tag for tag in links if 'rel="stylesheet"' in tag]
    assert any(
        re.search(r"fonts\.googleapis\.com/[^\"']*family=Poppins", tag)
        for tag in stylesheet_links
    ), "index.html must link the Poppins Google Fonts stylesheet"
    assert any("fonts.gstatic.com" in tag for tag in links), (
        "index.html should preconnect to fonts.gstatic.com so the font loads"
    )


def test_ac5_poppins_first_in_root_font_stack():
    root = _rule(_read(INDEX_CSS), ":root")
    assert root, "src/index.css must define a :root block"
    family = re.search(r"font-family:\s*([^;]+);", root)
    assert family, ":root must declare a font-family stack"
    first = family.group(1).split(",")[0].strip().strip("'\"")
    assert first == "Poppins", (
        f"the :root font stack must start with Poppins, got {first!r}"
    )


def test_ac5_card_info_uses_tokenised_warm_gradient():
    index_css = _read(INDEX_CSS)
    assert re.search(r"--card-gradient\s*:\s*rgba\(", index_css), (
        ":root must define a --card-gradient overlay token"
    )
    info = _rule(_read(SWIPE_CSS), ".card-info")
    assert info, ".card-info rule must exist in SwipeDeck.css"
    assert re.search(
        r"background:\s*linear-gradient\(\s*to top\s*,\s*var\(--card-gradient\)\s*,\s*transparent\s*\)",
        info,
    ), ".card-info must fade from the warm --card-gradient token at the bottom"


# ---------------------------------------------------------------------------
# AC4 — the ✕/♥ buttons are the styled 64px round ones
# ---------------------------------------------------------------------------


def test_ac4_swipe_btn_is_64px_round():
    btn = _rule(_read(SWIPE_CSS), ".swipe-btn")
    assert btn, ".swipe-btn rule must exist in SwipeDeck.css"
    assert re.search(r"width:\s*64px\s*;", btn), ".swipe-btn must be 64px wide"
    assert re.search(r"height:\s*64px\s*;", btn), ".swipe-btn must be 64px tall"
    assert re.search(r"border-radius:\s*50%\s*;", btn), (
        ".swipe-btn must be border-radius: 50%"
    )


def test_ac4_glyph_buttons_carry_swipe_btn_class():
    src = _read(DECK)
    assert re.search(r"className=\"swipe-btn\s+swipe-btn-reject\"", src), (
        "the ✕ button must use the swipe-btn swipe-btn-reject classes"
    )
    assert re.search(r"className=\"swipe-btn\s+swipe-btn-accept\"", src), (
        "the ♥ button must use the swipe-btn swipe-btn-accept classes"
    )
    css = _read(SWIPE_CSS)
    assert _rule(css, ".swipe-btn-reject"), ".swipe-btn-reject rule must exist"
    assert _rule(css, ".swipe-btn-accept"), ".swipe-btn-accept rule must exist"


# ---------------------------------------------------------------------------
# AC6 — the top bar is painted with the warm palette token
# ---------------------------------------------------------------------------


def test_ac6_topbar_uses_warm_palette_token():
    topbar = _rule(_read(APP_CSS), ".topbar")
    assert topbar, ".topbar rule must exist in App.css"
    assert re.search(r"background:\s*var\(--topbar-bg\)", topbar), (
        ".topbar must use the --topbar-bg warm palette token"
    )
    assert re.search(r"position:\s*fixed", topbar), "the top bar must be fixed per AC6"


# ---------------------------------------------------------------------------
# AC7 — .card-deck uses exactly min(340px, 90vw)
# ---------------------------------------------------------------------------


def test_ac7_card_deck_uses_min_340px_90vw():
    deck = _rule(_read(SWIPE_CSS), ".card-deck")
    assert deck, ".card-deck rule must exist in SwipeDeck.css"
    assert re.search(r"width:\s*min\(\s*340px\s*,\s*90vw\s*\)", deck), (
        ".card-deck must use width: min(340px, 90vw)"
    )
