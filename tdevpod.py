#!/usr/bin/env python3
"""
TDevPod: Toddler Dev Pod — a toddler-safe "developer pod".

A fullscreen pretend terminal (Tokyo Night, omarchy-flavored). The screen is
quiet until the toddler touches something: every keystroke reveals exactly one
word of pretend "code" (roughly word-per-key, Play-Doh style), and every
click pops a word plus a few sparks. When hands go quiet the screen goes
quiet. The palette tracks omarchy's active theme. The pretend corpus is the
repo's scripts/ folder; files dropped into ~/.config/tdevpod/scripts/ replace
it (shuffled, so no two sessions read the same code). Consecutive progress-bar
or spinner lines redraw in place, so a hammering toddler "animates" them. Nothing here is ever executed and no
real program is ever run.

Safe exit (for the grown-ups):
    SUPER + CTRL + SHIFT + ESC   (handled by the Hyprland submap, or in-app)
    ...or spell out:  exit-tdevpod  (letters land on sneaky ears)

Run it through the `tdevpod` wrapper so the compositor lockdown (submap)
is engaged and restored around this app.
"""

from __future__ import annotations

import ctypes
import ctypes.util
import os
import random
import re
import sys
import time

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gdk, GLib, Gtk, Pango, PangoCairo  # noqa: E402

# --------------------------------------------------------------------------
# Tokyo Night palette (matches the omarchy tokyo-night theme)
# --------------------------------------------------------------------------
BG      = (0x1A, 0x1B, 0x26)
DARK    = (0x13, 0x14, 0x1C)
DARKER  = (0x0E, 0x0E, 0x14)
LIGHTER = (0x24, 0x28, 0x3B)
FG      = (0xC0, 0xCA, 0xF5)
DIM     = (0x56, 0x5F, 0x89)
MUTED   = (0x41, 0x48, 0x68)
ACCENT  = (0x7A, 0xA2, 0xF7)
GREEN   = (0x9E, 0xCE, 0x6A)
YELLOW  = (0xE0, 0xAF, 0x68)
ORANGE  = (0xEB, 0x92, 0x7B)
RED     = (0xF7, 0x76, 0x8E)
CYAN    = (0x44, 0x9D, 0xAB)
MAGENTA = (0xAD, 0x8E, 0xE6)

FONT = "JetBrainsMono Nerd Font"
EXIT_KEYS = "SUPER+CTRL+SHIFT+ESC"

THEME_TOML = os.path.expanduser("~/.local/state/omarchy/current/theme/colors.toml")
SCRIPT_DIR = os.path.expanduser("~/.config/tdevpod/scripts")
REPO_SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")

# omarchy colors.toml key -> our palette constant. Loaded live so the pod
# always matches whatever theme omarchy is running right now.
_THEME_MAP = {
    "BG": "background",
    "DARK": "dark_background",
    "DARKER": "darker_background",
    "LIGHTER": "lighter_background",
    "FG": "bright_foreground",
    "DIM": "dark_foreground",
    "MUTED": "muted",
    "ACCENT": "accent",
    "GREEN": "green",
    "YELLOW": "yellow",
    "ORANGE": "orange",
    "RED": "red",
    "CYAN": "cyan",
    "MAGENTA": "magenta",
}


