"""Acceptance tests for Milestone 4 part 2: liked tracking and match wiring.

Maps to the acceptance criteria of the issue
"Wire liked tracking, 33% match trigger and Liked Horses grid into CardDeck":

- AC1: src/components/CardDeck.jsx declares swipeDirRef/swipeCardRef with
       useRef(null); triggerSwipe captures (direction, deck[0]) into both refs
       before setLeavingCard; finishSwipe appends the captured horse via
       setLiked on a right swipe, rolls Math.random() < 0.33 only inside the
       swipeDirRef.current === 'right' guard to call setMatchedHorse, nulls
       both refs, and does all of that before the unchanged
       setDeck(slice(1)) / setLeavingCard(null) / setAnimating(null) clears.
- AC2: CardDeck.jsx imports './MatchOverlay' and './LikedHorses' and renders
       <MatchOverlay horse={matchedHorse} onClose={() => setMatchedHorse(null)} />
       after the ProfileModal line plus
       {showLiked && <LikedHorses horses={liked} />}.
- AC3: a button with className="liked-nav-btn" renders 'Liked ({liked.length})',
       toggles showLiked via setShowLiked(s => !s), and sits outside the
       isEmpty ternary so the liked count survives deck exhaustion.
- AC4: handleReset calls setLiked([]) and setMatchedHorse(null) in addition to
       setDeck(shuffleDeck(horses)), setLeavingCard(null) and setAnimating(null).
- AC5: every M2/M3 regression string is preserved verbatim (pointer handlers,
       SWIPE_THRESHOLD 100, right/left mapping, swipe-right/swipe-left class,
       cards-remaining counter, isEmpty guard and ternary, Reset &amp; Shuffle,
       Fisher-Yates shuffleDeck, |deltaX| < 10 tap detection, ProfileModal
       wiring, './SwipeDeck.css' and '../data/horses' imports, 300ms timeout,
       onAnimationEnd and slice(1) removal); src/App.jsx keeps
       'Horse Tinder Demo' and './data/horses'; MatchOverlay.jsx and
       LikedHorses.jsx keep their merged export signatures.
- AC8 (partial): docs/project-spec.md keeps its Fixed section byte-for-byte
  unchanged (length + FNV-1a 64 digest pinned to the merged spec);
  package.json dependency sets are pinned by tests/test_swipe_deck.py.

Purely static: file-content analysis only — no shelling out, no remote
services, no conditional bypasses.  (Dynamic build self-verification is the
developer's step; the gate evidence is these static checks plus the
pre-existing suite.)
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DECK = SRC / "components" / "CardDeck.jsx"
APP = SRC / "App.jsx"
MATCH = SRC / "components" / "MatchOverlay.jsx"
LIKED = SRC / "components" / "LikedHorses.jsx"
SPEC = ROOT / "docs" / "project-spec.md"


def _deck() -> str:
    return DECK.read_text(encoding="utf-8")


def _fn(src: str, name: str) -> str:
    """Body of the component-level arrow function `name`, or ''."""
    m = re.search(
        r"const " + re.escape(name) + r" = [^{]*\{(.*?)\n  \};", src, re.DOTALL
    )
    return m.group(1) if m else ""


def _jsx_block_end(src: str, opener: int) -> int:
    """Index just past the '}' matching the '{' at `opener` (brace counting)."""
    depth = 0
    for i in range(opener, len(src)):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
    raise AssertionError("unbalanced JSX braces in CardDeck.jsx")


# ---------------------------------------------------------------------------
# AC1 — swipe refs, liked tracking and the 33% match roll
# ---------------------------------------------------------------------------


def test_swipe_refs_declared_with_use_ref_null():
    src = _deck()
    assert re.search(r"const swipeDirRef = useRef\(null\);", src), (
        "CardDeck must declare const swipeDirRef = useRef(null);"
    )
    assert re.search(r"const swipeCardRef = useRef\(null\);", src), (
        "CardDeck must declare const swipeCardRef = useRef(null);"
    )


def test_liked_match_and_show_liked_state():
    src = _deck()
    assert re.search(r"const \[liked, setLiked\] = useState\(\[\]\);", src), (
        "CardDeck must track liked horses in const [liked, setLiked] = useState([])"
    )
    assert re.search(
        r"const \[matchedHorse, setMatchedHorse\] = useState\(null\);", src
    ), "CardDeck must track matchedHorse in useState(null)"
    assert re.search(r"const \[showLiked, setShowLiked\] = useState\(false\);", src), (
        "CardDeck must track showLiked in useState(false)"
    )


def test_trigger_swipe_captures_refs_before_set_leaving_card():
    body = _fn(_deck(), "triggerSwipe")
    assert body, "triggerSwipe function body must exist"
    assert re.search(r"swipeDirRef\.current = direction;", body), (
        "triggerSwipe must store the direction in swipeDirRef.current"
    )
    assert re.search(r"swipeCardRef\.current = deck\[0\];", body), (
        "triggerSwipe must store deck[0] in swipeCardRef.current"
    )
    leaving = body.index("setLeavingCard")
    assert body.index("swipeDirRef.current = direction;") < leaving, (
        "swipeDirRef.current must be set before setLeavingCard"
    )
    assert body.index("swipeCardRef.current = deck[0];") < leaving, (
        "swipeCardRef.current must be set before setLeavingCard"
    )


def test_finish_swipe_match_roll_guarded_by_right_swipe():
    body = _fn(_deck(), "finishSwipe")
    assert body, "finishSwipe function body must exist"
    assert re.search(
        r"if \(swipeDirRef\.current === 'right' && swipeCardRef\.current\) \{", body
    ), (
        "finishSwipe must guard on swipeDirRef.current === 'right' && swipeCardRef.current"
    )
    assert re.search(r"const horse = swipeCardRef\.current;", body), (
        "finishSwipe must read the leaving horse from swipeCardRef.current"
    )
    guard = body.index("swipeDirRef.current === 'right'")
    roll = body.index("Math.random() < 0.33")
    assert guard < roll < body.index("setDeck"), (
        "the Math.random() < 0.33 roll must sit inside the right-swipe guard "
        "and before the setDeck clear"
    )
    assert re.search(
        r"if \(swipeDirRef\.current === 'right' && swipeCardRef\.current\) \{"
        r"[\s\S]*?if \(Math\.random\(\) < 0\.33\) \{[\s\S]*?setMatchedHorse\(horse\);",
        body,
    ), (
        "setMatchedHorse(horse) must be called only when Math.random() < 0.33 inside the guard"
    )


def test_finish_swipe_appends_liked_horse_before_deck_clear():
    body = _fn(_deck(), "finishSwipe")
    assert re.search(
        r"setLiked\(\s*\(\s*prev\s*\)\s*=>\s*\[\s*\.\.\.\s*prev\s*,\s*horse\s*\]\s*\)",
        body,
    ), "finishSwipe must append the horse via setLiked((prev) => [...prev, horse])"
    assert body.index("setLiked") < body.index("setDeck"), (
        "the liked append must precede the setDeck((d) => d.slice(1)) clear"
    )


def test_finish_swipe_nulls_both_refs():
    body = _fn(_deck(), "finishSwipe")
    assert re.search(r"swipeDirRef\.current = null;", body), (
        "finishSwipe must null swipeDirRef.current"
    )
    assert re.search(r"swipeCardRef\.current = null;", body), (
        "finishSwipe must null swipeCardRef.current"
    )
    assert body.index("swipeDirRef.current = null;") < body.index("setDeck"), (
        "both refs must be nulled before the setDeck clear"
    )
    assert body.index("swipeCardRef.current = null;") < body.index("setDeck"), (
        "both refs must be nulled before the setDeck clear"
    )


def test_finish_swipe_guard_timeout_and_removal_unchanged():
    src = _deck()
    body = _fn(src, "finishSwipe")
    assert re.search(r"if \(swipeDone\.current\) return;", body), (
        "the swipeDone.current early-return guard must be preserved"
    )
    assert re.search(r"swipeDone\.current = true;", body), (
        "finishSwipe must keep setting swipeDone.current = true"
    )
    assert re.search(r"clearTimeout\(timeoutRef\.current\);", body), (
        "finishSwipe must keep clearing the pending timeout"
    )
    assert re.search(r"setDeck\(\(d\) => d\.slice\(1\)\);", body), (
        "finishSwipe must keep removing the top card with setDeck((d) => d.slice(1))"
    )
    assert re.search(r"setTimeout\(finishSwipe, 300\);", _fn(src, "triggerSwipe")), (
        "triggerSwipe must keep the 300ms setTimeout(finishSwipe, 300)"
    )


# ---------------------------------------------------------------------------
# AC2 — MatchOverlay and LikedHorses wiring
# ---------------------------------------------------------------------------


def test_card_deck_imports_match_overlay_and_liked_horses():
    src = _deck()
    assert re.search(
        r"import\s+MatchOverlay\s+from\s+['\"]\./MatchOverlay['\"];", src
    ), "CardDeck must import './MatchOverlay'"
    assert re.search(r"import\s+LikedHorses\s+from\s+['\"]\./LikedHorses['\"];", src), (
        "CardDeck must import './LikedHorses'"
    )


def test_card_deck_renders_match_overlay_after_profile_modal():
    src = _deck()
    assert re.search(
        r"<MatchOverlay\s+horse=\{matchedHorse\}\s+"
        r"onClose=\{\(\)\s*=>\s*setMatchedHorse\(null\)\}\s*/>",
        src,
    ), (
        "must render <MatchOverlay horse={matchedHorse} "
        "onClose={() => setMatchedHorse(null)} />"
    )
    assert src.index("<ProfileModal") < src.index("<MatchOverlay"), (
        "the MatchOverlay must be rendered after the existing ProfileModal line"
    )


def test_card_deck_renders_liked_grid_conditionally():
    src = _deck()
    assert re.search(
        r"\{\s*showLiked\s*&&\s*<LikedHorses\s+horses=\{liked\}\s*/>\s*\}", src
    ), "must render {showLiked && <LikedHorses horses={liked} />}"
    assert src.index("showLiked && <LikedHorses") < src.index("<ProfileModal"), (
        "the liked grid must render alongside the deck, before the modal layer"
    )


# ---------------------------------------------------------------------------
# AC3 — liked nav button with live count, outside the isEmpty ternary
# ---------------------------------------------------------------------------


def test_liked_nav_button_label_and_toggle():
    src = _deck()
    assert re.search(r'<button className="liked-nav-btn"', src), (
        'the nav button must use className="liked-nav-btn"'
    )
    assert re.search(
        r"onClick=\{\(\)\s*=>\s*setShowLiked\(\s*\(?\s*s\s*\)?\s*=>\s*!\s*s\s*\)\}", src
    ), "the nav button onClick must toggle showLiked via setShowLiked(s => !s)"
    assert re.search(r"Liked \(\{liked\.length\}\)", src), (
        "the nav button must render the label 'Liked ({liked.length})'"
    )


def test_liked_nav_button_outside_is_empty_ternary():
    src = _deck()
    start = src.index("{isEmpty ? (")
    end = _jsx_block_end(src, start)
    btn = src.index('className="liked-nav-btn"')
    assert src.index("return (") < btn, (
        "the liked nav button must be rendered in the JSX"
    )
    assert not (start < btn < end), (
        "the liked nav button must render outside the isEmpty ternary so the "
        "liked count stays visible after the deck empties"
    )


# ---------------------------------------------------------------------------
# AC4 — handleReset clears liked and matchedHorse too
# ---------------------------------------------------------------------------


def test_handle_reset_clears_liked_and_match():
    body = _fn(_deck(), "handleReset")
    assert body, "handleReset function body must exist"
    assert re.search(r"setDeck\(shuffleDeck\(horses\)\);", body), (
        "handleReset must reshuffle with setDeck(shuffleDeck(horses))"
    )
    assert re.search(r"setLeavingCard\(null\);", body), (
        "handleReset must call setLeavingCard(null)"
    )
    assert re.search(r"setAnimating\(null\);", body), (
        "handleReset must call setAnimating(null)"
    )
    assert re.search(r"setLiked\(\[\]\);", body), (
        "handleReset must clear the liked collection with setLiked([])"
    )
    assert re.search(r"setMatchedHorse\(null\);", body), (
        "handleReset must clear the match overlay with setMatchedHorse(null)"
    )


# ---------------------------------------------------------------------------
# AC5 — M2/M3 regressions preserved verbatim
# ---------------------------------------------------------------------------


def test_pointer_handlers_wired_and_defined():
    src = _deck()
    assert re.search(r"onPointerDown=\{handlePointerDown\}", src), (
        "the deck must keep onPointerDown={handlePointerDown}"
    )
    assert re.search(r"onPointerMove=\{handlePointerMove\}", src), (
        "the deck must keep onPointerMove={handlePointerMove}"
    )
    assert re.search(r"onPointerUp=\{handlePointerUp\}", src), (
        "the deck must keep onPointerUp={handlePointerUp}"
    )
    assert re.search(r"const handlePointerDown = \(e\) =>", src), (
        "handlePointerDown must be preserved"
    )
    assert re.search(r"const handlePointerMove = \(e\) =>", src), (
        "handlePointerMove must be preserved"
    )
    assert re.search(r"const handlePointerUp = \(\) =>", src), (
        "handlePointerUp must be preserved"
    )


def test_swipe_threshold_and_direction_mapping():
    src = _deck()
    assert re.search(r"const SWIPE_THRESHOLD = 100;", src), (
        "SWIPE_THRESHOLD must stay 100"
    )
    assert re.search(r"Math\.abs\(deltaX\.current\) > SWIPE_THRESHOLD", src), (
        "the swipe decision must keep Math.abs(deltaX.current) > SWIPE_THRESHOLD"
    )
    assert re.search(r"deltaX\.current > 0 \? 'right' : 'left'", src), (
        "the direction mapping must keep deltaX.current > 0 ? 'right' : 'left'"
    )


def test_top_card_swipe_animation_classes():
    src = _deck()
    assert re.search(
        r"i === 0 && animating \? \(animating === 'right' \? 'swipe-right' : 'swipe-left'\)",
        src,
    ), "the top card must keep the swipe-right/swipe-left class expression on i === 0"


def test_counter_above_deck():
    src = _deck()
    assert re.search(
        r'<div className="counter">\{deck\.length\} cards remaining</div>', src
    ), (
        'the counter must render <div className="counter">{deck.length} cards remaining</div>'
    )
    assert src.index('className="counter"') < src.index('className="card-deck"'), (
        "the counter must sit above the deck"
    )


def test_is_empty_guard_and_conditional_render():
    src = _deck()
    assert re.search(
        r"const isEmpty = deck\.length === 0 && !leavingCard && !animating;", src
    ), "isEmpty must stay deck.length === 0 && !leavingCard && !animating"
    assert re.search(r"\{\s*isEmpty\s*\?\s*\(", src), (
        "the render must keep the {isEmpty ? ( ternary"
    )


def test_reset_button_calls_handle_reset():
    src = _deck()
    assert re.search(r'<button className="reset-btn" onClick=\{handleReset\}>', src), (
        'the empty state must render <button className="reset-btn" onClick={handleReset}>'
    )
    assert re.search(r"Reset &amp; Shuffle", src), (
        "the reset button label must stay 'Reset &amp; Shuffle'"
    )


def test_shuffle_deck_fisher_yates_and_usage():
    src = _deck()
    assert re.search(r"for \(let i = a\.length - 1; i > 0; i--\)", src), (
        "shuffleDeck must keep the Fisher-Yates loop"
    )
    assert re.search(r"Math\.floor\(Math\.random\(\) \* \(i \+ 1\)\)", src), (
        "shuffleDeck must keep Math.floor(Math.random() * (i + 1))"
    )
    assert re.search(r"\[a\[i\], a\[j\]\] = \[a\[j\], a\[i\]\];", src), (
        "shuffleDeck must keep the swap"
    )
    assert re.search(r"useState\(\(\) => shuffleDeck\(horses\)\)", src), (
        "the deck must initialize with useState(() => shuffleDeck(horses))"
    )
    assert re.search(r"setDeck\(shuffleDeck\(horses\)\)", src), (
        "handleReset must reshuffle with setDeck(shuffleDeck(horses))"
    )


def test_tap_detection_opens_profile():
    src = _deck()
    assert re.search(
        r"Math\.abs\(deltaX\.current\) < 10 && animating === null && deck\.length > 0",
        src,
    ), (
        "tap detection must keep Math.abs(deltaX.current) < 10 && animating === null && deck.length > 0"
    )
    assert re.search(r"setSelectedHorse\(deck\[0\]\)", src), (
        "a tap must call setSelectedHorse(deck[0])"
    )


def test_profile_modal_import_and_render():
    src = _deck()
    assert re.search(
        r"import\s+ProfileModal\s+from\s+['\"]\./ProfileModal['\"];", src
    ), "CardDeck must keep the './ProfileModal' import"
    assert re.search(
        r"<ProfileModal\s+horse=\{selectedHorse\}\s+"
        r"onClose=\{\(\)\s*=>\s*setSelectedHorse\(null\)\}\s*/>",
        src,
    ), (
        "must keep <ProfileModal horse={selectedHorse} "
        "onClose={() => setSelectedHorse(null)} />"
    )


def test_swipe_deck_css_and_horses_data_imports():
    src = _deck()
    assert re.search(r"import\s+['\"]\./SwipeDeck\.css['\"];", src), (
        "CardDeck must keep the './SwipeDeck.css' import"
    )
    assert re.search(r"import\s+horses\s+from\s+['\"]\.\./data/horses['\"];", src), (
        "CardDeck must keep the '../data/horses' import"
    )


def test_animation_end_and_slice_removal():
    src = _deck()
    assert re.search(r"onAnimationEnd=\{finishSwipe\}", src), (
        "the deck must keep onAnimationEnd={finishSwipe}"
    )
    assert re.search(r"setTimeout\(finishSwipe, 300\)", src), (
        "the 300ms setTimeout(finishSwipe, 300) must be preserved"
    )
    assert re.search(r"setDeck\(\(d\) => d\.slice\(1\)\)", src), (
        "the slice(1) card removal must be preserved"
    )


def test_app_unchanged():
    app = APP.read_text(encoding="utf-8")
    assert "Horse Tinder Demo" in app, "src/App.jsx must keep 'Horse Tinder Demo'"
    assert "./data/horses" in app, "src/App.jsx must keep './data/horses'"


def test_presentational_components_unchanged():
    match = MATCH.read_text(encoding="utf-8")
    assert re.search(
        r"export\s+default\s+function\s+MatchOverlay\s*\(\s*\{\s*horse\s*,\s*onClose\s*\}\s*\)",
        match,
    ), "MatchOverlay.jsx must keep its merged export signature"
    assert "It's a Match!" in match, "MatchOverlay.jsx must keep the match heading"
    assert re.search(r'className="match-overlay"', match), (
        "MatchOverlay.jsx must keep the match-overlay structure"
    )
    liked = LIKED.read_text(encoding="utf-8")
    assert re.search(
        r"export\s+default\s+function\s+LikedHorses\s*\(\s*\{\s*horses\s*\}\s*\)",
        liked,
    ), "LikedHorses.jsx must keep its merged export signature"
    assert re.search(r'className="liked-grid"', liked), (
        "LikedHorses.jsx must keep the liked-grid structure"
    )
    assert re.search(r'className="liked-thumb"', liked), (
        "LikedHorses.jsx must keep the liked-thumb structure"
    )


# ---------------------------------------------------------------------------
# AC8 (partial) — docs/project-spec.md Fixed section stays byte-for-byte stable
# ---------------------------------------------------------------------------

# FNV-1a 64-bit digest and character length of the Fixed section exactly as
# merged on main (PR #6). The Fixed part of the spec must be committed
# unchanged, so any byte or length change must break this pinned digest.
FIXED_FNV1A64 = 0x706BE30ACF599D9E
FIXED_LEN = 3544


def _fnv1a_64(data: bytes) -> int:
    h = 0xCBF29CE484222325
    for byte in data:
        h = ((h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF) ^ byte
    return h


def _fixed_section() -> str:
    spec = SPEC.read_text(encoding="utf-8")
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


def test_project_spec_fixed_section_unchanged():
    fixed = _fixed_section()
    assert len(fixed) == FIXED_LEN, (
        "the Fixed section of docs/project-spec.md changed length; it must be "
        "committed byte-for-byte unchanged"
    )
    assert _fnv1a_64(fixed.encode("utf-8")) == FIXED_FNV1A64, (
        "the Fixed section of docs/project-spec.md changed content; it must be "
        "committed byte-for-byte unchanged"
    )


def test_project_spec_fixed_section_structure_markers():
    fixed = _fixed_section()
    for marker in (
        "### Goal",
        "### Users",
        "### Milestones",
        "#### 1. Scaffold & Horse Data",
        "#### 2. Swipe Deck UI",
        "#### 3. Full Profile View",
        "#### 4. Match Animation & Liked Collection",
        "#### 5. Polish & Live Deploy",
        "### Out of scope",
        "### Constraints",
        "### Latitude",
        "Repository: bigdan88/horse_tinder (existing)",
        "Stack: React + Vite (static SPA build)",
        "Hosting: GitHub Pages",
        "Budget: $20.0",
        "Deadline: 3 days from approval",
    ):
        assert marker in fixed, (
            f"Fixed section of docs/project-spec.md lost marker {marker!r}"
        )


# ---------------------------------------------------------------------------
# Purity guard — this suite stays purely static
# ---------------------------------------------------------------------------


def test_suite_is_purely_static():
    """The suite itself must not shell out, hit remote services or bypass tests."""
    src = Path(__file__).read_text(encoding="utf-8")
    forbidden = [
        "sub" + "process",
        "py" + "test." + "sk" + "ip",
        "xf" + "ail",
        "os." + "system",
        "sock" + "et",
        "requ" + "ests",
        "url" + "open",
        "np" + "m",
        "net" + "work",
        "gi" + "t",
    ]
    for token in forbidden:
        assert token not in src, f"static suite must not use {token}"

    import_lines = [
        line.strip() for line in src.splitlines() if re.match(r"^(import|from)\s", line)
    ]
    assert import_lines == ["import re", "from pathlib import Path"], (
        "the suite may import only re and pathlib"
    )
