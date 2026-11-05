"""Acceptance tests for Milestone 3: tap-to-expand full profile modal overlay.

Maps to the acceptance criteria of the issue
"Implement tap-to-expand full profile modal overlay":

- AC1: src/components/ProfileModal.jsx exists and default-exports
       ProfileModal({ horse, onClose }) rendering the exact structure the
       issue mandates (overlay > modal > img/h2/breed/age/bio/close button),
       returning null when no horse is selected, and importing its CSS.
- AC2: src/components/ProfileModal.css exists with .profile-overlay
       (fixed, inset 0, dimmed backdrop, flex centering, z-index 100),
       .profile-modal (white rounded card, max-width 400px, 90vw, 85vh,
       scrollable, relative, shadow), .profile-photo, .profile-modal h2,
       .profile-breed, .profile-age, .profile-bio, .profile-close
       (absolute top-right red circle) and .profile-close:hover.
- AC3: CardDeck.jsx detects a tap: new `selectedHorse` state and, inside
       handlePointerUp, the tap branch (|deltaX| < 10, not animating,
       deck non-empty) sets selectedHorse to the top card — and only in the
       non-swipe branch, so swipes never open the modal.
- AC4: CardDeck.jsx imports ProfileModal and renders
       <ProfileModal horse={selectedHorse} onClose={() => setSelectedHorse(null)} />
       at the end of the returned JSX, outside the deck/empty-state branch.
- AC7 (partial, regression): the modal wiring does not disturb the existing
       swipe threshold / animation / counter / reset code paths.
- AC8 (partial): .gitignore keeps node_modules and package-lock.json out of
       `git add -A`; all 14 horse profiles carry the fields the modal shows.

Purely static: file-content analysis only, no npm, no network, no git,
no pytest.skip.  (Dynamic npm build/dev self-verification is the developer's
step; the gate evidence is these static tests plus the pre-existing suite.)
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
MODAL = SRC / "components" / "ProfileModal.jsx"
MODAL_CSS = SRC / "components" / "ProfileModal.css"
CARDDECK = SRC / "components" / "CardDeck.jsx"
GITIGNORE = ROOT / ".gitignore"
HORSES = SRC / "data" / "horses.ts"


def _rule(css: str, selector: str) -> str:
    """Body of a top-level CSS rule for `selector` (exact match), or ''."""
    m = re.search(
        r"^" + re.escape(selector) + r"\s*\{(.*?)\n\}", css, re.DOTALL | re.MULTILINE
    )
    return m.group(1) if m else ""


def _fn_body(src: str, name: str) -> str:
    """Body of `const name = (...) => { ... }` up to the closing brace line."""
    m = re.search(
        r"const " + re.escape(name) + r"\s*=\s*\((.*?)\)\s*=>\s*\{(.*?)\n\s*\};",
        src,
        re.DOTALL,
    )
    assert m, f"CardDeck.jsx must define {name}"
    return m.group(2)


# ---------------------------------------------------------------------------
# AC1 — ProfileModal.jsx component structure
# ---------------------------------------------------------------------------


def test_profile_modal_file_exists_and_default_exports_component():
    assert MODAL.is_file(), "src/components/ProfileModal.jsx must exist"
    src = MODAL.read_text(encoding="utf-8")
    assert re.search(
        r"export\s+default\s+function\s+ProfileModal\s*\(\s*\{\s*horse\s*,\s*onClose\s*\}\s*\)",
        src,
    ), "ProfileModal.jsx must default-export ProfileModal({ horse, onClose })"


def test_profile_modal_returns_null_without_horse():
    src = MODAL.read_text(encoding="utf-8")
    assert re.search(r"if\s*\(\s*!horse\s*\)\s*return\s+null\s*;", src), (
        "ProfileModal must render nothing (return null) when horse is null"
    )


def test_profile_modal_overlay_and_modal_containers():
    src = MODAL.read_text(encoding="utf-8")
    assert re.search(
        r'<div\s+className="profile-overlay"\s+onClick=\{onClose\}>', src
    ), 'overlay must be <div className="profile-overlay" onClick={onClose}>'
    assert re.search(
        r'<div\s+className="profile-modal"\s+onClick=\{\s*\(?\s*e\s*\)?\s*=>\s*e\.stopPropagation\(\)\s*\}>',
        src,
    ), (
        'inner must be <div className="profile-modal" onClick={e => e.stopPropagation()}>'
    )
    # overlay opens before the modal div and the modal nests inside it
    assert src.index("profile-overlay") < src.index("profile-modal")


def test_profile_modal_renders_all_horse_fields():
    src = MODAL.read_text(encoding="utf-8")
    assert re.search(
        r'<img\s+src=\{horse\.imageUrl\}\s+alt=\{horse\.name\}\s+className="profile-photo"\s*/>',
        src,
    ), (
        'must render <img src={horse.imageUrl} alt={horse.name} className="profile-photo" />'
    )
    assert re.search(r"<h2>\{horse\.name\}</h2>", src), (
        "must render <h2>{horse.name}</h2>"
    )
    assert re.search(r'<p\s+className="profile-breed">\{horse\.breed\}</p>', src), (
        'must render <p className="profile-breed">{horse.breed}</p>'
    )
    assert re.search(r'<p\s+className="profile-age">\{horse\.age\}\s+years</p>', src), (
        'must render <p className="profile-age">{horse.age} years</p>'
    )
    assert re.search(r'<p\s+className="profile-bio">\{horse\.bio\}</p>', src), (
        'must render <p className="profile-bio">{horse.bio}</p>'
    )


def test_profile_modal_close_button():
    src = MODAL.read_text(encoding="utf-8")
    assert re.search(
        r'<button\s+className="profile-close"\s+onClick=\{onClose\}>\s*✕\s*Close\s*</button>',
        src,
    ), (
        'must render <button className="profile-close" onClick={onClose}>✕ Close</button>'
    )


def test_profile_modal_imports_css():
    src = MODAL.read_text(encoding="utf-8")
    assert re.search(r"import\s+['\"]\./ProfileModal\.css['\"]", src), (
        "ProfileModal.jsx must import './ProfileModal.css'"
    )
    assert MODAL_CSS.is_file(), "src/components/ProfileModal.css must exist"


# ---------------------------------------------------------------------------
# AC2 — ProfileModal.css rules
# ---------------------------------------------------------------------------


def test_css_profile_overlay():
    css = MODAL_CSS.read_text(encoding="utf-8")
    rule = _rule(css, ".profile-overlay")
    assert rule, ".profile-overlay rule must exist"
    assert re.search(r"position:\s*fixed", rule), "overlay must be position: fixed"
    assert re.search(r"inset:\s*0", rule), "overlay must set inset: 0"
    assert re.search(
        r"background:\s*rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0?\.6\s*\)", rule
    ), "overlay backdrop must be rgba(0,0,0,0.6)"
    assert re.search(r"display:\s*flex", rule), "overlay must be flex"
    assert re.search(r"align-items:\s*center", rule), "overlay must center vertically"
    assert re.search(r"justify-content:\s*center", rule), (
        "overlay must center horizontally"
    )
    assert re.search(r"z-index:\s*100", rule), "overlay must have z-index: 100"


def test_css_profile_modal():
    css = MODAL_CSS.read_text(encoding="utf-8")
    rule = _rule(css, ".profile-modal")
    assert rule, ".profile-modal rule must exist"
    assert re.search(r"background:\s*#fff", rule), "modal background must be #fff"
    assert re.search(r"border-radius:\s*16px", rule), "modal border-radius must be 16px"
    assert re.search(r"max-width:\s*400px", rule), "modal max-width must be 400px"
    assert re.search(r"width:\s*90vw", rule), "modal width must be 90vw"
    assert re.search(r"max-height:\s*85vh", rule), "modal max-height must be 85vh"
    assert re.search(r"overflow-y:\s*auto", rule), "modal must scroll vertically"
    assert re.search(r"position:\s*relative", rule), "modal must be position: relative"
    assert re.search(r"box-shadow:", rule), "modal must have a box-shadow"


def test_css_profile_photo_and_text_rules():
    css = MODAL_CSS.read_text(encoding="utf-8")
    photo = _rule(css, ".profile-photo")
    assert photo, ".profile-photo rule must exist"
    assert re.search(r"width:\s*100%", photo), "photo must span the modal width"
    assert re.search(r"height:\s*280px", photo), "photo height must be 280px"
    assert re.search(r"object-fit:\s*cover", photo), "photo must use object-fit: cover"
    assert re.search(r"border-radius:\s*12px", photo), (
        "photo must have border-radius 12px"
    )

    h2 = _rule(css, ".profile-modal h2")
    assert h2, ".profile-modal h2 rule must exist"
    assert re.search(r"color:\s*#c0392b", h2), "name heading must use the accent color"
    assert re.search(r"font-size:\s*1\.6rem", h2), (
        "name heading font-size must be 1.6rem"
    )

    breed = _rule(css, ".profile-breed")
    assert breed, ".profile-breed rule must exist"
    assert re.search(r"font-weight:\s*600", breed), "breed must be semi-bold"

    assert _rule(css, ".profile-age"), ".profile-age rule must exist"
    bio = _rule(css, ".profile-bio")
    assert bio, ".profile-bio rule must exist"
    assert re.search(r"line-height:\s*1\.5", bio), "bio must use line-height 1.5"


def test_css_profile_close_button():
    css = MODAL_CSS.read_text(encoding="utf-8")
    rule = _rule(css, ".profile-close")
    assert rule, ".profile-close rule must exist"
    assert re.search(r"position:\s*absolute", rule), (
        "close button must be absolutely positioned"
    )
    assert re.search(r"top:\s*12px", rule), "close button must sit at top: 12px"
    assert re.search(r"right:\s*12px", rule), "close button must sit at right: 12px"
    assert re.search(r"background:\s*#e74c3c", rule), (
        "close button must be red (#e74c3c)"
    )
    assert re.search(r"border-radius:\s*50%", rule), "close button must be circular"
    assert re.search(r"width:\s*32px", rule) and re.search(r"height:\s*32px", rule), (
        "close button must be 32x32"
    )

    hover = _rule(css, ".profile-close:hover")
    assert hover, ".profile-close:hover rule must exist"
    assert re.search(r"background:\s*#c0392b", hover), (
        "close hover must darken to #c0392b"
    )


# ---------------------------------------------------------------------------
# AC3 — CardDeck tap detection
# ---------------------------------------------------------------------------


def test_carddeck_has_selected_horse_state():
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(
        r"const\s*\[\s*selectedHorse\s*,\s*setSelectedHorse\s*\]\s*=\s*useState\(\s*null\s*\)",
        src,
    ), (
        "CardDeck must add state: const [selectedHorse, setSelectedHorse] = useState(null)"
    )


def test_carddeck_tap_opens_modal_on_top_card():
    src = CARDDECK.read_text(encoding="utf-8")
    body = _fn_body(src, "handlePointerUp")
    assert re.search(r"Math\.abs\(\s*deltaX\.current\s*\)\s*<\s*10", body), (
        "handlePointerUp must treat |deltaX| < 10 as a tap"
    )
    assert re.search(r"(animating\s*===\s*null|!\s*animating)", body), (
        "tap must be ignored while a swipe animation runs"
    )
    assert re.search(r"deck\.length\s*>\s*0", body), (
        "tap must be ignored on an empty deck"
    )
    assert "setSelectedHorse(deck[0])" in body, (
        "tap must select the top card: setSelectedHorse(deck[0])"
    )


def test_carddeck_tap_only_fires_when_no_swipe_triggered():
    """The tap check must live in the non-swipe branch of handlePointerUp."""
    src = CARDDECK.read_text(encoding="utf-8")
    body = _fn_body(src, "handlePointerUp")
    swipe = re.search(
        r"if\s*\(\s*Math\.abs\(\s*deltaX\.current\s*\)\s*>\s*SWIPE_THRESHOLD\s*\)\s*\{(.*?)\}\s*else\s*\{",
        body,
        re.DOTALL,
    )
    assert swipe, (
        "handlePointerUp must branch on |deltaX| > SWIPE_THRESHOLD with an else block"
    )
    assert "triggerSwipe" in swipe.group(1), "swipe branch must call triggerSwipe"
    tap_pos = body.find("Math.abs(deltaX.current) < 10")
    else_pos = body.find("else")
    assert tap_pos != -1 and else_pos != -1 and tap_pos > else_pos, (
        "tap detection must run only in the else (no-swipe) branch"
    )
    # A drag of 10..100px is neither a swipe nor a tap: the strict < 10 guard
    # and the > SWIPE_THRESHOLD guard must both be present (no overlap).
    assert "SWIPE_THRESHOLD" in body and "< 10" in body


# ---------------------------------------------------------------------------
# AC4 — CardDeck renders ProfileModal wired to selectedHorse
# ---------------------------------------------------------------------------


def test_carddeck_imports_profile_modal():
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(
        r"import\s+ProfileModal\s+from\s+['\"]\./ProfileModal['\"]", src
    ), "CardDeck.jsx must import ProfileModal from './ProfileModal'"


def test_carddeck_renders_profile_modal_with_close_handler():
    src = CARDDECK.read_text(encoding="utf-8")
    assert re.search(
        r"<ProfileModal\s+horse=\{selectedHorse\}\s+onClose=\{\(\)\s*=>\s*setSelectedHorse\(\s*null\s*\)\}\s*/>",
        src,
    ), (
        "CardDeck must render "
        "<ProfileModal horse={selectedHorse} onClose={() => setSelectedHorse(null)} />"
    )


def test_profile_modal_rendered_outside_deck_branch():
    """The modal sits after the isEmpty ternary, so it renders in both states."""
    src = CARDDECK.read_text(encoding="utf-8")
    branch = src.find("{isEmpty ?")
    modal = src.find("<ProfileModal")
    assert branch != -1 and modal != -1, (
        "both the isEmpty branch and <ProfileModal must render"
    )
    assert modal > branch, (
        "<ProfileModal must be rendered after the deck/empty-state branch"
    )
    # ... and it is the last thing inside the component's returned root div.
    tail = src[modal:]
    assert re.search(r"</ProfileModal\s*/?>|/>", tail), (
        "ProfileModal must be self-closed"
    )
    assert tail.find("</div>") != -1 and tail.find("</div>") > tail.find(
        "<ProfileModal"
    ), "ProfileModal must sit inside the returned root <div>"


# ---------------------------------------------------------------------------
# AC7 (regression) — existing deck behavior untouched
# ---------------------------------------------------------------------------


def test_swipe_logic_intact_after_modal_wiring():
    src = CARDDECK.read_text(encoding="utf-8")
    assert "const SWIPE_THRESHOLD = 100;" in src, "swipe threshold must remain 100px"
    assert re.search(r"triggerSwipe\(deltaX\.current > 0 \? 'right' : 'left'\)", src), (
        "swipe direction dispatch must be unchanged"
    )
    assert re.search(r"setDeck\(\(d\)\s*=>\s*d\.slice\(1\)\)", src), (
        "finishSwipe must still remove the top card"
    )
    assert re.search(
        r"deck\.length\s*===\s*0\s*&&\s*!leavingCard\s*&&\s*!animating", src
    ), "leavingCard/animating empty-state guard must be preserved"
    assert re.search(r"\{deck\.length\}\s+cards remaining", src), (
        "counter must be preserved"
    )
    assert re.search(r"setDeck\(shuffleDeck\(horses\)\)", src), (
        "reset/shuffle must be preserved"
    )
    assert re.search(r"import\s+ProfileModal", src), (
        "modal import must not drop other imports"
    )


# ---------------------------------------------------------------------------
# AC8 — repo hygiene + data supports 14 distinct modal views
# ---------------------------------------------------------------------------


def test_gitignore_covers_node_modules_and_lockfile():
    """git add -A must stage no node_modules or package-lock.json."""
    text = GITIGNORE.read_text(encoding="utf-8")
    lines = [
        ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")
    ]
    assert "node_modules/" in lines, ".gitignore must ignore node_modules/"
    assert "package-lock.json" in lines, ".gitignore must ignore package-lock.json"


def test_all_14_profiles_have_modal_fields():
    """Every horse the modal can show carries name/breed/age/bio/imageUrl."""
    data = HORSES.read_text(encoding="utf-8")
    names = re.findall(r"name:\s*'([^']+)'", data)
    assert len(names) == 14, f"expected 14 profiles, found {len(names)}"
    assert len(set(names)) == 14, "the 14 profiles must have unique names"
    assert len(re.findall(r"breed:\s*'[^']+'", data)) == 14
    assert len(re.findall(r"age:\s*\d+", data)) == 14
    assert len(re.findall(r"bio:\s*'[^']+'", data)) == 14
    assert len(re.findall(r"""imageUrl:\s*["']""", data)) == 14, (
        "every profile needs an imageUrl for the modal <img src>"
    )