def _load_theme():
    """Read omarchy's active theme colors and adopt them (per-key fallback)."""
    try:
        with open(THEME_TOML, "r", encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return
    for const, key in _THEME_MAP.items():
        m = re.search(rf"^\s*{re.escape(key)}\s*=\s*\"#([0-9A-Fa-f]{{6}})\"", text, re.M)
        if not m:
            continue
        h = m.group(1)
        rgb = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        if const in globals():
            globals()[const] = rgb


# TDEVPOD_THEME=builtin keeps the Tokyo Night defaults (used by the demo GIF).
if os.environ.get("TDEVPOD_THEME") != "builtin":
    _load_theme()


GrabModeAsync = 1
CurrentTime = 0


def hex_to(c):
    return c[0] / 255.0, c[1] / 255.0, c[2] / 255.0


# --------------------------------------------------------------------------
# Best-effort global input grab via Xlib (XWayland).
# owner_events=True keeps the focus/pointer flow intact while telling every
# other X client to sit down.
# --------------------------------------------------------------------------
X11 = None


def _load_x11():
    global X11
    if X11 is not None:
        return X11
    lib = ctypes.util.find_library("X11")
    if not lib:
        return None
    try:
        x = ctypes.CDLL(lib)
    except OSError:
        return None
    x.XOpenDisplay.restype = ctypes.c_void_p
    x.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x.XDefaultRootWindow.restype = ctypes.c_ulong
    x.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
    x.XGrabKeyboard.restype = ctypes.c_int
    x.XGrabKeyboard.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int,
                                ctypes.c_int, ctypes.c_int, ctypes.c_ulong]
    x.XGrabPointer.restype = ctypes.c_int
    x.XGrabPointer.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_int,
                               ctypes.c_ulong, ctypes.c_int, ctypes.c_int,
                               ctypes.c_ulong, ctypes.c_void_p, ctypes.c_ulong]
    x.XUngrabKeyboard.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
    x.XUngrabPointer.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
    x.XFlush.argtypes = [ctypes.c_void_p]
    X11 = x
    return x


def grab_input():
    if _load_x11() is None:
        return False
    try:
        d = X11.XOpenDisplay(os.environ.get("DISPLAY", "").encode())
        if not d:
            return False
        root = X11.XDefaultRootWindow(d)
        mask = (1 << 2) | (1 << 3) | (1 << 6) | (1 << 7) | (1 << 8)
        kb = X11.XGrabKeyboard(d, root, True, GrabModeAsync, GrabModeAsync, CurrentTime)
        pt = X11.XGrabPointer(d, root, True, mask,
                              GrabModeAsync, GrabModeAsync, root, None, CurrentTime)
        X11.XFlush(d)
        return True
    except Exception:
        return False


def ungrab_input():
    if _load_x11() is None:
        return
    try:
        d = X11.XOpenDisplay(os.environ.get("DISPLAY", "").encode())
        if d:
            X11.XUngrabKeyboard(d, CurrentTime)
            X11.XUngrabPointer(d, CurrentTime)
            X11.XFlush(d)
    except Exception:
        pass


# --------------------------------------------------------------------------
# Script pool — pretend omarchy dotfiles. Only ever drawn, never executed.
# --------------------------------------------------------------------------
FILES = [
    {
        "name": "~/.config/hypr/bindings.lua",
        "lines": [
            "local o = require(\"omarchy\")",
            "",
            "-- TDevPod: toddler dev pod  (display only, never run)",
            "o.bind(\"SUPER + J\", \"TDevPod\", \"~/dev/tdevpod/tdevpod\")",
            "hl.unbind(\"SUPER + J\")",
            "",
            "hl.define_submap(\"tdevpod\", function()",
            "  hl.bind(\"SUPER + CTRL + SHIFT + ESCAPE\",",
            "          hl.dsp.exec_cmd(\"~/dev/tdevpod/tdevpod unlock\"))",
            "end)",
            "",
            "o.window(\"^tdevpod\", { float = true, fullscreen = 1 })",
        ],
    },
    {
        "name": "~/.local/share/omarchy/themes/tokyo-night/colors.toml",
        "lines": [
            "mode = \"dark\"",
            "",
            "accent = \"#7aa2f7\"",
            "background = \"#1a1b26\"",
            "dark_background = \"#13141c\"",
            "foreground = \"#a9b1d6\"",
            "red = \"#f7768e\"",
            "green = \"#9ece6a\"",
            "yellow = \"#e0af68\"",
            "cyan = \"#449dab\"",
            "magenta = \"#bb9af7\"",
        ],
    },
    {
        "name": "~/.config/omarchy/shell.json",
        "lines": [
            "{",
            "  \"version\": 1,",
            "  \"bar\": {",
            "    \"position\": \"top\",",
            "    \"centerAnchor\": \"omarchy.clock\",",
            "    \"layout\": {",
            "      \"left\": [{ \"id\": \"omarchy.menu\" }],",
            "      \"center\": [{ \"id\": \"omarchy.clock\" }],",
            "      \"right\": [{ \"id\": \"omarchy.tray\" }]",
            "    }",
            "  }",
            "}",
        ],
    },
    {
        "name": "~/.config/foot/foot.ini",
        "lines": [
            "[main]",
            "include=~/.local/state/omarchy/current/theme/foot.ini",
            "font=JetBrainsMono Nerd Font:size=9",
            "pad=14x14",
            "workers=0",
            "",
            "[scrollback]",
            "lines=10000",
            "multiplier=7.0",
            "",
            "[cursor]",
            "style=block",
        ],
    },
    {
        "name": "~/dev/tdevpod/tdevpod.py",
        "lines": [
            "#!/usr/bin/env python3",
            "import gi",
            "gi.require_version(\"Gtk\", \"3.0\")",
            "from gi.repository import Gtk, Gdk, GLib",
            "",
            "# toddler-safe: this source is only ever drawn, never imported",
            "def sprinkle(keys):",
            "    return \" \".join(c + \"🌱\" for c in keys)",
            "",
            "def rainbow(keys):",
            "    return \":)\".join(keys)",
        ],
    },
]

