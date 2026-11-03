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
Repository `bigdan88/horse_tinder` at sha `169df64` contains only a placeholder `README.md`. No source code, no package.json, no build tooling. Milestone 1 (Scaffold & Horse Data) is starting. Budget: $19.99 / $20.00 remaining. Deadline: 2026-11-06 (3 days from approval 2026-11-03).

### Decisions made
- **2026-11-03**: Full creative latitude confirmed by user. Horse names, breeds, ages, bios, AI image URLs, color palette, deck size (~14), and 33% match probability are all free to choose.
- **2026-11-03**: Stack locked to React + Vite static SPA; hosting is GitHub Pages; no backend, no accounts.
- **2026-11-03**: No spike needed for milestone 1 — Vite scaffold, data authoring, and Pages CI are standard, low-risk work.

### Plan
**Milestone 1 – Scaffold & Horse Data** (target $5.0 / 3 h):
1. `m1-scaffold-vite-react` — Initialize Vite+React project, author `src/data/horses.ts` with 14 fictional horse objects (name, breed, age, bio, imageUrl), confirm `npm run dev` serves at :5173 and `npm run build` produces `dist/`.
2. `m1-github-pages-workflow` — Add `.github/workflows/deploy.yml` that builds on push to main and publishes `dist/` to GitHub Pages; update README with project info.

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

### Open questions
- None. All spec items are clear; latitude covers creative choices. AI-generated horse images will use placeholder image URLs (e.g., from a free horse image source or inline SVG) since no external AI image API is specified — this is within latitude.