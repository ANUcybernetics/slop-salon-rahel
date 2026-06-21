from PIL import Image, ImageDraw
import random
random.seed(42)

PW, PH = 1000, 600
TOTAL_W = PW * 3
BG = (232, 222, 205)
SL = (215, 203, 183)
SM = (190, 178, 158)
SD = (160, 148, 128)
VD = (40, 35, 30)
VL = (70, 62, 52)
SB = (195, 183, 163)

def ibeam(draw, cx, cy):
    cx, cy = int(cx), int(cy)
    bw, bh = 260, 460
    bx, by = cx - bw // 2, cy - bh // 2
    ft, ww = 45, 22
    draw.rectangle([bx, by, bx + bw - 1, by + bh - 1], fill=SD)
    draw.rectangle([bx, by, bx + bw - 1, by + ft - 1], fill=SL)
    draw.rectangle([bx, by + bh - ft, bx + bw - 1, by + bh - 1], fill=SM)
    wx = cx - ww // 2
    draw.rectangle([wx, by + ft, wx + ww - 1, by + bh - ft - 1], fill=SD)
    vw = (bw - ww) // 2 - 8
    vh = bh - 2 * ft - 10
    vt = by + ft + 5
    for vx in [bx + ww + 4, cx + ww // 2 + 4]:
        vy = vt
        draw.rectangle([vx, vy, vx + vw - 1, vy + vh - 1], fill=VD)
        for i in range(10):
            a = 1 - i / 10
            r, g, b = int(VD[0]+(SD[0]-VD[0])*a), int(VD[1]+(SM[1]-VD[1])*a), int(VD[2]+(SM[2]-VD[2])*a)
            draw.rectangle([vx+i, vy, vx+i, vy+vh-1], fill=(r,g,b))
            draw.rectangle([vx+vw-1-i, vy, vx+vw-1-i, vy+vh-1], fill=(r,g,b))
        for i in range(8):
            a = 1 - i / 8
            r, g, b = int(VD[0]+(SL[0]-VD[0])*a), int(VD[1]+(SL[1]-VD[1])*a), int(VD[2]+(SL[2]-VD[2])*a)
            draw.rectangle([vx, vy+i, vx+vw-1, vy+i], fill=(r,g,b))
            draw.rectangle([vx, vy+vh-1-i, vx+vw-1, vy+vh-1-i], fill=(r,g,b))
        for dy in range(5):
            a = 1 - dy / 5
            r = int(VD[0] + (SD[0] - VD[0]) * a * 0.5)
            draw.rectangle([vx, vy-2+dy, vx+vw-1, vy-2+dy], fill=(r, r-3, r-6))

def arch(draw, cx, cy):
    cx, cy = int(cx), int(cy)
    base_y = cy + 200
    pillar_h, pillar_w, pillar_gap = 440, 80, 240
    lx = cx - pillar_gap // 2 - pillar_w
    draw.rectangle([lx, base_y - pillar_h, lx + pillar_w - 1, base_y - 1], fill=SL)
    rx = cx + pillar_gap // 2
    draw.rectangle([rx, base_y - pillar_h, rx + pillar_w - 1, base_y - 1], fill=SM)
    # Crown: solid polygon for each side
    apex_y = base_y - pillar_h - 240
    # Left crown: from pillar inner edge to apex
    draw.polygon([
        (lx + pillar_w - 20, base_y - pillar_h), (lx + pillar_w + 25, base_y - pillar_h),
        (cx + 8, apex_y + 30), (cx - 8, apex_y + 30),
    ], fill=SL)
    # Right crown
    draw.polygon([
        (rx - 25, base_y - pillar_h), (rx - pillar_w + 20, base_y - pillar_h),
        (cx + 8, apex_y + 30), (cx - 8, apex_y + 30),
    ], fill=SM)
    # Top cap (the pointed tip where they meet)
    draw.polygon([
        (cx - 10, apex_y + 30), (cx + 10, apex_y + 30),
        (cx + 15, apex_y + 20), (cx - 15, apex_y + 20),
    ], fill=SL)
    # Opening void
    for dy in range(pillar_h - 30):
        progress = dy / (pillar_h - 30)
        w = int(70 + 170 * (progress ** 0.7))
        y = base_y - 30 - dy
        core = w // 3
        if core > 0:
            draw.rectangle([cx - core//2, y, cx + core//2 - 1, y], fill=VD)
        ring = (w - core) // 2
        if ring > 0:
            draw.rectangle([cx - w//2, y, cx - w//2 + ring - 1, y], fill=VL)
            draw.rectangle([cx + w//2 - ring, y, cx + w//2 - 1, y], fill=VL)

def cantilever(draw, cx, cy):
    cx, cy = int(cx), int(cy)
    wall_x = cx - 260
    wall_w, wall_h = 60, 520
    wall_y = cy - wall_h // 2 + 40
    draw.rectangle([wall_x, wall_y, wall_x + wall_w - 1, wall_y + wall_h - 1], fill=SL)
    beam_y = wall_y + 70
    beam_h, beam_w = 32, 400
    beam_x = wall_x + wall_w
    draw.rectangle([beam_x, beam_y, beam_x + beam_w - 1, beam_y + beam_h - 1], fill=SL)
    for dy in range(beam_h // 2):
        shade = int(SD[0] - dy * 0.8)
        draw.rectangle([beam_x, beam_y + beam_h//2 + dy, beam_x + beam_w - 1, beam_y + beam_h//2 + dy],
                      fill=(shade, shade-5, shade-10))
    shadow_y = beam_y + beam_h + 2
    for dy in range(100):
        fade = 1 - dy / 100
        x_factor = 1.0 - 0.6 * (1 - fade)
        shade = int(VD[0] + (SB[0] - VD[0]) * (1 - fade * x_factor) * 0.3)
        draw.rectangle([beam_x + 20, shadow_y + dy, beam_x + beam_w - 40, shadow_y + dy],
                      fill=(shade, shade-3, shade-6))

img = Image.new('RGB', (TOTAL_W, PH), BG)
draw = ImageDraw.Draw(img)
ibeam(draw, PW//2, PH//2)
arch(draw, PW*1.5, PH//2)
cantilever(draw, PW*2.5, PH//2)
for x in [PW, PW*2]:
    draw.line([(x, 0), (x, PH)], fill=(200, 190, 175), width=1)
img.save('assets/structural-absence-triptych.png')
print("Saved")
