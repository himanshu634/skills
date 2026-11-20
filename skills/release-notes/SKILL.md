---
name: release-notes
description: Write Koshi's release announcements from git history — a WhatsApp-ready message per environment (staging for the internal team and testers, with the Linear ticket behind each change so a tester can check the build against it; production for retailers and the field team) and the store "What's new" notes for Google Play and the App Store, in English with a Gujarati draft. Use whenever the user asks for release notes, a changelog, a "what changed" or "what's new" message, a WhatsApp/Slack update about a build or version, a list of Linear tickets for testers to verify, Play Console or App Store Connect release text, or says they just ran `pnpm build:production`, `pnpm version:bump` or a staging build and need to tell people — even if they don't say "release notes".
---

# Release notes

One commit range, up to four renderings of it: a **staging** WhatsApp message, a **production** WhatsApp message, **Play Store** notes, **App Store** notes. They differ by audience and by the field they get pasted into, not by the commits they cover. The staging message also names the Linear ticket each change answers, so a tester checks the build against what was asked, not only against the PR. Output goes in the chat, ready to copy — nothing is written to the repo.

The hard part is not the prose. It is deciding what a user can actually _see_. Git history on `staging` is full of things that are real commits and invisible to a retailer: release chores, a web page, a POC behind `__DEV__`, a feature added and reverted in the same week. A note that announces one of those is worse than no note — a retailer goes looking for a button that isn't there.

## 1. Pin the range and the facts

