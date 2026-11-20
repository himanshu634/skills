---
name: "econ-short"
description: "Turns one sentence of Indian economy news into a finished 50-60 second vertical explainer for YouTube Shorts and Instagram Reels in the NeoChoc (Neon Chalkboard) style - deep research, an addictive screenplay, a mood-matched low-pitched score, the render and the upload kit, each behind a quality gate. Use it whenever the user gives a headline, news line or economy topic and wants a Short, Reel or video made from it, for example \"RBI cuts repo by 25 bps\", \"rupee hits 96\" or \"make a short on today's CPI print\", even if they do not name the skill."
---

# Economy Short: one sentence in, one 50–60 s explainer out

The user gives one sentence. You deliver a finished vertical video (1080×1920, 30 fps, 50.0–59.5 s, a different length every time) with a thumbnail, the YouTube title, description and tags, the Instagram caption, and a ZIP of all of them for YouTube Shorts and Instagram Reels, for the channel **Chalk & Rupee** (@chalkandrupee).

## The pipeline

| # | Section | Done by | Output | Gate |
|---|---|---|---|---|
| 1 | Research | this skill (+ `deep-research` if listed) | `story.md` | R |
| 2 | Screenplay | this skill | `screenplay.md`, `plan.json` | S |
| 3 | Sound design | `econ-short-sound` | `timeline.json`, `score.wav` (a new sound for every reel) | A |
| 4 | Video | NeoChoc + `econ-short-render` | MP4, thumbnail, YouTube and Instagram copy, captions-and-thumbnail ZIP | V |

Run the sections in this order. A section starts only after the previous gate passes; a failed gate means fixing and re-running that section, never shipping anyway. Sound comes before video because the picture is cut to the music's beat grid. Create a task list with the four sections and their gates, and work in one folder per video (`<slug>/`).

## Load these first

1. **NeoChoc**, the `neon-chalkboard-motion` skill (it may be listed as `anthropic-skills:neon-chalkboard-motion`). It is the visual theme of every video: palette, blueprint grid, flat vector shapes, chalk lines drawn on, abstract characters, motion grammar, word-by-word text and the share hooks. Read all of it before Section 2, because the screenplay is written in its visual language.
2. This skill.
3. `econ-short-sound` at Section 3 and `econ-short-render` at Section 4 (they may also be listed with a prefix).

If NeoChoc or a sub-skill is not available, stop and tell the user which one is missing. Never improvise the look or the sound.

## Shorts overrides of NeoChoc

NeoChoc is written for 16:9 long-form. Where it conflicts with the rules below, these win; everything else in NeoChoc applies as written (its colour tokens, grid, flat shapes, draw-on lines, characters, easing, text entrance, comment hook and share CTA).

| NeoChoc says | For these Shorts |
|---|---|
| 1920×1080; reference video 1:42 | 1080×1920, 30 fps, 50.0–59.5 s, a different length every video |
| 96 px margins; captions in the bottom band (y > 930), or at y ≈ 1500 for Shorts | essential text and numbers only inside x 72–948, y 260–1440; the apps' UI covers the rest |
| a 46 px caption line, one per 4–6 s beat | no caption band: the story is told by headline lines in the upper third, each block on screen 2.5–6 s; the .srt carries captions |
| big lines 76–86 px, sub-lines 44–50 px, labels 16–24 px | big lines 88–96 px, sub-lines 40–48 px, labels 26–30 px (sized for a 1080-wide phone frame); nothing essential under 26 px |
| arrows 3 px with 12–14 px heads | 4 px with 18 px heads |
| a slow push of 1.00 → 1.05–1.07 across each scene | 1.00 → 1.05 on the diagram only; text never moves |
| comment hook (no length given) | 1.6 s at most |
| end card of 8 s or more, lower 40% empty | no end card: the CTA sits in the last ~5 s and the last 0.45 s fades back to frame 0, so the video loops |
| 80 BPM ambient score with a minor-to-major lift | a mood-matched, low-pitched groove from `econ-short-sound`, with its own sound in every reel and the ka-ching logo as the constant (still original, still −14 LUFS) |
| 1280×720 thumbnail | a 1080×1920 cover with its key content inside x 84–960, y 420–1500 |
| chapters in the description | none (Shorts have no chapters); the description lists dates and sources |
| hook in the first 3 s | the same, and frame 0 already shows the hook line and the hero object, fully visible |

