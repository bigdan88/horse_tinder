"""Acceptance tests for the Milestone 2 swipe deck UI.

Maps to the acceptance criteria of the issue "Implement stacked swipe deck
with gestures, animations, counter, and reset/shuffle".  Everything here is
purely static: file-content analysis only, no network, no npm, no git
subprocess, no pytest.skip.

- AC1: CardDeck.jsx handles onPointerDown/onPointerMove/onPointerUp with a
       pixel threshold for left/right swipe detection
- AC2: SwipeDeck.css contains @keyframes slideRightFade/slideLeftFade with
       translateX + opacity transitions, bound to .card.swipe-* via
       `animation ... 300ms ... forwards`
- AC3: a visible counter renders the number of remaining cards
- AC4: when the deck is empty a 'Reset & Shuffle' button appears and
       restores all 14 horses in Fisher-Yates shuffled order
- AC5 (regression for the previous run's failure): the empty-state
       conditional is guarded by !leavingCard/!animating so the last card
       finishes its exit animation, and deck removal happens from the
       animation-end/timeout path, not unconditionally on pointerup
- AC6: Card.jsx renders a single horse card (image, name, breed, age)
- AC7: no new npm dependencies were added
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDDECK = ROOT / "src" / "components" / "CardDeck.jsx"
CARD = ROOT / "src" / "components" / "Card.jsx"
CSS = ROOT / "src" / "components" / "SwipeDeck.css"
PACKAGE = ROOT / "package.json"


def test_carddeck_exists_and_has_pointer_handlers():
    assert CARDDECK.is_file(), "src/components/CardDeck.jsx must exist"
    src = CARDDECK.read_text(encoding="utf-8")
    for handler in ("onPointerDown", "onPointerMove", "onPointerUp"):
        assert handler in src, f"CardDeck.jsx must wire {handler}"


def test_swipe_threshold():
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(
        r"(?:SWIPE_THRESHOLD|threshold)\D{0,30}100", src, re.IGNORECASE
    ), "a numeric swipe threshold of 100 px must be defined"
    assert "Math.abs" in src, "swipe decision must compare |delta| against the threshold"


def test_directional_swipe_classes():
    src = CARDDECK.read_text(encoding="utf-8")
    assert "swipe-right" in src, "CardDeck.jsx must apply the 'swipe-right' class"
    assert "swipe-left" in src, "CardDeck.jsx must apply the 'swipe-left' class"


def test_css_keyframes():
    css = CSS.read_text(encoding="utf-8")
    for name in ("slideRightFade", "slideLeftFade"):
        m = re.search(r"@keyframes\s+" + name + r"\s*\{(.*?)\n\}", css, re.DOTALL)
        assert m, f"SwipeDeck.css must define @keyframes {name}"
        block = m.group(1)
        assert "translateX" in block, f"{name} must animate translateX"
        assert "opacity" in block, f"{name} must animate opacity"
        assert "120vw" in block, f"{name} must slide the card fully off-screen (120vw)"
    for cls in ("swipe-right", "swipe-left"):
        m = re.search(r"\.card\." + cls + r"\s*\{(.*?)\n\}", css, re.DOTALL)
        assert m, f"SwipeDeck.css must style .card.{cls}"
        rule = m.group(1)
        assert "animation" in rule, f".card.{cls} must use the animation property"
        assert "300ms" in rule, f".card.{cls} animation must last 300ms"
        assert "forwards" in rule, f".card.{cls} animation must use forwards fill"


def test_counter_rendered():
    src = CARDDECK.read_text(encoding="utf-8")
    assert "deck.length" in src, "counter must read deck.length"
    assert "cards remaining" in src, "counter must render 'cards remaining'"


def test_reset_button_when_empty_and_last_card_animation_regression():
    src = CARDDECK.read_text(encoding="utf-8")
    assert "Reset" in src and "Shuffle" in src, "'Reset & Shuffle' button must exist"
    assert "reset-btn" in src, "reset button must be styled via .reset-btn"

    # Regression for the previous run's failure: the empty state must not
    # unmount the deck while the last card is still animating out.
    m = re.search(r"=\s*deck\.length\s*===\s*0(.{0,120})", src, re.DOTALL)
    assert m, "empty-state condition must start with deck.length === 0"
    cond = m.group(1)
    assert "!leavingCard" in cond or "!animating" in cond, (
        "empty-state condition must also guard on !leavingCard / !animating"
    )

    # Deck removal must be gated on the animation end / 300ms timeout path.
    assert re.search(r"setTimeout\s*\(\s*\w+,\s*300\s*\)", src), (
        "a 300ms setTimeout must schedule the post-animation cleanup"
    )
    assert "onAnimationEnd" in src, "deck must also finish the swipe on onAnimationEnd"
    assert re.search(r"slice\(1\)", src), "removal must drop the top card via slice(1)"
    # Removal is NOT done unconditionally inside the pointerup handler.
    up = re.search(r"handlePointerUp\s*=\s*\(\)\s*=>\s*\{(.*?)\n\s*\};", src, re.DOTALL)
    assert up, "handlePointerUp must be defined"
    assert "slice(1)" not in up.group(1), (
        "pointerup must only trigger the swipe, not remove the card directly"
    )


def test_fisher_yates_shuffle():
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(r"Math\.random\(\)\s*\*\s*\(i\s*\+\s*1\)", src), (
        "shuffle must use the Fisher-Yates pattern Math.random() * (i + 1)"
    )
    assert re.search(r"useState\(\s*\(\)\s*=>\s*shuffle", src), (
        "initial deck state must be shuffled"
    )
    reset = re.search(r"handleReset\s*=\s*\(\)\s*=>\s*\{(.*?)\n\s*\};", src, re.DOTALL)
    assert reset, "a reset handler must exist"
    assert "shuffle" in reset.group(1), "reset handler must reshuffle the horses"


def test_card_component():
    src = CARD.read_text(encoding="utf-8")
    assert re.search(r"export default function Card", src), "Card.jsx must default-export Card"
    assert "horse.imageUrl" in src, "Card must render horse.imageUrl"
    assert "<img" in src, "Card must render an <img> element"
    for field in ("horse.name", "horse.breed", "horse.age"):
        assert field in src, f"Card must display {field}"


def test_no_new_dependencies():
    pkg = json.loads(PACKAGE.read_text(encoding="utf-8"))
    deps = set(pkg.get("dependencies", {}))
    devdeps = set(pkg.get("devDependencies", {}))
    assert deps == {"react", "react-dom"}, f"unexpected dependencies: {deps}"
    assert devdeps == {"@vitejs/plugin-react", "vite"}, f"unexpected devDependencies: {devdeps}"
