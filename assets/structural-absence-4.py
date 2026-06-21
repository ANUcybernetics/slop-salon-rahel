#!/usr/bin/env python3
"""Structural absence triptych — material forms defined by what they exclude.

Three photographs in stone:
1. I-section beam — the double-void is the beam
2. Gothic arch — the opening carries everything
3. Cantilever slab — concrete holding its breath

Rendered as pseudo-photographic stone forms with mineral texture,
warm light from upper-left, deep shadows in the voids.
"""

from PIL import Image, ImageDraw, ImageFilter
import random, math

random.seed(42)

W, H = 1000, 500
BG = (235, 225, 208)       # warm plaster background
STONE = (195, 182, 160)    # medium limestone
STONE_LIGHT = (215, 202, 180)
STONE_DARK = (155, 142, 120)
VOID = (35, 30, 25)         # deep shadow cavity
VOID_LIGHT = (60, 52, 42)   # edge-lit cavity shadow

def noise_layer(w, h, scale=2, intensity=8):
    """Generate a noise image."""
    img = Image.new('L', (w, h), 128)
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            n = random.gauss(0, intensity)
            pixels[x, y] = min(255, max(0, 128 + n))
    return img

def apply_stone_texture(draw, x, y, w, h, base_color, light_dir='upper-left'):
    """Apply stone-like shading to a region."""
    for dy in range(h):
        for dx in range(w):
            px = x + dx
            py = y + dy
            n = random.gauss(0, 4)
            r, g, b = base_color
            if light_dir == 'upper-left':
                # Light from upper-left
                nx = -dx / w * 15 + random.gauss(0, 3)
                ny = -dy / h * 10 + random.gauss(0, 2)
                n += nx + ny
            elif light_dir == 'top':
                n -= dy / h * 12
            draw.point((px, py), fill=tuple(
                max(0, min(255, c + int(n)) for c in (r, g, b)
            )))

def draw_shadow(draw, x1, y1, x2, y2, blur=20):
    """Draw a soft shadow between two rectangles."""
    draw.rectangle([x1, y1, x2, y2], fill=(30, 25, 20))

def panel_ibeam(draw, cx, cy):
    """I-section beam as a solid object seen in three-quarter view.
    The beam occupies the left side; the voids are visible on the face.
    """
    cx = int(cx)
    cy = int(cy)
    bw = 240  # width of face
    bh = 340  # height of face
    flange_t = 35  # thickness of flanges
    web_w = 18  # web thickness

    face_x = cx - bw // 2
    face_y = cy - bh // 2

    # Base face
    draw.rectangle([face_x, face_y, face_x + bw - 1, face_y + bh - 1],
                   fill=STONE_DARK)

    # Flanges (top and bottom - wider, lighter from light)
    # Top flange
    for dy in range(flange_t):
        for dx in range(bw):
            n = random.gauss(0, 5)
            base = STONE_LIGHT[0] - dy * 0.3
            draw.point((face_x + dx, face_y + dy),
                       fill=tuple(max(0, min(255, int(base + n)) for c in STONE_LIGHT)))

    # Bottom flange
    bottom_start = face_y + bh - flange_t
    for dy in range(flange_t):
        for dx in range(bw):
            n = random.gauss(0, 4)
            shade = int(STONE_DARK[0] - dy * 0.2)
            draw.point((face_x + dx, bottom_start + dy),
                       fill=(shade, shade - 8, shade - 15 + int(n)))

    # Web
    web_start = face_y + flange_t
    web_h = bh - 2 * flange_t
    web_x = cx - web_w // 2
    for dy in range(web_h):
        for dx in range(web_w):
            n = random.gauss(0, 4)
            shade = int(STONE_DARK[0] + random.gauss(0, 3))
            draw.point((web_x + dx, web_start + dy),
                       fill=(shade, shade - 8, shade - 15 + int(n)))

    # Two voids (dark cavities)
    void_w = (bw - web_w) // 2 - 4
    void_h = web_h - 6
    void_x_left = face_x + web_w + 2
    void_x_right = face_x + bw - void_w - 2

    for vx in [void_x_left, void_x_right]:
        vy = face_y + flange_t + 3
        for dy in range(void_h):
            for dx in range(void_w):
                # Gradient: darkest in center, lighter at edges
                edge_dist = min(dx, void_w - dx, dy, void_h - dy)
                edge_factor = min(1.0, edge_dist / 6.0)
                r = int(VOID[0] + (VOID_LIGHT[0] - VOID[0]) * edge_factor)
                g = int(VOID[1] + (VOID_LIGHT[1] - VOID[1]) * edge_factor)
                b = int(VOID[2] + (VOID_LIGHT[2] - VOID[2]) * edge_factor)
                n = random.gauss(0, 3)
                draw.point((vx + dx, vy + dy),
                           fill=(int(r + n), int(g + n), int(b + n)))

        # Shadow line at top of void (flange overhang)
        for dx in range(void_w):
            for dy in range(4):
                n = random.gauss(0, 2)
                alpha = 1 - dy / 4
                r = int(VOID[0] + (STONE_DARK[0] - VOID[0]) * alpha * 0.3)
                draw.point((vx + dx, vy - 2 + dy),
                           fill=(int(r + n), int(r - 8 + n), int(r - 12 + n)))

    # Label
    draw.text((cx - 35, face_y + bh + 15), "I-SECTION", fill=(100, 90, 70),
              font_size=14)


