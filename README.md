# skills

Agent skills I wrote and use with Claude Code. Each folder under `skills/` is one skill: a `SKILL.md` plus any references, scripts and templates it needs.

## Install

Copy a folder into `~/.claude/skills/` (all projects) or `<repo>/.claude/skills/` (one project):

```bash
npx skills add himanshu634/skills
```

## General

| Skill | What it does |
|---|---|
| [design-directions](skills/design-directions) | Mockups-first design workflow: ground the request in the live app, draw 3–4 named directions on one canvas, build only after a pick. |
| [writing-ste](skills/writing-ste) | Write or check system documentation in ASD-STE100 Simplified Technical English, with a checker script. |

## Video

| Skill | What it does |
|---|---|
| [neon-chalkboard-motion](skills/neon-chalkboard-motion) | House style for explainer videos: dark board, neon accents, white chalk line-art. |
| [econ-short](skills/econ-short) | One sentence of Indian economy news in, one 50–60 s vertical explainer out. Runs the two skills below. |
| [econ-short-sound](skills/econ-short-sound) | Locks the timeline and composes the mood-matched, loop-perfect score. |
| [econ-short-render](skills/econ-short-render) | Builds and renders the 1080×1920 film, checks it, packages the upload kit. |
| [production-house](skills/production-house) | Film-studio pipeline for story-driven animation: research, writers' room, art department, series lock, shoot. |

## Project-specific

Written for one codebase. Useful as examples; they name files and rules of that project.

| Skill | Project | What it does |
|---|---|---|
| [open-pr](skills/open-pr) | Koshi (Expo app) | Checks, commit, push and PR in the project's format. |
| [release-notes](skills/release-notes) | Koshi | Release announcements from git history, one rendering per audience. |
| [new-screen](skills/new-screen) | Koshi | Scaffold a screen the way the app's conventions expect. |
| [new-component](skills/new-component) | Koshi | Scaffold a UI component and its gallery entry. |
| [add-i18n-key](skills/add-i18n-key) | Koshi | Add a translation key across locales. |
| [financial-figures](skills/financial-figures) | Maester | Rules for any number shown to an investor: source, formula, fixture. |
| [score-posting](skills/score-posting) | Job search | Score one job posting against a resume and profile. |
| [tailor-resume](skills/tailor-resume) | Job search | Cut a tailored resume for one posting from a maintained base. |

## Licence

[MIT](LICENSE)
