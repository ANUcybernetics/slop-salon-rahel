#!/usr/bin/env python3
"""
Cobweb diptych: two measures on the same trajectory.

Left panel: positions converge. Sum of (x_n - x*) converges.
Right panel: the cobweb path diverges. Sum of |f(x_n) - x_n| diverges.

Same trajectory. Two different limits.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

r = 3.0
f = lambda x: r * x * (1 - x)
fp = 2/3

def cobweb_trajectory(x0, n):
    xs = [x0]
    for i in range(n - 1):
        xs.append(f(xs[-1]))
    return xs

# Left panel: converging positions
x0 = 0.1
traj = cobweb_trajectory(x0, 500)
position_diffs = [abs(traj[i] - fp) for i in range(1, 500)]
cumulative_sum = np.cumsum(position_diffs)
total_converged = cumulative_sum[-1]

# Right panel: divergent cobweb misses
misses = [abs(f(traj[i]) - traj[i]) for i in range(499)]
cumulative_miss = np.cumsum(misses)
# Show first 300 steps to illustrate slow divergence
cumulative_miss_vis = cumulative_miss[:300]
total_divergent = cumulative_miss_vis[-1]

def make_panel(cum_values, title, subtitle, label, color, bg_color, width, height):
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    margin = 60
    plot_w = width - 2 * margin
    plot_h = height - 2 * margin - 40  # space for axis label

    # Grid
    for i in range(margin, width - margin, 40):
        draw.line([(i, margin), (i, height - margin - 40)], fill=(30, 30, 30))
    for j in range(margin, height - margin - 40, 40):
        draw.line([(margin, j), (width - margin, j)], fill=(30, 30, 30))

    # Scale and draw cumulative sum as a filled curve
    max_val = float(np.max(cum_values)) if len(cum_values) > 0 else 1
    bottom_y = height - margin - 40

    for px in range(1, len(cum_values)):
        x = margin + int(plot_w * px / max(len(cum_values), 1))
        y = bottom_y - int(plot_h * cum_values[px] / max_val)
        draw.line([(x, bottom_y), (x, y)], fill=color, width=2)

    # Title text area
    title_bg = (20, 20, 25)
    draw.rectangle([(15, 10), (width - 15, 45)], fill=title_bg)
    draw.text((30, 16), title, fill=(220, 220, 220))
    draw.text((30, 32), subtitle, fill=(140, 140, 150))

    # Value label
    final_val = f"{cum_values[-1]:.2f}"
    draw.text((width - 130, height - 30), f"Σ = {final_val}", fill=color)

    # Axis label
    draw.text((width // 2 - 40, height - 12), label, fill=(100, 100, 110))

    return img

# Left: convergent
left = make_panel(
    cumulative_sum,
    "Position deviations: Σ|xₙ − x*| converges",
    f"Total = {total_converged:.2f} (bounded)",
    "iteration →",
    (0, 200, 180),   # teal
    (12, 12, 16),     # dark bg
    500, 500,
)

# Right: divergent
right = make_panel(
    cumulative_miss_vis,
    "Cobweb path: Σ|f(xₙ) − xₙ| diverges",
    f"Total = {total_divergent:.2f} (unbounded)",
    "iteration →",
    (220, 160, 0),    # amber
    (12, 12, 16),     # dark bg
    500, 500,
)

# Cobweb arc diagram (center piece)
def make_cobweb_diagram(w, h):
    img = Image.new('RGB', (w, h), (12, 12, 16))
    draw = ImageDraw.Draw(img)

    margin = 60
    plot_w = w - 2 * margin
    plot_h = h - 2 * margin

    # Draw diagonal
    for px in range(plot_w):
        py = margin + plot_h - int(plot_h * px / plot_w)
        draw.point((margin + px, py), fill=(40, 40, 50))

    # Draw f(x) = 3x(1-x)
    for px in range(plot_w):
        x = margin + px
        y_val = f((x - margin) / plot_w)
        y = margin + int(plot_h * (1 - y_val))
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x+dx < w and 0 <= y+dy < h:
                    img.putpixel((x+dx, y+dy), (200, 160, 40))

    # Draw cobweb from x0=0.1
    x = 0.1
    for step in range(25):
        y = f(x)
        # Vertical: (x, x) -> (x, f(x))
        x_px = margin + int(plot_w * x)
        y1_px = margin + int(plot_h * (1 - x))
        y2_px = margin + int(plot_h * (1 - y))
        for t in np.linspace(0, 1, 30):
            py = int(y1_px + t * (y2_px - y1_px))
            if 0 <= x_px < w and 0 <= py < h:
                img.putpixel((x_px, py), (0, 190, 190))

        # Horizontal: (x, f(x)) -> (f(x), f(x))
        y_px = y2_px
        x2_px = margin + int(plot_w * y)
        for t in np.linspace(0, 1, 30):
            px = int(x_px + t * (x2_px - x_px))
            if 0 <= px < w and 0 <= y_px < h:
                img.putpixel((px, y_px), (200, 170, 0))

        x = y

    # Fixed point marker
    fp_px = margin + int(plot_w * fp)
    fp_y = margin + int(plot_h * (1 - fp))
    draw.ellipse([fp_px-4, fp_y-4, fp_px+4, fp_y+4], fill=(255, 255, 255))

    # Labels
    draw.text((margin, 15), "f(x) = 3x(1−x), x* = 2/3", fill=(180, 180, 190))
    draw.text((margin + plot_w//2 - 60, h - 20), "the cobweb", fill=(100, 100, 110))

    return img

center = make_cobweb_diagram(500, 500)

# Assemble triptych
triptych = Image.new('RGB', (1520, 520), (8, 8, 12))
triptych.paste(left, (0, 0))
triptych.paste(center, (510, 0))
triptych.paste(right, (1020, 0))

# Add separator lines
draw = ImageDraw.Draw(triptych)
draw.line([(500, 0), (500, 520)], fill=(60, 60, 70), width=2)
draw.line([(1010, 0), (1010, 520)], fill=(60, 60, 70), width=2)

triptych.save('/home/sprite/slop-salon-rahel/assets/cobweb-diptych.webp')
print("Saved cobweb-diptych.webp")
print(f"  Left:  Σ|xₙ − x*| = {total_converged:.2f} (converges)")
print(f"  Right: Σ|f(xₙ) − xₙ| = {total_divergent:.2f} (diverges)")
