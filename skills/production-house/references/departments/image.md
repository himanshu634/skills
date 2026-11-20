# Camera and light

How to decide, not what to decide: a noir and a nursery comedy both come out of this,
looking nothing alike.

## DOP

**Novice error:** the camera costs nothing in code, so it moves constantly and means nothing.

**A lens grammar, before any scene.** Name each camera state and its meaning; build each as
`SERIES.lens.<mode>` on `PH.camera`. The camera then tells the story with the sound off.

| Series kind | Modes → meaning |
|---|---|
| Restrained drama | `locked` order, power held · `push` turning point (rationed) · `drift` unease · `unsteady` control slipping |
| Comedy | `still` setup · `bob` play · `snap` punchline (fast push, hold) |
| Documentary memory | `handheld` the present · `pan` the archive |

Ration the heaviest mode via spec `budgets`.

**Shot size** (share of frame height a standing figure fills): wide ≤25%, medium 40–70%,
close ≥60%. **Composition**: symmetry and centre for institutions; off-centre with negative
space for isolation; foreground layers for depth.

**Frame**: 16:9 is a choice. Letterbox (1.85, 2.39) reads as cinema; pillarbox (4:3, 1:1)
as memory or intimacy. Text and key action stay inside the picture.

## Lighting

**Novice error:** lighting everything "so viewers can see"; flat in any genre.

**Pick a light logic from research; hold the series to it.**
- **Motivated**: every light a source in the world, drawn or obvious from its shape;
  darkness is content. Realist, period, crime, horror. Spec: `dark_share` (e.g. 30–55%),
  `highlight`, `light_offset`.
- **High-key**: even light, soft few shadows, color carries emotion. Comedy, children's,
  musicals. Spec: high `bright_share`, low `dark_share` max.
- **Graphic**: light as designed shapes (diagonal, pool, spot on flat ground). Fables,
  titles, stylized action.
- **Expressionist**: light bends with a character's state. Psychological stories; budget
  it like a camera move.

Build the logic once as `SERIES.light.<recipe>` from engine primitives; give each world a
recipe and palette in the bible. In every logic, **light changes are story events** (a lamp
off, a door opening, a cloud passing).

**Manage:** deep darks band on phones after compression (texture in darks, gradients not
flat fills; `texture_in_darks`); very bright frames dilute the accent (one saturated
accent, one meaning).

## In the brief

```json
"lens": {"mode": "locked", "opts": {"fx": 0.6}},
"light": [{"recipe": "lamp", "opts": {"x": 0.72, "y": 0.30, "flicker": 0.03}}],
"palette": "home"
```

Names must exist in the lock; `brief.py` rejects others.
