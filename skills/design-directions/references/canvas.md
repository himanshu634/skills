# The canvas: seeing the app, drawing the frames, adding rounds

Read this when you are about to take screenshots or build/extend the canvas (steps 2, 4 and 6 of the skill).

## Contents

1. Seeing the real screens (expo web + mocks)
2. Starting the canvas
3. A frame kit and a generator, not hand-written frames
4. Measuring, so lengths on the canvas are true
5. Rounds and finals on the same canvas
6. When the scratchpad is gone

## 1. Seeing the real screens

The point is the **anatomy** of the live screens — copy it, don't approximate it from `design.md`.

- If the user sent phone screenshots, use them; they beat anything you can render.
- Otherwise run expo web with mocks yourself. `preview_start {name}` fails in this repo, so start it from Bash in the background and open it by URL:
  - pick a free port first (`lsof -iTCP:<port>`; 8081 is usually the user's own device session — never kill it, and 8090-ish ports are often held by sibling worktrees). Pass the port explicitly; the non-interactive CLI cannot answer "use another port?".
  - `node node_modules/expo/bin/cli start --web --port <port>` (no `CI=1` from a worktree), then `preview_start {url: "http://localhost:<port>"}`.
  - log in with OTP `1234`; onboarding location: search "Anand".
  - the Browser pane may be hidden: `computer` clicks time out there, but `javascript_tool` clicks, `read_page` refs and `screenshot` work. Animations stall while the pane is hidden — that is the pane, not the code.
  - stop the server when you're done.
- **Traps.** A Metro started from a worktree runs on **mock services** (no `.env.local`) — fine for screenshots. While another tree is running Metro, a worktree's web build can resolve a sibling's files and die; check the startup banner names your tree, and if it still fails, don't burn turns — draw from the user's screenshots, earlier canvases of the same area, and the component code, and say the frames were not checked against a running build.
- Screens worth having for almost any brief: Home, Farmers (directory rows, search), a farmer profile (hero, pills, stats strip), the screen being redesigned and the one before and after it in the flow.

## 2. Starting the canvas

Use the Artifact tool — it is the first call when making a new canvas:

1. `Artifact {action: "quickstart", intent: "design"}` — returns the Design canvas type. (No design system is attached to this account; Koshi's tokens come from `src/global.css` and `design.md`.)
2. Publish with that `type_url`, a `title`, no files, `auto_open: "after_first_write"`. The create result carries the type's own instructions — page files, `canvas.json`, how artboards are laid out. **Follow those rather than anything remembered here**; the type evolves.
3. Fill it by publishing your data files to the returned `url`.

Title: what it is, two to four words, plus the round's nature if useful — "Poster Shelf", "Voice Ripple · Directions", "Product Details Review · Redesign". For a continuation, update the existing canvas by its `url` (read it first) instead of creating a second one.

## 3. A frame kit and a generator

Twelve hand-written frames drift apart; generated ones stay consistent and make round 2 a ten-minute job. In the session scratchpad keep a small folder per canvas:

- `lib.mjs` — the kit: phone frame at **390 pt** wide, status bar, header with back chip, `Screen` body, footer with the one full-width primary CTA, and the Koshi anatomies you captured in §1 (directory row with Gujarati-initial avatar, section label, card, pill, 48dp row, sheet, AlertDialog, snackbar). Colours and radii as CSS variables copied from `src/global.css` — both themes if the direction's idea depends on dark.
- `build.mjs` — composes frames from the kit into the canvas's page files + `canvas.json`.
- Every frame carries a small caption outside the phone: the letter + name ("B2 · Bin beside the button — after the tap") and, where it matters, the measured length.
- A notes board per page: the diagnosis, what is shared by every direction, the cost of each, the open questions. On round 2+, the user's constraint in their own words at the top.

Keep copy real (see the skill, step 4) and keep the floors: if the kit's row is 48dp and its text 16 px, no frame can quietly cheat.

## 4. Measuring

Claims like "2.7 screens instead of 4.0" are what let the user choose between calm and complete — so make them true. Render the direction's full-length content as a plain-HTML twin at 390 pt (the generator can emit it), serve it on localhost, read `scrollHeight` with `javascript_tool`, divide by 844. Put the number on the frame caption and in the chat summary. For a "fits one phone" claim, the twin must not scroll at 390×844 — check, don't assume.

## 5. Rounds and finals

- A new round is a **new page that opens first**; earlier rounds move behind it, untouched. Name pages for what they are: "Round 2 · One screen", "Round 3 · Complete, one screen".
- A pick with changes becomes **the final** on page 1 (same letter, e.g. "J · final"); the explored alternatives stay on later pages. The build is held against this page.
- Build the round by loading the published canvas state and appending, not by regenerating everything — that is how earlier rounds survive exactly as the user saw them.

## 6. When the scratchpad is gone

Scratchpads are per-session and get wiped. The published artifact is the durable copy: read it back (`Artifact {action: "read", url}` and its files listing), re-seed `lib.mjs` from the frames' markup, and carry on. Record in the memory file which canvas a kit came from ("frame shell from the enrichment-onboarding canvas") so the next session knows where to re-seed from — several Koshi canvases already share one kit.
