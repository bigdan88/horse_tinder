# Horse Tinder Demo

A React + Vite single-page demo where you swipe through 14 fictional horse profiles.

## Getting started

```
npm install
npm run dev   # http://localhost:5173
npm run build # produces dist/
npm test      # placeholder
```

## Live

https://bigdan88.github.io/horse_tinder/

## Testing

The real test command is `python -m pytest -q`, run from the repository root.
The committed static pytest suite is the gate: it inspects the source, CSS and
config files directly and needs no network access. The `npm test` entry in the
Getting started block above is a placeholder echo that runs no tests.

## Capabilities

The demo ships five capabilities:

- A swipe deck where left or right swipes remove the top card with a
  slide-and-fade animation, and a visible counter shows the remaining cards.
- Tapping a card opens the full profile modal showing name, breed, age, bio and
  photo, with a close button that returns to the deck.
- A right-swipe has a 33% chance of triggering an 'It's a Match!' overlay.
- A 'Liked Horses' grid, opened from the nav button, shows a thumbnail and name
  for every liked horse.
- 'Reset & Shuffle' restores all 14 horses in a new random order.
