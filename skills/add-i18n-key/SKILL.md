---
name: add-i18n-key
description: Add a new translation key to Koshi's i18n catalogues in the correct order (gu/ first, then en/, then verify). Use whenever a feature needs new user-facing copy, or a zod schema needs a new error-message key.
---

# Add an i18n key

Koshi's `src/i18n/locales/README.md` and `CLAUDE.md` are explicit: **`gu/` is the source, `en/` is the gloss.** A key exists once it exists in `gu/` — types are generated off the Gujarati catalogue. Adding it to `en/` first, or only, does not make it real and will fail `pnpm i18n:check`. This skill exists because that order is easy to do backwards under deadline pressure.

## Steps

1. **Pick the namespace file.** One file per module: `common` (shared chrome), `auth` (M1), `farmers` (M2), `catalogue` (M3), `billing` (M4), `home`, `settings`. A brand-new module gets a brand-new namespace file, not a growing existing one — check `src/i18n/locales/gu/` for the current list before assuming.

2. **Pick the key path.** Match the existing nesting style in that namespace file (e.g. `login.phone.label`, `errors.phone.invalid`). For a zod schema `error` value, the key must be a **full i18n key** including namespace, e.g. `"auth:errors.phone.invalid"` — `FieldError` resolves it at render, it is not auto-prefixed.

3. **Write the Gujarati value first**, in `src/i18n/locales/gu/<namespace>.json`. If you (the assistant) are not a native Gujarati speaker's substitute for review, say so — per the README, all committed Gujarati strings are either reviewed content or explicitly-flagged provisional scaffolding, and machine translation is forbidden (X-L2). Ask the user whether this string needs human review before it ships, and if it's provisional, don't imply otherwise.

4. **Numerals**: never bake a formatted number into the string. If the copy needs a number, use an i18next interpolation placeholder (e.g. `{{count}}`, `{{phone}}`) and let the call site format it via `formatNumber`/`formatCurrency` from `src/lib/format.ts` — never `Intl` directly, never a literal digit sequence meant to vary (X-L4).

5. **Mirror the exact same key path into `src/i18n/locales/en/<namespace>.json`** with the English gloss. The key sets must be identical — same nesting, same leaf keys, nothing extra in one and not the other.

6. **Verify:**
   ```bash
   pnpm i18n:check
   ```
   This fails loudly on any drift between `gu/` and `en/`. Don't consider the key added until this passes — if a `PostToolUse` hook is configured for locale files, it will also run this automatically after you save.

7. **Use it with `t()` called at render time** — never store the resolved string in `useState` or a module-level constant (it won't react to a language change), and never key a layout/navigator on the locale.

## Common mistakes this exists to prevent

- Adding the key to `en/` only (or first), which passes a casual glance but fails `pnpm i18n:check` and blocks the PR.
- Baking a formatted digit string into the Gujarati/English value instead of interpolating it, silently breaking X-L4 (Latin numerals regardless of UI language).
- Writing a zod `error` as a bare string instead of a namespaced i18n key, which `FieldError` won't resolve.
