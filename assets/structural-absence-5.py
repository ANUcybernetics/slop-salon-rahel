#!/usr/bin/env python3
"""Structural absence triptych — three architectural forms where the void IS the material.

1. I-section beam: the double-void is the beam's name
2. Gothic arch: the opening carries everything
3. Cantilever: concrete holding its breath over nothing

Minimal graphic style — thick planes of limestone against warm plaster,
deep voids rendered as shadow gradients.
"""

from PIL import Image, ImageDraw, ImageFilter
import random

random.seed(42)

TW, TH = 1000, 600  # total width, per-panel height
BG = (235, 225, 208)       # warm plaster
STONE = (200, 187, 165)    # medium limestone
STONE_LIGHT = (220, 208, 188)
STONE_MED = (185, 172, 150)
STONE_DARK = (155, 142, 122)
VOID = (38, 33, 28)         # deep cavity
VOID_MID = (55, 48, 40)

def add_noise(img, intensity=2):
    """Add subtle noise to image using band-audio trick."""
    import io
    # Convert to bands, add noise, recombine
    r, g, b, a = img.split() if img.mode == 'RGBA' else (img.split())
    bands = list(a if a.mode == 'L' else [] for a in [r, g, b])

    for band_idx in range(3):
        pixels = bands[band_idx].load()
        w, h = bands[band_idx].size
        for y in range(h):
            for x in range(w):
                n = random.gauss(0, intensity)
                pixels[x, y] = max(0, min(255, pixels[x, y] + int(n)))

    if img.mode == 'RGBA':
        return Image.merge('RGBA', bands + [a])
    return Image.merge('RGB', bands)

def panel_frame(draw, ox, border=8):
    """Draw a subtle frame for a panel."""
    # Outer border
    draw.rectangle([ox, 0, ox + TW - 1, TH - 1],
                   outline=(120, 110, 95), width=2)
    # Inner subtle line
    draw.rectangle([ox + border, border, ox + TW - border - 1, TH - border - 1],
                   outline=(210, 200, 185), width=1)