Channel colour meanings (NeoChoc allows one meaning per accent per video; use these unless the story needs otherwise): yellow = money and liquidity; blue = RBI, policy, the answer; pink = stress, the problem, whoever gains least; green = relief, whoever gains most.

## Section 1: Research → story.md

Goal: what is happening, how it is happening and why it is happening, for the Indian economy, with every number sourced and dated.

1. **Read the sentence.** Identify the event, the actors, the numbers and the date. If several events fit and nothing says which, take the most recent and state the reading at the top of `story.md` and in your first message. If the sentence is wrong or out of date (it says RBI cut when it hiked), the story is about what is true; say so.
2. **Research deeply.** If the `deep-research` skill is listed, load it and give it this brief: "*sentence*. For Indian viewers: exactly what happened (numbers, dates), the mechanism step by step, the immediate and underlying causes, who gains and who loses, what happens next with dates, and what it means for an ordinary person's EMI, savings, prices and job. Primary sources first; every number with its date." Otherwise research directly with web search (extended mode for fresh news). Either way, open the primary document yourself for every number that goes on screen.
3. **Source ladder.** Primary: RBI (press releases, MPC statements and minutes, auction results, Weekly Statistical Supplement), MoSPI (CPI, IIP, GDP), Ministry of Finance, PIB and Budget documents, CGA, Ministry of Commerce, SEBI, NSE and BSE, PPAC, IMD; abroad, the Federal Reserve, ECB, US Treasury and OPEC. Secondary, to explain or as two independent confirmations when no primary exists: Business Standard, Mint, The Economic Times, Reuters, Bloomberg, The Hindu BusinessLine, Moneycontrol.
4. **Fact rules.** Every number carries its value, unit, as-of date (IST) and source URL. Use Indian units (₹ crore, ₹ lakh crore) and say "about" for rounded figures. Market moves are closing values with their date. Never write FY when you mean a calendar year. No individual stock with a view on where it goes (SEBI): market data is news, never a call.
5. **Build the storyline**: what, then how, then why; then the twist (the non-obvious part, or the misconception to bust), who gains and who loses, what to watch next (dated) and the "you" line.
6. **Classify for the sound** (Section 3 uses it). Tone: negative, positive, mixed or neutral. Pace: rapid (things changed within days, or an emergency move), steady (scheduled data or policy) or slow-burn (a structural trend). Justify each in one line from the facts, not from the headline's wording.

`story.md` (keep these headings). Gate V checks every number and date on screen, and on the cover, against this file as written: write dates as Mon D, YYYY (Dec 4, 2026) and write each number the way it will appear on screen (₹1 lakh crore, 5.50%, 25 bps). A range like "Dec 2-4" does not cover "Dec 4" on screen; state the day you show.

```markdown
# <working title>
Sentence: "<the user's sentence>"   Reading taken: <which event>
As of: <Mon D, YYYY, HH:MM IST>
Tone: <negative|positive|mixed|neutral> - <why>   Pace: <rapid|steady|slow-burn> - <why>
## One-line takeaway        (12 words or fewer)
## What is happening
## How it is happening      (3-6 linked steps)
## Why it is happening      (immediate cause, then underlying cause)
## The twist / misconception
## Who gains / who loses
## What to watch next       (dated)
## What it means for you
## Facts table
| # | fact | value | unit | as of | source |
## Open questions / disputed points
## Sources
```

**Gate R** (all must hold): the core event has a primary source; every number and date that may appear on screen is in the facts table with its source and date; contested points are labelled; the takeaway is one sentence of 12 words or fewer; tone and pace are set.

## Section 2: Screenplay → screenplay.md and plan.json

