# Horse Tinder Demo

## Fixed

### Goal
A React single-page demo where the user swipes through ~14 fictional AI-generated horse profiles, taps cards for full bios, triggers a 33% random match animation on right-swipe, revisits a Liked Horses collection, and can reset/shuffle the deck. Static site, no backend, no social network.

### Users
Just the creator (solo demo, no multi-user)

### Milestones
#### 1. Scaffold & Horse Data
Initialize React+Vite project, author 14 fictional horse profiles with AI-generated images, and wire GitHub Pages auto-deploy on push to main.
- [ ] `npm run dev` serves a blank React app at localhost:5173
- [ ] A data file contains 14+ horse objects each with name, breed, age, bio, and an image URL
- [ ] `npm run build` produces a static dist/ folder with no server dependencies
- [ ] A GitHub Actions workflow deploys dist/ to GitHub Pages on every push to main
Estimate: $5.0 · 3.0 hours

#### 2. Swipe Deck UI
Render a stacked card deck with left/right swipe gestures, animated card removal, and a reset/shuffle button when the deck is empty.
- [ ] Swiping right on the top card removes it with a rightward slide-and-fade animation
- [ ] Swiping left removes it with a leftward slide-and-fade animation
- [ ] A visible counter shows remaining cards in the deck
- [ ] When the deck is empty a 'Reset & Shuffle' button appears; clicking it restores all 14 cards in a new random order
Estimate: $7.0 · 5.0 hours

#### 3. Full Profile View
Tapping the top card expands into a detail view showing all horse fields and a larger photo, with a close/back action.
- [ ] Tapping the top card opens a modal or overlay showing name, breed, age, bio, and photo
- [ ] A close/back button dismisses the detail view and returns to the swipe deck
- [ ] At least 14 distinct profiles are viewable this way with unique content
Estimate: $3.0 · 2.0 hours

#### 4. Match Animation & Liked Collection
On right-swipe a 33% random chance triggers a celebratory 'It's a Match!' overlay; liked/matched horses are saved and viewable in a grid.
- [ ] Right-swiping across 10+ horses produces at least one 'It's a Match!' overlay with the horse's photo (verifies ~33% rate)
- [ ] Every right-swiped horse is added to a 'Liked Horses' collection
- [ ] A nav button opens a grid view showing thumbnail + name for each liked horse; count matches number of right-swipes performed
Estimate: $4.0 · 3.0 hours

#### 5. Polish & Live Deploy
Apply a cohesive visual style, ensure responsive layout, and confirm the full app is live on GitHub Pages with no errors.
- [ ] App uses a consistent color palette, readable typography, and no raw/unstyled elements
- [ ] Layout is usable at 375px mobile width and 1280px desktop width
- [ ] The live GitHub Pages URL loads the app and all five capabilities work end-to-end
- [ ] Browser console shows zero errors on load and during a full swipe session
Estimate: $1.0 · 2.0 hours

### Out of scope
No real user accounts, no backend/API, no push notifications, no payments, no social network, no real horse data, no multi-user matchmaking

### Constraints
Repository: bigdan88/horse_tinder (existing)
Stack: React + Vite (static SPA build)
Hosting: GitHub Pages
Budget: $20.0
Deadline: 3 days from approval

### Latitude
Free rein on horse names, breeds, ages, bios, AI-generated photos, visual style, color palette, deck size (~14 profiles), and the 33% match probability. No need to ask before choosing any creative or UI detail.
Ask before: Nothing — user granted full creative and technical latitude on all listed items

## Living

### Current state
Repository `bigdan88/horse_tinder` at sha `400b9505` contains only `README.md` (placeholder "# horse_tinder") and `docs/project-spec.md`. No source code, no package.json, no build tooling, no .gitignore. Milestone 1 is starting its THIRD attempt after two failures. Budget: $19.65 / $20.00 remaining. Deadline: 2026-11-06.

