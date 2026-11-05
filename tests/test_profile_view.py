"""Static acceptance tests for Milestone 3: Full Profile View.

Purely static analysis of committed source files (pathlib + re only).
No npm, no network, no skipping.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_ac1_modal_renders_all_fields():
    text = read("src/components/ProfileModal.jsx")
    for field in ("name", "breed", "age", "bio", "imageUrl"):
        assert re.search(r"horse\." + field + r"\b", text), (
            f"ProfileModal.jsx does not reference horse.{field}"
        )


def test_ac2_close_button():
    text = read("src/components/ProfileModal.jsx")
    pattern = (
        r"<button[^>]*onClick=\{[^}]*(onClose|close)[^}]*\}>[\s\S]{0,40}?(Close|✕)"
    )
    assert re.search(pattern, text), "No close button with onClick handler found"


def test_ac3_overlay_positioning():
    text = read("src/components/ProfileModal.css")
    overlay = re.search(r"\.profile-overlay\s*\{([^}]*)\}", text)
    assert overlay, ".profile-overlay rule missing in ProfileModal.css"
    body = overlay.group(1)
    assert "position: fixed" in body, ".profile-overlay must be position: fixed"
    assert "z-index" in body or "inset: 0" in body, (
        ".profile-overlay must have z-index or inset: 0"
    )
    modal = re.search(r"\.profile-modal\s*\{([^}]*)\}", text)
    assert modal, ".profile-modal rule missing in ProfileModal.css"
    modal_body = modal.group(1)
    assert "background" in modal_body, ".profile-modal must set a background"
    assert "border-radius" in modal_body, ".profile-modal must set border-radius"


def test_ac4_tap_detection_in_carddeck():
    text = read("src/components/CardDeck.jsx")
    assert re.search(r"<\s*(10|15|20)\b", text), (
        "No small-threshold tap-vs-swipe comparison in CardDeck.jsx"
    )
    assert re.search(r"setSelectedHorse\s*\(", text), (
        "No setSelectedHorse state setter in CardDeck.jsx"
    )
    assert re.search(r"import\s+ProfileModal\s+from", text), (
        "ProfileModal is not imported in CardDeck.jsx"
    )


def test_ac5_modal_rendered():
    text = read("src/components/CardDeck.jsx")
    assert re.search(r"<ProfileModal\b", text), (
        "<ProfileModal is not rendered in CardDeck.jsx"
    )
    assert re.search(r"<ProfileModal[^>]*horse=\{", text), (
        "ProfileModal missing horse prop"
    )
    assert re.search(
        r"<ProfileModal[\s\S]{0,120}onClose=\{[\s\S]{0,80}setSelectedHorse\(null\)",
        text,
    ), "ProfileModal missing onClose prop that clears selection"


def test_ac6_14_profiles_accessible():
    data = read("src/data/horses.ts")
    assert len(re.findall(r"id:\s*\d", data)) == 14, (
        "horses.ts must contain exactly 14 horse profiles"
    )
    text = read("src/components/CardDeck.jsx")
    assert re.search(r"from\s+'\.\./data/horses'", text), (
        "CardDeck.jsx must import horses from '../data/horses'"
    )
    assert re.search(r"setSelectedHorse\s*\(\s*(deck|visible)\[0\]", text), (
        "Selection must use deck[0] or visible[0] so all 14 profiles are reachable"
    )


def test_ac7_no_new_deps():
    text = read("package.json")
    block = re.search(r'"dependencies"\s*:\s*\{([^}]*)\}', text)
    assert block, "No dependencies block in package.json"
    deps = block.group(1)
    keys = re.findall(r'"([^"]+)"\s*:', deps)
    assert set(keys) == {"react", "react-dom"}, (
        f"Dependencies must be only react and react-dom, got {sorted(keys)}"
    )
    for forbidden in (
        "framer-motion",
        "react-modal",
        "@mui",
        "radix",
        "headless",
        "motion",
    ):
        assert forbidden not in deps, f"Forbidden dependency present: {forbidden}"


def test_ac8_spec_unchanged():
    text = read("docs/project-spec.md")
    start = text.find("## Fixed")
    end = text.find("## Living")
    assert start != -1 and end != -1, (
        "Spec must contain ## Fixed and ## Living sections"
    )
    fixed = text[start:end]
    pos = -1
    for heading in (
        "### Goal",
        "### Users",
        "### Milestones",
        "### Out of scope",
        "### Constraints",
        "### Latitude",
    ):
        idx = fixed.find(heading, pos + 1)
        assert idx != -1, f"Heading {heading} missing or out of order in Fixed section"
        assert fixed.find(heading, idx + 1) == -1, (
            f"Heading {heading} appears more than once"
        )
        pos = idx
