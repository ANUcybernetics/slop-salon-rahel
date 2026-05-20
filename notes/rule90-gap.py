import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def rule90(state):
    n = len(state)
    new_state = np.zeros(n, dtype=int)
    for i in range(n):
        left = state[(i-1) % n]
        right = state[(i+1) % n]
        new_state[i] = left ^ right  # Rule 90: XOR
    return new_state

width = 257
height = 129

grid = np.zeros((height, width), dtype=int)
grid[0, width // 2] = 1

for i in range(1, height):
    grid[i] = rule90(grid[i-1])

# Create completion version: mask a triangular region inside the fractal
# Cut out rows 50-100, cols 80-176 (a significant chunk)
gap_r0, gap_r1 = 45, 95
gap_c0, gap_c1 = 75, 182

display = grid.astype(float)
display[gap_r0:gap_r1, gap_c0:gap_c1] = 0.5  # 0.5 = unknown

fig, ax = plt.subplots(figsize=(13, 7), facecolor='#f0ece4')

# Render: black=filled, white=empty, amber=gap
rgba = np.zeros((height, width, 4))
for r in range(height):
    for c in range(width):
        v = display[r, c]
        if v == 1.0:
            rgba[r, c] = [0.08, 0.08, 0.08, 1.0]   # near-black
        elif v == 0.0:
            rgba[r, c] = [0.94, 0.91, 0.88, 0.0]   # transparent (background shows)
        else:
            rgba[r, c] = [0.85, 0.68, 0.35, 0.55]  # amber, semi-transparent

ax.imshow(rgba, interpolation='nearest', aspect='auto',
          extent=[0, width, height, 0])

# Draw a faint border around the gap
rect = patches.Rectangle((gap_c0, gap_r0),
                           gap_c1 - gap_c0, gap_r1 - gap_r0,
                           linewidth=0.7, edgecolor='#b08040',
                           facecolor='none', linestyle='--')
ax.add_patch(rect)

ax.axis('off')
fig.patch.set_facecolor('#f0ece4')
plt.tight_layout(pad=0.3)
plt.savefig('assets/rule90-gap.png', dpi=160, bbox_inches='tight',
            facecolor='#f0ece4')
plt.close()
print("done")
