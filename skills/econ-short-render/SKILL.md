---
name: "econ-short-render"
description: "Section 4 of the econ-short video pipeline. Builds the 1080x1920 NeoChoc-style film on the locked timeline, renders it with the score, proves it with Gate V (file specs, loudness, safe zone, text overlaps, every number traced to story.md, motion every 2 s, captions, cover) and packages the YouTube Shorts and Instagram Reels upload kit. Use it after econ-short-sound has made timeline.json and score.wav, or to re-render or fix an econ-short video."
---

# Economy Short: video (Section 4)

Inputs: `story.md`, `screenplay.md`, `timeline.json`, `score.wav`. Outputs: the MP4, the thumbnail, the YouTube title, description and tags, the Instagram caption, `<slug>_Captions_and_Thumbnail.zip` with all of them, and `upload_text.md` for the final reply.

**Load NeoChoc first** (`neon-chalkboard-motion`). Its colour tokens, grid, draw-on lines, characters, easing and text entrance are already built into engine.py; this skill adds the vertical layout and the checks. Where NeoChoc and this skill differ, this skill wins (the econ-short skill lists every override). engine.py already holds NeoChoc's tokens plus those overrides, so use it unchanged. The one allowed edit: if the user has changed NeoChoc's colour or grid tokens since this skill was written, update the token block in engine.py to match and tell the user.

## Layout for 1080×1920

- **Safe zone** `SAFE = (72, 260, 948, 1440)`: every essential word and number stays inside it, because the apps' titles, buttons and captions cover the rest. Decoration may bleed to the edges.
- **Rows**: chapter chip at y 276; headline baselines `H1, H2, H3 = 450, 556, 662` for 88–96 px Inter Display SemiBold; diagrams inside x 84–948, y 720–1300; a note or equation row with its baseline at `NOTE_Y = 1410`.
- **Sizes** (NeoChoc sizes scaled up for a 1080-wide frame): big lines 88–96 px; sub-lines 40–48 px in Inter Light or Regular; labels ALL CAPS Inter Medium 26–30 px with 4 px tracking; the payoff title (`tracked_title`) 110–132 px; arrows 4 px with 18 px heads; nothing essential under 26 px.
- **Camera**: the NeoChoc push (1.00 → 1.05) only on diagrams, through `with push(c, t, scene):`; text never moves with it.
- **Frame 0** shows the hook line and the hero object fully: declare those lines with `t_in = -1` (a smaller head start is still mid-fade on frame 0).
- **Loop**: `loop_back(hook)` fades the hook frame back in over the last 0.45 s.

## Steps

### 1. Engine files

Every command in this skill runs in the video folder (where `timeline.json` is); if your shell does not keep its directory between calls, begin each command with `cd <video folder> && `. The engine files are on the user's engine page, https://claude.ai/artifact/DrJYL895KCzyvtqYSkc3eP.

1. Read the five files with the Artifact tool: `action: "read"`, `url: "https://claude.ai/artifact/DrJYL895KCzyvtqYSkc3eP"`, `paths: ["engine/engine.py", "engine/stage.py", "engine/render.py", "engine/qa.py", "engine/package.py"]`. Leave `out_dir` unset. The result names the folder it saved them under (they are in its `engine/` subfolder) and may also show their text, which you do not need to read.
2. Copy exactly these files into the video folder: `cp <that folder>/engine/{engine,stage,render,qa,package}.py <video folder>/`
3. Check them, with the video folder's path in place of `<video folder>`:

```bash
python3 - '<video folder>' <<'EOF'
import hashlib, os, sys
os.chdir(sys.argv[1])
SUMS = {
    'engine.py': '866c6eab2bd876e24b03e4cab04c2abe0ac2150dc28917e5b8193d48f682d6aa',
    'stage.py': 'a9bd225baec589b239569e7daaa4a2d3681aa75a889f67c02206a621c83c0b6a',
    'render.py': 'cfa3ba8694e28e7d20059be4d48b2ec6697a8a81a3e11887569dd396ec1ddadb',
    'qa.py': '637a3cf10e2bf91751ddebdb3f333cdd213ce7c50c7872d8ed12cd53970fd660',
    'package.py': '84df1c61fa40c82e567ca1d777cb60e20d7f9343df9a4183267c03369bf434ad',
}
bad = [n for n, s in SUMS.items() if not os.path.isfile(n) or hashlib.sha256(open(n, 'rb').read()).hexdigest() != s]
print(('ENGINE OK: ' + ', '.join(SUMS) if not bad else 'ENGINE BAD: ' + ' '.join(bad)) + ' (in ' + os.getcwd() + ')')
EOF
```