Goal: viewers stop on frame 0, stay to the end, replay it, comment and send it to someone.

### The hook (0–3 s)

Pick the hook the facts support best. Never fake a contradiction.

| Type | Example |
|---|---|
| Paradox | "RBI pumped ₹1 lakh crore… and the market FELL." |
| Myth-bust | "It's NOT free money." |
| Number shock | "₹95 for one dollar." |
| Personal stake | "Your EMI just changed." |
| Countdown | "In 44 days, RBI decides your EMI." |
| Before and after | "2024: ₹83. Today: ₹95." |
| Question | "Why didn't petrol get cheaper?" |

Seven words or fewer on frame 0, a number or a contradiction, the hero object on screen, all fully visible on frame 0 (it is also the frame the loop returns to), then an open loop by 3 s ("Here's why.").

### Retention architecture

- Chapter chips (01 · WHAT HAPPENED, 02 · WHY, 03 · THE CATCH…) every 8–12 s: progress markers that re-hook.
- The hook's open loop ("Here's why.") is paid off by the what and how scenes.
- A second open loop at the catch, about 45% in ("But there's a catch…"), paid off by who gains and the "you" line (about 55–75%).
- At most two pattern interrupts, on the biggest beats: a tape-stop (`stop` cue) with a visual flip.
- A comment prompt at the end of the catch scene, right before that payoff: NeoChoc's comment hook with the scene dimmed to about 12%, kept to 1.6 s at most for Shorts, such as "HIKE or PAUSE? Comment."
- The "you" line (EMI, FD, prices, job) before the end.
- A share CTA that names a specific person ("Send this to the friend who thinks RBI just printed free money.") with NeoChoc's paper-plane motif, then a follow line with a dated reason ("Follow for the Dec 4 breakdown.").
- The loop: the last 0.45 s fades the hook frame back in, so the end flows into 0:00.
- Something draws, moves or arrives at least every 2 s (Gate V measures it).

### Beat sheet

Shares of the total length; the exact length is locked in Section 3.

| Scene | Role | Share | Content |
|---|---|---|---|
| hook | hook | ~9% (exactly 2 bars) | claim, hero, open loop |
| 01 what | core | ~15% | the event and its key number |
| 02 how | core or refill | ~18% | the mechanism, drawn on |
| 03 why / the catch | twist | ~13% | the cause or the catch; the comment prompt |
| who gains | core | ~15% | two rows, green and pink |
| what next | drive | ~15% | a dated timeline; dates pop on the beat |
| takeaway + CTA | outro | ~15% | one line, share CTA, follow line, data line, disclaimer, loop |

Use 6–8 scenes; the first has the role `hook`, the last `outro`. Roles drive the music: hook (full groove from the first frame), core (groove), refill (groove that lifts in its last third), twist (drops out and darkens: a heartbeat, a filter sink or a ticking clock, chosen per reel), drive (full, with stabs, a counter-line or the hook doubled), outro (light, then full from the CTA).

### Text

At most three headline lines per block; big lines of 18 characters or fewer at 88–96 px; sub-lines of 32 characters or fewer at 40–48 px (30 or fewer when centred); one keyword per line in its accent colour; at most one chalk underline per line; ALL CAPS only for labels. Every number on screen must be in the facts table. The outro ends with "Data: *sources* · as of *Mon D, YYYY*" and "Analysis, not investment advice."

### Outputs

`screenplay.md`:

```markdown
# Screenplay: <title>
Hook type: ... · Frame-0 text: "..." · Hero object: ...
Accent map: yellow = ... · blue = ... · pink = ... · green = ...
| # | scene | role | share | on-screen text (exact) | visual (NeoChoc terms) | cues |
Comment prompt: ... · Share CTA: ... · Follow line: ... · Loop: ...
Facts used: #1, #3, ... (from story.md)
```

`plan.json`, the machine-readable screenplay that Section 3 locks to the beat:

