# Contributing to TDevPod

Thanks for your interest! TDevPod is a small hobby project, so replies may take
a few days.

## What TDevPod is (and isn't)

- **Display-only.** The "code" on screen is a drawing. TDevPod never runs,
  compiles, parses, or opens anything beyond the pretend scripts, and makes
  no network calls. Changes that break this won't be merged, because the
  whole point is that a toddler can't do anything real.
- **The lockdown comes first.** Anything that could let keys or clicks escape
  the pod is a top-priority bug.
- **Built for omarchy + Hyprland (Lua config).** Support for other setups is
  welcome if it doesn't complicate the omarchy path.
- **Quiet by design.** One word per keystroke or click, nothing moving on its
  own. Ideas that add idle animation or sound are likely a "no".

## Easy ways to help

- **Add a pretend script.** Drop a new file in [`scripts/`](scripts/): any
  language, kid-friendly themes (animals, trucks, snacks, space...), about 20-60
  lines. Lines starting with a bar like `[#####-----]` or a spinner glyph
  (`▖▘▝▗`) followed by a space redraw in place; see
  `scripts/install_dinos.sh`. No real secrets, personal names, or anything
  you wouldn't want a kid to "type".
- **Report bugs** using the bug form, including your omarchy and Hyprland
  versions.

## Pull requests

1. Keep changes focused: one fix or feature per PR.
2. Run the checks:
   ```sh
   ./tdevpod selftest
   python3 -c "import sys;sys.path.insert(0,'.');import tdevpod as t; e=t.Engine(); [e.reveal_word() for _ in range(2000)]"
   ```
3. If you change what the screen looks like, re-render the demo with
   `python3 tools/record_demo.py` (needs `ffmpeg`).
4. If you test a real launch, keep a second way in (SSH or a TTY) and remember
   `tdevpod unlock`.
