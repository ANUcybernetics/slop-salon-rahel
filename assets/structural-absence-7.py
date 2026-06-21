#!/usr/bin/env python3
"""Structural absence triptych - three forms where the void IS the form."""

from PIL import Image, ImageDraw
import random

random.seed(42)

PW, PH = 1000, 600
TOTAL_W = PW * 3
BG = (232, 222, 205)
STONE_L = (215, 203, 183)
STONE_M = (190, 178, 158)
STONE_D = (160, 148, 128)
VOID = (40, 35, 30)
VOID_L = (70, 62, 52)
STONE_BASE = (195, 183, 163)

def ibeam(draw, cx, cy):
    cx, cy = int(cx), int(cy)
    bw, bh = 260, 460
    bx, by = cx - bw // 2, cy - bh // 2
    ft = 45
    web_w = 22
    draw.rectangle([bx, by, bx + bw - 1, by + bh - 1], fill=STONE_D)
    draw.rectangle([bx, by, bx + bw - 1, by + ft - 1], fill=STONE_L)
    draw.rectangle([bx, by + bh - ft, bx + bw - 1, by + bh - 1], fill=STONE_M)
    web_x = cx - web_w // 2
    draw.rectangle([web_x, by + ft, web_x + web_w - 1, by + bh - ft - 1], fill=STONE_D)
    void_w = (bw - web_w) // 2 - 8
    void_h = bh - 2 * ft - 10
    void_top = by + ft + 5
    for vx in [bx + web_w + 4, cx + web_w // 2 + 4]:
        vy = void_top
        draw.rectangle([vx, vy, vx + void_w - 1, vy + void_h - 1], fill=VOID)
        for i in range(10):
            a = 1 - i / 10
            r = int(VOID[0] + (STONE_D[0] - VOID[0]) * a)
            g = int(VOID[1] + (STONE_M[1] - VOID[1]) * a)
            b = int(VOID[2] + (STONE_M[2] - VOID[2]) * a)
            draw.rectangle([vx + i, vy, vx + i, vy + void_h - 1], fill=(r, g, b))
            draw.rectangle([vx + void_w - 1 - i, vy, vx + void_w - 1 - i, vy + void_h - 1], fill=(r, g, b))
        for i in range(8):
            a = 1 - i / 8
            r = int(VOID[0] + (STONE_L[0] - VOID[0]) * a)
            g = int(VOID[1] + (STONE_L[1] - VOID[1]) * a)
            b = int(VOID[2] + (STONE_L[2] - VOID[2]) * a)
            draw.rectangle([vx, vy + i, vx + void_w - 1, vy + i], fill=(r, g, b))
            draw.rectangle([vx, vy + void_h - 1 - i, vx + void_w - 1, vy + void_h - 1 - i], fill=(r, g, b))
        for dy in range(5):
            a = 1 - dy / 5
            r = int(VOID[0] + (STONE_D[0] - VOID[0]) * a * 0.5)
            draw.rectangle([vx, vy - 2 + dy, vx + void_w - 1, vy - 2 + dy], fill=(r, r - 3, r - 6))

def arch(draw, cx, cy):
    cx, cy = int(cx), int(cy)
    base_y = cy + 200
    pillar_h = 440
    pillar_w = 80
    pillar_gap = 240
    lx = cx - pillar_gap // 2 - pillar_w
    draw.rectangle([lx, base_y - pillar_h, lx + pillar_w - 1, base_y - 1], fill=STONE_L)
    rx = cx + pillar_gap // 2
    draw.rectangle([rx, base_y - pillar_h, rx + pillar_w - 1, base_y - 1], fill=STONE_M)
    crown_h = 240
    apex_y = base_y - pillar_h - crown_h
    draw.line([(lx + pillar_w, base_y - pillar_h), (cx, apex_y + 30)], fill=STONE_L, width=40)
    draw.line([(rx, base_y - pillar_h), (cx, apex_y + 30)], fill=STONE_M, width=40)
    draw.polygon([(lx + pillar_w, base_y - pillar_h), (lx + pillar_w + 40, base_y - pillar_h),
                  (cx + 12, apex_y + 30), (cx - 12, apex_y + 30)], fill=STONE_L)
    draw.polygon([(rx - 40, base_y - pillar_h), (rx, base_y - pillar_h),
                  (cx + 12, apex_y + 30), (cx - 12, apex_y + 30)], fill=STONE_M)
    for dy in range(pillar_h - 30):
        progress = dy / (pillar_h - 30)
        w = int(70 + 170 * (progress ** 0.7))
        y = base_y - 30 - dy
        core = w // 3
        if core > 0:
            draw.rectangle([cx - core // 2, y, cx + core // 2 - 1, y], fill=VOID)
        ring = (w - core) // 2
        if ring > 0:
            draw.rectangle([cx - w // 2, y, cx - w // 2 + ring - 1, y], fill=VOID_L)
            draw.rectangle([cx + w // 2 - ring, y, cx + w // 2 - 1, y], fill=VOID_L)

def cantilever(draw, cx, cy):
    cx, cy = int(cx), int(cy)
    wall_x = cx - 240
    wall_w = 55
    wall_h = 500
    wall_y = cy - wall_h // 2 + 50
    draw.rectangle([wall_x, wall_y, wall_x + wall_w - 1, wall_y + wall_h - 1], fill=STONE_L)
    beam_y = wall_y + 60
    beam_h = 26
    beam_w = 380
    beam_x = wall_x + wall_w
    draw.rectangle([beam_x, beam_y, beam_x + beam_w - 1, beam_y + beam_h - 1], fill=STONE_L)
    for dy in range(beam_h // 2):
        shade = int(STONE_D[0] - dy * 0.8)
        draw.rectangle([beam_x, beam_y + beam_h // 2 + dy, beam_x + beam_w - 1, beam_y + beam_h // 2 + dy],
                      fill=(shade, shade - 5, shade - 10))
    shadow_y = beam_y + beam_h + 2
    for dy in range(100):
        fade = 1 - dy / 100
        x_factor = 1.0 - 0.6 * (1 - fade)
        shade = int(VOID[0] + (STONE_BASE[0] - VOID[0]) * (1 - fade * x_factor) * 0.3)
        draw.rectangle([beam_x + 20, shadow_y + dy, beam_x + beam_w - 30, shadow_y + dy],
                      fill=(shade, shade - 3, shade - 6))

img = Image.new('RGB', (TOTAL_W, PH), BG)
draw = ImageDraw.Draw(img)
ibeam(draw, PW // 2, PH // 2)
arch(draw, PW * 1.5, PH // 2)
cantilever(draw, PW * 2.5, PH // 2)
for x in [PW, PW * 2]:
    draw.line([(x, 0), (x, PH)], fill=(200, 190, 175), width=1)
img.save('assets/structural-absence-triptych.png')
print("Saved assets/structural-absence-triptych.png")
