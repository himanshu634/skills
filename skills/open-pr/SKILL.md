---
name: open-pr
description: Push the current Koshi worktree branch and open a GitHub pull request into `staging` with a body in the repo's house style (what/why prose, decisions, the checks actually run, open items, requirement IDs). Use whenever the user says "push", "open a PR", "raise a PR", "send it for review", "ship this branch", or finishes a feature and wants it up for review — even if they don't name the base branch. Not for merging, releasing (`pnpm build:production`) or reviewing someone else's PR.
---

# Push and open a PR into staging

Koshi's work branch is **`staging`**, not `main` — every feature PR targets it. Several sessions edit this repo at once, each in its own worktree under `.claude/worktrees/`, so most of this skill is about proving the PR contains exactly your work and that the checks you quote ran on _your_ tree.

Run every command from the worktree path, as plain single commands. The worktree guard refuses git invoked through variables, `$(...)` or long `&&` chains, and a green check run in the primary checkout validates someone else's tree while looking identical.

## 1. Make sure it is yours, and not already up

- `git status --short` — the only untracked entry should be the `node_modules` symlink. Anything else unexpected: stop and ask.
- `git log --oneline origin/staging..HEAD` — the commits you are about to publish. A commit you don't recognise means the branch was cut from a stale or foreign head; ask before pushing.
- `gh pr list --state all --search "<two or three keywords>"` — concurrent sessions have shipped the same change first before. If an open PR covers it, say so instead of opening a second one.
- **The Linear ticket.** The session should have found or made it when the work began (rule in `~/.claude/CLAUDE.md`). If it did not, do it now through the Linear connector (ToolSearch `linear list issues save issue`): search the team's open issues for the change (`list_issues` with `query`); none fits → `save_issue` with `team: "Bull Agritech"`, `project: "Koshi"`, a one-line title in the ticket's own words and a short why. Leave it in `In Progress` (or move it there). A ticket in `Done`, `Released`, `Canceled` or `Duplicate` is not this change's: make a new one rather than reopening it. Its ID goes in the PR title (step 4) — that is the link Linear's automation acts on. Linear not connected: say so and open the PR without an ID.

## 2. Run the checks from the worktree

The `pnpm` scripts abort inside a worktree (the symlinked `node_modules` trips verify-deps), so call the binaries:

| Check  | Command                                                                                           | Notes                                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Types  | `mkdir -p .expo/types` then `node scripts/typed-routes.mjs` then `node_modules/.bin/tsc --noEmit` | A lone `Cannot find module '@/global.css'` means the gitignored `expo-env.d.ts` is missing from the worktree — recreate it with `/// <reference types="expo/types" />`, it is not your bug |
| Lint   | `CI=true node_modules/.bin/eslint <changed files>`                                                |                                                                                                                                                                                            |
| Format | `node_modules/.bin/prettier --check <changed files>`                                              | Never `pnpm format` — it rewrites other sessions' files                                                                                                                                    |
| i18n   | `node scripts/manage.mjs i18n:check`                                                              | Only when a locale file changed                                                                                                                                                            |
| Tests  | `node_modules/.bin/jest --testPathIgnorePatterns "/node_modules/" --testPathPattern "<regex>"`    | Pattern must go through the flag; a bare `jest <file>` finds nothing here                                                                                                                  |

Note the counts (tests passed, i18n keys) — the PR body quotes them. If something fails, fix it or report it; never open the PR claiming a check you didn't see pass.

**Changelog.** Every PR into `staging` adds a fragment `changelog.d/<slug>.md` and never edits `CHANGELOG.md` itself (the release folds fragments in; editing the shared file is what made PRs conflict). Format and rules: `changelog.d/README.md` (modules front matter, Added / Changed / Fixed / Removed, requirement IDs, the PR number, an **Open:** line for what is unfinished). Run `pnpm changelog:check`. The PR number is only known after step 4, so add it to the fragment then and push it as a follow-up commit. Nothing user-visible or team-visible? Label the PR `no-changelog` instead.

**Base moved.** If `gh pr view` or the `ccd_pr` status says the PR conflicts, `git fetch origin staging` then `git merge origin/staging` (merge, not rebase — the branch is already public, so no force push). Resolve by keeping both sides where two sessions appended to the same line (`CLAUDE.md`'s lists), rerun the step 2 checks on the merged tree, commit, push.

Uncommitted fixes from this step: stage **by name** (`git add <path> <path>`; `git add -A` stages the `node_modules` symlink) and commit with the requirement ID in the subject.

## 3. Push

`git push -u origin <branch>` — never ask first; the user's standing rule is to push and open the PR without a confirmation question. No force push.

## 4. Write the body to a file, then create the PR

Heredocs are awkward under the worktree guard, so write the body with the Write tool to the session scratchpad (e.g. `<scratchpad>/pr-body.md`) and pass it with `--body-file`.

Title: the conventional-commit subject of the change, requirement ID and Linear ticket in parentheses — `feat(billing): open WhatsApp on the farmer's chat with the bill PDF (M4-F14, BULL-123)`. Types in use: `feat`, `fix`, `chore`, `docs`, `refactor`. The ticket ID in the title is what links the PR: opening it keeps the ticket `In Progress`, and the merge into `staging` moves it to `In Review` with no hand edit. A PR that touches a ticket without delivering it names it in the body as `Part of BULL-123` instead, so the merge leaves its status alone.

Body, in this order (see `gh pr view 125` for a real one):

1. **What and why, as prose** — what the retailer experienced before, what changes, which requirement / principle it serves (`M4-F14`, `P2`, `X-O1`). He is the user; write about him, not about the code.
2. **Bullets for the how** — the moving parts a reviewer needs to find: new files, seams, what was deliberately left alone.
3. **Decisions (say so to change them)** — every judgement call made without the user. Open decisions D1–D7 are never resolved here; name them as open.
4. **Docs touched** — the spec file / `CLAUDE.md` line updated in the same PR.
5. **Checks from the worktree** — the commands from step 2 with their real counts, plus anything else run (prebuild, gradle, expo web walk).
6. **Open before merge** — a checklist of what you could not do: `pnpm build:dev` for native changes, a device pass, Gujarati review for new copy, a backend dependency.
7. Attribution line as the last line: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

Then:

```
gh pr create --base staging --head <branch> --title "<title>" --body-file <scratchpad>/pr-body.md
```

## 5. After it is open

- Give the user the PR URL as a markdown link, plus the open-before-merge items in a line or two.
- In the desktop app, bind the PR with the `ccd_pr` tools to read CI instead of polling `gh`. Never enable auto-merge unless asked.
- Record the open branch in the auto-memory "Open branches" list (one file + one `MEMORY.md` line: PR number, date, what is still open) — later sessions use it to avoid duplicate work.
