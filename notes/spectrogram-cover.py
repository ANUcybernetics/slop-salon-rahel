"""Generate a simple spectrogram image for the phase boundary audio cover."""
import math
import random
import os

random.seed(123)
W, H = 1080, 1080
OUTPUT = "assets/phase-boundary-cover.png"

# Simple PPM with compression, then convert to PNG via ImageMagick
# Actually, just write PPM
out = open("/tmp/cover.ppm", "wb")
out.write(b"P6\n")
out.write(f"{W} {H}\n255\n".encode())

pixels = bytearray()
for y in range(H):
    for x in range(W):
        # Spectrogram-like: diagonal structure
        # Ordered region (left) -> phase boundary (diagonal) -> noise (right)
        nx = x / W
        ny = y / H

        # Frequency axis (top = high, bottom = low)
        freq = ny * 500  # Hz

        # Distance from diagonal
        dist_to_diag = abs(nx - (1 - ny))

        # Ordered: clean harmonics at specific frequencies
        harmonics = [220, 330, 440, 660, 880]
        harmonics_norm = [h / 1000.0 for h in harmonics]
        freq_norm = freq / 1000.0

        order = 1.0 if nx < 0.3 else max(0, 0.3 / nx)

        sample = 0
        for h in harmonics_norm:
            if abs(freq_norm - h) < 0.05 * order:
                sample += order * 255 * (1 - abs(freq_norm - h) / (0.05 * order))

        # Phase boundary: rainbow interference
        if 0.3 < nx < 0.65:
            interference = math.sin((nx - 0.3) * 50) * math.sin((1 - ny) * 30)
            interference *= 0.5 * max(0, 1 - (nx - 0.3) / 0.35)
            sample += abs(interference) * 200

        # Noise region (right)
        if nx > 0.65:
            noise_val = random.random() * 80 * (nx - 0.65) / 0.35
            sample += noise_val

        # Bright background for ordered, dark for noise
        bg = 20 if order < 0.5 else 5 + 30 * (1 - order) * (1 - ny)
        r = min(255, int(sample * 0.6 + bg * 0.3))
        g = min(255, int(sample * 0.3 + bg * 0.2))
        b = min(255, int(sample * 0.8 + bg * 0.5))

        pixels.extend(bytes([r, g, b]))

out.write(pixels)
out.close()

os.system(f"convert /tmp/cover.ppm {OUTPUT} 2>&1")
print(f"Cover: {OUTPUT} ({os.path.getsize(OUTPUT)} bytes)")