_LUA_KW = {"local", "function", "return", "end", "if", "then", "else",
           "for", "in", "do", "true", "false", "nil", "require"}


def _discover_scripts(directory, shown_as):
    """Return pretend-file dicts for every text file in `directory`.

    Content is read once and only ever drawn; `shown_as` is the fake path
    prefix displayed in the header.
    """
    try:
        names = sorted(os.listdir(directory)) if os.path.isdir(directory) else []
    except OSError:
        names = []
    files = []
    for name in names:
        if name.startswith("."):
            continue
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
        except OSError:
            continue
        if lines:
            files.append({"name": f"{shown_as}/{name}", "lines": lines})
    return files


def load_pool():
    """Drop-ins in ~/.config/tdevpod/scripts/ win; else the repo's scripts/."""
    try:
        os.makedirs(SCRIPT_DIR, exist_ok=True)
    except OSError:
        pass
    return (_discover_scripts(SCRIPT_DIR, "~/.config/tdevpod/scripts")
            or _discover_scripts(REPO_SCRIPT_DIR, "~/dev/tdevpod/scripts")
            or list(FILES))


# Lines that "animate": consecutive matches overwrite each other in place.
#   [██████░░░░]  60%  fueling rocket      (progress bar)
#   ▘ resolving dinosaurs...               (spinner)
_BAR_RE = re.compile(r"^\s*\[[█▓▒░#=>\-. ]{4,}\]")
_SPIN = "▖▘▝▗◐◓◑◒⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
_SPIN_RE = re.compile(rf"^\s*[{_SPIN}] ")
_BAR_FILL = set("█▓#=>")


def is_live_line(line):
    return bool(_BAR_RE.match(line) or _SPIN_RE.match(line))


_TOML_KEYS = {"accent", "background", "foreground", "red", "green",
              "yellow", "cyan", "magenta", "font", "pad", "lines",
              "multiplier", "position", "centerAnchor", "version",
              "mode", "layout", "bar", "style", "scrollback", "-config",
              "main", "cursor"}


