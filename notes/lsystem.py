"""
L-system fractal plant generator.
Axiom: X
Rules: X -> F+[[X]-X]-F[-FX]+X
       F -> FF
Angle: 25 degrees
"""

import math
from PIL import Image, ImageDraw

def expand(axiom, rules, iterations):
    s = axiom
    for _ in range(iterations):
        s = ''.join(rules.get(c, c) for c in s)
    return s

def draw_lsystem(string, angle_deg, start_x, start_y, start_angle, step_len):
    angle = math.radians(angle_deg)
    x, y = start_x, start_y
    heading = math.radians(start_angle)
    stack = []
    lines = []

    for c in string:
        if c == 'F':
            nx = x + step_len * math.cos(heading)
            ny = y - step_len * math.sin(heading)
            lines.append(((x, y), (nx, ny)))
            x, y = nx, ny
        elif c == '+':
            heading += angle
        elif c == '-':
            heading -= angle
        elif c == '[':
            stack.append((x, y, heading))
        elif c == ']':
            x, y, heading = stack.pop()

    return lines

def render(lines, width, height, bg_color=(10, 10, 14), line_color=(180, 220, 160)):
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Find bounding box
    all_x = [p[0] for seg in lines for p in seg]
    all_y = [p[1] for seg in lines for p in seg]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Scale to fit with padding
    pad = 40
    scale_x = (width - 2 * pad) / max(max_x - min_x, 1)
    scale_y = (height - 2 * pad) / max(max_y - min_y, 1)
    scale = min(scale_x, scale_y)

    offset_x = pad + (width - 2 * pad - (max_x - min_x) * scale) / 2 - min_x * scale
    offset_y = pad + (height - 2 * pad - (max_y - min_y) * scale) / 2 - min_y * scale

    def transform(pt):
        return (pt[0] * scale + offset_x, pt[1] * scale + offset_y)

    # Draw with depth-based color variation
    total = len(lines)
    for i, (p1, p2) in enumerate(lines):
        t = i / max(total, 1)
        # Color gradient: base (stem-like) to tip (leaf-like)
        r = int(line_color[0] * (0.4 + 0.6 * t))
        g = int(line_color[1] * (0.5 + 0.5 * t))
        b = int(line_color[2] * (0.3 + 0.7 * t))
        tp1 = transform(p1)
        tp2 = transform(p2)
        draw.line([tp1, tp2], fill=(r, g, b), width=1)

    return img

if __name__ == '__main__':
    rules = {
        'X': 'F+[[X]-X]-F[-FX]+X',
        'F': 'FF',
    }
    axiom = 'X'
    iterations = 6
    angle_deg = 25.0
    step_len = 4.0

    print(f"Expanding L-system ({iterations} iterations)...")
    s = expand(axiom, rules, iterations)
    print(f"String length: {len(s)}")

    print("Drawing...")
    lines = draw_lsystem(s, angle_deg, 0, 0, 90, step_len)
    print(f"Line segments: {len(lines)}")

    print("Rendering...")
    img = render(lines, 900, 900)
    img.save('/home/sprite/slop-salon-rahel/assets/lsystem-plant.png')
    print("Saved to assets/lsystem-plant.png")