def panel_ibeam(draw, cx, cy):
    """I-section beam: the voids define the identity.

    Drawn front-on as a thick beam. The face is mostly dark stone;
    the two large voids cut through it. The flanges (top/bottom) and web
    are the stone, everything else is void.
    """
    cx = int(cx)
    cy = int(cy)

    # Overall beam bounding
    beam_w = 220
    beam_h = 420
    bx = cx - beam_w // 2
    by = cy - beam_h // 2

    # Full beam silhouette as dark stone
    draw.rectangle([bx, by, bx + beam_w - 1, by + beam_h - 1], fill=STONE_DARK)

    # Flanges (top and bottom) — lighter, from upper-left light
    # Top flange
    ft = 40
    for dx in range(beam_w):
        for dy in range(ft):
            shade = int(STONE_LIGHT[0] - dx * 0.08 - dy * 0.05)
            r = max(0, min(255, shade))
            draw.point((bx + dx, by + dy), fill=(r, r - 8, r - 15))

    # Bottom flange
    by_bottom = by + beam_h - ft
    for dx in range(beam_w):
        for dy in range(ft):
            shade = int(STONE_MED[0] - dx * 0.05)
            r = max(0, min(255, shade))
            draw.point((bx + dx, by_bottom + dy), fill=(r, r - 6, r - 10))

    # Web (center vertical)
    web_w = 20
    web_x = cx - web_w // 2
    web_top = by + ft
    web_h = beam_h - 2 * ft
    for dx in range(web_w):
        for dy in range(web_h):
            shade = int(STONE_DARK[0] - dx * 0.5)
            r = max(0, min(255, shade))
            draw.point((web_x + dx, web_top + dy), fill=(r, r - 5, r - 10))

    # Voids — two large dark rectangles cutting through
    void_w = (beam_w - web_w) // 2 - 6
    void_h = web_h - 8
    void_top = by + ft + 4

    for vx in [bx + web_w + 3, cx + web_w // 2 + 3]:
        vy = void_top
        # Void fill (deep shadow)
        draw.rectangle([vx, vy, vx + void_w - 1, vy + void_h - 1], fill=VOID)

        # Inner shadow gradient on all four edges
        # Left edge (toward web)
        for dx in range(6):
            alpha = 1 - dx / 6
            r = int(VOID[0] + (STONE_DARK[0] - VOID[0]) * alpha)
            draw.rectangle([vx + dx, vy, vx + dx, vy + void_h - 1],
                          fill=(r, r - 3, r - 6))
        # Right edge (toward flange)
        for dx in range(4):
            alpha = 1 - dx / 4
            r = int(VOID[0] + (STONE[0] - VOID[0]) * alpha)
            draw.rectangle([vx + void_w - 1 - dx, vy, vx + void_w - 1 - dx, vy + void_h - 1],
                          fill=(r, r - 3, r - 6))
        # Top edge (toward top flange)
        for dy in range(5):
            alpha = 1 - dy / 5
            r = int(VOID[0] + (STONE_LIGHT[0] - VOID[0]) * alpha)
            draw.rectangle([vx, vy + dy, vx + void_w - 1, vy + dy],
                          fill=(r, r - 4, r - 8))
        # Bottom edge (toward bottom flange)
        for dy in range(4):
            alpha = 1 - dy / 4
            r = int(VOID[0] + (STONE_DARK[0] - VOID[0]) * alpha)
            draw.rectangle([vx, vy + void_h - 1 - dy, vx + void_w - 1, vy + void_h - 1 - dy],
                          fill=(r, r - 3, r - 6))

    # Shadow cast by beam onto background (bottom-right)
    shadow = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    # Soft shadow below and to the right
    for dx in range(30):
        alpha = int(60 * (1 - dx / 30))
        shadow_draw.rectangle([bx + 15 + dx, by + 15, bx + beam_w - 1 + 15 + dx,
                               by + beam_h - 1 + 15],
                             fill=(0, 0, 0, alpha))

    # Composite shadow
    img_shadow = shadow.convert('RGB')
    shadow_pixels = img_shadow.load()
    beam_pixels = draw.im.load()
    for y in range(TH):
        for x in range(TW):
            s = shadow_pixels[x, y]
            b = beam_pixels[x, y]
            if s[3] > 0:
                blend = s[3] / 255
                draw.point((x, y), fill=tuple(int(b[i] * (1 - blend)) for i in range(3)))

    # Label
    draw.text((cx - 40, by + beam_h + 18), "I-SECTION", fill=(110, 100, 85),
              font_size=13)


def panel_arch(draw, cx, cy):
    """Gothic arch: the opening carries the load.

    Seen head-on. Two pillars rise and form a pointed arch overhead.
    The void between them is the main feature — rendered as deep shadow
    that fades slightly toward the back.
    """
    cx = int(cx)
    cy = int(cy)

    base_y = cy + 200
    apex_y = cy - 220
    pillar_w = 90
    pillar_gap = 200  # width between pillars at base

    # Left pillar
    lx = cx - pillar_gap // 2 - pillar_w
    for dy in range(420):
        for dx in range(pillar_w):
            light = max(0, 25 * (1 - dx / pillar_w))
            shade = int(STONE_LIGHT[0] + light - dy * 0.03)
            r = max(0, min(255, shade))
            draw.point((lx + dx, base_y - dy), fill=(r, r - 8, r - 12))

    # Right pillar
    rx = cx + pillar_gap // 2
    for dy in range(420):
        for dx in range(pillar_w):
            light = max(0, 20 * (1 - (pillar_w - dx) / pillar_w))
            shade = int(STONE_MED[0] + light - dy * 0.03)
            r = max(0, min(255, shade))
            draw.point((rx + dx, base_y - dy), fill=(r, r - 6, r - 10))

    # Pointed crown — left side
    crown_h = 200
    for dy in range(crown_h):
        progress = dy / crown_h
        # Crown gets thinner and shifts toward center
        current_left_x = lx + pillar_w - int(pillar_w * progress * 0.6)
        current_thickness = max(8, int(35 * (1 - progress * 0.5)))

        for dx in range(current_thickness):
            shade = int(STONE_LIGHT[0] * (1 - progress * 0.2) - dx * 0.3)
            r = max(0, min(255, shade))
            draw.point((current_left_x + dx, base_y - crown_h + dy),
                       fill=(r, r - 8, r - 14))

    # Crown right side
    for dy in range(crown_h):
        progress = dy / crown_h
        current_right_x = rx - int((pillar_w + 20) * progress * 0.6)
        current_thickness = max(8, int(35 * (1 - progress * 0.5)))

        for dx in range(current_thickness):
            shade = int(STONE_MED[0] * (1 - progress * 0.2) - dx * 0.3)
            r = max(0, min(255, shade))
            draw.point((current_right_x - dx, base_y - crown_h + dy),
                       fill=(r, r - 6, r - 10))

    # The arch opening (void)
    # Narrow at top (pointed), wider at bottom
    opening_top_y = base_y - crown_h + 10
    opening_top_w = 60  # width at apex
    opening_bot_w = pillar_gap - 20  # width at base

    for dy in range(base_y - opening_top_y):
        progress = dy / (base_y - opening_top_y)
        current_w = int(opening_top_w + (opening_bot_w - opening_top_w) * progress)
        current_x = cx - current_w // 2

        # Draw void with slight back-light
        edge_dist = min(12, dy, (base_y - dy - opening_top_y),
                       current_x + current_w - current_x,
                       (current_x + current_w) - current_x)

        if edge_dist < 12:
            edge_factor = edge_dist / 12
            r = int(VOID[0] + (VOID_MID[0] - VOID[0]) * edge_factor)
            g = int(VOID[1] + (VOID_MID[1] - VOID[1]) * edge_factor)
            b = int(VOID[2] + (VOID_MID[2] - VOID[2]) * edge_factor)
            draw.rectangle([current_x, opening_top_y + dy,
                           current_x + current_w - 1, opening_top_y + dy],
                          fill=(r, g, b))

    # Deep core void (center, darkest)
    for dy in range(base_y - opening_top_y):
        progress = dy / (base_y - opening_top_y)
        current_w = int(opening_top_w + (opening_bot_w - opening_top_w) * progress)
        current_x = cx - current_w // 2
        core = int(current_w * 0.5)
        if core > 0:
            draw.rectangle([cx - core // 2, opening_top_y + dy,
                           cx + core // 2 - 1, opening_top_y + dy],
                          fill=VOID)

    # Label
    draw.text((cx - 25, base_y + 20), "ARCH", fill=(110, 100, 85),
              font_size=13)


def panel_cantilever(draw, cx, cy):
    """Cantilever slab: absence in tension.

    Wall on left, horizontal beam extending right. The shadow below
    the beam is the deep void — absence that holds weight.
    """
    cx = int(cx)
    cy = int(cy)

    # Wall
    wall_x = cx - 220
    wall_w = 50
    wall_h = 440
    wall_y = cy - wall_h // 2 + 60

    for dy in range(wall_h):
        for dx in range(wall_w):
            light = 30 * (1 - dx / wall_w)
            shade = int(STONE_LIGHT[0] * 0.85 + light - dy * 0.05)
            r = max(0, min(255, shade))
            draw.point((wall_x + dx, wall_y + dy), fill=(r, r - 6, r - 10))

    # Beam
    beam_y = wall_y + 50
    beam_h = 24
    beam_w = 340
    beam_x = wall_x + wall_w

    # Beam top (lightest surface)
    for dy in range(beam_h // 2):
        for dx in range(beam_w):
            fade = dx / beam_w * 15  # slight fade toward free end
            shade = int(STONE_LIGHT[0] - fade)
            r = max(0, min(255, shade))
            draw.point((beam_x + dx, beam_y + dy), fill=(r, r - 5, r - 10))

    # Beam bottom (darker, shadow side)
    for dy in range(beam_h // 2):
        for dx in range(beam_w):
            shade = int(STONE_DARK[0] * 0.7 - dx * 0.02)
            r = max(0, min(255, shade))
            draw.point((beam_x + dx, beam_y + beam_h // 2 + dy),
                       fill=(r, r - 5, r - 8))

    # Free edge (thin vertical line at beam end)
    free_x = beam_x + beam_w
    for dy in range(beam_h + 6):
        shade = int(STONE_LIGHT[0] * 0.9)
        draw.point((free_x, beam_y + dy), fill=(shade, shade - 4, shade - 8))

    # Shadow beneath beam — the deep void
    shadow_y = beam_y + beam_h + 2
    shadow_h = 100
    shadow_w = beam_w - 30

    for dy in range(shadow_h):
        dist_factor = 1 - dy / shadow_h  # fades with distance from beam
        # Also fades with distance from wall
        for dx in range(shadow_w):
            x_factor = 1.0 - 0.4 * (dx / shadow_w)
            darkness = dist_factor * x_factor

            r = int(VOID[0] + (STONE[0] - VOID[0]) * (1 - darkness) * 0.3)
            g = int(VOID[1] + (STONE[1] - VOID[1]) * (1 - darkness) * 0.3)
            b = int(VOID[2] + (STONE[2] - VOID[2]) * (1 - darkness) * 0.3)
            draw.point((beam_x + 15 + dx, shadow_y + dy),
                       fill=(int(r), int(g), int(b)))

    # Label
    draw.text((cx - 60, beam_y + beam_h + shadow_h + 25), "CANTILEVER",
              fill=(110, 100, 85), font_size=13)


# === Main ===
img = Image.new('RGB', (TW * 3, TH), BG)
draw = ImageDraw.Draw(img)

# Frame panels
panel_frame(draw, 0)
panel_frame(draw, TW)
panel_frame(draw, TW * 2)

# Draw forms
panel_ibeam(draw, TW // 2, TH // 2)
panel_arch(draw, TW * 1.5, TH // 2)
panel_cantilever(draw, TW * 2.5, TH // 2)

# Add noise
img = add_noise(img, intensity=2)

img.save('assets/structural-absence-triptych.png')
print(f"Saved assets/structural-absence-triptych.png ({TW*3}x{TH})")