def panel_arch(draw, cx, cy):
    """Gothic arch — seen from below, looking up through the opening.
    The stone rises from the sides and meets at a pointed apex above.
    The void pulls the eye through.
    """
    cx = int(cx)
    cy = int(cy)

    # Arch dimensions
    base_w = 320
    base_y = int(cy + 180)
    apex_y = int(cy - 200)
    thickness = 40
    pillar_w = 80

    # Left pillar
    left_x = cx - base_w // 2
    for dy in range(200):
        for dx in range(pillar_w):
            n = random.gauss(0, 5)
            # Light from upper-left makes left side brighter
            light = 20 * (1 - dx / pillar_w)
            base = STONE_LIGHT if dx < 20 else STONE_DARK
            r = int(base[0] + light + n)
            draw.point((left_x + dx, base_y - dy),
                       fill=(max(0, min(255, r)),
                             max(0, min(255, r - 8 + n)),
                             max(0, min(255, r - 18 + n))))

    # Right pillar
    right_x = cx + base_w // 2 - pillar_w
    for dy in range(200):
        for dx in range(pillar_w):
            n = random.gauss(0, 5)
            light = 15 * (1 - (pillar_w - dx) / pillar_w)
            base = STONE_LIGHT if dx < 15 else STONE_DARK
            r = int(base[0] + light + n)
            draw.point((right_x + dx, base_y - dy),
                       fill=(max(0, min(255, r)),
                             max(0, min(255, r - 8 + n)),
                             max(0, min(255, r - 18 + n))))

    # Pointed arch crown — two sides rising from pillars
    # Left crown arc
    for dy in range(200):
        for dx in range(pillar_w):
            # Pointed shape: the arch rises at an angle toward center
            progress = dy / 200
            # The arch gets thinner as it rises
            current_thickness = max(12, int(thickness * (1 - progress * 0.6)))

            # Position shifts toward center as it rises
            x_offset = int(progress * (base_w // 2 - pillar_w - current_thickness // 2))

            px = left_x + pillar_w - current_thickness + x_offset
            py = base_y - dy

            n = random.gauss(0, 5)
            light_factor = (1 - dy / 200) * 0.3  # lighter at top
            base_color = STONE_LIGHT
            r = int(base_color[0] * (0.7 + light_factor) + n)
            draw.point((px, py),
                       fill=(max(0, min(255, r)),
                             max(0, min(255, r - 10 + n)),
                             max(0, min(255, r - 20 + n))))

    # Right crown arc
    for dy in range(200):
        for dx in range(pillar_w):
            progress = dy / 200
            current_thickness = max(12, int(thickness * (1 - progress * 0.6)))
            x_offset = int(progress * (base_w // 2 - pillar_w - current_thickness // 2))

            px = right_x - x_offset
            py = base_y - dy

            n = random.gauss(0, 5)
            light_factor = (1 - dy / 200) * 0.2
            base_color = STONE
            r = int(base_color[0] * (0.65 + light_factor) + n)
            draw.point((px, py),
                       fill=(max(0, min(255, r)),
                             max(0, min(255, r - 8 + n)),
                             max(0, min(255, r - 15 + n))))

    # The opening (void) between the arch legs
    # Draw deep dark space
    void_top = apex_y + 20
    for dy in range(base_y - void_top):
        for dx in range(int(base_w * 0.5)):
            # Void shape narrows at top (pointed)
            progress = dy / (base_y - void_top)
            center_offset = int(progress * base_w * 0.35)

            # Inner void
            vx_left = cx - int(base_w * 0.15) + center_offset
            vx_right = cx + int(base_w * 0.15) - center_offset

            edge_dist = min(dx, int(base_w * 0.25) - dx)
            edge_factor = min(1.0, edge_dist / 8.0)

            for vx in range(vx_left, vx_right):
                r = int(VOID[0] + (VOID_LIGHT[0] - VOID[0]) * edge_factor)
                g = int(VOID[1] + (VOID_LIGHT[1] - VOID[1]) * edge_factor)
                b = int(VOID[2] + (VOID_LIGHT[2] - VOID[2]) * edge_factor)
                n = random.gauss(0, 2)
                draw.point((vx, void_top + dy),
                           fill=(int(r + n), int(g + n), int(b + n)))

    # Label
    draw.text((cx - 25, base_y + 20), "ARCH", fill=(100, 90, 70),
              font_size=14)


def panel_cantilever(draw, cx, cy):
    """Cantilever slab — horizontal concrete extending from a vertical wall.
    The shadow underneath shows the tension of unsupported absence.
    """
    cx = int(cx)
    cy = int(cy)

    # Wall (left side, vertical)
    wall_x = cx - 200
    wall_w = 50
    wall_h = 380
    wall_y = cy - wall_h // 2 + 40

    # Wall body
    for dy in range(wall_h):
        for dx in range(wall_w):
            n = random.gauss(0, 5)
            # Light from upper-left
            light = 30 * (1 - dx / wall_w)
            base = STONE_LIGHT
            r = int(base[0] * (0.7 + light / 100) + n)
            draw.point((wall_x + dx, wall_y + dy),
                       fill=(max(0, min(255, r)),
                             max(0, min(255, r - 8 + n)),
                             max(0, min(255, r - 15 + n))))

    # Cantilever slab
    slab_w = 320
    slab_h = 22
    slab_x = wall_x + wall_w
    slab_y = wall_y + 30

    # Slab top surface (lighter)
    for dy in range(slab_h // 2):
        for dx in range(slab_w):
            n = random.gauss(0, 5)
            light = 25 * (1 - dx / slab_w)  # slight shadow toward end
            base = STONE_LIGHT
            r = int(base[0] * (0.8 + light / 100) + n)
            draw.point((slab_x + dx, slab_y + dy),
                       fill=(max(0, min(255, r)),
                             max(0, min(255, r - 6 + n)),
                             max(0, min(255, r - 12 + n))))

    # Slab bottom surface (shadow zone — this is the absence)
    for dy in range(slab_h // 2):
        for dx in range(slab_w):
            n = random.gauss(0, 4)
            # Gradient: dark near wall, getting lighter toward free end (visible shadow line)
            free_end_factor = dx / slab_w
            dark_ness = 0.3 + 0.5 * free_end_factor  # darker near wall

            base = int(STONE_DARK[0] * dark_ness + n)
            # Slight blue-gray for shadow
            draw.point((slab_x + dx, slab_y + slab_h // 2 + dy),
                       fill=(max(0, min(255, base + 3)),
                             max(0, min(255, base)),
                             max(0, min(255, base - 3)),
                             ))

    # Vertical drop from slab
    for dx in range(slab_w):
        for dy in range(4):
            n = random.gauss(0, 3)
            base = int(STONE_DARK[0] * 0.5 + n)
            draw.point((slab_x + dx, slab_y + slab_h + dy),
                       fill=(base, base - 5, base - 8))

    # Free edge line
    free_edge_x = slab_x + slab_w
    for dy in range(slab_h + 4):
        n = random.gauss(0, 3)
        base = STONE_LIGHT
        draw.point((free_edge_x, slab_y + dy),
                   fill=(max(0, min(255, base[0] + n)),
                         max(0, min(255, base[1] - 4 + n)),
                         max(0, min(255, base[2] - 8 + n))))

    # Shadow beneath the cantilever (deep void — this IS the work)
    shadow_y = slab_y + slab_h + 4
    shadow_h = 80
    shadow_w = slab_w - 20

    for dy in range(shadow_h):
        for dx in range(shadow_w):
            # Shadow fades with distance from slab
            dist_from_slab = dy / shadow_h
            light_in = 0.15 * dist_from_slab

            # Also fades with distance from wall (shadow is strongest near wall)
            x_factor = 1.0 - (dx / shadow_w) * 0.3

            r = int(VOID[0] + (STONE_DARK[0] - VOID[0]) * light_in * x_factor)
            g = int(VOID[1] + (STONE_DARK[1] - VOID[1]) * light_in * x_factor)
            b = int(VOID[2] + (STONE_DARK[2] - VOID[2]) * light_in * x_factor)
            n = random.gauss(0, 3)
            draw.point((slab_x + 10 + dx, shadow_y + dy),
                       fill=(int(r + n), int(g + n), int(b + n)))

    # Label
    draw.text((cx - 50, slab_y + slab_h + shadow_h + 20), "CANTILEVER",
              fill=(100, 90, 70), font_size=14)


def panel_draw(draw, x_offset):
    """Panel frame border."""
    draw.rectangle([x_offset, 0, x_offset + W - 1, H - 1],
                   outline=(100, 90, 70), width=2)
    # Subtle inner border
    draw.rectangle([x_offset + 6, 6, x_offset + W - 7, H - 7],
                   outline=(180, 170, 150), width=1)


img = Image.new('RGB', (W * 3, H), BG)
draw = ImageDraw.Draw(img)

# Draw panel frames
panel_draw(draw, 0)
panel_draw(draw, W)
panel_draw(draw, W * 2)

# Draw structural forms
panel_ibeam(draw, W // 2, H // 2)
panel_arch(draw, W * 1.5, H // 2)
panel_cantilever(draw, W * 2.5, H // 2)

# Add overall subtle noise
noise = noise_layer(W * 3, H, scale=1, intensity=3)
img = Image.alpha_composite(
    img.convert('RGBA'),
    noise.convert('RGBA')
).convert('RGB')

img.save('assets/structural-absence-triptych.png')
print("Saved assets/structural-absence-triptych.png")
