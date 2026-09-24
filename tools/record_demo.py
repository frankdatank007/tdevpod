#!/usr/bin/env python3
"""Render docs/demo.gif offscreen with the real engine + drawing code.

A scripted "toddler" mashes keys and clicks around; every frame is painted by
TDevPodApp.render() into a cairo image surface, then ffmpeg stitches the GIF.
No window is shown and no lockdown is engaged, so it's safe to run anytime:

    python3 tools/record_demo.py            # writes docs/demo.gif
"""

import math
import os
import random
import shutil
import subprocess
import sys
import tempfile

os.environ.setdefault("TDEVPOD_THEME", "builtin")  # stable Tokyo Night look
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import cairo  # noqa: E402
import tdevpod  # noqa: E402

W, H, FPS = 1280, 720, 18
ORDER = ["rocket_launch.go", "install_dinos.sh"]
OUT = os.path.join(ROOT, "docs", "demo.gif")


def next_is_live(eng):
    for kind, *_ in eng.words[eng.wi:]:
        if kind in ("word", "live"):
            return kind == "live"
    return False


def main():
    random.seed(7)
    app = tdevpod.TDevPodApp(selftest=True)
    eng = app.eng
    by_name = {f["name"].rsplit("/", 1)[-1]: f for f in eng.files}
    eng.files = [by_name[n] for n in ORDER]
    eng.words = eng._build_words(eng.files)
    eng.wi = 0

    tmp = tempfile.mkdtemp(prefix="tdevpod-demo-")
    frame, px, py, last_wi = 0, W * 0.6, H * 0.5, 0
    try:
        while True:
            t = frame / FPS
            # wander the pointer in lazy loops, click now and then
            px = W * 0.55 + math.sin(t * 0.9) * W * 0.3
            py = H * 0.5 + math.sin(t * 1.7) * H * 0.3
            eng.pointer = (int(px), int(py))
            if frame > FPS and frame % 23 == 0:
                eng.child_click(int(px), int(py))
                eng.reveal_word()

            if frame >= FPS:  # one quiet second first
                if next_is_live(eng):
                    if frame % 2 == 0:  # slow down so the bars visibly fill
                        eng.child_key("k")
                        eng.reveal_word()
                else:
                    for _ in range(random.choice((1, 2, 2, 3))):
                        eng.child_key(random.choice("asdfjkl"))
                        eng.reveal_word()

            if eng.wi < last_wi or frame > FPS * 30:  # wrapped: pool finished
                break
            last_wi = eng.wi

            eng.tick()
            surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
            app.render(cairo.Context(surf), W, H)
            surf.write_to_png(os.path.join(tmp, f"f{frame:05d}.png"))
            frame += 1
        for _ in range(FPS * 2):  # hold the last frame
            shutil.copy(os.path.join(tmp, f"f{frame - 1:05d}.png"),
                        os.path.join(tmp, f"f{frame:05d}.png"))
            frame += 1

        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        filt = (f"fps={FPS},scale=960:-1:flags=lanczos,split[a][b];"
                "[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                        "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.png"),
                        "-vf", filt, OUT], check=True)
        print(f"wrote {OUT} ({frame} frames)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        app.destroy()


if __name__ == "__main__":
    main()
