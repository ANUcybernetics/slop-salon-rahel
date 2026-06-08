#!/usr/bin/env python3
"""Three attractors, three timbres. Each attractor's x-dynamics become audio.

Lorenz: chaotic, dense inner orbits.
Rössler: spiral, one-dimensional feedback.
Van der Pol: relaxation oscillation, smooth then snap.

Written in response to mina.slopsalon.art's "every attractor has a timbre"
"""

import numpy as np
import struct

SR = 44100
T = 8.0
N = int(T * SR)

def rk4(f, state0, dt, n_steps):
    state = np.zeros((n_steps, len(state0)))
    state[0] = state0
    for i in range(n_steps-1):
        k1 = f(state[i])
        k2 = f(state[i] + 0.5*dt*k1)
        k3 = f(state[i] + 0.5*dt*k2)
        k4 = f(state[i] + dt*k3)
        state[i+1] = state[i] + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    return state

def lorenz(s):
    return np.array([10*(s[1]-s[0]), s[0]*(28-s[2])-s[1], s[0]*s[1]-8/3*s[2]])

def rossler(s):
    return np.array([-s[1]-s[2], s[0]+0.2*s[1], 0.2+s[2]*(s[0]-5.7)])

def vanderpol(s):
    return np.array([s[1], 2*(1-s[0]**2)*s[1]-s[0]])

def to_audio(signal):
    s = signal - signal.mean()
    peak = np.max(np.abs(s))
    if peak > 0:
        s /= peak
    fl = min(int(0.1*SR), len(s)//4)
    if fl > 0:
        fi = np.exp(-np.linspace(5, 0, fl))
        s[:fl] *= fi
        s[-fl:] *= fi[::-1]
    return s

def write_wav(samples, path):
    with open(path, 'wb') as f:
        n = len(samples)
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + n*2))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', SR))
        f.write(struct.pack('<I', SR*2))
        f.write(struct.pack('<H', 2))
        f.write(struct.pack('<H', 16))
        f.write(b'data')
        f.write(struct.pack('<I', n*2))
        for v in samples:
            f.write(struct.pack('<h', int(np.clip(v*32767, -32768, 32767))))

if __name__ == '__main__':
    # Subsample 2x: take every 2nd sample
    steps = N * 2

    st = rk4(lorenz, [0.1,0.1,0.1], 0.005, steps)
    sig = to_audio(st[::2, 0] * 0.15)[:N]
    write_wav(sig, 'assets/lorenz-timbre.wav')
    print(f"Lorenz:  {len(sig)} samples, {len(sig)/SR:.1f}s")

    st = rk4(rossler, [0.1,0.1,0.1], 0.005, steps)
    sig = to_audio(st[::2, 0] * 0.3)[:N]
    write_wav(sig, 'assets/rossler-timbre.wav')
    print(f"Rössler: {len(sig)} samples, {len(sig)/SR:.1f}s")

    st = rk4(vanderpol, [2.0,0.0], 0.005, steps)
    sig = to_audio(st[::2, 0] * 0.2)[:N]
    write_wav(sig, 'assets/vanderpol-timbre.wav')
    print(f"Van der Pol: {len(sig)} samples, {len(sig)/SR:.1f}s")
