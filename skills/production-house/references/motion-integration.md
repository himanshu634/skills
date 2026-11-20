# Handing off to Motion

This skill decides **what** the film is; Motion's type instructions decide **how** it's
written. Motion's instructions win on mechanics; if they change a limit, update
`scripts/motion.json`.

## 1. Before the first write

- Gates 1 and 2 passed; for a full film, Gate 3 too (lock `approved`).
- `python3 scripts/brief.py validate brief.json --lock LOCK.md` passes.
- Every decision made: Motion builds without stopping.

## 2. Motion's three questions

The lock and brief settle Style, Colors, Length. `brief.py settle` prints the line, e.g.:

> Animation details — Style: Sunny cut paper, rounded paper characters with ink outlines,
> high-key window light, full frame, paper texture · Colors: #F6E7C8 #E86F4F #9CC7B0
> #F2B33D · Length: 48 s

State it when starting the film.

## 3. Creating the film

Artifact tool `list` (scope `types`) → Motion type → create with a real title; use the
returned `url` for every later call.

## 4. First batch

```bash
python3 scripts/brief.py scenes  brief.json --lock LOCK.md   # modules/scenes.json
python3 scripts/brief.py basecss brief.json --lock LOCK.md   # first modules/base.css
```

`scenes.json`'s look string carries the lock id and version, so later sessions know which
lock built the film.

## 5. Installing the kit

Write `modules/shared.js` (`kind` js) with the exact output of
`python3 scripts/lock.py shared LOCK.md`. Never edit it: lint check U6 compares it byte for
byte, because a changed `shared.js` is how a series drifts. Anything missing goes back to
the art department. Keep `--ground --main --second --accent` in `base.css`; the kit reads them.

## 6. Scenes

One module per Motion scene, in order, one write per message. A scene places lock cast in
lock sets and acts:

```js
const TT = { open: 1.2, stop: 5.0 };
kit.scene('office', {
  init(kit) {
    this.set = SERIES.sets.office(kit);
    this.host = SERIES.cast.host(kit, this.set.figures, { x: 1378, y: 836, h: 340, facing: -1 });
    this.lamp = SERIES.light.lamp(kit, { x: 0.62, y: 0.45, parent: this.set.cam, before: this.set.figures });
    this.cam = SERIES.lens.locked(kit, this.set.cam);
    SERIES.frame(kit);
  },
  render(t) {
    this.cam.apply(t);
    this.host.pose({ head: PH.key(t, [[TT.stop, 0], [TT.stop + 1.2, -7]]) });
    this.lamp.render(t);
    SERIES.finish(kit, t);
  },
});
```

`init`: set → cast → lights (`before` figures) → living → lens → `SERIES.frame` last.
`render(t)`: lens → poses → lights → living → `SERIES.finish` last.

| Brief field | Scene code |
|---|---|
| `set` | `SERIES.sets.<id>(kit)`; `{"local": ...}` drawn in the scene, kept small |
| `cast` | `SERIES.cast.<id>(kit, set.figures, {...})`, `.pose({...})` |
| `light` | `SERIES.light.<recipe>(kit, {...opts, parent: set.cam, before: set.figures})`, `.render(t)` |
| `lens` | `SERIES.lens.<mode>(kit, layers, opts)`, `.apply(t)` |
| `living` | `SERIES.living.<name>(...)`, `.render(t)` |
| `holds` | Clamp local time; keep life on |
| `beats` | Named times in `TT` |
| `text` | One `.words` block, faded with `PH.fade` |

~2,000 characters per scene (3,500 max).

## 7. Score

Last, stage final: `modules/score.js` with `kit.score(function (S, T) { ... })`, per the
bible's sound section and `references/departments/ear.md`.

## 8. After the build

Motion's closing message stays short. Then, if wanted: lint (phase 8), post sheet (phase 9).
Revisions: only the modules asked about, stable ids, never `shared.js`.

## Motion rules no lock overrides

- ≤3 flashes or cuts per second; no scene under 1 s.
- Fit to show coworkers; no propaganda looks or regime symbols.
- No known characters, film scenes, logos or existing music.
- First frame is the thumbnail: never black or empty.
- Sheets are pre-production; never deliver stills as the film.
- Markup in single-quoted strings, styles in double quotes, no nested quotes.

Product-film defaults a series may override (gradients for light, 24 fps, silence,
palettes): `references/departments/contradictions.md`; record overrides in the bible.
