"""Supplementary static acceptance tests for Milestone 2 (stacked swipe deck).

Complements tests/test_swipe_deck.py by covering the gaps:

- AC1/AC2: SwipeDeck.css is imported by CardDeck.jsx so the keyframe classes
  are actually wired into the component.
- AC3: the counter element is rendered *above* the deck in the JSX tree.
- AC4: the deck and the reset handler both restore the FULL imported horses
  dataset (all 14), not a subset.
- AC5: swipe direction maps to the correct animation class ('right' ->
  swipe-right, 'left' -> swipe-left); the top card receives the class while
  animating; the animated card stays mounted (empty branch is gated by the
  combined isEmpty condition, never by deck.length alone).
- AC6: static build config (build script runs vite; vite config exists).
- AC7: App.jsx keeps 'Horse Tinder Demo' and './data/horses', renders
  <CardDeck />, and the placeholder list view is gone.
- AC8: no package-lock.json was created in the repository.

Purely static: file-content analysis only, no npm, no network, no git,
no pytest.skip.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
APP = SRC / "App.jsx"
APP_CSS = SRC / "App.css"
CARDDECK = SRC / "components" / "CardDeck.jsx"
CSS = SRC / "components" / "SwipeDeck.css"
PACKAGE = ROOT / "package.json"
VITE_CONFIG = ROOT / "vite.config.js"


def test_carddeck_wires_swipe_deck_css():
    """AC2: the component must actually import the stylesheet with keyframes."""
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(r"import\s+['\"]\./SwipeDeck\.css['\"]", src), (
        "CardDeck.jsx must import ./SwipeDeck.css"
    )
    assert CSS.is_file(), "src/components/SwipeDeck.css must exist"


def test_counter_rendered_above_deck():
    """AC3: counter with '{deck.length} cards remaining' precedes the deck."""
    src = CARDDECK.read_text(encoding="utf-8")
    counter = re.search(r'<div\s+className="counter">\s*\{deck\.length\}\s+cards remaining', src)
    assert counter, "counter must render {deck.length} cards remaining"
    assert src.find("card-deck") > counter.start(), (
        "counter must be rendered above the .card-deck container"
    )


def test_deck_initialized_from_full_horses_dataset():
    """AC4: initial deck is the shuffled full 14-horse dataset."""
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(
        r"import\s+horses\s+from\s+['\"]\.\./data/horses['\"]", src
    ), "CardDeck must import the horses dataset"
    assert re.search(r"useState\(\s*\(\)\s*=>\s*shuffleDeck\(\s*horses\s*\)\s*\)", src), (
        "initial deck must be shuffleDeck(horses) — all 14 horses, shuffled"
    )


def test_reset_restores_all_14_horses_shuffled():
    """AC4: 'Reset & Shuffle' rebuilds the deck from the full dataset."""
    src = CARDDECK.read_text(encoding="utf-8")
    reset = re.search(r"handleReset\s*=\s*\(\)\s*=>\s*\{(.*?)\n\s*\};", src, re.DOTALL)
    assert reset, "handleReset must be defined"
    body = reset.group(1)
    assert re.search(r"setDeck\(\s*shuffleDeck\(\s*horses\s*\)\s*\)", body), (
        "reset must restore the full horses list in a new shuffled order"
    )
    assert 'onClick={handleReset}' in src, "reset button must call handleReset"
    assert re.search(r"Reset\s*&amp;\s*Shuffle", src), "button label must be 'Reset & Shuffle'"
    # The dataset really has 14 horses for the reset to restore.
    data = (SRC / "data" / "horses.ts").read_text(encoding="utf-8")
    assert len(re.findall(r"^\s*id:\s*\d+\s*,\s*$", data, re.MULTILINE)) == 14


def test_direction_maps_to_animation_class():
    """AC5: right swipe -> swipe-right class, left swipe -> swipe-left class."""
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(r"deltaX\.current\s*>\s*0\s*\?\s*'right'\s*:\s*'left'", src), (
        "swipe direction must be derived from the sign of the pointer delta"
    )
    assert re.search(
        r"animating\s*===\s*'right'\s*\?\s*'swipe-right'\s*:\s*'swipe-left'", src
    ), "animating state must select the matching swipe animation class"
    # The class is applied to the TOP card (index 0) only.
    assert re.search(r"i\s*===\s*0\s*&&\s*animating", src), (
        "only the top card may receive the swipe animation class"
    )


def test_leaving_card_stays_mounted_until_animation_done():
    """AC5 regression: last swiped card must play its slide-and-fade.

    The empty branch must be gated by the combined condition (deck.length
    === 0 AND no leavingCard AND no animating), never by deck.length alone,
    and triggerSwipe must keep the card mounted while it animates out.
    """
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(
        r"deck\.length\s*===\s*0\s*&&\s*!leavingCard\s*&&\s*!animating", src
    ), "isEmpty must be deck.length === 0 && !leavingCard && !animating"
    assert re.search(r"\{isEmpty\s*\?", src), (
        "render must branch on the combined isEmpty flag, not on deck.length alone"
    )
    trig = re.search(r"triggerSwipe\s*=\s*\(direction\)\s*=>\s*\{(.*?)\n\s*\};", src, re.DOTALL)
    assert trig, "triggerSwipe must be defined"
    body = trig.group(1)
    assert "setLeavingCard(deck[0])" in body, "triggerSwipe must track the leaving card"
    assert "setAnimating(direction)" in body, "triggerSwipe must set the animating direction"
    assert "slice(1)" not in body, (
        "triggerSwipe must not remove the card immediately (animation would be cut off)"
    )
    # Re-entrancy guard: no new swipe while one is animating.
    assert re.search(r"if\s*\(\s*animating\s*!==\s*null\s*\)\s*return", body), (
        "triggerSwipe must ignore swipes while an animation is running"
    )


def test_app_renders_carddeck_and_keeps_required_strings():
    """AC7: App.jsx keeps 'Horse Tinder Demo' + './data/horses', uses CardDeck,
    and the old placeholder list view is removed."""
    app = APP.read_text(encoding="utf-8")
    assert "Horse Tinder Demo" in app, "App.jsx must keep the 'Horse Tinder Demo' title"
    assert "./data/horses" in app, "App.jsx must keep importing from './data/horses'"
    assert re.search(
        r"import\s+CardDeck\s+from\s+['\"]\./components/CardDeck['\"]", app
    ), "App.jsx must import CardDeck"
    assert "<CardDeck" in app, "App.jsx must render <CardDeck />"
    assert "horses.map(" not in app, "placeholder list view must be removed from App.jsx"


def test_app_css_deck_layout():
    """Task step 5: .app container styles for the full-height centered deck layout."""
    css = APP_CSS.read_text(encoding="utf-8")
    m = re.search(r"\.app\s*\{(.*?)\n\}", css, re.DOTALL)
    assert m, "App.css must define an .app container rule"
    rule = m.group(1)
    assert re.search(r"(min-)?height:\s*100vh", rule), ".app must span the viewport height"
    assert "center" in rule, ".app must center the deck"


def test_static_build_config():
    """AC6 (static evidence): `npm run build` maps to vite and config exists."""
    pkg = json.loads(PACKAGE.read_text(encoding="utf-8"))
    assert pkg["scripts"]["build"] == "vite build", "build script must run vite build"
    assert VITE_CONFIG.is_file(), "vite.config.js must exist"
    cfg = VITE_CONFIG.read_text(encoding="utf-8")
    assert "react()" in cfg, "vite config must use the react plugin"


def test_no_package_lock_created():
    """AC8: package-lock.json must not exist in the repository."""
    assert not (ROOT / "package-lock.json").exists(), (
        "package-lock.json must not be created"
    )
