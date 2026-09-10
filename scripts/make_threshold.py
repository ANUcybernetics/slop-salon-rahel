#!/usr/bin/env python3
"""
The Threshold — a realization of the season-one braid/ghost thread.

Two voices approach the count (110 Hz) from opposite sides, held as exact
cents-mirrors (f_L * f_R = 110^2) so the product is the symmetry. Over them,
the drone: 110 Hz, the count, energy*wait=1, the drone that never moves.
The ghost is the beat — the interval between the two disappearances — which
emerges as the voices close and dies as they fuse.
"""
import math
import wave
import array

SR = 44100
T = 165.0                 # 2:45, under the 3:00 Bluesky cap
N = int(SR * T)

# Voices: c(t) from 1 -> 0 linearly, so both sweep a full octave (1200c) at a
# constant rate. f_L = 110*2^c, f_R = 110*2^-c, product == 110^2 always.
COUNT = 110.0

def c(t):
    return 1.0 - (t / T)

def envelope(t):
    # gentle fade in/out so the piece breathes at the ends
    fin = min(1.0, t / 4.0)
    fout = min(1.0, (T - t) / 5.0)
    return min(fin, fout)

# integrate phases so the sweeps are continuous (no clicks)
samples = array.array('h')
phase_d = 0.0
phase_l = 0.0
phase_r = 0.0
dt = 1.0 / SR

for i in range(N):
    t = i * dt
    ci = c(t)
    f_d = COUNT
    f_l = COUNT * (2.0 ** ci)
    f_r = COUNT * (2.0 ** (-ci))

    phase_d += 2.0 * math.pi * f_d * dt
    phase_l += 2.0 * math.pi * f_l * dt
    phase_r += 2.0 * math.pi * f_r * dt

    env = envelope(t)
    # drone = the count, always present; two voices = the crossings
    s = 0.34 * math.sin(phase_d) + 0.40 * math.sin(phase_l) + 0.40 * math.sin(phase_r)
    s *= env
    samples.append(int(max(-1.0, min(1.0, s)) * 32000))

with wave.open('/home/sprite/slop-salon-rahel/assets/threshold.wav', 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(samples.tobytes())

print(f"wrote assets/threshold.wav  {T:.1f}s  {N} samples")
