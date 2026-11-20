---
name: new-screen
description: Use when adding a screen, route, page or flow step to Koshi — a new file under src/app/, a new step in a flow (bill, onboarding, add a product or farmer, poster, send), a new route group, or moving a screen between groups. Also when a screen slides, rises or fades the wrong way, Back animates like Next, or the keyboard or an entrance starts while the screen is still moving.
---

# New screen

A screen in Koshi is five things kept in step: a route file, a screen, an href, a **kind** (how it moves), and the copy. Most rules live elsewhere; this is the order to apply them in and where each is written down. Read the source named, never this summary of it.

**A design request comes first:** a new screen nobody has drawn runs `design-directions` (mockups, then a pick) before any of this.

## 1. Where it lives

- **Group:** the module's group under `src/app/(<module>)/` — pushed over the tabs, covers the bottom bar. Never a new tab (X-U5 nav ceiling, `src/app/(app)/_layout.tsx`).
- **File name:** a real name, never `index.tsx` inside a group (`test/app-routes.test.ts` says why). Params as `[id].tsx`.
- **Route file** is one line: `export { XScreen as default } from "@/features/<module>/screens/x-screen";`
- **Deep link anchor:** if the screen can be opened from outside its flow, check the group's `unstable_settings.initialRouteName` gives Back somewhere to go.
- **Href** in `src/features/<module>/routes.ts` (onboarding: `steps.ts`) — a function when it takes params. Never a string literal in a screen.

## 2. Its kind — how it moves (X-U13)

Add the route to its module's `*_SCREENS` map in `routes.ts`, keyed exactly as expo-router names it (`"profile/[id]"`). `test/screen-kinds.test.ts` fails until you do. The moves come from `src/lib/screen-motion.ts`; never set `animation` on a `Stack.Screen` by hand.

| He is…                                                   | Kind     | Moves                            |
| -------------------------------------------------------- | -------- | -------------------------------- |
| looking closer at something (a farmer, a bill, a list)   | `deeper` | slides in from the right         |
| starting something he will finish (a bill, a form, edit) | `task`   | rises; Back drops it             |
| on the next step of that task                            | `step`   | slides; opened on its own, rises |
| on the screen the task ends on (saved, the poster)       | `done`   | fades in place                   |

Ask "does he leave this by finishing it?" — yes: `task` (its first screen) or `step`. Ends it: `done`. Otherwise `deeper`.

**A new route group:** add its map to its module, spread `useStackMotion(MAP)` on its `<Stack>`, give its root entry `options={opens(MAP)}` in `src/app/_layout.tsx`, and add it to `KINDS_BY_GROUP` in `test/screen-kinds.test.ts`.

## 3. Moving between screens

| Need                                       | Call                                                                                                                                                                                                                                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| forward                                    | `router.push(href)`                                                                                                                                                                                                                                                                               |
| back                                       | `router.back()` / `router.dismissTo(href)`                                                                                                                                                                                                                                                        |
| a screen's Back (deep link: nothing under) | `backOr(router, fallbackHref)` from `@/lib/screen-motion` — pops, or replaces with the fallback as Back. Never hand-write `if (router.canGoBack()) router.back(); else router.replace(…)`                                                                                                         |
| a Back that must be a replace (onboarding) | `router.replace(asBack(href))` — plays as a pop                                                                                                                                                                                                                                                   |
| a task ends on its `done` screen           | collapse the group's own steps, then `replace(doneHref)`: `if ((navigation.getState()?.index ?? 0) > 0) router.dismissAll();` — `poster-screen.tsx` `toFarmers`. Not `router.canDismiss()`: it is true whenever any group is open, and on a one-screen group `dismissAll()` pops the group itself |
| "make another"                             | `replace(firstStepHref)` from the done screen                                                                                                                                                                                                                                                     |

## 4. Inside the screen

- **Header:** `AppBar` (it holds `BackChip`); stacks show no native header.
- **Inputs:** inside `Screen` (keyboard lives there only) — `docs/agents/components.md` → Keyboard. Form UI from `@/components/form`.
- **`autoFocus`:** only through `Input` / `OtpInput` (they wait for the screen to land); never in a `Modal`.
- **Motion on mount:** an entrance that is the screen's moment uses `NativeOnlyAnimatedView afterLanding`; a step bar uses `StepProgress animateOnMount`. Nothing starts while the screen still moves.
- **Server data:** a `queries.ts` hook, never `services`; a list takes the pull + `RefreshFailedNote` (X-U11); skeleton over 300 ms (X-U7).
- **Leaving with unsaved edits:** `useDiscardGuard` + `DiscardDialog`. A `BackHandler` returns `true` only when it acted (X-U9).
- **One primary action** (X-U5), destructive behind `AlertDialog` (X-U6), floors on everything (`ui-floor-reviewer`).
- **Copy:** `add-i18n-key`, Gujarati first; short (`design.md` → Copy).

## 5. Before the PR

`mkdir -p .expo/types && node scripts/typed-routes.mjs && node_modules/.bin/tsc --noEmit`; jest on the screen's tests plus `test/screen-kinds|test/app-routes`; a test per screen family (`renderWithProviders`). Spec row appended for the requirement, `changelog.d/` fragment, then `open-pr`.

## Common mistakes

| Mistake                                                               | Fix                                                            |
| --------------------------------------------------------------------- | -------------------------------------------------------------- |
| New route, no kind — the screen-kinds test fails                      | Add it to the module's `*_SCREENS` map                         |
| `animation: "..."` on a `Stack.Screen`                                | Change the kind instead; one source                            |
| Back implemented as `router.replace(prev)`                            | `router.replace(asBack(prev))`, or `router.back()`             |
| `if (router.canGoBack()) router.back(); else router.replace(x)`       | `backOr(router, x)`                                            |
| Saved screen pushed on top of the steps                               | collapse the group's steps, then `replace(saved)`; kind `done` |
| `if (router.canDismiss()) router.dismissAll()` before the done screen | guard on the group's own `navigation.getState().index`         |
| `autoFocus` on a raw `TextInput`, or `.focus()` in an effect on mount | `Input autoFocus` — it waits for the landing                   |
| Entrance `entering={…}` on a screen that slides in                    | add `afterLanding`                                             |
| New group wired in `_layout.tsx` but not in the kinds test            | add it to `KINDS_BY_GROUP`                                     |