def word_color(w):
    """Colour one revealed word, Tokyo Night style."""
    low = w.lower()
    if low in _LUA_KW:
        return MAGENTA
    if low in ("hl", "o", "gdk", "gtk", "gi", "glib", "gtk3"):
        return CYAN
    if low in _TOML_KEYS:
        return ACCENT
    if w.startswith("\""):
        return GREEN
    if w.startswith("#") or w == "<<":
        return GREEN
    if low.startswith("super") or low in ("ctlr", "ctrl", "shift", "escape", "ctrl+shift", "super+ctrl"):
        return YELLOW
    if any(ch.isdigit() for ch in w):
        return YELLOW
    if w.startswith("--") or w.startswith("//"):
        return DIM
    if w and w[0].isupper():
        return ACCENT
    return FG


# --------------------------------------------------------------------------
# The engine: a quiet terminal that only answers back one word per touch.
# --------------------------------------------------------------------------
class Engine:
    def __init__(self):
        self.lines = []          # rows of (char, color)
        self.max_col = 80
        self.top_row = 0
        self.keystrokes = 0
        self.clicks = 0
        self.pointer = (0, 0)
        self.sparks = []
        self.status_note = "quiet ... until the keys start"
        self.file_index = 0

        boot = [
            "▼ TDevPod armed",
            "  every key = one word of pretend code · nothing is executed",
        ]
        for i, (line, color) in enumerate(((boot[0], DIM), (boot[1], GREEN))):
            self.write(line + "\n", color)
            if i == 0:
                self.newline()

        self.files = load_pool()
        random.shuffle(self.files)
        self.words = self._build_words(self.files)
        self.wi = 0
        self.need_space = False
        self.last_live = False
        self.letter_ring = ""

    # --- buffer -----------------------------------------------------------
    def newline(self):
        self.lines.append([])

    def write_char(self, ch, color=FG):
        if not self.lines or len(self.lines[-1]) >= self.max_col:
            self.newline()
        self.lines[-1].append((ch, color))

    def write(self, text, color=FG):
        for ch in text:
            if ch == "\n":
                self.newline()
            else:
                self.write_char(ch, color)

    def backspace(self):
        if self.lines:
            if self.lines[-1]:
                self.lines[-1].pop()
            elif len(self.lines) > 1:
                self.lines.pop()
        self.need_space = False

    # --- script -----------------------------------------------------------
    def _build_words(self, files):
        toks = []
        for idx, f in enumerate(files):
            toks.append(("open", idx, f["name"]))
            for line in f["lines"]:
                line = line.expandtabs(4)
                if is_live_line(line):
                    toks.append(("live", line))
                    toks.append(("lineend", "lineend"))
                    continue
                if not line.strip():
                    toks.append(("lineend", "lineend"))
                    continue
                for w in line.split(" "):
                    toks.append(("word", w))
                toks.append(("lineend", "lineend"))
        return toks

    def reveal_word(self):
        """Advance the pretend script by exactly one word."""
        scanned = 0
        while scanned <= len(self.words):
            if self.wi >= len(self.words):
                self.wi = 0
                random.shuffle(self.files)
                self.words = self._build_words(self.files)
            kind, *rest = self.words[self.wi]
            self.wi += 1
            scanned += 1
            if kind == "open":
                idx, name = rest
                self.file_index = idx
                self.newline()
                self.write("│ vim " + name, ACCENT)
                self.newline()
                self.need_space = False
                self.last_live = False
                continue
            if kind == "lineend":
                self.newline()
                self.need_space = False
                continue
            if kind == "live":
                self._put_live(rest[0])
                return
            if kind == "word":
                self.last_live = False
                w = rest[0]
                if self.need_space:
                    self._put(" ", MUTED)
                self._put_word(w)
                self.need_space = True
                return

    def _put_live(self, line):
        """Draw a progress/spinner line, replacing the previous one in place."""
        if self.last_live and len(self.lines) >= 2 and not self.lines[-1]:
            self.lines.pop()        # the blank row the previous lineend opened
            self.lines[-1] = []
        elif self.lines and self.lines[-1]:
            self.newline()
        line = line[: self.max_col]
        m = _BAR_RE.match(line) or _SPIN_RE.match(line)
        head, tail = line[: m.end()], line[m.end():]
        for ch in head:
            if ch in "[]":
                color = DIM
            elif ch in _BAR_FILL:
                color = GREEN
            elif ch in _SPIN:
                color = MAGENTA
            else:
                color = MUTED
            self.write_char(ch, color)
        for w in re.split(r"(\s+)", tail):
            color = YELLOW if w.endswith("%") or any(c.isdigit() for c in w) else FG
            for ch in w:
                self.write_char(ch, color)
        self.need_space = False
        self.last_live = True

    def _put(self, ch, color):
        if not self.lines or len(self.lines[-1]) >= self.max_col:
            self.newline()
        self.lines[-1].append((ch, color))

    def _put_word(self, w):
        row = self.lines[-1] if self.lines else []
        room = self.max_col - len(row) - (1 if self.need_space else 0)
        if room < len(w):
            self.newline()
        for ch in w:
            self.write_char(ch, word_color(w))

    # --- input -------------------------------------------------------------
    def child_key(self, ch):
        self.keystrokes += 1
        if ch and ch.isalpha():
            self.letter_ring = (self.letter_ring + ch.lower())[-40:]
        return "exit-tdevpod" in self.letter_ring

    def child_click(self, x, y):
        self.clicks += 1
        for _ in range(10):
            self.sparks.append({
                "x": x, "y": y,
                "vx": random.uniform(-2.4, 2.4),
                "vy": random.uniform(-2.4, 2.4),
                "c": random.choice([ACCENT, CYAN, MAGENTA, GREEN, YELLOW]),
                "life": random.randint(8, 20),
            })

    def tick(self):
        self.sparks = [s for s in self.sparks if s["life"] > 0]
        for s in self.sparks:
            s["life"] -= 1
            s["x"] += s["vx"]
            s["y"] += s["vy"]

    def visible_range(self, rows):
        total = len(self.lines)
        top = max(0, total - rows)
        self.top_row = top
        return range(top, min(total, top + rows))


