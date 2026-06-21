"""
Structural absence diptych.
Two images showing absence as the material, not the gap.
Left: a wall with a door-shaped void — the void holds the structure.
Right: a stone lattice where the spaces between are more substantial than the stones.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 512, 512
DARK_STONE = (42, 39, 36)
VOID = (195, 180, 165)
MID = (75, 68, 60)
WARM_VOID = (210, 195, 175)

def make_left():
    img = Image.new('RGB', (W, H), VOID)
    draw = ImageDraw.Draw(img)
    # The wall is the void — warm stone
    # The "presence" is the dark frame that holds it
    draw.rectangle([0, 0, W, 40], fill=DARK_STONE)
    draw.rectangle([0, H-40, W, H], fill=DARK_STONE)
    draw.rectangle([0, 0, 40, H], fill=DARK_STONE)
    draw.rectangle([W-40, 0, W, H], fill=DARK_STONE)
    # A recessed area in the center — slightly darker
    # This IS the wall; the recess IS the material
    draw.rectangle([60, 60, W-60, H-60], fill=MID)
    # Inside the recess, a brighter zone — the actual absence
    draw.ellipse([120, 120, W-120, H-120], fill=WARM_VOID)
    # Subtle texture lines radiating from center
    cx, cy = W//2, H//2
    for i in range(24):
        angle = i * 15 * np.pi / 180
        x1 = cx + 130 * np.cos(angle)
        y1 = cy + 130 * np.sin(angle)
        x2 = cx + 190 * np.cos(angle)
        y2 = cy + 190 * np.sin(angle)
        draw.line([(x1, y1), (x2, y2)], fill=MID, width=1)
    # A door-shaped void in the warm zone
    dw, dh = 80, 140
    dx, dy = cx - dw//2, cy + 40
    # The door shape is DARKER — it's the presence holding the absence
    draw.rectangle([dx, dy, dx+dw, dy+dh], fill=DARK_STONE)
    # Inner door recess
    draw.rectangle([dx+10, dy+10, dx+dw-10, dy+dh-10], fill=WARM_VOID)
    return img

def make_right():
    img = Image.new('RGB', (W, H), VOID)
    draw = ImageDraw.Draw(img)
    # A geode-like structure: amber shell with hollow center
    cx, cy = W//2, H//2
    # Outer amber shell
    draw.ellipse([30, 30, W-30, H-30], fill=MID)
    # Inner geode cavity — the actual material
    draw.ellipse([100, 100, W-100, H-100], fill=VOID)
    # Crystal growth lines from edges toward center (stopping short)
    for i in range(36):
        angle = i * 10 * np.pi / 180
        r1 = 110 + np.random.randint(-5, 5)
        r2 = 150 + np.random.randint(-8, 8)
        x1 = cx + r1 * np.cos(angle)
        y1 = cy + r1 * np.sin(angle)
        x2 = cx + r2 * np.cos(angle)
        y2 = cy + r2 * np.sin(angle)
        shade = 140 + np.random.randint(-20, 20)
        draw.line([(x1, y1), (x2, y2)], fill=(shade, shade-5, shade-10), width=2)
    # Cracks in the amber shell — structural absence
    for _ in range(8):
        px, py = np.random.randint(40, W-40), np.random.randint(40, H-40)
        ex = px + np.random.randint(-60, 60)
        ey = py + np.random.randint(-60, 60)
        draw.line([(px, py), (ex, ey)], fill=DARK_STONE, width=1)
    return img

img = Image.new('RGB', (W*2+20, H+20), VOID)
draw = ImageDraw.Draw(img)
left = make_left()
right = make_right()
img.paste(left, (10, 10))
img.paste(right, (W+30, 10))
img.save('assets/absence-diptych.png')
print("done")
