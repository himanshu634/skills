---
name: design-directions
description: Mockups-first design workflow for Koshi — grounds the request in the live app, pulls in the design skills (`frontend-design`, `ui-ux-pro-max`, the `design:*` plugin skills, plus `animate-expo`, `dataviz` and others as the brief needs), draws 3–4 named directions (A/B/C/D) on one design canvas for the user to review, then reads the reply — a pick gets built, feedback gets a new round. Use whenever the user asks to design, redesign, mock up, restyle or "improve the UI/UX of" a screen, flow, component or state; says a screen is cluttered, confusing, generic, ugly or "not intuitive"; sends a screenshot and asks for something better; asks for "options", "directions", "variations" or "mockups"; or replies to an earlier canvas ("go with B", "I like J but…", "redo these"). Use it even when they don't say "mockup" — in this repo a design request means mockups before code. Not for a change the user has already specified exactly (just make it), or for scaffolding a component whose design is settled (`new-component`).
---

# Design directions: mockups first, then the pick, then the build

The user decides design by looking, not by reading a plan. Every design request in this repo that went well followed the same loop: look at the real screen → draw a few genuinely different answers on one canvas → the user picks, mixes or pushes back → only then code. Every one that went badly skipped a step: frames drawn from tokens instead of the running app were rejected as "generic"; a redesign that hid information cost two rounds before the real constraint surfaced. This skill is that loop, with the lessons kept.

```
brief → ground in the live app → load the design skills → 3–4 directions on a canvas
      → present + STOP → read the reply ─┬─ pick / mix      → build in a worktree → PR when asked
                                          └─ feedback / no   → next round on the same canvas
```

Nothing under `src/` changes before a pick. The canvas is cheap to throw away; a half-built screen in the wrong direction is not.

## 1. Frame the brief

Say back, in two or three lines, what you are designing: the screen or flow (file path), what the retailer is trying to get done there (`design-philosophy.md` → "Who we design for"), the requirement IDs it lives under, and what is wrong today in the user's words.

Before anything else, check whether this is a continuation:

- **Memory** — a `*-directions.md` record for the same screen means there is already a canvas, a history of rejected ideas and possibly a pick. Continue that canvas; never restart from A.
- **`gh pr list --state all --search "<keywords>"`** — concurrent sessions have built the same thing first before.

Ask only what you cannot infer and what changes the drawing (for example "one screen or may it become two steps?"). A garbled or dictated prompt that names no screen is a question to confirm, not a task to guess at.

## 2. Ground it in the real app

Read, in this order: `docs/00-product-context.md`, `docs/02-cross-cutting.md`, the module file for the area, `design-philosophy.md`, `design.md`, then the screen's code and the components it composes.

Then **look at the screen running**. Frames are drawn from the app's real anatomy — its directory rows, hero cards, section labels, footer CTA — because that is what reads as "Koshi" to the user; a frame that only gets the hexes and the 48dp right still looks like a template. How to get screenshots from expo web with mocks, and the traps around ports and sibling worktrees, are in `references/canvas.md`. If the user sent phone screenshots, those are the ground truth for "today".

Finish with a **diagnosis you can measure**, because "cleaner" is not a brief: how many phone-heights the screen scrolls at 390 pt, how many blocks compete at one volume, which things need him versus which are merely shown, what is said more than once, what overflows or clips. The diagnosis becomes the **Today** frame on the canvas and the yardstick every direction is compared against ("4.0 screens → 2.7").

## 3. Load the design skills

Invoke these with the Skill tool — don't work from memory of them, they change. Use what the brief needs; the first three are the default set for any new-screen or redesign request.