```json
{"title": "RBI's 1 lakh crore is not free money", "slug": "rbi-vrr-oct-2026", "date": "2026-10-20",
 "tone": "mixed", "pace": "steady", "avoid_seconds": [52.5], "avoid_sounds": [],
 "scenes": [
  {"name": "hook", "role": "hook", "share": 9,
   "cues": [["hook_l1", 0, "sting"], ["hook_drop", 4, "stop"], ["hook_why", 5.5, "tick"]]},
  {"name": "what", "role": "core", "share": 15, "cues": [["what_t1", 0.5, "tick"], ["what_coin", 1, "pop"]]},
  {"name": "catch", "role": "twist", "share": 13, "cues": [["c_t1", 0.5, "tick"], ["c_ask", 3, "pop"]]},
  {"name": "end", "role": "outro", "share": 15,
   "cues": [["e_t1", 0.5, "tick"], ["e_cta", 4, "sting"], ["e_follow", 7.5, "tick"]]}],
 "duck": [["catch", 3, 2]]}
```

(A real plan has all 6–8 scenes.)

- A cue is `[key, beat offset from the scene start (quarter-beat steps), type]`. Types: `sting` (the sound logo: at 0:00 and on the share CTA), `tick` (a text line lands), `pop` (an object appears), `scratch` (a chalk line draws), `whoosh`, `date` (a timeline date; plays a glockenspiel note), `check`, `boom`, `stop` (a tape-stop: two per video at most, one per scene, only in hook, core, refill or drive scenes), `drop`. Keys are unique; the film uses them by name.
- `duck` = `[scene name, beat, length in beats]` for the comment prompt (music drops to 40%). It takes the scene's name, not its role.
- The length is chosen in Section 3: it cycles with the date, so videos made on different days differ. `avoid_seconds` lists the lengths of earlier videos made the same day or that you can see (this conversation, `<slug>_<seconds>s.mp4` names in the working folder, the README.txt in earlier ZIPs, or what the user tells you). `target_seconds` only if the user asks for a length.
- The sound is also chosen in Section 3, from the sound registry on the engine page, so every reel sounds different. `avoid_sounds` lists the sound codes of earlier reels the registry may not know: the code in square brackets on the Video line of README.txt in earlier ZIPs, in earlier Gate A output, or what the user tells you. Leave it empty when the registry can be read. Add `"sound"` (a world, lead or groove by name) only if the user asks for a specific feel.

**Gate S**: every on-screen number and date maps to a fact in story.md; the hook has 7 words or fewer and is visible on frame 0; the scenes cover what, how and why; the first scene is `hook` and the last `outro`; two `stop` cues at most, one per scene, none in twist or outro scenes; the comment prompt, share CTA, follow line, data line and disclaimer are present; no individual stock tips.

## Section 3: Sound → load `econ-short-sound`

Give it plan.json. It reads the sound registry, locks `timeline.json` (preset, the reel's own sound, key, BPM, the exact length, scene times, cue times), makes `score.wav` and adds the reel to the registry. Gate A is defined there; it also proves the reel sounds unlike the earlier ones.

## Section 4: Video → NeoChoc + `econ-short-render`

Give it story.md, screenplay.md, timeline.json and score.wav. It writes film.py, checks the text before rendering, renders, writes the YouTube and Instagram copy, packages the deliverables and runs Gate V. Gate V is defined there.

## Delivering

Only after all four gates pass:

1. Send three files: `<slug>_<seconds>s.mp4` (the video), `<slug>_thumbnail_1080x1920.png` (the thumbnail, shown as an image) and `<slug>_Captions_and_Thumbnail.zip` (the YouTube title, description and tags, the Instagram caption, the thumbnail and the other upload files).
2. Reply with a few lines first: the length, the mood preset and the reel's sound (its name and code), the reading taken of the sentence, anything in the sentence you had to correct, and the sources.
3. Then paste `upload_text.md` exactly as written: the YouTube title with two other options, the description, tags and pinned comment, the Instagram caption and first comment, and where the thumbnail goes. Never retype or shorten it; Gate V checked that file.