from PIL import Image, ImageDraw
import random
random.seed(42)

PW, PH = 1000, 600
TOTAL_W = PW * 3

def make_panel(draw_func, bg_color, structural_colors):
    img = Image.new('RGB', (PW, PH), bg_color)
    draw = ImageDraw.Draw(img)
    draw_func(draw, structural_colors)
    return img

def ibeam(draw, c):
    """I-beam cross-section with voids: structural form, hollowed."""
    cx, cy = PW//2, PH//2
    bw, bh = 260, 460
    bx, by = cx - bw//2, cy - bh//2
    ft, ww = 45, 22
    sl, sm, sd, vd, vl, sb = c
    # Body
    draw.rectangle([bx, by, bx+bw-1, by+bh-1], fill=sd)
    # Flanges
    draw.rectangle([bx, by, bx+bw-1, by+ft-1], fill=sl)
    draw.rectangle([bx, by+bh-ft, bx+bw-1, by+bh-1], fill=sm)
    # Web
    wx = cx - ww//2
    draw.rectangle([wx, by+ft, wx+ww-1, by+bh-ft-1], fill=sd)
    # Voids with gradient edges
    vw = (bw-ww)//2 - 8
    vh = bh - 2*ft - 10
    vt = by + ft + 5
    for vx in [bx+ww+4, cx+ww//2+4]:
        vy = vt
        draw.rectangle([vx, vy, vx+vw-1, vy+vh-1], fill=vd)
        for i in range(10):
            a = 1 - i/10
            r = int(vd[0]+(sd[0]-vd[0])*a)
            g = int(vd[1]+(sm[1]-vd[1])*a)
            b = int(vd[2]+(sm[2]-vd[2])*a)
            draw.rectangle([vx+i,vy,vx+i,vy+vh-1], fill=(r,g,b))
            draw.rectangle([vx+vw-1-i,vy,vx+vw-1-i,vy+vh-1], fill=(r,g,b))
        for i in range(8):
            a = 1 - i/8
            r = int(vd[0]+(sl[0]-vd[0])*a)
            g = int(vd[1]+(sl[1]-vd[1])*a)
            b = int(vd[2]+(sl[2]-vd[2])*a)
            draw.rectangle([vx,vy+i,vx+vw-1,vy+i], fill=(r,g,b))
            draw.rectangle([vx,vy+vh-1-i,vx+vw-1,vy+vh-1-i], fill=(r,g,b))

def arch(draw, c):
    """Archway: two pillars and a crown, the opening is the absence."""
    cx, cy = PW//2, PH//2
    sl, sm, sd, vd, vl, sb = c
    base_y = cy + 200
    ph, pw, gap = 440, 80, 240
    lx = cx - gap//2 - pw
    # Left pillar
    draw.rectangle([lx, base_y-ph, lx+pw-1, base_y-1], fill=sl)
    # Right pillar
    draw.rectangle([cx+gap//2, base_y-ph, cx+gap//2+pw-1, base_y-1], fill=sm)
    apex_y = base_y - ph - 240
    # Crown: triangles from pillar tops to apex center
    draw.polygon([
        (lx+pw, base_y-ph), (lx+pw+35, base_y-ph),
        (cx+6, apex_y+30), (cx-6, apex_y+30),
    ], fill=sl)
    draw.polygon([
        (cx+gap//2-35, base_y-ph), (cx+gap//2, base_y-ph),
        (cx+6, apex_y+30), (cx-6, apex_y+30),
    ], fill=sm)
    # Top cap
    draw.polygon([
        (cx-8, apex_y+30), (cx+8, apex_y+30),
        (cx+10, apex_y+18), (cx-10, apex_y+18),
    ], fill=sb)
    # Opening void: concentric rings getting wider at bottom
    for dy in range(ph-30):
        progress = dy / (ph-30)
        w = int(70 + 170 * (progress**0.7))
        y = base_y - 30 - dy
        core = w // 3
        if core > 0:
            draw.rectangle([cx-core//2, y, cx+core//2-1, y], fill=vd)
        ring = (w-core)//2
        if ring > 0:
            draw.rectangle([cx-w//2, y, cx-w//2+ring-1, y], fill=vl)
            draw.rectangle([cx+w//2-ring, y, cx+w//2-1, y], fill=vl)

def cantilever(draw, c):
    """Cantilever: wall on left, beam extending right, shadow below."""
    cx, cy = PW//2, PH//2
    sl, sm, sd, vd, vl, sb = c
    wall_x = cx - 180
    wall_w, wall_h = 60, 520
    wall_y = cy - wall_h//2 + 40
    draw.rectangle([wall_x, wall_y, wall_x+wall_w-1, wall_y+wall_h-1], fill=sl)
    beam_y = wall_y + 70
    beam_h, beam_w = 32, 400
    beam_x = wall_x + wall_w
    draw.rectangle([beam_x, beam_y, beam_x+beam_w-1, beam_y+beam_h-1], fill=sl)
    for dy in range(beam_h//2):
        shade = int(sd[0] - dy*0.8)
        draw.rectangle([beam_x, beam_y+beam_h//2+dy, beam_x+beam_w-1, beam_y+beam_h//2+dy],
                      fill=(shade, shade-5, shade-10))
    shadow_y = beam_y + beam_h + 2
    for dy in range(100):
        fade = 1 - dy/100
        x_factor = 1.0 - 0.6*(1-fade)
        shade = int(vd[0] + (sb[0]-vd[0])*(1-fade*x_factor)*0.3)
        draw.rectangle([beam_x+20, shadow_y+dy, beam_x+beam_w-40, shadow_y+dy],
                      fill=(shade, shade-3, shade-6))

# Color palettes per panel
palette_light = (232, 222, 205)  # bg
palette_sl = (120, 100, 75)
palette_sm = (100, 82, 60)
palette_sd = (85, 70, 50)
palette_vd = (40, 35, 30)
palette_vl = (70, 58, 42)
palette_sb = (160, 145, 120)

palette_dark = (50, 42, 35)  # bg
palette_sl2 = (180, 168, 148)
palette_sm2 = (160, 148, 128)
palette_sd2 = (140, 130, 110)
palette_vd2 = (20, 18, 14)
palette_vl2 = (90, 82, 70)
palette_sb2 = (195, 185, 165)

# Build
img1 = make_panel(ibeam, palette_light, (palette_sl, palette_sm, palette_sd, palette_vd, palette_vl, palette_sb))
img2 = make_panel(arch, palette_dark, (palette_sl2, palette_sm2, palette_sd2, palette_vd2, palette_vl2, palette_sb2))
img3 = make_panel(cantilever, palette_dark, (palette_sl2, palette_sm2, palette_sd2, palette_vd2, palette_vl2, palette_sb2))

# Compose
result = Image.new('RGB', (TOTAL_W, PH), palette_light)
result.paste(img1, (0, 0))
result.paste(img2, (PW, 0))
result.paste(img3, (PW*2, 0))

# Separators
dr = ImageDraw.Draw(result)
for x in [PW, PW*2]:
    dr.line([(x, 0), (x, PH)], fill=(200, 190, 175), width=1)

result.save('assets/structural-absence-triptych.png')
print("Saved assets/structural-absence-triptych.png")