| Skill                                               | What it is for here                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `frontend-design`                                   | The point of view: one idea per direction, one signature moment, copy as design material, the self-critique pass. Koshi's palette, type and sizing are ratified (`design.md`), so spend the boldness on **structure, hierarchy, the hero moment and motion** — not on a new colour or typeface.                             |
| `ui-ux-pro-max`                                     | Evidence for the choices: query the UX outcome you need (`--domain ux`), then `--stack react-native`. Results are recommendations — where they disagree with the repo (its 44 px touch floor vs Koshi's 48dp, X-U1) the repo wins. If a query returns nothing useful, say so and move on rather than padding the rationale. |
| `design:design-critique`                            | Twice: on **Today** (sharpens the diagnosis) and on your own draft frames before you publish them.                                                                                                                                                                                                                          |
| `design:ux-copy`                                    | Labels, empty states, errors, confirmations. Mockup copy is English; the shipped copy is Gujarati-first and goes through `add-i18n-key` at build time.                                                                                                                                                                      |
| `design:accessibility-review`                       | Contrast, target size, selected-state-is-more-than-colour (X-U3) — when a direction introduces a new control or a tinted surface.                                                                                                                                                                                           |
| `design:design-system`                              | When a direction needs a pattern `src/components/` doesn't have — decide whether it extends an existing component before inventing one.                                                                                                                                                                                     |
| `design:user-research`, `design:research-synthesis` | When the user brings retailer feedback, field notes or recordings as the reason for the redesign.                                                                                                                                                                                                                           |
| `animate-expo`                                      | Any direction whose idea _is_ motion (a wait screen, a transition, press feedback). Draw the rest pose and the reduced-motion frame too.                                                                                                                                                                                    |
| `dataviz`                                           | A direction with a chart, stat tile or meter.                                                                                                                                                                                                                                                                               |
| `product-management:product-brainstorming`          | The problem itself is unclear and drawing would be premature.                                                                                                                                                                                                                                                               |

If a skill named here isn't in this session's list, carry on without it and say which one was missing — don't stall. If the brief touches something this table doesn't cover, look through the available skills for one that does; the table is a starting set, not a fence.

## 4. Draw 3–4 directions

**Different ideas, not different paint.** Each direction answers the diagnosis with a different structural bet — what comes first, what is grouped, what becomes its own step, what the hero is. If two directions differ only in colour, radius or icon, they are one direction; merge them and find another idea. Three strong directions beat four where one is filler.

- **Letter + name, and they stay stable**: "A · Needs you first", "B · The product, then rows". The user replies with letters, memory records them, PRs cite them. A new round continues the alphabet (round 2 is E–H; skip I and O, they read as digits) — a letter is never reused for a different idea.
- **Show the states that decide it**, not one happy frame: the landing, the key interaction, and the edge that breaks weak designs — empty, error, offline, a long Gujarati name, six items instead of two. Two or three frames per direction is typical.
- **Real content**: real product names, Gujarati farmer names as data, Latin numerals, plausible amounts. UI copy in English for now (a standing preference for mockups — the app itself stays Gujarati-primary, P1).
- **The floors hold in a mockup too**: 48dp controls, 16 px text, one primary action per screen, destructive actions behind a confirm. A direction that only works at `text-sm` is not a direction.
- **Shared fixes go in every direction** and are listed once ("in every direction: uses grouped by source, the warning said once"). That keeps the choice about the idea, not about who got the bug fix.
- **Say what each costs**: new components, new copy, a backend ask, a requirement that would change (cite the ID; append, never renumber). If a direction would settle one of the open decisions D1–D7, flag it on the canvas as a question — do not settle it by drawing it.
- **Recommend one** and say why in a sentence. The user often overrules the recommendation; that is the canvas doing its job.

Build **one design canvas** (Artifact, design type) holding Today + all directions, so the user compares them side by side on one link. Mechanics — starting the canvas, the frame kit, measuring heights, adding a round as a new page, re-seeding a wiped generator — are in `references/canvas.md`. Before publishing, look at your own frames (screenshot or inspect them): text that overflows its pill, a CTA pushed off the frame, and a frame taller than you claimed are all things the user will see first.

## 5. Present, record, stop

The chat message is short, because the canvas does the talking:

```
Canvas: <link>
Today — <the measured diagnosis, one line>
A · <name> — <the bet, one line> (<length / cost>)
B · …
C · …
In every direction: <shared fixes>
I'd pick <letter>: <why, one sentence>.
Open questions: <at most three, each answerable in a word>
Pick a letter, mix them ("B with A's header"), or tell me what's off.
```

Write the memory record now, not after the build: `<topic>-directions.md` with the canvas link, the directions by letter and name, the recommendation, the open questions and "wait for a pick" — plus the `MEMORY.md` line. The next session (or the next round) starts from it.

Then stop. No worktree, no component, no i18n key until the user answers.

## 6. Read the reply

The reply is rarely a bare letter. Work out which of these it is — and when it could be two, ask one short question rather than building on a guess.

| They say                                                                     | It means                            | Do                                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------- | ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Go with B" · "B, build it" · "implement C"                                  | Pick **and** go-ahead               | Record PICKED, go to step 7. Open questions left unanswered take your recommended default — list each under _Decisions_ in the PR.                                                                                                                                         |
| "I like J" · "J looks good" — no build verb                                  | A pick, maybe not a go-ahead        | Record PICKED. If open questions remain, ask them with "…then I'll build it"; if none remain, say you're starting and start.                                                                                                                                               |
| "B, but move the total up" · "A with C's footer"                             | Pick with a change, or a mix        | Redraw it as **the final** on page 1 of the same canvas, share it, then build on their OK. Small, unambiguous changes ("make the fill light red") can be drawn and built in one go — say so.                                                                               |
| "Too busy" · "keep it one screen" · "must show everything" · "none of these" | A **constraint** not stated before  | New round. Write the constraint down in their exact words — on the canvas page and in memory — then draw new letters that obey it. Don't re-offer a rejected idea in new clothes; if two rounds taught "never hide information here", round three does not contain a fold. |
| "Looks generic" · "doesn't match the app"                                    | The grounding failed, not the ideas | Back to step 2: fresh screenshots of the real screens, redraw the same ideas on the real anatomy.                                                                                                                                                                          |
| A question ("what happens offline in B?")                                    | They are still deciding             | Answer it — add the frame if a picture answers it better. The canvas stands.                                                                                                                                                                                               |
| Three rounds, no pick                                                        | The brief is off, not the drawings  | Stop drawing. Say what the rounds had in common and ask what about _that_ is wrong.                                                                                                                                                                                        |

Each new round goes on the **same canvas** as a new page that opens first, with earlier rounds kept behind it — the history of what was rejected, and why, is part of the design. Update the memory record every round: what was rejected, the constraint learned, the new letters.

## 7. Build the pick

Now it is an ordinary Koshi feature, and the repo's rules take over:

1. **Worktree off `staging`** (`EnterWorktree`). Check `git log --oneline origin/staging..HEAD` is empty before your first commit — a fresh worktree can start from a local head that carries someone else's commit.
2. **Spec first**: add or amend the requirement in the module's doc (new ID appended), and `design.md` if the direction adds a pattern or a motion value. Same PR.
3. **Build from the library**: compose `src/components/`; anything missing goes through the `new-component` skill (four floors, gallery section). Copy goes through `add-i18n-key`, `gu/` first — new Gujarati you composed is provisional and gets a "Gujarati review" open item. Motion through `animate-expo`. Tests with `react-native-testing` / `tdd`.
4. **Hold it against the picked frame.** See it running where you can (expo web with mocks — `references/canvas.md` lists when a worktree can't) and compare to the canvas frame by frame. Report honestly what differs and what you could not see running; "never seen running — device pass open" is a legitimate line, a silent mismatch is not.
5. **Reviewers**: `ui-floor-reviewer` after any component change, `retailer-scope-reviewer` if a query or service moved.
6. **PR only when the user asks** — the `open-pr` skill. The body names the direction by letter and links the canvas.
7. **Memory**: the directions record becomes "X PICKED and BUILT (see `<branch>-branch`)", and the branch gets its own record under _Open branches_.

## What this skill is not for

- "Make the Discard button light red" — the user has already designed it. Do it (on the canvas if a round is open, in code if the build is).
- A bug that looks like a design problem (clipped label, swallowed touch). Diagnose it first; a redesign doesn't fix a `self-stretch`.
- Posters, icons, store graphics — visual assets, not app screens. `frontend-design` and the canvas still help; the ground-in-the-live-app and build steps don't apply.
