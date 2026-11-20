---
name: new-component
description: Scaffold a new Koshi UI component (primitive or composed) pre-patched with the four UI floors (X-U1–U4) and registered in the gallery.tsx dev screen. Use when the user asks to create a new component, or when implementing a feature needs a component that doesn't exist yet in src/components/.
---

# New component scaffold

Koshi's `CLAUDE.md` requires every component in `src/components/` to carry four non-negotiable floors, and every new one to get a section in `src/app/(dev)/gallery.tsx`. Both are easy to forget by hand — this skill does them together, in order.

Ask the user (if not already clear from context):
1. **Name** — PascalCase, e.g. `StatusPill`.
2. **Tier** — which directory it belongs in:
   - `src/components/ui/` — RNR/shadcn-style single-purpose primitive (only if it doesn't already exist via `npx @react-native-reusables/cli add <name>` — check that first for anything shadcn-shaped).
   - `src/components/form/` — combines primitives with form behaviour (bound field, `FieldFrame`, etc.). **Reminder**: if this is form UI, it must be exported from the `@/components/form` barrel — screens are eslint-forbidden from importing form internals directly.
   - `src/components/layout/`, `src/components/feedback/`, `src/components/illustration/` — as named.
   - A feature-scoped component instead belongs in `src/features/<module>/components/` — those still get a gallery.tsx section but skip the barrel-export step below.
3. **Shape** — a one-line description of what it renders and its variants (if any use `cva`).

## Steps

1. **Look at a sibling first.** Read an existing component in the same tier (e.g. `src/components/ui/chip.tsx` for a primitive, or something in `src/components/form/` for a bound field) to match the file's real conventions — import order, `cva` variant shape, `cn()` usage, whether it needs `TextClassContext`. Don't invent a different pattern.

2. **Write the component with all four floors present from the first draft:**
   - `min-h-12` (48dp) on the interactive/touch root — never a smaller explicit height, never `h-` on a text button. The only exception: painting 40dp inside a 48dp hit target (see `chip.tsx`'s `size="sm"` for the pattern) — the *touch target* still has to resolve to 48dp via `hitSlop`, the visual paint is what shrinks.
   - `text-base` (never `text-sm`/`text-xs`) on any label, button, or input text.
   - `leading-normal` (never `leading-none`) on any text — Gujarati conjuncts clip under `leading-none`.
   - Ink colors from a `-foreground` token (e.g. `text-primary-foreground`) — never `text-white`, never a hex value, never `StyleSheet`. Non-style colors (icon fills, etc.) use the `accent-` prefix.
   - If the component has a selected/checked state, show it with more than color (an icon, a border weight change) — X-U3.

3. **Add the barrel export** if this is a `src/components/form/` component — add it to that directory's index/barrel file alongside the existing exports.

4. **Register it in `src/app/(dev)/gallery.tsx`:**
   - Import it at the top with the other component imports (grouped by source, matching the existing import block).
   - Add a `<Section title="...">` block demonstrating the component's states/variants — model it on the closest existing section (e.g. the "Chip" section for a selectable control, "Badge" for a status indicator).
   - The gallery has one global light/dark toggle (`useUniwind` near the top of the screen) — you don't duplicate the section per theme. Instead, after adding it, mentally (or via the dev server) check the section renders correctly with the toggle in both positions, since `-foreground`/`-background` tokens should just work if you used them correctly in step 2.

5. **Run `pnpm typecheck`** to catch prop-type mismatches, and `pnpm lint` if the component touches import ordering.

## Common mistakes this exists to prevent

- Shipping a control at `h-10` or `text-sm` because it "looked fine" against a mock — the floors exist so nothing needs a special case.
- Forgetting the gallery.tsx section entirely — per `CLAUDE.md`, this is a guaranteed review comment.
- A form component built and used in a screen but never added to the `@/components/form` barrel, which then trips the eslint `no-restricted-imports` rule the first time someone imports it directly.
