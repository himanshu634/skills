---
name: "econ-short-sound"
description: "Section 3 of the econ-short video pipeline. Locks the video's timing (a whole number of bars, 50.0-59.5 s, different for every video), gives the reel its own sound (lead, kit and groove, keys, bass, a newly written hook and chord loop, chosen to be unlike the channel's earlier reels), composes the mood-matched (dark for bad news, bright for good news, denser for fast-moving events), low-pitched, loop-perfect score, masters it to -14 LUFS, proves it with Gate A (including that it sounds new) and adds it to the sound registry. Use it after the econ-short screenplay is written, or whenever an econ-short video needs its timeline or music made or redone."
---

# Economy Short: sound (Section 3)

Input: `plan.json` from the screenplay. Output: `timeline.json` (the timing contract the picture follows, now carrying this reel's sound), `score.wav`, and `sound_entry.json` (the reel's row for the sound registry). Sound comes before the picture because every visual event is placed on this beat grid.

## Every reel sounds new; the channel still sounds like itself

The first engine moved only the key and the tempo from reel to reel, and listeners hear a transposed or faster tune as the same tune. What they use to tell tracks apart, within half a second, is the instruments; what they remember is the hook's rhythm and contour. So each reel now gets its own **sound DNA**, and only the brand stays fixed.

**The same in every reel (keep all of it):**

- **The sound logo**: the "ka-ching" at 0:00 and on the share CTA. Never change it; it is how viewers recognise the channel.
- **The pocket**: 84–108 BPM, never faster (128 BPM was rejected as "too fast"); a swung groove with a sidechain pump; the hook from the first frame and never gone for long.
- **Low and warm**: bass roots in the lowest octave, the hook between E3 and F5, a 9 kHz ceiling, and every bass with harmonics a phone speaker can play. A tonal guard gives any palette that lands brighter than the channel's sound a gentle shelf (never on the logo). Gate A measures it; the approved mixes sat near 0.8% of energy above 2 kHz and a 210 Hz centroid.
- **Controlled surprises**: two tape-stops at most; the twist drops out and darkens; the payoff brings the groove back with the hook doubled an octave up.
- **The loop**: the outro's pickup notes lead into the hook's first note at 0:00, and every tail (reverb, echo, decays) wraps around to the start.
- **The balance**: every palette is levelled to the first engine's approved mix (lead −4.4, bass −5.2, kick −5.6, drums −17.2, keys −17.4 dB, gated and K-weighted), then mastered to −14 LUFS.

**New in every reel (the sound DNA, chosen by lock_timeline.py):**

