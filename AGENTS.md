# AGENTS.md — TDevPod: Toddler Dev Pod

Quick brief so a fresh session can pick up instantly. Read this first, then
`tdevpod.py` and the `tdevpod` wrapper for the real source of truth.

## What this is

A fullscreen pretend terminal for omarchy/Hyprland that turns toddler
keyboard/mouse banging into fake "typing code". Every keystroke/click reveals
exactly **one word** of pretend code; the screen is quiet otherwise. It is
**display-only** — the pretend source lives in a drawing buffer and is never
parsed/compiled/executed. The only real "escape hatches" are the recharge
combos. Goal: the computer underneath is safely on timeout while the kid plays.

## Where things live

| Path | Role |
|---|---|
| `<repo>/tdevpod` | Bash wrapper: `start` / `unlock` / `install` / `selftest` |
| `<repo>/tdevpod.py` | The GTK3 theatre + Engine (word-per-key reveal) |
| `<repo>/tdevpod.py` `_load_theme()` | Loads omarchy's live theme colors at startup |
| `<repo>/scripts/` | Default pretend-code pool (15 files, many languages) |
| `~/.config/tdevpod/scripts/` | User drop-in pool; replaces `scripts/` if non-empty (dir auto-created) |
| `<repo>/tools/record_demo.py` | Renders `docs/demo.gif` offscreen via `TDevPodApp.render()` |
| `~/.config/hypr/bindings.lua` | `TDEVPOD MARKER` block: SUPER+J launcher, window rule, submap exit bind |
| `/usr/share/omarchy/themes/<t>/colors.toml` | Theme sources (all share the same key format) |
| `~/.local/state/omarchy/current/theme/colors.toml` | Active theme copy; `theme.name` = current theme name |

## Verified environment facts (omarchy/this machine, do not re-litigate)

- OS is omarchy on Hyprland/Wayland, `DISPLAY=:0`, Python 3.14.7. Original
  tkinter was **broken** (missing `libtk8.6.so`); the app uses **GTK3 via `gi`**
  (works). `GDK_BACKEND=wayland,x11,*`.
