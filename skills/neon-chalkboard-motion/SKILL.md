---
name: "neon-chalkboard-motion"
description: "Load before making any motion video, animation or motion image in the Neon Chalkboard style - flat vector, dark board, neon accents, white chalk line-art, geometric characters."
---

# Neon Chalkboard Motion

A house style for explainer videos and motion graphics that make complex science, math and technical ideas easy to see. Every output must look like it came from the same channel. Treat the numbers below as fixed tokens, not suggestions. Change them only if the user asks.

The reference production is "The Planet Found With a Pen" (Neptune's discovery, 1:42, 1920x1080). When in doubt, match it.

## The five characteristics (what they mean in practice)

### 1. Flat vector art
- Every shape is a solid fill: circles, rounded rectangles, trapezoids, triangles. No gradients, no drop shadows, no glows, no blur, no textures, no 3D shading, no lighting.
- Detail comes from **flat bands and flat shapes**, never from shading. Example: a planet gets 2-4 horizontal bands in a lighter and a darker tint of its own color, plus one flat oval "spot", all clipped to the disk.
- Depth comes from **overlap and size** only. Tilted orbits are flat ellipses (ry ≈ 0.42 × rx), not perspective.
- Anti-aliased edges, crisp geometry. Rounded caps and joins on every stroke.

### 2. High-contrast palette
Dark void + neon accents. Use exactly these:

| token | hex | use |
|---|---|---|
| bg | #0B0F17 | the board / space; every frame starts here |
| panel | #111724 | flat lifted panels (a board-within-the-board) |
| deep | #05070C | telescope views, deep space inserts |
| chalk | #F2EFE8 | all line-art and main text |
| dim | #8A93A6 | secondary text, faint guides |
| pink | #FF4FA3 | primary accent: the problem, the protagonist, CTAs |
| blue | #3E8BFF (lt #7CB8FF, dk #2A62D6) | the answer / hero object |
| yellow | #FFD43B | predictions, targets, "look here", highlights |
| green | #2EE6A6 (dk #1FB585) | secondary character / secondary object |
| orange | #FF8A3D | minor objects only |
| skin / hair / leg / shoe / eye | #F6D2B0 / #39404F / #5A6378 / #C9CED8 / #11151F | characters only |

Rules: at most **3 accent colors on screen at once**. Give each accent one meaning per video and keep it: if yellow means "prediction", it never means anything else in that video. Highlighted words in text use the same accent as the object they refer to.

### 3. Chalkboard / diagram motif
- Background: flat bg plus a faint blueprint grid. Minor lines every 60 px at chalk 2.8% alpha, major lines every 240 px at 5.5%. The grid is always present and never animates.
- Line-art is thin white chalk: 2-3 px for orbits and guides (alpha 0.25-0.6), 3 px for active lines (alpha 0.8-0.9), 4 px for frames such as a telescope ring. Use dashed lines (dash 8-16 / gap 8-12) for predicted, hypothetical or invisible things, and solid lines for observed or real things.
- **Everything is drawn on, never popped on.** Lines reveal along their length (trim path 0→1, ease-in-out, 0.8-1.6 s) with a small chalk-white dot at the drawing tip (radius ≈ 1.4 × stroke width).
- Equations are set in **Latin Modern Math** with real typesetting: math-italic variables, true fractions, sub/superscripts. They are written on left→right with a clip reveal plus a chalk tip dot (≈1.5-2 s per line). Equations must be real and relevant to the topic, never decorative gibberish.
- Small labels: Inter Medium, ALL CAPS, 16-24 px, letter-spacing 3-5 px, in dim or the object's accent color. Examples: PREDICTED, OBSERVED, GRAVITY.
- Annotations follow the diagram grammar: arrows (3 px, 12-14 px heads), crosshairs, angle arcs, dashed rings, and "ping" rings that expand from an important point.

### 4. Stylized, abstract characters
Researchers are assembled from primitives, about 340 px tall at scale 1, with feet as the origin:
- head: circle r 38 in skin; hair as a flat hair-colored shape clipped to the head
- body: trapezoid coat (100 px shoulders → 132 px hem) in the character's accent color, with a chalk-white V for the shirt
- legs: two rounded rectangles in leg color; shoes are small rounded rectangles in shoe color
- arms: 21 px round-capped strokes in coat color, with a skin circle for each hand; animate by angle only
- face: **two dot eyes only**. No mouth, nose or eyebrows, and no anatomy. Eyes blink every ~3.7 s (they become a short line for 0.13 s).
- one identity prop per character, e.g. a cravat, round chalk spectacles or a piece of chalk
- idle motion: ±2.5 px breathing bob. Gestures (point, write, wave) last 0.4-0.6 s with ease-in-out. While writing, the arm wiggles ±7°.
- Each real person gets their own coat color, used consistently. Never draw a real person's likeness. These are abstract stand-ins, labeled by name in caps.

### 5. Sleek, conceptual, simple
- One idea per beat. Each 4-6 s caption beat shows **one new visual change** that matches the caption.
- Keep 96 px safe margins. The bottom band (y > 930) is reserved for captions; diagrams stay above y ≈ 900.
- Show the mechanism (a pull, a deviation, a prediction locking on), never decoration. If a visual element doesn't explain something, cut it.
- Use only real names, dates and facts. Check anything about the present or anything you are unsure of before putting it on screen.

## Soft on-screen text (no voiceover by default)
Text carries the story, so it must be calm and easy to read:
- Captions: Inter Regular, 46 px, chalk at 93% opacity, centered, baseline y = 968, one line of 12 words or fewer.
- Hook or big lines: Inter Display SemiBold, 76-86 px. Sub-lines: Inter Light, 44-50 px, in dim.
- Entrance: **word-by-word**. Each word fades in and drifts up 16 px over 0.42 s, with a 55 ms stagger between words. Exit: the whole line fades out over 0.45 s. No typewriter effect, no bounce, no slide-ins.
- Emphasis: color the key words with the matching accent. For at most one phrase per line, draw a chalk underline in that accent: a slightly curved stroke drawn on 0.35 s after the line lands.
- Timing: a caption stays on screen for 4-6 s. Leave at least 0.3 s between captions.
- Always export a matching `.srt` built from the same caption list.

## Motion grammar
- Easing: ease-in-out cubic for camera moves and line draws; ease-out cubic for fades; ease-out-back (overshoot 1.9) when objects pop into existence.
- Camera: a slow push of 1.00 → 1.05-1.07 across each scene. Never shake, never spin. Zoom transitions push into the next scene's hero object (up to ×7, ease-in) while crossfading.
- Scene transitions: 0.5 s crossfades with overlapping scenes. Elements that persist across scenes (a character, a panel) live on their own layer so they never double-fade.
- Twinkling stars: tiny chalk dots, r 0.8-2.6, alpha 0.25-0.85, with slow sine flicker. In space scenes, a parallax drift of 5 px/s at most.
- Pace: 30 fps. Something should be drawing, moving or arriving at least every 2 s.

## Background score recipe (original, synthesized)
Ambient and curious, then a lift at the payoff. Never use copyrighted music.
- 80 BPM, so one bar = 3.0 s. Line scene boundaries up with bars.
- A minor key for the problem/mystery acts (e.g. D minor: Dm9 · Bbmaj7 · Fmaj7 · Cadd9). Switch to the **parallel major at the reveal** (Dmaj9 → E/D lydian → Gmaj7 · D/F# · Em7 → Gmaj7 · A6 · Dmaj9).
- Layers:
  - pad: additive saws, 3 detuned voices (±7 cents), 1.1 s attack, low-passed at 2.4 kHz
  - plucked eighth-note arpeggio with a dotted-eighth ping-pong delay; one octave higher after the reveal
  - sine bass from act 2 onward, pulsing on quarter notes during "the work"
  - soft clock ticks (high-passed noise, 16ths) while math or work happens
  - gentle sub kick on beats 1 and 3
- Sync points:
  - soft bell chime (partials 1, 2, 2.76, 5.4) on every glint / appearance
  - band-passed noise whoosh on every object that flies
  - 3 s riser into the suspense pause, then a hard cut
  - low boom plus a bright major bell chord on the reveal frame
- Drop the music to about 40% under a direct question to the viewer.
- Mix: reverb is a synthetic 3 s exponential-noise IR. Master with tanh soft-clip, fade out over the last 3 s, then loudnorm to **-14 LUFS, true peak -1.5 dB**.

## YouTube structure and share hooks (bake these into every video)
1. **0-3 s hook:** a visible, surprising claim that sets up a curiosity gap ("This planet was found with a pen."). The hero object appears in the first second, and the first frame must already be readable.
2. **Context in 1-2 beats**, then the problem stated visually.
3. **The idea, then the work:** show the reasoning (equations written on, diagrams) instead of just stating it.
4. **Comment hook right before the payoff:** a direct question on screen, for example "Pause. How close do you think he got? Drop your guess in the comments." Dim the scene to about 12%.
5. **Payoff** with the sync-point impact and a big tracked title (Inter Display Bold, about 132 px, 34 px tracking, letters staggered 70 ms).
6. **Meaning line:** one sentence on why it matters.
7. **Share CTA:** name a specific person to send it to ("Know someone who says 'When will I ever use math?' … Send them this."), plus a paper-plane share motif.
8. **End card ≥ 8 s:** a small hero object, a channel line, and "Subscribe · Share · Comment what we should explain next". Keep the lower 40% of the frame empty for YouTube end-screen elements. Fade to black over the final 0.8 s.

Deliverables for each video:
- the MP4
- a 1280x720 thumbnail: hero object right, 2-3 huge words left in Inter Display Black with one word in yellow, a yellow crosshair on the hero, one pink underline
- the `.srt`
- the upload package: 3 title options, a description with chapters (first chapter at 0:00, each chapter 10 s or longer), tags, and a pinned comment that repeats the comment hook

## Production pipeline (code-first, deterministic)
- Draw with **skia-python** (`pip install --break-system-packages skia-python`) into a numpy RGBA array (`skia.Surface(arr)`). Synthesize audio with numpy/scipy. Encode with ffmpeg.
- Fonts: Inter (`/usr/share/fonts/opentype/inter/`), Inter Display, and Latin Modern Math (`/usr/share/texmf/fonts/opentype/public/lm-math/latinmodern-math.otf`). Use math-italic Unicode letters (U+1D434 / U+1D44E, with ℎ for h). Superscript and subscript digits must be built with layout, because the math font lacks them.
- Structure: `engine.py` holds the style primitives (palette, easing, chalk_reveal, soft_text, math_box/draw_math, planet, person, props). `film.py` holds the caption list, the scene functions (each a pure function of global time t), and the scene table `(t0, t1, fn, fade_in, fade_out)`. `score.py` uses the same timeline.
- Prove the look first: render 15-25 stills across the timeline into a contact sheet, inspect them, fix collisions, then do the full render.
- Render in parallel chunks, pipe raw RGBA to ffmpeg, and concat with `-c copy`.
- Video: libx264 high, CRF 16, yuv420p, BT.709 tags, GOP 60.
- Mux: AAC 320 kbps, 48 kHz, `+faststart`.
- 1920x1080 at 30 fps. For Shorts, use a 1080x1920 re-layout of the same scenes (captions at y ≈ 1500, diagrams scaled into the center square).

## Consistency checklist (run before delivering)
- [ ] No gradients, shadows, glows, textures or 3D shading anywhere
- [ ] bg #0B0F17 and the grid are present in every frame; at most 3 accents on screen; each accent keeps one meaning
- [ ] Every line is drawn on with a chalk tip; dashed means predicted or unseen
- [ ] Characters have two dot eyes and nothing else on the face; each person keeps their coat color
- [ ] Captions are one line, 12 words or fewer, revealed word by word, inside the bottom band, never overlapping diagrams
- [ ] Equations are real, typeset, and written on
- [ ] Hook lands in 3 s; a comment hook comes before the payoff; the share CTA names a person; end card ≥ 8 s with the lower 40% clear
- [ ] Score: minor → major lift on the payoff; sync hits land on visual events; audio at -14 LUFS
- [ ] Facts checked; `.srt`, thumbnail and upload package delivered with the MP4