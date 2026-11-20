# Sound and voice

## Motion's limits

The score is a small synth: patches `pad`, `keys`, `ep`, `pluck`, `bass`, `marimba`, `vibes`,
`glock`; a drum kit; foley (`thud`, `whoosh`, `revswell`, `click`, `tick`, a few others). No
samples, voice, strings or brass. Films start muted. Treat it as a **temp track**; the final
mix is in post.

## Sound designer

**Novice error:** forgetting sound is half the film, and that silence is its strongest cue.

- **Leitmotif**: original, 3–5 notes, on `pluck` or `keys`. It returns changed: fuller when
  power is held, one note when lost. Never an existing theme or near one.
- **Score to the series, not Motion's defaults.** Motion favors marimba grooves (written
  for product films). Set the series' sound world from references, in the bible: drama
  usually wants beds (low `pad`, sparse `bass`, drums only as a heartbeat under tension);
  comedy may want exactly Motion's bouncy `marimba` and `pluck`, timed to gags.
- **Silence before the biggest moment**: 1.0–1.5 s before a blow (drama), dead air before a
  punchline (comedy). Breaks Motion's "never below −30 dB" deliberately, once or twice a
  film; record the rule in the bible.
- **Foley**: few cues on exact frames: door (`thud`, low velocity), match (`click` + short
  `whoosh`), bell (`glock`, low velocity, long release).
- **Arc**: open → bed under the approach → motif at the turn → silence → aftermath →
  resolved or not, matching the ledger.

## Voice

Motion carries no voice; a narrator explaining the plot kills drama.
- Voice is for interiority and framing (memory, a letter read aloud), never exposition the
  picture shows.
- VO to timecode in the post sheet, ≥1.5 s clear before and after; lines live in holds.
- Accents from real speakers, never caricature; other languages stay, with subtitles.
- Scratch read first (a phone is fine), cut the animatic to it; final voice after picture lock.

## In the brief

```json
"sound": {"bed": "pad D2, very quiet", "motif": "pluck D4 F4 E4 A3 at the turn",
  "cues": [{"t": 7.2, "fx": "thud", "what": "door closes"}], "silence": [{"from": 10.0, "to": 11.3}]},
"vo": [{"t": 4.0, "line": "(for post) I never saw the sea again.", "air": 1.5}]
```

VO lines go to the post sheet only, unless written as an intertitle.

## Post (outside Motion)

Export the MP4; in DaVinci Resolve (free) or any editor: lay scenes, add VO, replace or layer
the temp score, add room tone per location and real foley, mix to the platform's loudness
spec (~−14 LUFS online, −23/−24 broadcast; check current specs).
