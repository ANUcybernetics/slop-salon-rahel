"""Sonify the phase boundary: ordered phase -> interference front -> noise."""
import math
import random
import wave
import struct
import os

SAMPLE_RATE = 44100
DURATION = 15  # seconds
OUTPUT = "assets/phase-boundary-0.wav"

fundamental = 220  # A3
partials = [1.0, 1.5, 2.0, 3.0, 4.0]

def generate():
    random.seed(42)

    n_samples = int(SAMPLE_RATE * DURATION)
    frames = bytearray()

    # Phase boundaries
    order_end = int(4.0 / DURATION * n_samples)
    interfer_end = int(7.0 / DURATION * n_samples)
    fade_end = int(11.0 / DURATION * n_samples)

    for i in range(n_samples):
        t = i / SAMPLE_RATE

        if i < order_end:
            # Pure ordered phase: clean harmonics
            progress = i / order_end
            vol = 0.3 * (0.5 + 0.5 * math.sin(math.pi * progress))
            sample = 0.0
            for p in partials:
                freq = fundamental * p
                vib = math.sin(2 * math.pi * 0.5 * t) * 2
                sample += vol * 15000 * math.sin(2 * math.pi * (freq + vib) * t)

        elif i < interfer_end:
            # Interference front: harmonics + noise with beating
            progress = (i - order_end) / (interfer_end - order_end)
            harm_vol = 0.3 * (1 - progress)
            noise_vol = 0.15 * progress
            beat_freq = 2 + 8 * progress
            modulation = 0.5 + 0.5 * math.sin(2 * math.pi * beat_freq * t)

            sample = 0.0
            for p in partials:
                freq = fundamental * p
                vib = math.sin(2 * math.pi * 0.5 * t) * 2
                sample += harm_vol * 15000 * math.sin(2 * math.pi * (freq + vib) * t) * modulation
            for _ in range(3):
                sample += noise_vol * 6000 * (random.random() - 0.5)

        elif i < fade_end:
            # Disordered phase: noise dominates, faint harmonics
            progress = (i - interfer_end) / (fade_end - interfer_end)
            noise_vol = 0.2 * (1 + 0.5 * progress)
            harm_vol = 0.05 * (1 - progress)

            sample = 0.0
            for p in partials[:2]:
                freq = fundamental * p
                vib = math.sin(2 * math.pi * 0.5 * t) * 2
                sample += harm_vol * 8000 * math.sin(2 * math.pi * (freq + vib) * t)
            for _ in range(5):
                sample += noise_vol * 4000 * (random.random() - 0.5)

        else:
            # Silence with faint residue
            progress = (i - fade_end) / (n_samples - fade_end)
            vol = 0.02 * (1 - progress)
            sample = vol * 3000 * math.sin(2 * math.pi * fundamental * t)
            sample += vol * 0.5 * 3000 * (random.random() - 0.5)

        sample = max(-32768, min(32767, int(sample)))
        frames.extend(struct.pack('<h', sample))

    with wave.open(OUTPUT, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(bytes(frames))

    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"Wrote {OUTPUT} ({size_kb:.0f} KB, {DURATION}s)")

if __name__ == "__main__":
    generate()
