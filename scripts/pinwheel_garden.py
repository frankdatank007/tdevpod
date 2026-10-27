# pinwheel_garden.py: spin three paper pinwheels until the breeze is happy (never runs)
import itertools
import time

BLADES = "◐◓◑◒"
COLORS = ["red", "yellow", "blue"]


class Pinwheel:
    def __init__(self, color):
        self.color = color
        self.turns = 0

    def spin(self, breeze):
        self.turns += breeze
        return BLADES[self.turns % len(BLADES)]


def water_bar(pct, width=20):
    filled = pct * width // 100
    return "[" + "█" * filled + "░" * (width - filled) + "]"


def main():
    garden = [Pinwheel(c) for c in COLORS]
    for wheel in itertools.cycle(garden):
        print(wheel.spin(1), f"spinning the {wheel.color} pinwheel...")
        time.sleep(0.08)
    print("the garden is dizzy and delighted")


# $ python pinwheel_garden.py

# ── output ────────────────────────────────────────────
◐ spinning the red pinwheel...
◓ spinning the red pinwheel...
◑ spinning the red pinwheel...
◒ spinning the red pinwheel...
◐ spinning the red pinwheel...
◓ spinning the red pinwheel...
◑ spinning the red pinwheel...
◒ spinning the red pinwheel...
◐ spinning the red pinwheel...
◓ spinning the red pinwheel...
◑ spinning the red pinwheel...
◒ spinning the red pinwheel...
✔ red pinwheel is whooshing
◓ spinning the yellow pinwheel...
◑ spinning the yellow pinwheel...
◒ spinning the yellow pinwheel...
◐ spinning the yellow pinwheel...
◓ spinning the yellow pinwheel...
◑ spinning the yellow pinwheel...
◒ spinning the yellow pinwheel...
◐ spinning the yellow pinwheel...
◓ spinning the yellow pinwheel...
◑ spinning the yellow pinwheel...
◒ spinning the yellow pinwheel...
◐ spinning the yellow pinwheel...
✔ yellow pinwheel is whooshing
[░░░░░░░░░░░░░░░░░░░░]   0%  watering the sunflowers
[█░░░░░░░░░░░░░░░░░░░]   5%  watering the sunflowers
[██░░░░░░░░░░░░░░░░░░]  10%  watering the sunflowers
[███░░░░░░░░░░░░░░░░░]  15%  watering the sunflowers
[████░░░░░░░░░░░░░░░░]  20%  watering the sunflowers
[█████░░░░░░░░░░░░░░░]  25%  watering the sunflowers
[██████░░░░░░░░░░░░░░]  30%  watering the sunflowers
[███████░░░░░░░░░░░░░]  35%  watering the sunflowers
[████████░░░░░░░░░░░░]  40%  watering the sunflowers
[█████████░░░░░░░░░░░]  45%  watering the sunflowers
[██████████░░░░░░░░░░]  50%  watering the sunflowers
[███████████░░░░░░░░░]  55%  watering the sunflowers
[████████████░░░░░░░░]  60%  watering the sunflowers
[█████████████░░░░░░░]  65%  watering the sunflowers
[██████████████░░░░░░]  70%  watering the sunflowers
[███████████████░░░░░]  75%  watering the sunflowers
[████████████████░░░░]  80%  watering the sunflowers
[█████████████████░░░]  85%  watering the sunflowers
[██████████████████░░]  90%  watering the sunflowers
[███████████████████░]  95%  watering the sunflowers
[████████████████████] 100%  watering the sunflowers
→ next up!
◑ spinning the blue pinwheel...
◒ spinning the blue pinwheel...
◐ spinning the blue pinwheel...
◓ spinning the blue pinwheel...
◑ spinning the blue pinwheel...
◒ spinning the blue pinwheel...
◐ spinning the blue pinwheel...
◓ spinning the blue pinwheel...
◑ spinning the blue pinwheel...
◒ spinning the blue pinwheel...
◐ spinning the blue pinwheel...
◓ spinning the blue pinwheel...
✔ all 3 pinwheels spinning, 0 dizzy bees
[▓▒░░░░░░░░░░░░░░░░░░]   0%  growing the pinwheel tree
[▓▒░░░░░░░░░░░░░░░░░░]   4%  growing the pinwheel tree
[█▓▒░░░░░░░░░░░░░░░░░]   8%  growing the pinwheel tree
[██▓▒░░░░░░░░░░░░░░░░]  12%  growing the pinwheel tree
[███▓▒░░░░░░░░░░░░░░░]  16%  growing the pinwheel tree
[████▓▒░░░░░░░░░░░░░░]  20%  growing the pinwheel tree
[████▓▒░░░░░░░░░░░░░░]  24%  growing the pinwheel tree
[█████▓▒░░░░░░░░░░░░░]  28%  growing the pinwheel tree
[██████▓▒░░░░░░░░░░░░]  32%  growing the pinwheel tree
[███████▓▒░░░░░░░░░░░]  36%  growing the pinwheel tree
[████████▓▒░░░░░░░░░░]  40%  growing the pinwheel tree
[████████▓▒░░░░░░░░░░]  44%  growing the pinwheel tree
[█████████▓▒░░░░░░░░░]  48%  growing the pinwheel tree
[██████████▓▒░░░░░░░░]  52%  growing the pinwheel tree
[███████████▓▒░░░░░░░]  56%  growing the pinwheel tree
[████████████▓▒░░░░░░]  60%  growing the pinwheel tree
[████████████▓▒░░░░░░]  64%  growing the pinwheel tree
[█████████████▓▒░░░░░]  68%  growing the pinwheel tree
[██████████████▓▒░░░░]  72%  growing the pinwheel tree
[███████████████▓▒░░░]  76%  growing the pinwheel tree
[████████████████▓▒░░]  80%  growing the pinwheel tree
[████████████████▓▒░░]  84%  growing the pinwheel tree
[█████████████████▓▒░]  88%  growing the pinwheel tree
[██████████████████▓▒]  92%  growing the pinwheel tree
[███████████████████▓]  96%  growing the pinwheel tree
[████████████████████] 100%  growing the pinwheel tree
