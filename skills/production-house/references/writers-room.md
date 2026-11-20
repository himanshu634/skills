# Writers' room

The screenplay is where a film is cheapest to fix. A one-line note here saves a set, a
character and a minute of animation later.

## 1. Draft

The screenwriter writes from the dossier and the user's answers in `templates/screenplay.md`:
- **Logline** and the episode's **"about" sentence** (a theme, not a plot).
- Dramatic scenes, each with slug line, **power ledger** (who holds power at start and
  end; no change → cut the scene), action written for picture, the **turn** in one line,
  sound / intertitle / VO marks.
- Estimated duration per scene, held against Motion's limits (≤300 s per film; a longer
  episode is a chain of films).

Motion has no dialogue track: unless the voice model puts voice in post, story lives in
behavior (who sits, who opens the door, an object changing hands, a light switched off).

## 2. Table read

Each chair reads the whole draft once and asks its own question
(`references/departments/` for each chair's craft).

| Chair | Reads for | Example note |
|---|---|---|
| **Director** (chairs) | Every scene serves the "about"? The one set piece? Rhythm? | "4 restates 2's turn; merge, spend the time on the hold in 5." |
| **DOP** | Each turn told in a picture? Where the one big move goes? What stays unseen? | "The betrayal reads better from across the room." |
| **Lighting** | Which light tells each turn? Where light changes as an event? | "Let the lamp going out be 6's turn; drop the intertitle." |
| **Production designer** | Sets needed, and does each earn its build? A recurring object? | "Market and dock can be one place at two times of day." |
| **Animator** | What the medium does badly here (lip-sync, crowds, fine hands)? Where holds go? | "Card trick needs finger work we can't sell; pass a coin." |
| **Sound** | Where silence goes; where the motif first sounds and returns changed | "Drop the bed a full second before the door in 7." |
| **Editor** | Runtime vs estimate; start late, leave early; split into Motion scenes (2–5 each: establish, approach, turn, aftermath) | "Enter 1 with the stranger already at the window." |
| **Continuity & standards** | Originality (no beat nameable as a famous film's scene), cliché, stereotype, period errors; for a continuing series, the bible | "The kiss on the hand is that film's signature; use the power object." |

≤3 notes per chair, most important first; "nothing material" is a valid answer. "Hard to
animate" is a note only with a better way to tell the same beat.

## 3. Note format

```
[Chair] Scene 4: <problem, one sentence>
Why: <research principle (films) or craft reason>
Fix: <concrete change>
Cost: <saves or costs: a set, seconds, a character, nothing>
```

No "why" = taste, least weight. A triangulated principle as "why" = most weight.

## 4. Conflicting notes

Log each as *A wants X, B wants Y*. Resolve by: the "about" sentence → the clearer ledger
→ the cheaper version. Director rules in one line. Recurring conflicts:
`references/departments/contradictions.md`.

## 5. Revision and log

One revision with every accepted note, then the log:

| Note | Decision | Reason |
|---|---|---|
| Director: merge 2 and 4 | Accepted | Same turn twice |
| DOP: wide for the betrayal | Rejected | Ledger needs the face turning away |

The log is part of the deliverable; the user may overrule any line.

## 6. Gate 1

Deliver: revised screenplay (Claude Doc when Docs tools exist, for line comments;
otherwise in the reply), the log, ≤3 open decisions. Apply changes, show changed scenes,
pass on clear approval. Nothing visual is built before it.

## 7. Continuing series

The lock's bible is the room's memory (arc, characters, power object, motif). Continuity
& standards checks against it. Flag new sets or characters in the log for the art department.