| Gene | Choices |
|---|---|
| World | 14 families of instruments that belong together: Marimba Pocket (the first engine's family, never again its exact sound), Lo-fi Desk, Kalimba Dusk, Santoor Monsoon, Sitar Noir, Vibes Lounge, Steel Sunrise, Bansuri Breeze, Glass Circuit, Music Box Mystery, Dhol Express, Dembow Ledger, Harp Daylight, Guitar Dawn |
| Lead | the hook's voice: marimba, vibraphone, kalimba, music box, glass bell, Rhodes, nylon guitar, santoor, sitar, steel pan, bansuri, harp, synth pluck, mallet synth; plus a second voice for counter-lines |
| Groove | 22 kit-and-pattern grooves: pocket, push, half-time and dembow on the pocket kit; boom-bap; half-time and bounce trap; afro-house; amapiano-lite; brush swing; jazz-hop; keherwa and laggi on tabla; taiko; heartbeat; electro; dhol chaal; bhangra; light pop |
| Keys, bass | 10 keys (warm EP, Rhodes, Wurlitzer, felt piano, pad, string machine, organ, harmonium, choir, guitar) in 6 comping patterns; 8 basses (808, sub, analog, electric, upright, FM, reese, log drum) in 9 lines |
| Hook | written for this reel: one of 14 rhythm cells, 6 contours, 4 ways to answer in bar 2, following the chords or holding its tune; the best of 48 drafts by an earworm score (a common contour with one unusual leap or repeat) |
| Harmony | one of 30 chord loops in the mood's modes, one or two bars per chord |
| Texture | clean, warm tape, lo-fi (wow, flutter, crackle), big hall or wide; room size, echo time and pump depth |
| Arrangement | how the twist drops (heartbeat, sink, clock), what the refill and the drive add, how the outro opens |

How it is chosen: lock_timeline.py draws 240 candidates inside the mood and keeps the one farthest from the earlier reels it knows (novelty search). The lead, the groove and the hook rhythm never repeat from the last three reels, no lead comes back with the same groove or hook rhythm within eight, the first engine's marimba never returns over its pocket groove, and tempo and key are pushed away from the last reels too. Earlier reels come from the **sound registry** on the engine page, from earlier video folders next to this one, and from `avoid_sounds` in plan.json. The reel's sound has a readable code, `lead.keys.bass.groove.rhythm-contour.loop.texture`; Gate A, timeline.json and the README.txt in the upload ZIP show it in square brackets.

## Mood presets

lock_timeline.py picks the preset from the tone and pace in plan.json (from story.md):

| tone ↓ / pace → | rapid | steady | slow-burn |
|---|---|---|---|
| negative | dark-urgent | dark-steady | dark-steady |
| mixed | mixed-groove | mixed-groove | neutral-curious |
| positive | bright-urgent | bright-steady | bright-steady |
| neutral | neutral-curious | neutral-curious | neutral-curious |

| Preset | BPM | Modes | Colour |
|---|---|---|---|
| dark-urgent | 98–108 | aeolian, phrygian, harmonic minor | dark filters, hook a little lower, driving grooves |
| dark-steady | 84–94 | aeolian, harmonic minor, dorian | the darkest filters, hook lower |
| mixed-groove | 88–102 | aeolian (with a major lift), dorian | warm |
| bright-steady | 88–100 | ionian, lydian, mixolydian | the brightest filters, hook a little higher |
| bright-urgent | 100–108 | mixolydian, ionian | bright, driving grooves |
| neutral-curious | 86–100 | dorian, mixolydian, aeolian | laid-back grooves |

Mode and tempo carry most of a mood, then register and brightness, so they are fixed by the preset and everything else is free to change. Pace shapes whichever preset is chosen: **rapid** news gets the upper half of the tempo window and driving grooves; **slow-burn** stories get the lower half, laid-back grooves and sometimes two bars per chord. Set `"preset"`, `"bpm"` or `"sound"` in plan.json only when the user asks for a specific feel; `"sound"` takes genes by name, for example `{"world": "lofi-desk"}`, `{"lead": "sitar"}` or `{"groove": "tabla.keherwa"}`.

## Steps

### 1. Put the engine in the video folder

Every command in this skill runs in the video folder (where `plan.json` is); if your shell does not keep its directory between calls, begin each command with `cd <video folder> && `. The engine files are on the user's engine page, https://claude.ai/artifact/DrJYL895KCzyvtqYSkc3eP.

1. Read the five files with the Artifact tool: `action: "read"`, `url: "https://claude.ai/artifact/DrJYL895KCzyvtqYSkc3eP"`, `paths: ["engine/lock_timeline.py", "engine/sounds.py", "engine/score.py", "engine/master.py", "engine/audio_qa.py"]`. Leave `out_dir` unset. The result names the folder it saved them under (they are in its `engine/` subfolder) and may also show their text, which you do not need to read.
2. Copy exactly these files into the video folder: `cp <that folder>/engine/{lock_timeline,sounds,score,master,audio_qa}.py <video folder>/`
3. Check them, with the video folder's path in place of `<video folder>`:

```bash
python3 - '<video folder>' <<'EOF'
import hashlib, os, sys
os.chdir(sys.argv[1])
SUMS = {
    'lock_timeline.py': '3f37ade51baaeb425c79f539b273a90fb821792f0afb18a4d4bb487f196bd6d9',
    'sounds.py': '23c3b3560fc78e2ce25449bc8d2a9af1f858d1b5a99241bb29a521bdc2a42baf',
    'score.py': '55c4646a8458aa172213eb149094202b16392e258a40040bb852e15c88732008',
    'master.py': '5e3dda68ab2556540a03c982f4b9200bbd568627cdcb64808995e078be215668',
    'audio_qa.py': 'c6436f7263cd4321cf816c9c924e89fe6b81ddda481cadb65d3f1f02fe4f2f2d',
}
bad = [n for n, s in SUMS.items() if not os.path.isfile(n) or hashlib.sha256(open(n, 'rb').read()).hexdigest() != s]
print(('ENGINE OK: ' + ', '.join(SUMS) if not bad else 'ENGINE BAD: ' + ' '.join(bad)) + ' (in ' + os.getcwd() + ')')
EOF
```

It must print `ENGINE OK` followed by the video folder's path before you go on. Never edit an engine file to make the check pass.

- `ENGINE BAD` names the files that are missing or differ: read those again, copy them and re-run the check.
- If the page cannot be read (this session has no Artifact tool, or the page is gone), use the user's offline copy `econ_short_engine.zip`, which holds all ten engine files (these five and the five that econ-short-render uses): look for it among the attached files and the linked folders, or ask the user to attach it; unzip it into the video folder (`python3 -m zipfile -e econ_short_engine.zip <video folder>`) and re-run the check.
- If a file keeps failing although its `sha256sum` equals the value listed for it on the engine page, the value in `SUMS` above was mistyped: continue, and tell the user.
- If neither source passes, stop and tell the user which engine files are missing.

Needs Python 3 with numpy and scipy (`pip install --break-system-packages numpy scipy`) and ffmpeg.

### 2. Read the sound registry

The registry is the engine page's database: one row per reel, with its sound DNA and soundprint. Use the `ArtifactData` tool (if it is listed as a deferred tool, load it with ToolSearch first): `action: "query"`, `url: "https://claude.ai/artifact/DrJYL895KCzyvtqYSkc3eP"`, `collection: "sounds"`, `query: {"limit": 1000}`, `out_dir: "<video folder>/sound_history"`. It saves each earlier reel as a JSON file under `sound_history/`; you do not need to read them.

If the tool is missing or the read fails, carry on and say so in the final reply: lock_timeline.py also looks at earlier video folders next to this one and at `avoid_sounds`. In that case fill `avoid_sounds` in plan.json with the sound codes of earlier reels you can see (the bracketed code in each README.txt in earlier ZIPs, in earlier Gate A output in this conversation, or what the user tells you), as you do for `avoid_seconds`.

### 3. Lock the timeline

`python3 lock_timeline.py plan.json timeline.json`

It prints the preset and this reel's sound (its world, instruments, code, key, mode and BPM, and the nearest earlier reel with its distance), the chosen length with the alternatives, and each scene's start and end. What it enforces:

- the sound: drawn inside the mood, as far as possible from the earlier reels it found, with no repeat of the lead, the groove or the hook rhythm of the last three reels;
- the length is a whole number of bars inside 50.0–59.5 s, nearest to a target that moves 3.7 s a day through that range (so videos made on different days differ), at least 1 s away from every value in `avoid_seconds`, or nearest to `target_seconds` when the user asked for a length;
- the hook is exactly 2 bars; the outro at least 2.5 bars; every other scene at least 1.5 bars; all boundaries on half bars;
- cue offsets land on 16th notes; a scene that came out shorter than its cues need has them compressed, with a warning;
- two `stop` cues at most, one per scene, and only in hook, core, refill or drive scenes (the twist and outro arrangements have their own drops); the sound logo at 0:00 and on the outro's CTA (added with a warning when missing).

Read the warnings. A compressed scene usually means its cues should be re-spaced in plan.json and the lock re-run. A re-run of the same video keeps its sound unless the registry or the earlier folders changed.

### 4. Compose and master

```bash
python3 score.py timeline.json score_raw.wav
python3 master.py score_raw.wav score.wav
```

The arrangement follows the scene roles, the cues and the reel's DNA; a normal video needs no hand edits. Change score.py only for a deliberate one-off moment, and keep every rule above when you do. A score takes 20–60 s to compute.

### 5. Gate A

`python3 audio_qa.py score.wav timeline.json` must end with `GATE A: PASS`. On a pass it also writes `sound_entry.json`.

| Failure | Fix |
|---|---|
| duration differs from the timeline | re-run score.py with the same timeline.json; never trim the WAV |
| loudness or true peak | re-run master.py on score_raw.wav |
| a low-pitched check | something bright was added: lower it an octave or low-pass it; if it is a stock sound, re-run the lock with that gene named in `"sound"` (another lead or texture) |
| loop seam | an event was added outside `Bus.add`, or a full-length signal was filtered without `circ` |
| dead air | a stop's silence is too long, or a scene has no music: check the roles in plan.json |
| first 100 ms quiet | the hook must open with the groove and the logo at 0:00 |
| new sound: lead, groove or hook rhythm repeats, or the DNA distance is too small | the history changed after the lock: re-run steps 3–5 |
| sounds new: an earlier score is too close | add that reel's code to `avoid_sounds` in plan.json and re-run steps 3–5 |

### 6. Add the reel to the registry

With `ArtifactData`: `action: "set"`, `url: "https://claude.ai/artifact/DrJYL895KCzyvtqYSkc3eP"`, `collection: "sounds"`, `doc_id` as Gate A printed it (`<date>_<slug>`), `file_path: "<video folder>/sound_entry.json"`. If the set is refused because the document exists (a re-run of this video), `get` that document and `set` again with `if_version` from the get. If the registry cannot be written, say so in the final reply; the sound code is still in README.txt for `avoid_sounds`.

Then hand `timeline.json` and `score.wav` to Section 4 (`econ-short-render`). If the screenplay changes later, redo this whole section: the picture must be rebuilt on the new timeline.