It must print `ENGINE OK` followed by the video folder's path before you go on. Never edit an engine file to make the check pass.

- `ENGINE BAD` names the files that are missing or differ: read those again, copy them and re-run the check.
- If the page cannot be read (this session has no Artifact tool, or the page is gone), use the user's offline copy `econ_short_engine.zip`, which holds all ten engine files (these five and the five that econ-short-sound uses): look for it among the attached files and the linked folders, or ask the user to attach it; unzip it into the video folder (`python3 -m zipfile -e econ_short_engine.zip <video folder>`) and re-run the check.
- If a file keeps failing although its `sha256sum` equals the value listed for it on the engine page, the value in `SUMS` above was mistyped: continue, and tell the user.
- If neither source passes, stop and tell the user which engine files are missing.

Needs skia-python, numpy and Pillow (`pip install --break-system-packages skia-python numpy pillow`), ffmpeg, and the fonts from `fonts-inter` and `fonts-lmodern` (`apt-get install -y fonts-inter fonts-lmodern`); engine.py stops with that message if a font is missing.

### 2. Write film.py

film.py is the only file you write by hand. Start from this skeleton:

```python
"""<Title>: scenes for econ-short. Pure functions of global time t; times come only from timeline.json."""
import math

from stage import *  # noqa: F401,F403  engine + D, SC, T, beat(), line(), show(), push(), loop_back(), SCENE_FN

# 1) Declare every story line once: the frames and the .srt both come from these.
line('h1', -1, T['hook_drop'], 'RBI just put', H1, 96)               # t_in = -1: fully visible on frame 0
line('h2', -1, T['hook_drop'], [('₹1 lakh crore', YELLOW)], H2, 96)
line('h3', T['hook_drop'], SC['hook']['t1'] + 0.2, [("It's ", CHALK), ('NOT', PINK)], H1, 96, ul=(1, 1, PINK))
line('w1', T['what_t1'], SC['what']['t1'] + 0.2, [('A ', CHALK), ('7-day loan', YELLOW)], H1, 96)
line('lab', T['what_coin'], SC['what']['t1'] + 0.2, 'Weighted average rate', NOTE_Y, 28, 'med', srt=False)


# 2) One function per scene name in timeline.json.
def hook(c, t):
    for i in ('h1', 'h2', 'h3'):
        show(c, t, i)
    with push(c, t, 'hook'):
        c.drawCircle(540, 1010, 230, stroke(CHALK, 3, 0.45, dash=(14, 10), phase=-t * 30))   # idle motion
        coin(c, 540, 1010, 140 * breathe(t))


def what(c, t):
    show(c, t, 'w1')
    show(c, t, 'lab')
    with push(c, t, 'what'):
        chalk_line(c, t, [(160, 1000), (920, 1000)], T['what_coin'], 1.0, 4, CHALK, 0.85, dash=(14, 10), march=True)
        k = pop_scale(t, T['what_coin'])
        if k > 0:
            coin(c, 540, 1000, 60 * k)


SCENE_FN.update(hook=hook, what=what)   # ...every scene in timeline.json
loop_back(hook)                         # the end flows back into frame 0


def draw_cover(c):                      # 1080x1920 cover; its text stays inside COVER_SAFE
    board(c)
    text(c, '₹1 lakh crore', 540, 780, 'd_black', 124, YELLOW, align='center')
    coin(c, 540, 1180, 130)
```

Rules:

- **Timing comes only from `T['cue_key']` and `beat(scene, b)`**; never type seconds. That is what keeps the picture on the music. Every visual event with a sound has a cue, and every cue has a visual event (a `pop` cue means something appears at that moment).
- **NeoChoc grammar through the engine**: lines are drawn on (`chalk_line`, `draw_on`), never popped on; dashed lines (`dash=`, `march=True`) mean predicted or unseen; objects appear with `pop_scale` (ease-out-back 1.9); text enters with `show` (word by word); equations are real and written on with `math_text`; characters are `person` (two dot eyes, blink, bob, one prop); at most three accents on screen.
- **Idle motion in every scene** (marching dashes, `breathe`, a character, an orbit): Gate V fails any 2 s stretch without visible motion.
- **Numbers only from story.md.** A `counter` starts at 0 or at a real earlier value.
- `essential=False` only for decorative text inside a drawing; labels that are not part of the story use `srt=False` (they are still checked).
- **Comment prompt**: dim the scene with `c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill(BG, 0.88 * a))`, then show its two lines.
- **The outro** ends with the follow line, "Data: … · as of *Mon D, YYYY*" and "Analysis, not investment advice." (26 px or larger, inside SAFE), all gone by `D - 0.5` so the loop fade is clean.

