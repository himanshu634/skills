# Art department

Turns the approved screenplay and the dossier into the series' look, built as code, shown
as sketches drawn by that code. After Gate 2, every film renders with these functions.

## Contents
1. Style research
2. Look development
3. Look frames
4. The series layer
5. Sets and characters as code
6. The spec
7. Sheets and the art board
8. Review rounds and Gate 2
9. Extend mode

## 1. Style research

Runs after Gate 1, because the screenplay decides what the animation must do. Phase 1's
medium lane picked 1–2 films before the story existed; this goes further.

1. **Demands.** List 5–8 things the screenplay asks of animation, each tied to scenes:
   "two people held 10 s in one frame (S3)", "market crowd (S5)", "night rain (S6)",
   "a child among adults (S2)", "chase (S7)", period, tone, runtime.
2. **Survey.** 4–6 animated works spanning ≥3 techniques (cut-out, silhouette theatre,
   limited cel, ink and wash, painterly planes, rounded toy forms, collage, motion
   graphics), chosen because they solved these demands in a similar kind of story. Search
   each work separately (director or animator interviews, making-of notes, criticism);
   tag evidence as in `research-method.md` §4.
3. **Technique table**, one row per technique:

| Technique | Works | Handles demands | Struggles with | Engine fit | Signature (don't copy) |
|---|---|---|---|---|---|

   *Engine fit*: what `PH` renders well (flat shapes, layers, rigs, light primitives,
   particles, textures) and badly (lip-sync, fine hand acting, realistic motion, large
   detailed crowds), and the scene-budget cost.
4. **Triangulate.** A style principle needs ≥2 works; one-work traits are signatures.
5. **Directions.** Propose 1–2 directions, each a technique plus its principles, the
   demands it solves, and what it gives up. Add the table and directions to the dossier
   ("Style research") and to the playbook if one exists.

## 2. Look development

Each department sets its part from the chosen direction and the dossier. Record each in the
bible's look table (`templates/lock-bible.md`) with its principle, films, and the
alternative it beat.

| Decision | Owner | Range |
|---|---|---|
| Design language | Designer | from style research |
| Depth | DOP, designer | single plane, parallax layers, deep staging with foreground frames |
| Frame | DOP | 16:9, letterbox 1.85/2.39, pillarbox 4:3/1:1, drawn border |
| Texture | Designer | none, grain, paper, canvas, halftone, print registration |
| Light logic | Lighting | motivated, high-key, graphic, expressionist (`departments/image.md`) |
| Lens grammar | DOP | named camera states and what each means |
| Palette per world | Designer, lighting | four colors (ground, main, second, accent); accent has one job |
| Typography | Designer | from where the world's lettering lived |
| Character construction | Animator, designer | rig type, proportions, what carries acting |
| Motion signature | Animator | easing, overshoot or none, hold lengths, speed by power |
| Living frame | Animator, lighting | weather, smoke, steam, leaves, flicker, breathing, or nothing |

Every row must be defensible from this series' research. The checks hold a comedy to its
bright light as strictly as a noir to its darkness.

## 3. Look frames

Two directions from style research → build the key set (usually the turn's) in each, one
sheet each, on the first board. The user picks; build the rest in that direction. Never
more than two.

## 4. The series layer

Start from `templates/series-layer.js`; read `engine/ENGINE.md` first. It defines
`window.SERIES`:

| Key | Holds | Returns |
|---|---|---|
| `id`, `version` (semver), `engine` | Identity | |
| `look` | Plain values (aspect, fps, texture) | |
| `light.<recipe>(kit, opts)` | Recipes from `PH.shade/pool/beam/wash/glow/light` | `{render(t)}` |
| `lens.<mode>(kit, layers, opts)` | Camera states on `PH.camera` | `{apply(t)}` |
| `living.<name>(kit, ...)` | Atmosphere from `PH.particles/sprites` | `{render(t)}` |
| `frame(kit, opts)` | Matte, border or nothing; required, may be no-op | last in `init` |
| `finish(kit, t)` | Texture, grade; required, may be no-op | last in `render` |
| `cast.<id>(kit, svg, opts)` | Each recurring character | `{root, pose(p)}` |
| `sets.<id>(kit, opts)` | Each recurring location | `{cam, figures, anchors}` |
| other helpers | Shared builders (a figure factory, a sign painter) | |

Rules (the tooling and Motion depend on them):
- Load defines functions only; no DOM until a builder is called (`lock.py` loads it in
  node to read the vocabulary).
- Pure in `t`: `PH.rng`, never `Math.random`; no timers, no CSS transitions.
- Colors from `var(--ground|--main|--second|--accent)`.
- Name by story meaning (`lamp`, `kitchen`, `keeper`), not drawing method.

## 5. Sets and characters as code

Everything recurring is a lock function: it keeps episodes matching and scenes small.

- **Set**: builds ground, art and depth layers; returns `cam` (what the lens moves),
  `figures` (SVG for the cast; lights insert before it), `anchors` (door, desk, floor
  line). No lights inside sets; each scene lights its beat.
- **Character**: wraps `PH.rig`; `pose()` in the character's own terms. Opts at least
  `x`, `y` (feet), `h` (px), `facing`. Reads by outline at 200 px, recognizable at 80 px.
- **Extras**: one factory helper with variation parameters.

## 6. The spec

`templates/series-spec.example.json` makes the look measurable:

- `scene_contract`: `require`, `require_any`, `forbid` (with `unless` brief flag),
  lens `budgets`, `max_words_per_scene`, `allow_black_red_white`.
- `frames`: declare only checks the look stands behind (dark look: `dark_share`,
  `highlight`, `light_offset`, `texture_in_darks`; high-key: `bright_share`, low
  `dark_share` max; every series: `matte`).
- `palettes`, `fonts`, `stage.fps`, `look.name`, `look.line`.

Set thresholds from measured values in `board/checks.json` of approved sheets, with margin.

## 7. Sheets and the art board

One sheet module per item in `sheets/`, written like a Motion scene, headed by `@sheet`
(`templates/sheet.example.js`):
- **Sets**: key light, 1–2 moments. `check: true`.
- **Characters**: neutral, power pose, low pose, in motion. `check: false`.
- **Look frames** when there are two directions.

```bash
python3 scripts/lock.py pack --bible bible.md --spec spec.json --series series.js --out LOCK.md
python3 scripts/board.py LOCK.md sheets/ board/ --auto --note "What to look at"
```

`--auto` adds palettes-and-type and the cast lineup. The kit runs in headless Chromium
with a stand-in for Motion's scene API, so sheets are real renders. View every PNG
yourself; fix and re-render before showing. Publish `board/board.html` with the Artifact
tool; read comments with its `comments` action.

## 8. Review rounds and Gate 2

Each round: apply notes to layer, sheets or spec; repack the draft lock; re-render;
republish to the **same** link; list changes in 2–3 lines. Gate 2 passes on approval of
look, every set and every character. Record date and board link in the bible.

## 9. Extend mode

Continuing series: design only what the screenplay log flagged as new, in the lock's
existing language. Run style research only if a demand is new to the series (a first
crowd, a first chase). Sheet the new items plus one sheet placing new beside old. On
approval, repack with a minor bump and `--previous OLD.md`; changing an approved entry
needs a major bump and a new tone test.
