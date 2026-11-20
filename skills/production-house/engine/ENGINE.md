# PH engine API (`window.PH`, v2.0)

Look-neutral core: no palette, recipe, lens grammar or character. A series layer composes
it into a look (`references/art-department.md`); both are frozen in the lock.

Stage helpers take the **scene's** `kit` first. Everything is pure in `t`: build in `init`,
drive in `render(t)`. Positions are stage fractions (1920×1080) unless marked px.

## Time

| Call | Returns |
|---|---|
| `PH.key(t, [[t0, v0], ...], ease?)` | Eased value between keys (numbers or arrays); equal keys = hold; `ease` is a function or name |
| `PH.ease.linear / inOut / out / in / sine / back` | Easings (`back` overshoots) |
| `PH.fade(t, a, b, c?, d?)` | Opacity in over [a,b], out over [c,d] |
| `PH.osc(t, period, amp, phase?)` | Sine |
| `PH.seg`, `PH.lerp`, `PH.clamp01`, `PH.mod1` | Basics |
| `PH.noise(seed)` → `x => -1..1` | Smooth noise |
| `PH.rng(seed)` → `() => 0..1` | Deterministic random; never `Math.random` |

## Stage and DOM

| Call | Does |
|---|---|
| `PH.layer(kit, parent?, {z, before, clip, css})` | Full-stage div layer |
| `PH.svg(kit, parent?, {z, before})` | Full-stage SVG in stage px |
| `PH.el(tag, attrs, parent)` | One SVG element |
| `PH.div(kit, parent, css, before?)` | One absolute div |
| `PH.mix(color, pct, other?)` | `color-mix()` string; use with `var(--ground)` etc. |
| `PH.W(kit)`, `PH.H(kit)` | Stage size |

## Picture and frame

| Call | Does |
|---|---|
| `PH.matte(kit, {aspect, color, z})` | Bars to an aspect (wider → top/bottom, narrower → sides, `0` none); sets the picture area; last in `init` |
| `PH.picture(kit)` | `{x, y, w, h}` |
| `PH.clip(kit, ctx)` | Clip a canvas context to the picture |

## Shared canvas

| Call | Does |
|---|---|
| `PH.texture(kit, t, {amount, rate, mode, size, blend})` | Surface texture; `mode` `'grain'` or `'soft'` (seamless, paper-like); `rate` per second, `0` static |
| `PH.particles(kit, {n, seed, init(r, i), draw(ctx, state, t, i)})` → `{render(t)}` | Canvas particles, clipped to the picture |
| `PH.sprites(kit, parent, {n, css(i), place(i, t)})` → `{render(t)}` | DOM sprites; `place` → `{x, y, s, sx, sy, r, o}` |
| `PH.ctx(kit)` | Canvas context |

## Light primitives

All take `{parent, before, z}` (insert `before: set.figures` so light falls behind the cast)
and `background` to replace the default gradient.

| Call | Draws |
|---|---|
| `PH.shade(kit, {dark, shape: 'radial', x, y, rx, ry, inner})` | Darkness with a soft hole; `shape: 'linear'` takes `angle`, `from` |
| `PH.pool(kit, {x, y, rx, ry, color, stops})` | Radial pool; `stops` `[[pct, alpha%], ...]` |
| `PH.beam(kit, {poly: [[x, y], ...], color, angle, a0, a1, blur})` | Polygon of light (door spill, lamp cone, spot) |
| `PH.wash(kit, {angle, color, a0, reach})` | Directional wash (sun, sky, window wall) |
| `PH.glow(kit, {x, y, size, h, color, core})` | Visible source (bulb, flame, moon) |
| `PH.light(kit, {parts: [{el, k, flick}], keys, flicker, seed, blackout: {dark}})` → `{render(t), level(t)}` | Drives layers: `keys` `[[t, level]]`; `flicker` 0..0.08 (never a strobe); `flick` = share of flicker per part; `blackout` darkens as level falls |

## Camera

| Call | Does |
|---|---|
| `PH.camera(kit, layers, motion(t) → {s, x, y, r}, {fx, fy})` → `{apply(t), state}` | Moves `el` or `[[el, depth], ...]` (1 main, <1 far, >1 near) |
| `PH.shake(seed)` → `(t, amp, roll, speed) → {x, y, r}` | Smooth handheld |
| `PH.cover(kit, deg)` | Scale keeping a rotated frame covered |

## Rigs

| Call | Does |
|---|---|
| `PH.rig(kit, svg, {x, y, scale, facing, fill, stroke, strokeWidth, filter, parts})` → `{root, part(id), pose(p)}` | Jointed character of any design. `parts`: `[{id, parent, pivot: [x, y], draw}]` in rig units (feet 0,0; up negative); `draw` = path string or `function (g, PH)`. `pose({x, y, lean, opacity, joints: {id: angle or {r, sx, sy, dx, dy}}})` |
| `PH.gait(t, a, b, x0, x1, steps, ease?)` → `{x, phase, moving, swing, lift}` | Walk or hop over [a,b] |
| `PH.rim(node, color, dx, dy)` | Thin edge light (drop-shadow) |

Overlapping shapes in one part: separate elements via a `draw` function, not subpaths
(opposite winding punches holes).

## Scene order

`init`: set → cast → lights (`before` figures) → living → lens → `SERIES.frame(kit)`.
`render(t)`: lens → poses → lights → living → `SERIES.finish(kit, t)`. Example:
`engine/example-scene.js`.