| Call (engine.py / stage.py) | Does |
|---|---|
| `line(id, t_in, t_out, segs, y, size=88, key='d_semi', x=84, align='left', srt=True, ul=None)` | declare a line; `segs` is a string or `[(text, colour)]`; `ul=(i_first, i_last, colour)` underlines words i_first..i_last (0-based word positions in the line) |
| `show(c, t, id)` | draw it: words fade in and drift up 16 px, 55 ms apart; the line fades out over 0.45 s |
| `chalk_line(c, t, pts, t0, dur, w, rgb, a, dash=None, seed=3, march=False)`, `draw_on`, `arrow`, `ping` | lines drawn on with a chalk tip; arrows; ping rings |
| `pop_scale(t, t0)`, `breathe(t)`, `ease_io`, `ease_out`, `ease_back`, `prog`, `window`, `lerp` | motion |
| `text`, `label`, `chip`, `counter`, `tracked_title`, `math_text` | text pieces (all checked by Gate V) |
| `coin`, `person`, `rrect`, `path_of`, `fill`, `stroke`, `board` | props and primitives |
| `push(c, t, scene)`, `overlay(c, fn, t_draw, a)`, `loop_back(fn)`, `beat(scene, b)` | camera push for diagrams, frozen overlay, loop, beat times |

