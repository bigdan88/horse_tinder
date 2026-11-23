# Verification status

## Automated checks

`python -m pytest -q` covers the static CSS, source-preservation and
spec-digest assertions for the M5 styling task. The suite is purely static:
it reads committed files and never shells out, fetches a URL or drives a
browser.

## Unverified checks (human confirmation required)

The following checks are deliberately **not** verified by this task, and no
pass is claimed for them:

- **Live GitHub Pages URL load** — the deployed app at
  <https://bigdan88.github.io/horse_tinder/> was not loaded or exercised by an
  agent; browser journeys are unavailable in this environment.
- **Zero browser-console errors** — the browser console was not inspected on
  load or during a full swipe session.

Both checks remain unverified pending human confirmation.
