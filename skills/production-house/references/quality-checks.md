# Quality checks

**Universal** checks hold for every film. **Series** checks are whatever the lock's spec
declares; no series inherits another's rules.

## Universal: code (`scripts/lint_scenes.py`)

| # | Check |
|---|---|
| U1 | Every scene in `scenes.json` has a module |
| U2 | Scene ≤3,500 characters (aim ~2,000) |
| U3 | Durations match the brief within 0.1 s |
| U4 | No `Math.random`, clocks, timers, CSS transitions or animations |
| U5 | No quote nested in `style="..."` |
| U6 | `shared.js` is the lock's build, byte for byte |
| U7 | Only lock-defined recipes, modes, cast, sets, helpers |
| U8 | Palette not only black/red/white-cream unless the spec allows |
| U9 | A draft lock shoots only a tone test |

## Universal: frames and film (`scripts/analyze_frames.py`)

| # | Check |
|---|---|
| U1 | No empty frame |
| U2 | First frame works as a thumbnail |
| U3 | ≤3 flashes in any second (video input) |

## Series: `scene_contract` (lint)

| Field | Meaning | Example |
|---|---|---|
| `require` | Calls every scene makes | `{"call": "SERIES.finish(", "why": "grain is the look"}` |
| `require_any` | One of a group | `{"calls": ["SERIES.light."], "why": "every light is a source"}` |
| `forbid` | Never used; `unless` = brief flag that lifts it | `{"pattern": "ease\\.back", "why": "no overshoot", "unless": "comic"}` |
| `budgets` | Lens modes per minute or film | `{"lens_mode": "push", "per_60s": 1, "min": 1}` |
| `max_words_per_scene` | Outside first and last scene | `12` |
| `allow_black_red_white` | User asked for that palette | `false` |

## Series: `frames` (declare only what the look stands behind)

| Field | Measures | For |
|---|---|---|
| `dark_share {threshold, min, max}` | Share below a luminance | low-key (min), high-key (low max) |
| `bright_share {threshold, min, max}` | Share above a luminance | high-key |
| `highlight {min}` | Brightest 0.3% | looks needing something lit |
| `light_offset {min}` | Lit centroid off centre | directional light |
| `texture_in_darks {min}` | Fine texture in darks | dark looks on phones (banding) |
| `matte {aspect, tol_px}` | Bars match aspect; `0` = none | every series |

Thresholds come from approved board values (`board/checks.json`), with margin.

## Viewer tests (hand to the user; record results in the bible)

1. **Cold viewers**: 3–5 people with no context answer *who holds power at the end?* and
   *one word for the feeling*. Pass: most match the ledger and "about".
2. **Phone**: MP4 on a phone at normal brightness. Pass: no banding, characters read, text legible.
3. **Consistency**: frame beside an earlier episode's. Pass: a stranger can't tell sessions apart.
4. **Professional review**: an animator or cinematographer leaves timecoded comments.
5. **Originality**: someone who knows the genre's famous films finds nothing borrowed.
6. **Lock repeatability** (new lock or major bump): same brief built in two sessions; both
   pass lint, frame checks and the consistency test.