- **Version and build** come from `package.json` (`version`, `koshi.build`). Nothing else declares them.
- **Range default:** the previous `v*` tag → the current one (`git tag --sort=-creatordate`). If `HEAD` is ahead of the newest tag (a staging build before the bump), use newest tag → `HEAD` and name it "unreleased".
- `v*` tags are shared by every environment, but production can lag staging (a version can reach staging at build 7 and production at build 9, or skip production entirely). **What reached a store is on `main`:** each production build adds a release commit there, tagged `prod-<platform>-<version>-<build>` (README → `main` is production). So for a production message and store notes the range is the platform's last `prod-*` tag → the build being announced (`git fetch origin main --tags`, then `git describe --tags --abbrev=0 --match 'prod-android-*' origin/main`), and `git log origin/main..origin/staging` is what has not shipped. A record means "sent to the store", not "approved": if the user says the last one was rejected, start from the one before. `releases/*.aab|apk` filenames look like a record but are gitignored and exist on one machine only — don't depend on them.
- **A tag is not a build of everything before `HEAD`.** A PR merged after the newest tag is in no installed build yet (`git log -1 --format=%ci <tag>` against the PR's merge time). Don't title the staging message with that tag's build, or testers look for features their phone doesn't have. Say the next staging build (`version:bump`, then `distribute`) comes first.
- **Print the range in one line before anything else** (`Range: v0.4.0 → v0.5.0 (build 10), 58 commits`) so a wrong default is caught at a glance.
- Read `eas.json` → `build.production.env.EXPO_PUBLIC_API_URL`. If it contains `staging`, production installs write to the staging backend — say so in the notes-for-you section (see step 5). `scripts/manage.mjs` → `productionCautions()` records this as deliberate; repeat it, don't "fix" it.
- Read `eas.json` → `submit.production.android.track`. Anything other than `production` (it is `internal` today) means `eas submit` puts the build on a testing track that retailers never see. A "please update from the Play Store" message sent before someone promotes the release in Play Console sends retailers looking for an update that isn't there. Put **promote to production in Play Console first** at the top of the notes-for-you, not buried in the list.

## 2. Gather

```bash
git log --no-merges --format='%h %s' <from>..<to>
git log --merges --format='%h %s' <from>..<to>     # PR numbers
gh pr view <n> --json title,body                    # open items: device pass, Gujarati review, backend pending
```

Commits follow `type(scope): subject (REQ-IDs)`. The subject is written for engineers; the PR body usually says what the user sees and what is still open. Read the PR body for anything user-facing before describing it.

Also check the backend PRs a body names (`gh pr view <n> --repo TechatBull/koshi-backend --json state,mergedAt`). What a tester sees often depends on whether that one is merged and deployed to staging.

### Linear tickets

Testers check the build against the ticket. For each PR in the range, find the Linear issue it implements.

- **Read Linear through the connector**: ToolSearch `linear get issue list issues` loads `get_issue` and `list_issues`. Its tool names change per session, so don't hardcode them. If no Linear tools load, or they need auth, say so in the notes-for-you and use PR numbers only. Never open linear.app in a browser or WebFetch it: it is behind a sign-in.
- **Join keys**, strongest first:
  1. the issue's `attachments` hold the PR URL (`get_issue` with `fields: ["attachments"]`). Linear's GitHub integration adds it when the ID is in the PR title or branch;
  2. the ID (`BULL-<n>`, `KID-<n>`) is in the PR title, a commit subject or the branch (`tech/bull-<n>-…`);
  3. the ID or a `linear.app` link is in the PR body or a commit body.

  ```bash
  git log --format=%B <from>..<to> | grep -oE '(BULL|KID)-[0-9]+' | sort -u
  gh pr view <n> --json title,headRefName,body --jq '.title+" "+.headRefName+" "+.body' \
    | grep -oE '(BULL|KID)-[0-9]+|linear\.app/[^ )]*' | sort -u
  ```

- **Implements vs related.** Only keys 1 and 2 make the ticket the spec a tester checks against. An ID found only in body prose is often a cross-reference: #362's body names BULL-199 only because both backend PRs add the same migration. Read the sentence. A ticket you find by searching Linear for the feature (`list_issues` with `query`) is _related_. It may ask for more, or for something else: BULL-143 asks for crop, tab-bar and other icons, and #360 shows only the crop marks staff set in the Console. Keep a related ticket out of the tester's message and name it in the notes-for-you, or a tester fails the build for scope it never had.
- **Read the ticket, not only its title** (`fields: ["title","url","status","description"]`). Compare its ask with the PR body and name each deliberate difference: an owner decision, a list that product still has to confirm, Android only. Then a tester doesn't file it as a bug.
- Use each `url` exactly as `get_issue` returns it.
- **Every ticket the message names is in review.** Linear's GitHub automation moves a ticket to `In Review` when its PR merges into `staging`, so most already are. Read each one's `status` before you hand the message over. One still in `Backlog`, `Todo` or `In Progress` (its PR had no ID in the title, or the automation missed it) moves to `In Review` (`save_issue` with `id` and `state: "In Review"`). The tester moves it to `Done` after a pass; `pnpm release:shipped` moves it to `Released` once the store approves the build (README → Linear tickets follow the build). Take the state name from `list_issue_statuses` for the ticket's team, because KID is a different team from BULL. If that team has no review state, leave the ticket and say so. Never move a ticket back from `Done` or `Released`. Never move a `Canceled` or `Duplicate` one: name it in the notes-for-you. Never move a related ticket: its scope is not built.
- A PR with no ticket keeps its PR number and requirement ID, and says "no Linear ticket".

## 3. Decide what is visible

Work through every commit. Keep a list of what you dropped and why — it is part of the output.

**Drop both sides of a revert.** Look for `revert(...)` / `Revert "..."` and for a later commit whose subject undoes an earlier one (`the crop cycle has no start date` cancels `the cycle screen carries its start week`). Net zero change is not a feature.

**Drop what no user touches:** `chore(release|build)`, `docs(...)`, `test(...)`, tooling, CI, `.claude/`, the marketing website, a web-only page (the account-deletion page is for the Play listing, not the app), refactors with no visible effect. A `perf` or `refactor` stays only if a user would notice ("the list is faster").

**Check that a `feat` is reachable before announcing it.** POCs land on `staging` routinely. For each feature find its entry point (the button, row or route that opens it) and confirm:

- it is not inside `__DEV__ ? … : …`, the `(dev)` route group, or a dev-only menu;
- it isn't hidden by a flag or env check;
- its service has a real adapter, not only `services/mock/` — a mock-only feature shows UI but saves nothing. It can go in the **staging** message ("UI only, not saved yet"), never in production or store notes.

`git grep -n <route-const-or-testID> <tag> -- src/features src/app` against the tag, not the working tree.

**Then check that it finishes what it promises.** Reachable is not the same as working. Follow the feature to the result the user expects and confirm something delivers it. The voice poster in v0.5.0 is the example: the Home button is live for every retailer and the recording uploads for real, but the backend has no voice-note route, so the screen ends on "your poster will appear here" and nothing ever comes. Signs of a dead end: a success screen that only says something _will_ happen, an upload with no consumer, a PR body that says "POC" or "backend pending", a service method with no http adapter.

- A dead-end feature goes in the **staging** message, labelled ("records and uploads — no poster comes back yet").
- It stays out of production and store notes.
- Because retailers can still tap it, name it in the notes-for-you with what they will see, so the person posting can decide to hide the button or brief the field team. Leaving it out of the announcement does not make it invisible.

**Collapse follow-ups into their feature.** Three commits fixing the send list after it shipped in the same range are one line: the feature. A fix counts as its own line only if the bug existed in the _previous_ release.

**Group by what the retailer does**, not by module ID: sending to farmers, farmers & crops, billing, look and feel. Requirement IDs (`M6-F7`, `X-U2`) and Linear IDs or links (`BULL-142`) never appear in production or store text. Linear is private to the team.

## 4. Render

WhatsApp formatting is not Markdown: `*bold*`, `_italic_`, `•` or `-` bullets, no `#` headers, no `**`, no links in production text. Put each message in a fenced block so it copies clean.

### Staging — internal team and testers

Purpose: tell testers what to test and what is known-broken. Engineers read it, so depth is welcome.

```
*Koshi staging v0.5.0 (build 10)* 🧪
Range v0.4.0 → v0.5.0

*New — please test*
• <feature> — <where to find it> — <what to try> (#117 · BULL-142)

*Fixed*
• <what used to go wrong> (#119 · BULL-150)

*Known gaps*
• <device pass / Gujarati review / backend field pending> (#124)

*Not in this build for users*
• <reachable only in dev, mock-only, reverted>

*Check against Linear*
• BULL-142 · <ticket title, shortened> · In Review
https://linear.app/bull-agritech/issue/BULL-142/…
Asks: <the ticket's ask in one line>
Built: <as asked / each deliberate difference> (#117)
• No Linear ticket: <feature> (#122, M8-F15)

Report issues in the group with a screenshot 🙏
```

Include mock-only and not-yet-reviewed-Gujarati items here, labelled. The PR number goes on each line, with the Linear ID when the ticket is one the PR implements (step 2). Put each Linear URL on a line of its own so WhatsApp makes it tappable.

### Production — retailers and field team

Purpose: say what got better for a shop owner. Only reachable, real, finished features. Benefit first, plain words, one line each, no jargon ("virtualised", "hand-off", "endpoint"), no PR numbers, no "POC".

```
*Koshi app v0.5.0 is out* 🚀

*📲 <group>*
• <benefit in the retailer's words>

*🌱 <group>*
• …

Please update from the Play Store and tell us if anything looks wrong 🙏
```

Keep it under ~15 bullets; if there are more, merge. English by default. If the user wants a Gujarati version, follow the Gujarati rules below.

Remember P2: the app never contacts a farmer. Describe sending as the retailer sending from his own WhatsApp ("send to your farmers on WhatsApp"), never "Koshi messages your farmers".

### Play Store — "What's new in this release"

**500 characters per language**, spaces and newlines included. It is the tightest field, so write it last, from the production list, keeping the top 3–5 items.

Paste format for Play Console, one block per language:

```
<en-US>
• Send photos and products to your farmers on WhatsApp
• Set each crop's sowing week when adding a farmer
• Payment dates now save correctly
• New app icon
</en-US>
<gu>
…
</gu>
```

No headers, no emoji-heavy lines, no version number (Play shows it). Confirm the Gujarati locale tag in the console on first use; Play lists it as Gujarati (`gu`).

### App Store — "What's New in This Version"

Up to **4000 characters**, plain text (no Markdown renders). One short lead sentence, then `•` bullets — it can carry the full production list. English (U.K.) is India's default App Store language and Gujarati is a supported localization, so give both. Not shown on an app's first version; iOS is not submitted yet, so label the block "prepared ahead".

### Character counts

Report the count next to every store block, counted by code point (Gujarati combining marks count — this overestimates slightly, which is the safe side):

```bash
node -e 'const s=require("fs").readFileSync(0,"utf8").replace(/\n$/,"");console.log([...s].length)' <<'EOF'
<text>
EOF
```

Over the limit → cut items, don't abbreviate words.

## Gujarati drafts

Gujarati is the product's primary language (P1, X-L1) and machine translation is forbidden in shipped copy (X-L2). A Gujarati draft here is a starting point for a native reviewer, not publishable text:

- Label it outside the pasteable block: **Gujarati — provisional, needs native review before publishing.**
- Reuse the app's own Gujarati for feature names — `git grep` the English label in `src/i18n/locales/en/`, take the same key from `gu/`. A retailer should read the same word in the note as on the button.
- Numbers stay Latin (`v0.5.0`, `26 weeks`) per X-L4.

## 5. Notes for you (outside the messages)

After the blocks, a short plain list for the person posting — never inside a pasteable block:

- **first, for a production message:** the Play track, if it isn't `production` — promote the release before posting;
- for a production message: once the store approves, `pnpm release:shipped --platform=<android|ios>` moves the build's tickets to `Released`;
- the range used, and that it can be changed;
- PRs merged after the newest build's tag, and the build they wait for;
- Linear: whether the connector was used, each ticket you moved to `In Review` (from which state), tickets you could not move and why, and related tickets left out of the message with what this build covers of each;
- features retailers can reach that don't deliver yet, and what they will see if they tap them;
- **left out on purpose**, with one reason each (reverted, dev-only, web page, tooling);
- anything announced to staging but held from production and why;
- open items from PR bodies that a retailer might hit;
- the production-API-on-staging caution, if step 1 found it;
- character counts that came close to a limit.

## Which blocks to produce

- User names an environment → that WhatsApp message (plus store notes if production and they ask).
- User asks for notes for testers, or for Linear tickets to verify → the staging message with its _Check against Linear_ block.
- User asks for store / Play / App Store notes → both stores, English + Gujarati draft.
- User says only "release notes" / "what changed" → all four.
- `development` gets no message; dev clients are for engineers. Say so if asked.
