# Series lock

One file freezing a series' look: bible (words), spec (numbers), series layer (code), and a
frozen engine copy. The user keeps it in the project; every film is built from it.

## 1. Contents

`<series>-lock.md`, written by `lock.py pack`:

| Section | Holds | Edited by |
|---|---|---|
| Header | `production-house:lock` marker, id, version, status (draft/approved) | tool |
| Bible | Story, look decisions with principles, lens grammar, light per world, cast, sets, sound, rules, approvals | art department, via repack |
| Spec | Palettes, fonts, fps, scene contract, frame checks | art department, via repack |
| Manifest | Vocabulary, per-entry hashes, code hashes | generated only |
| Series layer | `window.SERIES` | art department, via repack |
| Engine | Frozen copy of `engine/engine.js` | never |

The engine copy keeps an approved series on the engine it was approved with; moving engines
is a major bump. Markdown so the user can read their bible; code blocks are extracted
mechanically.

## 2. Creating and freezing

Pack a **draft** once the first series layer exists; repack each review round. After Gate 3,
record the tone test in the bible and pack with `--status approved`.

## 3. Handing over

Copy the lock to `/mnt/user-data/outputs/` and `present_files` it (a file, not a published
page). Tell the user:
1. Save it to this project's files.
2. Add the `lock.py instructions LOCK.md` snippet to the project instructions.
3. Look changes go through a version bump, never hand edits.

A playbook skill may also hold a copy; the project file is the working copy.

## 4. Loading later

Find the lock (project files, conversation, playbook skill), copy it to the working
directory:

```bash
python3 scripts/lock.py check LOCK.md       # hand edits caught by hash
python3 scripts/lock.py manifest LOCK.md    # allowed vocabulary
python3 scripts/lock.py unpack LOCK.md lock/
```

Read the bible before the writers' room. If `check` fails, show the user what changed
(`lock.py diff` against their last approved copy) and ask: adopt as a bump, or restore.

## 5. Versioning

Enforced by `lock.py pack --previous OLD.md`:

| Change | Bump | Needs |
|---|---|---|
| Bible/spec wording, palette correction, approval record | patch | user's OK |
| New set, character, recipe or mode; nothing approved touched | minor | Gate 2 on new items |
| Changed or removed approved entry; new engine | major | Gate 2 + new tone test |

A film keeps the lock version it was built with (in `scenes.json`'s look and `shared.js`'s
header); rebuild on a new major only if asked.

## 6. Commands

```bash
lock.py pack --bible B --spec S --series J [--status approved] [--previous OLD] --out LOCK.md
lock.py check | manifest | shared | instructions LOCK.md
lock.py unpack LOCK.md DIR
lock.py diff OLD.md NEW.md
```