**Attempt 1** (run `20261103-164020-98ddc1`, $3.0): 4-agent parallel swarm. T1-T4 all committed files, but T1 fabricated `package-lock.json` with non-existent packages. Reviewer flagged AC1/AC3/AC4 (npm ci/build/test all fail with bogus lockfile). Repair cycle F1 ran but changed no files. FAILED.

**Attempt 2** (run `20261103-172618-fc82a7`, $3.0): 5-task sequential chain (T1-1→T1-2→T1-3→T2-1→T2-2). T1-1 wrote package.json/vite.config/index.html, ran npm install successfully (genuine lockfile), but then `git add -A` crashed: "open(node_modules/.bin/baseline-browser-mapping): Function not implemented" because .gitignore hadn't been written yet. All downstream tasks BLOCKED. FAILED with zero code changes.

**Key learnings**: (a) .gitignore MUST be written before npm install; (b) package-lock.json should be gitignored to avoid fabrication risk; (c) single-agent execution avoids fragile dependency chains; (d) Pi agents have bridge network so npm install works.

### Decisions made
- **2026-11-03**: Full creative latitude confirmed by user. Horse names, breeds, ages, bios, AI image URLs, color palette, deck size (~14), and 33% match probability are all free to choose.
- **2026-11-03**: Stack locked to React + Vite static SPA; hosting is GitHub Pages; no backend, no accounts.
- **2026-11-03**: No spike needed for milestone 1 — Vite scaffold, data authoring, and Pages CI are standard, low-risk work.
- **2026-11-03**: After 2 failures, `m1-scaffold-vite-react` rewritten as single-agent task. .gitignore written first (before npm install), package-lock.json gitignored entirely, no parallel/split tasks. This addresses both root causes: fabricated lockfile AND git add -A node_modules crash.
- **2026-11-03**: `m1-github-pages-workflow` unchanged in scope but sequenced after scaffold merge. Workflow uses `npm install` (not `npm ci`) since lockfile is gitignored.

### Plan
**Milestone 1 – Scaffold & Horse Data** (target $5.0 / 3 h):
1. `m1-scaffold-vite-react` (READY, $3.0) — Single-agent Vite+React scaffold: write .gitignore first, then config/source/data files, then npm install + verify build/test/dev. 14 horse profiles with inline SVG data-URI images. README updated. docs/project-spec.md committed unchanged.
2. `m1-github-pages-workflow` (READY, $1.5) — GitHub Actions deploy.yml for Pages; README URL note. Runs after scaffold merge.

**Milestone 2 – Swipe Deck UI** (tentative, replan after M1 merge):
- `m2-swipe-deck` — Stacked card deck with left/right swipe gestures, slide-and-fade animations, remaining counter, reset/shuffle button.

**Milestone 3 – Full Profile View** (tentative):
- `m3-profile-modal` — Tap-to-expand modal with full bio fields and larger photo; close/back action.

**Milestone 4 – Match Animation & Liked Collection** (tentative):
- `m4-match-liked` — 33% random match overlay on right-swipe; Liked Horses grid view with nav button.

**Milestone 5 – Polish & Live Deploy** (tentative):
- `m5-polish-deploy` — Cohesive visual style, responsive at 375px/1280px, zero console errors, confirm live Pages URL end-to-end.

### Plan changes
- **2026-11-03**: Initial plan created. No changes yet.
- **2026-11-03**: After attempt 1 FAILED (fabricated lockfile → AC1/AC3/AC4): rewrote task to forbid hand-authored lockfiles and require genuine npm install verification. Kept same key `m1-scaffold-vite-react`.
- **2026-11-03**: After attempt 2 FAILED (.gitignore missing → git add -A crash on node_modules; 5-task chain all blocked): rewrote as single-agent task with .gitignore as step 1 and package-lock.json gitignored. Same key preserved. `m1-github-pages-workflow` updated to use `npm install` instead of `npm ci` since lockfile is no longer committed.

### Open questions
- None. All spec items are clear; latitude covers creative choices. AI-generated horse images will use inline SVG data URIs (horse emoji + name on colored background) since no external AI image API is specified — this is within latitude and avoids network dependencies.