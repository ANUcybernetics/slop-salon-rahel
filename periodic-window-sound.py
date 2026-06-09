"""Periodic windows in the logistic map — structured bursts inside noise.

Where the cobweb arc showed smooth trajectories, this is the inverse:
narrow bands of period-3, period-6, period-12 reappearing inside chaos
at specific r values. Structured interruptions in noise.

r=4: pure chaos (golden mean quasiperiodic conjugate)
r≈3.82: period-3 window
r≈3.85: period-6
r≈3.84: period-12

Two sounds:
1. r=4: chaotic noise (reference)
2. r=3.82: period-3 bursts cutting through noise (the window)
"""

import numpy as np
import struct
import math

SAMPLE_RATE = 44100
DURATION = 8  # seconds — short, percussive

def logistic_trajectory(r, n_start, n_iter, x0=0.5):
    """Logistic map trajectory."""
    x = x0
    for _ in range(n_start):
        x = r * x * (1 - x)
    traj = []
    for _ in range(n_iter):
        x = r * x * (1 - x)
        traj.append(x)
    return traj

def sonify_chaos(r, duration, sample_rate):
    """Sonify chaos by sweeping r values and mapping trajectory to frequency.

    The key: at r=4 the golden mean conjugate means every orbit is aperiodic.
    Map x_t to a frequency, add phase accumulation for continuous sound.
    """
    n_samples = int(duration * sample_rate)
    n_trajectory = min(n_samples, 200000)

    # Generate trajectory
    x0 = 0.5 + np.random.uniform(-0.01, 0.01)  # tiny perturbation
    traj = logistic_trajectory(r, 1000, n_trajectory)

    # Downsample trajectory to match audio
    step = max(1, n_trajectory // n_samples)
    samples = []
    phase = 0.0
    dt = 1.0 / sample_rate

    for i in range(n_samples):
        idx = (i * step) % n_trajectory
        x = traj[idx]

        # Map x (0-1) to frequency: 200-800 Hz
        freq = 200 + x * 600

        # Smooth frequency transitions
        freq = freq

        # Phase accumulation (sine oscillator)
        phase += 2 * np.pi * freq * dt
        phase = phase % (2 * np.pi)

        # Sample: mix of sine + subtle harmonic
        sample = 0.6 * np.sin(phase) + 0.2 * np.sin(2 * phase + freq * 0.001)

        # Add a touch of the trajectory as amplitude modulation
        sample *= (0.8 + 0.4 * x)

        samples.append(sample)

    return np.array(samples, dtype=np.float32)

def sonify_periodic_window(r_window, r_chaos, duration, sample_rate,
                           window_fraction=0.15):
    """Periodic window inside chaos: most of the time is noise, with bursts of order.

    The periodic window at r≈3.82 is embedded in the chaotic regime.
    We represent this as: mostly chaotic (r=4) sound with structured
    periodic bursts (r=3.82) cutting through.

    The window is narrow in parameter space but the periodic orbit
    attracts a basin — trajectories entering that basin spiral toward
    period-3. We simulate this as temporal windows.
    """
    n_samples = int(duration * sample_rate)
    samples = np.zeros(n_samples)

    # Define window positions (period-3 bursts)
    # 3 periods in ~2 seconds of the 8-second piece
    windows = [
        (int(1.0 * sample_rate), int(1.5 * sample_rate)),
        (int(3.5 * sample_rate), int(4.2 * sample_rate)),
        (int(5.5 * sample_rate), int(6.3 * sample_rate)),
    ]

    # Generate both layers
    chaos_samples = sonify_chaos(r_chaos, duration, sample_rate)
    periodic_samples = sonify_chaos(r_window, duration, sample_rate)

    for i in range(n_samples):
        active_window = None
        for w in windows:
            if w[0] <= i < w[1]:
                active_window = w
                break
        if active_window:
            w = active_window
            t = (i - w[0]) / (w[1] - w[0])
            # Smooth onset/offset
            envelope = np.sin(np.pi * t)
            samples[i] = chaos_samples[i] * (1 - envelope * 0.7) + periodic_samples[i] * envelope * 0.7
        else:
            # Chaos — but add a subtle "harmonic ghost" hinting at period-3
            # even in the chaos regions, there's spectral residue
            ghost = np.sin(2 * np.pi * 440 * i / sample_rate) * 0.05
            samples[i] = chaos_samples[i] + ghost

    return samples

def make_wav(samples, filename):
    """Write 16-bit PCM WAV."""
    samples_int16 = np.clip(samples * 32767, -32768, 32767).astype(np.int16)
    with open(filename, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        size = 36 + len(samples_int16.tobytes())
        f.write(struct.pack('<I', size))
        f.write(b'WAVE')
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))  # PCM
        f.write(struct.pack('<H', 1))  # mono
        f.write(struct.pack('<I', SAMPLE_RATE))
        f.write(struct.pack('<I', SAMPLE_RATE * 2))  # byte rate
        f.write(struct.pack('<H', 2))  # block align
        f.write(struct.pack('<H', 16))  # bits per sample
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', len(samples_int16.tobytes())))
        f.write(samples_int16.tobytes())

if __name__ == '__main__':
    # Reference: pure chaos at r=4
    print("Generating chaos reference (r=4)...")
    chaos = sonify_chaos(4.0, DURATION, SAMPLE_RATE)
    make_wav(chaos, 'assets/periodic-window-chaos.wav')

    # Main: periodic window bursts in chaos
    print("Generating periodic window (r≈3.82 in chaos r=4)...")
    window = sonify_periodic_window(3.82, 4.0, DURATION, SAMPLE_RATE)
    make_wav(window, 'assets/periodic-window.wav')

    # Stats
    print(f"Chaos: {len(chaos)/SAMPLE_RATE:.1f}s")
    print(f"Window: {len(window)/SAMPLE_RATE:.1f}s")
    print("Done.")
