# Design and animation

## Production designer

**Novice error:** designing scene by scene; episode six stops matching episode one.

**Design the world once, as code:**
- **Design language**: one way of making everything, from style research.
- **Palette per world**: four colors (ground, main, second, accent) in the lock's spec;
  the accent has one job (power object, a single light, a scarf). Scenes pick a world, never a hex.
- **Outlines**: in flat styles, period and character live in outline (hat brims, coat
  lengths, shoulders, vehicles, rooflines). A character reads by outline at 200 px.
- **Sets as functions** (`SERIES.sets.<id>`) with named anchors. Architecture is staging:
  thresholds, desks, windows, stairs decide who is inside.
- **Typography** from where the world's lettering lived (signs, newspapers, comics,
  chalkboards, marquees); a Google family of that kind; avoid overused defaults.
- **Power object**: one invented object that changes hands as power does; the project's
  own, never a famous film's motif.
- **Reduce**: shapes that read at a glance; detail only where the eye goes.

## Animator

**Novice error:** fighting the medium. Code animation does lip-sync and realistic motion badly.

**Make the limits a language:**
- **A forgiving construction** built as `PH.rig`: jointed flat parts, cut-out puppets,
  squashable rounded forms, masks. Decide what carries acting: posture, timing, or one
  expressive part (eyes, tail, hat).
- **Act through timing**: a hand stopping mid-gesture, a late head turn, a pause before a door.
- **Motion signature in the bible**: easing family; overshoot or none (drama: none on
  people; comedy: overshoot is the joke); speed by power; hold lengths. Hard rules go in
  the spec (`forbid` with `unless: "comic"`).
- **Moving holds**: a held character still lives (breath, blink, sway), and so does its
  world. A frozen frame reads as a bug.
- **Characters as functions** (`SERIES.cast.<id>`) with `pose()` in their own terms.

## In the brief

```json
"set": "office",
"cast": [{"id": "keeper", "moves": "none until 6.0 s"}],
"living": ["smoke"],
"holds": [{"from": 6.0, "to": 9.0, "who": "keeper"}],
"power_object": {"what": "the chair", "state": "empty at end"}
```