Font keys: `reg`, `light`, `med`, `semi`, `d_semi`, `d_bold`, `d_black`, `math`. Colours: `BG`, `PANEL`, `DEEP`, `CHALK`, `DIM`, `PINK`, `YELLOW`, `ORANGE`, `BLUE`, `BLUE_L`, `BLUE_D`, `GREEN`, `GREEN_D` (NeoChoc's tokens).

### 3. Prove the look before the full render

`python3 render.py sheet sheet.png 20`, then look at the sheet (Read the PNG). Fix collisions, crowding and anything outside the green box. Then check `python3 render.py stills <t> <t> …` at the moments that matter: frame 0, each stop, the comment prompt, the CTA and the last frame.

Then run the text audit, which needs no video: `python3 qa.py --audit story.md` must end with `TEXT AUDIT: PASS` (safe zone, sizes, overlaps, the frame-0 hook, every number and date on screen and on the cover traced to story.md). Fix everything it names before rendering; each full render takes minutes.

### 4. Render

`python3 render.py video final.mp4 score.wav` (parallel chunks; x264 High, CRF 16, GOP 60, BT.709; AAC 320 kbps 48 kHz; faststart).

### 5. Upload copy

Write `copy_youtube.txt` and `copy_instagram.txt` from story.md and screenplay.md with the templates below. Each heading (TITLE OPTIONS, DESCRIPTION, TAGS, PINNED COMMENT, SETTINGS; CAPTION, FIRST COMMENT, ALT TEXT, COVER) is a line of its own, exactly as written there. package.py and Gate V check these rules:

- **YouTube title**: three numbered options, the first being the one to use; 60 characters or fewer each; the hook as people would search it (the question or the myth-bust) with the key number.
- **YouTube description**: 5,000 characters at most; the hook line, what happened with the key numbers and dates, what it means for you, the dates to watch, then "Data: *sources*, as of *Mon D, YYYY*. Educational analysis, not investment advice." and 3–6 hashtags ending with #shorts (15 at most).
- **YouTube tags**: 5–15 comma-separated search terms, all lowercase, 500 characters at most in total.
- **Pinned comment**: the comment prompt as a question.
- **Instagram caption**: the point in the first 125 characters (all that shows before "more"); 2,200 characters at most; "as of *Mon D, YYYY*" and "not investment advice"; five hashtags at most, at the end. The first comment holds the dates to watch and the comment question, with no hashtags.
- **Hashtags and tags in lowercase**: the channel uses no capital letters in them. Every hashtag (in a title, the description, the pinned comment, the caption or the alt text) and every YouTube tag is all lowercase: #indianeconomy, #shorts, #rbi; rbi repo rate, cpi inflation. The titles, description and caption themselves keep their normal capitals. package.py stops on any capital in a hashtag or tag and lists the lowercase spelling, and Gate V checks it again.
- **Numbers**: every number and date in the titles, description, tags, pinned comment, caption, first comment and alt text is written as in story.md (Gate V traces each one), and there are no others ("60-second", "3 things"). No "<" or ">" anywhere: YouTube rejects them, and they mark a placeholder left in.

### 6. Package

`python3 package.py final.mp4 <slug>` (the slug from plan.json) first checks the copy and stops with a list of what to fix. Then it writes `captions.srt`, `cover.png`, `cover_grid_3x4.png` and `cover_check.png`, and the deliverables:

| File | What it is |
|---|---|
| `<slug>_<seconds>s.mp4` | the video, one file for YouTube Shorts and Instagram Reels |
| `<slug>_thumbnail_1080x1920.png` | the thumbnail: the YouTube Short thumbnail and the Instagram Reel cover |
| `<slug>_Captions_and_Thumbnail.zip` | `YouTube_title_description_tags.txt`, `Instagram_caption.txt`, the thumbnail, `Instagram_grid_preview_1080x1440.png`, `subtitles_en.srt`, `story_and_sources.md` and `README.txt` (length, preset with the reel's sound code in square brackets, tempo and key; the next video uses the length for `avoid_seconds` and, when the sound registry cannot be read, the code for `avoid_sounds`) |
| `upload_text.md` | the YouTube title, other title options, description, tags and pinned comment, and the Instagram caption and first comment, formatted for the final reply |

### 7. Gate V

`python3 qa.py final.mp4 story.md captions.srt cover.png` must end with `GATE V: PASS`. Also look at `cover_check.png`.

| Failure | Fix |
|---|---|
| length or sync | re-render with the current timeline.json and score.wav |
| safe zone, overlap or size | move or shrink the named text, then re-render |
| a number or date not in story.md (screen, cover or copy) | either the text is wrong or the facts table is missing it; fix whichever is wrong, never the check; write dates in story.md as Mon D, YYYY |
| still run | add idle motion to that scene |
| frame 0 hook | declare the hook lines with `t_in = -1` |
| captions | keep all story text in `line()` declarations (`srt=False` for labels) |
| cover | move the cover's text inside `COVER_SAFE` |
| upload copy rules | fix the named section, then re-package |
| a capital letter in a hashtag or tag | write it as package.py lists it, all lowercase, then re-package |
| deliverables missing or out of date | re-run package.py after the last change to the video, the cover or the copy |

Order matters: package (step 6) before the gate, because the gate reads the captions, the cover and the deliverables that package.py writes. After any fix: re-render (step 4) if the picture changed, re-package (step 6) and re-run the gate. Deliver only on PASS, and only the files the gate checked.

## Upload copy templates

Replace everything in angle brackets; the finished files contain none.

`copy_youtube.txt`:

```
TITLE OPTIONS
1. <the title to use>
2. <another option>
3. <another option>

DESCRIPTION
<hook sentence>. <what happened, with the key numbers and dates>.
What it means for you: <1-2 lines>.
Dates to watch: <date - event> · <date - event>
Data: <sources>, as of <Mon D, YYYY>. Educational analysis, not investment advice.
#<topic> #<topic> #indianeconomy #shorts

TAGS
<5-15 comma-separated search terms, all lowercase>

PINNED COMMENT
<the comment prompt as a question>

SETTINGS
Not made for kids · Altered or synthetic content: No · Category: Education · Subtitles: subtitles_en.srt
Thumbnail: <slug>_thumbnail_1080x1920.png, uploaded in YouTube Studio on desktop
```

`copy_instagram.txt`:

```
CAPTION
<the point in the first 125 characters> <the story in 2-4 short lines> <the share line>
Data: <sources>, as of <Mon D, YYYY>. Analysis, not investment advice.
#<five lowercase hashtags at most>

FIRST COMMENT
<dates to watch and the comment question; no hashtags>

ALT TEXT
<one sentence describing the animation>

COVER
<slug>_thumbnail_1080x1920.png; check Instagram_grid_preview_1080x1440.png for the profile-grid crop
```