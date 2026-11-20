---
name: "production-house"
description: Film-studio pipeline for story-driven animation in Claude's Motion artifact type. Researches genre, period and place; runs a writers' room where every department reviews the screenplay; researches animation styles against what the screenplay demands; builds the series' own look as code and sketches its sets and characters for approval; then shoots. Each series' look is frozen in a series lock kept in the project, so later episodes match. Use whenever the user wants a film, scene, episode, series, short, trailer or story animated in Motion and cares how it looks and plays, or mentions a script, screenplay, treatment, storyboard, series bible, saga, director, DOP, lighting, character or set design, even without saying cinematic. Also use when a project has a series lock file. Not for product demos, UI walkthroughs, explainers or logo stings.
---

# Production House

Sits upstream of Motion: Motion builds films from code; this skill researches, writes,
designs, lights and directs them first, in studio order.

- **Each series gets its own look, from research.** The skill ships no look, only a
  look-neutral engine (`engine/engine.js`) and a method. The art department composes the
  engine into the series' kit: light recipes, lens grammar, textures, characters, sets.
- **Within a series, the look never drifts.** The approved kit, its spec and the bible are
  frozen in one **series lock** file the user keeps in the project. Later films install it
  verbatim; checks reject anything it doesn't define. It changes only by an approved
  version bump.

## Pipeline

| Phase | Produces | Read |
|---|---|---|
| 0. Intake | New series, or continuing (lock found) | `references/series-lock.md` |
| 1. Research | Fingerprint + dossier | `references/research-method.md` |
| 2. Questions | ≤5 answers with defaults | `references/questions.md` |
| 3. Writers' room | Screenplay reviewed by every department | `references/writers-room.md` |
| **Gate 1** | **Screenplay approved** | |
| 4. Art department | Style research → draft kit → art board | `references/art-department.md`, `engine/ENGINE.md` |
| **Gate 2** | **Look, sets, characters approved** | |
| 5. Shot brief | JSON brief validated against the lock | `references/departments/*.md`, `templates/brief.example.json` |
| 6. Tone test | 6–10 s Motion film of the riskiest scene | `references/motion-integration.md` |
| **Gate 3** | **Tone test approved → lock frozen, handed over** | `references/series-lock.md` |
| 7. Shoot | The Motion film | `references/motion-integration.md` |
| 8. Check | Lint, frame report, viewer tests | `references/quality-checks.md` |
| 9. Post handoff | Cue sheet, VO to timecode | `templates/post-handoff.md` |

Gate messages are short: what to open, the 2–3 decisions that matter, what comes next.
Make requested changes and show them again; a gate passes only on clear approval. If the
user explicitly asks to skip a gate, state in one line what's skipped and the risk.

### 0. Intake

Look first for a series lock (a file starting `production-house:lock`, often
`<series>-lock.md`, in project files, the conversation, or named in project instructions),
then a script, treatment, playbook, drawings, earlier films.

- **Lock found (continuing series):** `scripts/lock.py check`, then unpack. The lock
  outranks fresh ideas. Research only what's new; writers' room as usual; art department
  only for new sets or characters (minor bump); no tone test unless the look changed.
- **No lock (new series):** run every phase.

If the user names a copyrighted story they don't own, say once that Motion won't depict its
characters, scenes or music, offer an original story in the same tradition, and continue
(`references/originality.md`).

### 1. Research

Fingerprint the script; study 5–7 films across four lanes (genre, made-in-period, place,
medium); triangulate (a principle needs ≥2 films; one-film traits go under "don't copy");
translate each principle into a department decision. Tag findings *observed*,
*documented* or *recalled*; never present recalled as observed. Dossier readable in two
minutes. Nothing here presumes darkness, letterbox, grain, silhouettes or a still camera;
those are one genre's answers.

### 2. Questions

≤5, each with a researched one-tap default (use the question tool when available). Only
what changes the film and research can't settle: voice model, audience, fidelity, length.
Never the look or palette; the art department answers those with pictures.

### 3. Writers' room → Gate 1

Screenwriter drafts from the dossier (`templates/screenplay.md`). Table read: director, DOP,
lighting, production designer, animator, sound, editor, continuity & standards; ≤3 notes
each, each with why, fix, cost. Conflicts resolved by the "about" sentence, then the
ledger, then cost. Revise once; deliver screenplay + change log + ≤3 open decisions, as a
Claude Doc when Docs tools are available.

### 4. Art department → Gate 2

1. **Style research.** From the approved screenplay, list what it demands of animation
   (crowds, action, intimacy, weather, period, runtime). Research 4–6 animated works
   across ≥3 techniques that solved those demands; score each technique on fit and on
   what the engine can render; triangulate; propose 1–2 directions.
2. **Look development.** Each department sets its part of the look (language, frame,
   texture, light logic, lens grammar, palettes, type, character construction, motion
   signature), each citing its principle. Two directions → render both on one key set;
   the user picks.
3. **Draft kit.** Series layer (`templates/series-layer.js`) with named recipes, modes,
   living elements, frame, finish, and every recurring set and character as a function;
   spec (`templates/series-spec.example.json`); pack a draft lock with `lock.py pack`.
4. **Art board.** Sheet modules rendered by the kit itself (`scripts/board.py`), checked
   against the draft spec, published for comments. Revise and republish to the same link.

### 5. Shot brief

`templates/brief.example.json`. Every scene names its screenplay scene, ledger, set, cast,
light recipes, lens mode, living elements, holds, beats, sound, using only lock names.
Resolve department conflicts in the brief (`references/departments/contradictions.md`).
`python3 scripts/brief.py validate brief.json --lock LOCK.md`

### 6. Tone test → Gate 3

Riskiest scene as its own 6–10 s Motion film on the draft lock (`"kind": "tone-test"`).
On approval: record it in the bible, `lock.py pack --status approved`, present the lock
file for the project's files with the `lock.py instructions` snippet.

### 7. Shoot

Follow Motion's type instructions for mechanics. Install `lock.py shared LOCK.md` verbatim
as `modules/shared.js`; one scene module per Motion scene.

### 8. Check

`scripts/lint_scenes.py OUT_DIR --lock LOCK.md --brief brief.json` (universal checks +
series contract). Fix all errors in one round; report warnings. With exported frames or
MP4: `scripts/analyze_frames.py FILES --lock LOCK.md`. Hand over the viewer tests.

### 9. Post handoff

`templates/post-handoff.md`: timecodes, VO to timecode, cues, silences, composer notes.

## Non-negotiables

- **Original work only** (`references/originality.md`).
- **The look comes from this series' research**; every look decision cites its principle.
- **The lock is law in its series**: kit installed verbatim, only its vocabulary used. New
  sets, characters or recipes go through the art department and a bump; never invent one
  in a scene.
- **Gates are the user's**: no shooting before Gate 2, no full film before Gate 3, unless
  the user explicitly skips.
- **Fit to show at work**: harm implied, never graphic; no regime imagery; no stereotypes.
- **≤3 flashes per second**; the first frame is never black.