- Hyprland config is **Lua here**, so:
  - `hyprctl keyword` FAILS ("keyword can't work with non-legacy parsers. Use
    eval."). `hyprctl eval` always prints `ok`. `hyprctl repl '<lua>'` evaluates
    and returns values.
  - Use `hl.define_submap("name", function() hl.bind(...) end)` to register
    submap binds; enter with `hyprctl dispatch 'hl.dsp.submap("name")'`, exit
    with `'hl.dsp.submap("reset")'`. While a submap is active, ONLY its binds
    work. Right-click/other binds are dead.
  - Keysym is `ESCAPE`, never `ESC` ("Unknown keysym" error).
  - `SUPER + J` was already bound by omarchy default ("Toggle window split") →
    `hl.unbind("SUPER + J")` must come before `o.bind("SUPER + J", …)`.
  - Valid window-rule keys in this build: `float`, `fullscreen`, `pin`,
    `no_focus`, `opacity`, `suppress_event`, `tag`. `border`, `noborder`,
    `keepaspectratio`, `noanim` → "unknown field" errors.
  - Hyprland sees the app window class as `tdevpod.py` regardless of
    `Gdk.set_program_class`; matchers must use `^tdevpod`.
- The app window is **native Wayland**, not XWayland (`xwayland: 0`). The Xlib
  `XGrabKeyboard`/`XGrabPointer` in `tdevpod.py` is **best-effort** and only
  covers XWayland clients; the authoritative toddler lockdown is the submap.

## Lockdown model

1. `./tdevpod start` → enters the `tdevpod` submap, launches the app, and
   after ~1s dispatches `focuswindow class:^tdevpod`. When the app exits for
   ANY reason, the wrapper exits the submap and runs `hyprctl reload` so normal
   binds return.
2. Exit paths (all verified working):
   - `SUPER + CTRL + SHIFT + ESC` — submap bind running `…/tdevpod unlock`,
     also handled in-app.
   - Spell `exit-tdevpod` — tracked via a raw-letter ring (typed letters vs.
     displayed script words are different things, so the ring tracks real
     keystrokes).
   - Emergency: `./tdevpod unlock` from any terminal.
3. `./tdevpod install` idempotently appends the `TDEVPOD MARKER` block to
   `~/.config/hypr/bindings.lua` (with timestamped backup). It contains:
   `hl.unbind("SUPER + J")`, `o.bind("SUPER + J", …, "<abs>/tdevpod")`,
   `o.window("^tdevpod", { float = true, fullscreen = 1 })`, and the submap
   with its exit bind. Note: bindings use ABSOLUTE paths
   (`<repo>/tdevpod`); re-run `install` after moving the
   repo. `hyprctl configerrors` must stay clean; inspect the block with
   `hyprctl binds | rg -i tdevpod`.

## Verify / test

- `./tdevpod selftest` — brief non-grabbing smoke test (opens/renders/closes
  a window); exit 0 = pass.
- Headless engine test (no display needed):
  `python3 -c "import sys;sys.path.insert(0,'.');import tdevpod as t; e=t.Engine(); [e.reveal_word() for _ in range(20)]"`.
- Full cycle: `setsid --fork ./tdevpod start >/tmp/tdevpod.log 2>&1 </dev/null &`,
  sleep ~3, check `hyprctl submap` == `tdevpod` and the window is fullscreen
  (`hyprctl clients | rg -A8 'class: tdevpod'`), screenshot with
  `grim -l 1 /tmp/shot.png`, then `./tdevpod unlock` (verify `submap` back to
  `default`).
- VERIFY SUPERVISION: NEVER leave the pod running when done — the user's
  keyboard is toddler-locked while the submap is active.

## Behavior contract to preserve (don't regress)

- Screen quiet until touched; ONE word per keystroke and per click (click also
  spawns sparks). No idle auto-typing, no injected system lines, no stray
  "finalize". `reveal_word()` returns after one real word (also must handle
  `open`/`lineend` tokens: those skip without drawing a word).
- Footer: line 1 = status left (elided via `draw_fit` with reserved space for
  the right-anchored green `exit:` text), line 2 = "…or spell out:
  exit-tdevpod". They must never overlap.
- Palette: module constants are adopted from omarchy's ACTIVE theme via
  `_load_theme()` (per-key TOML regex, per-key fallback to Tokyo Night
  defaults). TOML keys map: `background`→BG, `dark_background`→DARK,
  `darker_background`→DARKER, `lighter_background`→LIGHTER,
  `bright_foreground`→FG, `dark_foreground`→DIM, `muted`→MUTED, `accent`→ACCENT
  (also `blue`), plus named `red`,`yellow`,`orange`,`green`,`cyan`,`magenta`.
- Pool: `load_pool()` = `~/.config/tdevpod/scripts/` if non-empty, else the
  repo's `scripts/`, else the built-in `FILES`. Tabs are expanded to 4 spaces
  (the renderer is cell-based; raw tabs overlap text). `Engine` shuffles the pool per launch and
  reshuffles on wrap, so each session differs.
- Live lines (`is_live_line()`: `[####--]`-style bar or spinner glyph + space)
  are one token each; consecutive live lines overwrite each other in place
  (`Engine._put_live`), still one token per keystroke. Separate distinct bar
  groups with a normal line or they merge into one row.
- Do NOT execute, parse, or even imply the content runs. It is a drawing buffer.

## Gotchas / history worth knowing

- **grim** may transiently hang on screenshot capture (times out; even a small
  `-g` crop). It is NOT deterministically caused by the app; a
  `hyprctl reload` (which `unlock` does anyway) clears it — retry, don't
  chase a compositor bug.
- Reveal-word "open"-token unpack bug (`_, idx, name = rest` vs 2-value rest)
  was fixed; it would have crashed on the first real keystroke. Keep tests
  exercising `reveal_word()` headlessly.
- `__pycache__/` is gitignored; remove generated pyc if you ship a tree.

## Git

- Repo: `origin → https://github.com/frankdatank007/tdevpod.git`
  (https://github.com/frankdatank007/tdevpod)
- Branch: `main` (tracks `origin/main`). Install-side bindings use absolute
  paths, so pulling a new version does NOT require re-running `install` unless
  the wrapper path or keybinds changed.