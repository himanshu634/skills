# Research method

Turns "make it good" into decisions grounded in films that already work.

## Contents
1. Fingerprint
2. Reference slate: four lanes
3. What to study
4. Sources and trust
5. Triangulation
6. Translation into decisions
7. Saving it

## 1. Fingerprint

Read the whole script first. Fill `templates/fingerprint.md`:
- **Genre and subgenre**: "crime" steers nothing; "family saga", "heist", "noir" do.
- **Years**: span, and where the main action sits.
- **Places**: as specific as the script allows (a harbor district, not "the city").
- **Social world**: class, community, institutions.
- **Tone**: restrained or operatic, tragic or ironic, intimate or epic.
- **Central tension**: what the story keeps returning to.

What the script doesn't settle becomes a candidate question.

## 2. Reference slate: four lanes

5–7 films. A "best of the genre" list gives everyone the same titles, so spread them:

| Lane | Gives | Count |
|---|---|---|
| **Genre** | How this kind of story is staged, paced, lit | 2 |
| **Made-in-period** | How the era saw itself: real light sources, streets, clothes, pacing | 1–2 |
| **Place** | Texture of the settings, including non-English cinema | 1–2 |
| **Medium** | Animation that told a similar story (first pass; full style research follows the screenplay, `art-department.md` §1) | 1–2 |

Prefer public-domain films (in the US, published 1930 or earlier as of 2026; the line moves
each January): they can be studied frame by frame. The genre's single most famous film is
studied but marked as the one the project must not resemble.

## 3. What to study

Decisions a department head cares about, not plot:
- **Light**: sources, hard or soft, direction, share of frame dark, warm vs cold by place.
- **Camera**: shot sizes, how often and how it moves, framing, foreground layers.
- **Pacing**: average shot length (ASL), hold lengths, where it speeds up.
- **Power and violence**: distance, what is hidden, who stands, who sits.
- **Design**: palette per world, outlines (hats, coats, vehicles, architecture), recurring objects.
- **Sound**: what happens at the big moments (often it drops out).

## 4. Sources and trust

Claude cannot watch films. Every finding carries a tag; never present a weaker one as stronger.

| Tag | Source | Trust |
|---|---|---|
| **observed** | Stills the user uploaded; frames of public-domain films Claude can see | Highest |
| **documented** | Cinematographer or director interviews, production notes, serious criticism, shot-length databases (Cinemetrics) | Good |
| **recalled** | Memory, unchecked this session | Lowest: label it; verify if it drives a major choice |

Search each film separately ("Road to Perdition cinematography Conrad Hall interview");
combined queries give shallow results. Prefer interviews over listicles. Paraphrase; quote
nothing long. Without web search, say so in one line, use playbooks and memory, tag accordingly.

## 5. Triangulation

- Shared by ≥2 films → **principle** (goes forward).
- Unique to one → **signature** ("don't copy").
- Shared by everyone and every parody → **cliché** (flag; `originality.md`).

This keeps the work original and filters one-off quirks.

## 6. Translation into decisions

Every principle ends as a decision, or it won't reach the film. Decisions feed the writers'
room (story, pacing, staging) and the art department (the look → the kit).

| Principle (films) | Dept | Decision | Becomes |
|---|---|---|---|
| Light from a visible practical (A, C) | Lighting | Every light a drawn source | light recipes; `require_any` on `SERIES.light.` |
| Violence watched from afar, sound drops (B, D) | Camera, sound | Wide and still for the act; silence before | a "watched" lens mode; bible silence rule |
| Long holds, ASL ≈ 9 s (A, E; documented) | Edit | Shots 6–12 s, a hold ≥2 s per scene | brief durations, holds |
| Bright even light, nothing hidden (F, G) | Lighting | High-key world light | a wash recipe; `bright_share` in the spec |

Principles point either way by series; the method is fixed, the answers aren't.

## 7. Saving it

For a genre, period or project with no playbook yet, end the dossier with a section in the
playbook format (`playbooks.md`) and offer it to the user. Research saves its cost next
time; the series lock keeps the look consistent.
