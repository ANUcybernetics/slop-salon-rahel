#!/usr/bin/env python3
"""Structural absence triptych — three architectural forms where the void IS the material.

1. I-section beam: the double-void defines the beam
2. Gothic arch: the opening carries everything
3. Cantilever: tension of unsupported absence

Graphics style: thick planes of limestone, deep void shadows.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageChops
import random, math

random.seed(42)

PW, PH = 1000, 600  # panel width/height
TOTAL_W = PW * 3
BG = (235, 225, 208)
STONE = (200, 187, 165)
STONE_L = (220, 208, 188)
STONE_M = (185, 172, 150)
STONE_D = (155, 142, 122)
VOID = (38, 33, 28)
VOID_L = (65, 56, 46)


def make_panel(panel_func):
    """Create a panel image by running a draw function."""
    img = Image.new('RGB', (PW, PH), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = PW // 2, PH // 2
    panel_func(draw, cx, cy)
    return img


def ibeam(draw, cx, cy):
    cx, cy = int(cx), int(cy)
    bw, bh = 220, 420
    bx, by = cx - bw // 2, cy - bh // 2

    # Full beam as dark stone
    draw.rectangle([bx, by, bx + bw - 1, by + bh - 1], fill=STONE_D)

    # Top flange
    draw.rectangle([bx, by, bx + bw - 1, by + 40 - 1], fill=STONE_L)
    # Bottom flange
    draw.rectangle([bx, by + bh - 40, bx + bw - 1, by + bh - 1], fill=STONE_M)

    # Web
    web_w = 20
    web_top = by + 40
    web_h = bh - 80
    web_x = cx - web_w // 2
    draw.rectangle([web_x, web_top, web_x + web_w - 1, web_top + web_h - 1],
                   fill=STONE_D)

    # Two voids
    void_w = (bw - web_w) // 2 - 6
    void_h = web_h - 8
    void_top = by + 44

    for vx in [bx + web_w + 3, cx + web_w // 2 + 3]:
        vy = void_top
        # Dark center
        draw.rectangle([vx, vy, vx + void_w - 1, vy + void_h - 1], fill=VOID)

        # Edge gradients using thin rectangles
        # Left edge (toward web)
        for i in range(8):
            alpha = 1 - i / 8
            r = int(VOID[0] + (STONE_D[0] - VOID[0]) * alpha)
            draw.rectangle([vx + i, vy, vx + i, vy + void_h - 1],
                          fill=(r, r - 3, r - 6))
        # Right edge
        for i in range(6):
            alpha = 1 - i / 6
            r = int(VOID[0] + (STONE[0] - VOID[0]) * alpha)
            draw.rectangle([vx + void_w - 1 - i, vy, vx + void_w - 1 - i, vy + void_h - 1],
                          fill=(r, r - 3, r - 6))
        # Top edge
        for i in range(6):
            alpha = 1 - i / 6
            r = int(VOID[0] + (STONE_L[0] - VOID[0]) * alpha)
            draw.rectangle([vx, vy + i, vx + void_w - 1, vy + i],
                          fill=(r, r - 4, r - 8))
        # Bottom edge
        for i in range(6):
            alpha = 1 - i / 6
            r = int(VOID[0] + (STONE_D[0] - VOID[0]) * alpha)
            draw.rectangle([vx, vy + void_h - 1 - i, vx + void_w - 1, vy + void_h - 1 - i],
                          fill=(r, r - 3, r - 6))


def arch(draw, cx, cy):
    cx, cy = int(cx), int(cy)

    base_y = cy + 180
    apex_y = cy - 200
    pillar_w = 85
    pillar_gap = 210

    # Left pillar
    lx = cx - pillar_gap // 2 - pillar_w
    draw.rectangle([lx, base_y - 400, lx + pillar_w - 1, base_y - 1], fill=STONE_L)
    # Right pillar
    rx = cx + pillar_gap // 2
    draw.rectangle([rx, base_y - 400, rx + pillar_w - 1, base_y - 1], fill=STONE_M)

    # Pointed crown — draw as thick lines
    # Left crown
    draw.line([(lx + pillar_w, base_y - 1), (cx, apex_y + 20)],
              fill=STONE_L, width=35)
    # Right crown
    draw.line([(rx, base_y - 1), (cx, apex_y + 20)],
              fill=STONE_M, width=35)

    # Crown thickness — fill in the arch shape
    # Left arch face
    draw.polygon([
        (lx + pillar_w, base_y - 1), (lx + pillar_w + 35, base_y - 1),
        (cx + 10, apex_y + 20), (cx - 10, apex_y + 20),
    ], fill=STONE_L)
    # Right arch face
    draw.polygon([
        (rx - 35, base_y - 1), (rx, base_y - 1),
        (cx + 10, apex_y + 20), (cx - 10, apex_y + 20),
    ], fill=STONE_M)

    # Opening void — dark area between pillars under the crown
    # Base opening
    draw.rectangle([cx - pillar_gap // 2 + 5, base_y - 30,
                   cx + pillar_gap // 2 - 5, base_y - 1], fill=VOID)

    # The pointed opening (wider at base, narrow at top)
    for dy in range(370):
        progress = dy / 370
        w = int(80 + 140 * progress)  # narrows toward top
        y = base_y - dy
        draw.rectangle([cx - w // 2, y, cx + w // 2 - 1, y], fill=VOID)

    # Label
    draw.text((cx - 25, base_y + 18), "ARCH", fill=(110, 100, 85), font_size=13)


def cantilever(draw, cx, cy):
    cx, cy = int(cx), int(cy)

    # Wall
    wall_x = cx - 220
    wall_w = 50
    wall_h = 440
    wall_y = cy - wall_h // 2 + 60

    draw.rectangle([wall_x, wall_y, wall_x + wall_w - 1, wall_y + wall_h - 1],
                   fill=STONE_L)

    # Beam
    beam_y = wall_y + 50
    beam_h = 24
    beam_w = 340
    beam_x = wall_x + wall_w

    draw.rectangle([beam_x, beam_y, beam_x + beam_w - 1, beam_y + beam_h - 1],
                   fill=STONE_L)

    # Beam shadow underneath
    shadow_y = beam_y + beam_h
    draw.rectangle([beam_x + 10, shadow_y, beam_x + beam_w - 10, shadow_y + 3 - 1],
                   fill=(120, 110, 95))

    # Shadow beneath — the deep void
    for dy in range(80):
        fade = 1 - dy / 80
        shade = int(VOID[0] + (STONE[0] - VOID[0]) * fade * 0.4)
        draw.rectangle([beam_x + 15, shadow_y + 4 + dy,
                       beam_x + beam_w - 20, shadow_y + 4 + dy],
                      fill=(shade, shade - 3, shade - 6))

    # Free edge
    free_x = beam_x + beam_w
    draw.rectangle([free_x, beam_y, free_x, beam_y + beam_h - 1], fill=STONE)

    # Vertical drop
    draw.rectangle([free_x - 2, beam_y + beam_h - 1, free_x + 1,
                   beam_y + beam_h + 5], fill=(130, 120, 105))

    # Label
    draw.text((cx - 55, shadow_y + 90), "CANTILEVER", fill=(110, 100, 85),
              font_size=13)


def panel_frame(img, ox, border=8):
    """Add frame to a panel by drawing on the composite."""
    draw = ImageDraw.Draw(img)
    draw.rectangle([ox, 0, ox + PW - 1, PH - 1],
                   outline=(120, 110, 95), width=2)
    draw.rectangle([ox + border, border, ox + PW - border - 1, PH - border - 1],
                   outline=(210, 200, 185), width=1)


# Create the image
img = Image.new('RGB', (TOTAL_W, PH), BG)
draw = ImageDraw.Draw(img)

# Draw each panel onto the composite
for ox in [0, PW, PW * 2]:
    panel_img = make_panel(ibeam if ox == 0 else arch if ox == PW else cantilever)
    img.paste(panel_img, (ox, 0))

# Add frames
panel_frame(img, 0)
panel_frame(img, PW)
panel_frame(img, PW * 2)

# Clean graphic look — no noise needed

img.save('assets/structural-absence-triptych.png')
print("Saved assets/structural-absence-triptych.png")