# --------------------------------------------------------------------------
# The window
# --------------------------------------------------------------------------
class TDevPodApp(Gtk.Window):
    def __init__(self, selftest=False):
        super().__init__()
        self.selftest = selftest
        self.eng = Engine()

        self.set_title("TDevPod")
        self.set_decorated(False)
        self.set_app_paintable(True)
        self.set_keep_above(True)
        self.set_can_focus(True)
        self.set_accept_focus(True)
        self.fullscreen()
        try:
            Gdk.set_program_class("TDevPod")
        except Exception:
            pass

        self.area = Gtk.DrawingArea()
        self.add(self.area)
        self.area.set_events(
            Gdk.EventMask.POINTER_MOTION_MASK
            | Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.POINTER_MOTION_HINT_MASK
            | Gdk.EventMask.SCROLL_MASK
        )

        self.area.connect("draw", self.on_draw)
        self.connect("key-press-event", self.on_key)
        self.connect("button-press-event", self.on_button)
        self.connect("motion-notify-event", self.on_motion)
        self.connect("map-event", self.on_map)
        self.connect("destroy", self.on_destroy)

        self.pango = self.area.get_pango_context()
        self.cell_font = Pango.FontDescription(f"{FONT} 15")
        self.head_font = Pango.FontDescription(f"{FONT} 20")
        self.head_font.set_weight(Pango.Weight.BOLD)
        m = self.pango.get_metrics(self.cell_font, None)
        self.cell_w = m.get_approximate_char_width() / Pango.SCALE
        self.cell_h = (m.get_ascent() + m.get_descent()) / Pango.SCALE
        self.layouts = {}
        self.clock = time.strftime("%H:%M:%S")

        GLib.timeout_add(55, self.tick)
        if not selftest:
            GLib.timeout_add(1000, self.clock_tick)

    # --- lifecycle ---------------------------------------------------------
    def on_map(self, widget, event):
        GLib.timeout_add(150, self.grab_late)
        return False

    def grab_late(self):
        grab_input()
        self.hide_cursor()
        try:
            self.present()
            self.grab_focus()
        except Exception:
            pass
        return False

    def hide_cursor(self):
        try:
            cur = Gdk.Cursor.new_from_name(self.get_display(), "none")
            self.get_window().set_cursor(cur)
        except Exception:
            pass

    def on_destroy(self, widget):
        ungrab_input()

    def tick(self):
        self.eng.tick()
        self.area.queue_draw()
        return True

    def clock_tick(self):
        self.clock = time.strftime("%H:%M:%S")
        return True

    # --- input -------------------------------------------------------------
    def is_exit_combo(self, event):
        st = event.state
        return (
            event.keyval == Gdk.KEY_Escape
            and bool(st & Gdk.ModifierType.CONTROL_MASK)
            and bool(st & Gdk.ModifierType.SHIFT_MASK)
            and bool(st & Gdk.ModifierType.SUPER_MASK)
        )

    def on_key(self, widget, event):
        if self.is_exit_combo(event):
            self.quit_app()
            return True
        key = event.keyval
        uni = Gdk.keyval_to_unicode(key)
        ch = chr(uni) if 0x21 <= uni <= 0x7E else ""
        if self.eng.child_key(ch):
            self.quit_app()
            return True

        if key == Gdk.KEY_BackSpace:
            self.eng.backspace()
        elif key in (Gdk.KEY_Return, Gdk.KEY_space) or (0x21 <= uni <= 0x7E):
            self.eng.reveal_word()
        return True

    def on_button(self, widget, event):
        self.eng.child_click(int(event.x), int(event.y))
        self.eng.reveal_word()
        return True

    def on_motion(self, widget, event):
        self.eng.pointer = (int(event.x), int(event.y))
        return True

    def quit_app(self):
        self.destroy()

    # --- drawing -----------------------------------------------------------
    def layout(self, text, color, face):
        key = (text, color, face)
        if key not in self.layouts:
            lay = Pango.Layout.new(self.pango)
            lay.set_font_description(face)
            lay.set_text(text, -1)
            self.layouts[key] = lay
        return self.layouts[key]

    def draw_text(self, cr, text, color, x, y, face, right=False):
        lay = self.layout(text, color, face)
        w = lay.get_size()[0] / Pango.SCALE
        if right:
            x -= w
        cr.set_source_rgb(*hex_to(color))
        cr.move_to(x, y)
        PangoCairo.show_layout(cr, lay)
        return w

    def draw_fit(self, cr, text, color, x, y, face, maxw):
        """Draw text elided so it never runs past maxw (no overlaps)."""
        if self.layout(text, color, face).get_size()[0] / Pango.SCALE <= maxw:
            return self.draw_text(cr, text, color, x, y, face)
        lo, hi = 0, len(text)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.layout(text[:mid] + "…", color, face).get_size()[0] / Pango.SCALE <= maxw:
                lo = mid
            else:
                hi = mid - 1
        return self.draw_text(cr, text[:lo] + "…", color, x, y, face)

    def on_draw(self, widget, cr):
        return self.render(cr, widget.get_allocated_width(),
                           widget.get_allocated_height())

    def render(self, cr, w, h):
        """Paint one full frame at w×h (also used offscreen by demo/record.py)."""
        self.eng.max_col = max(20, int((w - 8) / self.cell_w))

        cr.set_source_rgb(*hex_to(BG))
        cr.paint()

        hh = int(self.cell_h * 1.7)
        fh = int(self.cell_h * 1.35) * 2 + 10
        body_top = hh
        body_rows = max(3, int((h - hh - fh) / self.cell_h))

        self.draw_header(cr, w, hh)
        self.draw_body(cr, w, body_top, body_rows)
        self.draw_footer(cr, w, body_top + body_rows * self.cell_h + 4, fh)
        self.draw_pointer(cr)
        return False

    def draw_header(self, cr, w, hh):
        cr.set_source_rgb(*hex_to(DARK))
        cr.rectangle(0, 0, w, hh)
        cr.fill()
        cr.set_source_rgb(*hex_to(ACCENT))
        cr.rectangle(0, 0, 4, hh)
        cr.fill()
        f = self.eng.files[self.eng.file_index]["name"]
        self.draw_text(cr, "  ❯ TDevPod — Toddler Dev Pod", ACCENT, 6,
                       (hh - 22) / 2, self.head_font)
        maxw = w * 0.45
        fw = min(maxw, self.layout(f, CYAN, self.cell_font).get_size()[0] / Pango.SCALE)
        self.draw_fit(cr, f, CYAN, w - 12 - fw, (hh - 18) / 2, self.cell_font,
                      maxw=maxw)

    def draw_footer(self, cr, w, y, fh):
        cr.set_source_rgb(*hex_to(DARK))
        cr.rectangle(0, y, w, fh)
        cr.fill()
        line_h = int(self.cell_h * 1.35)
        left = (f"keystrokes: {self.eng.keystrokes:05d}"
                f"   ·   clicks: {self.eng.clicks:05d}"
                f"   ·   grab: LOCKED")
        right_txt = f"exit: {EXIT_KEYS}"
        # line 1: status left, exit truly right — never overlapping
        maxl = w - 16 - self.layout(right_txt, DIM, self.cell_font).get_size()[0] / Pango.SCALE
        self.draw_fit(cr, left, MUTED, 8, y + 4, self.cell_font, maxw=maxl)
        self.draw_text(cr, right_txt, GREEN, w - 8, y + 4, self.cell_font,
                       right=True)
        # line 2: the fallback phrase
        self.draw_text(cr, "…or spell out: exit-tdevpod", DIM, 8,
                       y + 4 + line_h, self.cell_font)

    def draw_body(self, cr, w, top, body_rows):
        vis = self.eng.visible_range(body_rows)
        y = top
        for i in vis:
            self.draw_row(cr, self.eng.lines[i], y)
            y += self.cell_h
        self.draw_caret(cr, top, body_rows)

    def draw_row(self, cr, row, y):
        if not row:
            return
        row = row[: self.eng.max_col]
        x = 4.0
        buf = []
        col = None
        for ch, color in row:
            if color != col:
                if buf:
                    self.draw_text(cr, "".join(buf), col, x, y, self.cell_font)
                    x += self.cell_w * len(buf)
                    buf = []
                col = color
            buf.append(ch)
        if buf:
            self.draw_text(cr, "".join(buf), col, x, y, self.cell_font)

    def draw_caret(self, cr, top, body_rows):
        if not self.eng.lines or int(time.time() * 2) % 2 == 0:
            return
        idx = len(self.eng.lines) - 1
        if idx < self.eng.top_row:
            return
        col = len(self.eng.lines[-1])
        if col >= self.eng.max_col:
            return
        x = 4 + col * self.cell_w
        y = top + (idx - self.eng.top_row) * self.cell_h
        cr.set_source_rgb(*hex_to(ACCENT))
        cr.rectangle(x, y + 1, self.cell_w - 2, self.cell_h - 4)
        cr.fill()

    def draw_pointer(self, cr):
        x, y = self.eng.pointer
        cr.set_source_rgb(*hex_to(ACCENT))
        cr.rectangle(x - 2, y - 8, 4, 16)
        cr.rectangle(x - 8, y - 2, 16, 4)
        cr.fill()
        for s in self.eng.sparks:
            cr.set_source_rgb(*hex_to(s["c"]))
            cr.rectangle(int(s["x"]) - 1, int(s["y"]) - 1, 3, 3)
            cr.fill()


def main():
    selftest = "--selftest" in sys.argv
    app = TDevPodApp(selftest=selftest)
    app.show_all()
    if selftest:
        def end():
            app.destroy()
            Gtk.main_quit()
            return False
        GLib.timeout_add(1500, end)
    Gtk.main()


if __name__ == "__main__":
    main()