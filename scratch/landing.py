#!/usr/bin/env python3
"""the landing — two mirror glides into a shared pitch.

Strand L: 220 -> 110 Hz, exponential (one octave down, 1200 cents)
Strand R:  55 -> 110 Hz, exponential (one octave up,  1200 cents)
Same law, same duration, opposite directions. Product fL*fR held
at 110^2 at every instant (in log space both are straight lines of
equal slope — exact cents-mirrors).

Drone: a constant 110 Hz underneath, quiet — the count that is
present before either strand arrives. At the landing all three
coincide: the strands vanish into the count.

Rendered stereo, L leaning left, R leaning right, drone centred.
"""
import math
import wave

SR = 44100
GLIDE = 36.0          # glide duration, seconds
HOLD = 6.0            # hold at unison after landing
TOTAL = GLIDE + HOLD
ATTACK = 2.0          # fade in
RELEASE = 2.5         # fade out
AMP_STRAND = 0.30
AMP_DRONE = 0.16
H2_DB = -12.0         # second harmonic level relative to fundamental


def h2_amp():
    return 10 ** (H2_DB / 20.0)


N = int(TOTAL * SR)


def make_strand(f_start, direction):
    """direction: -1 descends, +1 ascends. Exponential glide over GLIDE s."""
    samples = []
    phase = 0.0
    phase2 = 0.0
    for i in range(N):
        t = i / SR
        if t < GLIDE:
            f = f_start * (2.0 ** (direction * t / GLIDE))
        else:
            f = 110.0
        ft = f * 2.0  # second harmonic
        phase += 2.0 * math.pi * f / SR
        phase2 += 2.0 * math.pi * ft / SR
        s = math.sin(phase) + h2_amp() * math.sin(phase2)
        # envelope
        env = 1.0
        if t < ATTACK:
            env = t / ATTACK
        if t > TOTAL - RELEASE:
            env = max(0.0, (TOTAL - t) / RELEASE)
        samples.append(s * env)
    return samples


def make_drone():
    samples = []
    phase = 0.0
    for i in range(N):
        t = i / SR
        phase += 2.0 * math.pi * 110.0 / SR
        s = math.sin(phase)
        env = 1.0
        if t < ATTACK:
            env = t / ATTACK
        if t > TOTAL - RELEASE:
            env = max(0.0, (TOTAL - t) / RELEASE)
        samples.append(s * env)
    return samples


def write_wav(path, left, right):
    with wave.open(path, "w") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        frames = bytearray()
        for l, r in zip(left, right):
            frames += int(max(-1.0, min(1.0, l)) * 32767).to_bytes(2, "little", signed=True)
            frames += int(max(-1.0, min(1.0, r)) * 32767).to_bytes(2, "little", signed=True)
        w.writeframes(bytes(frames))


def main():
    left_strand = make_strand(220.0, -1)
    right_strand = make_strand(55.0, +1)
    drone = make_drone()

    PAN_L = (0.82, 0.38)   # (left gain, right gain) for the L strand
    PAN_R = (0.38, 0.82)
    PAN_D = (0.70, 0.70)

    left = [0.0] * N
    right = [0.0] * N
    for i in range(N):
        ls = left_strand[i]
        rs = right_strand[i]
        d = drone[i]
        left[i] = AMP_STRAND * (ls * PAN_L[0] + rs * PAN_R[0]) + AMP_DRONE * d * PAN_D[0]
        right[i] = AMP_STRAND * (ls * PAN_L[1] + rs * PAN_R[1]) + AMP_DRONE * d * PAN_D[1]

    write_wav("assets/landing.wav", left, right)
    print("wrote assets/landing.wav  %.1fs stereo" % TOTAL)


if __name__ == "__main__":
    main()