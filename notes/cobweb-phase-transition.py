#!/usr/bin/env python3
"""Sonify cobweb trajectory data from the logistic map at three r values."""

import numpy as np
from scipy.io import wavfile

SAMPLE_RATE = 44100
TONE_DURATION = 0.100  # 100ms per tone
ATTACK = 0.005          # 5ms fast attack
DECAY = 0.080           # 80ms decay
GAPS = 2.0              # 2-second silence between tracks

# C major pentatonic frequencies
FREQUENCIES = [
    130.81,   # C3
    146.83,   # D3
    164.81,   # E3
    196.00,   # G3
    220.00,   # A3
    261.63,   # C4
    293.66,   # D4
    329.63,   # E4
    392.00,   # G4
    440.00,   # A4
]

R_VALUES = [
    (3.2, "r32", 2),
    (3.5, "r35", 4),
    (3.9, "r39", "chaotic"),
]


def logistic_trajectory(r, n_transient=500, n_steps=2000, x0=0.5):
    """Generate logistic map trajectory, discarding transients."""
    x = x0
    traj = []
    for _ in range(n_transient):
        x = r * x * (1 - x)
    for _ in range(n_steps):
        x = r * x * (1 - x)
        traj.append(x)
    return np.array(traj)


def generate_audio(r_val, label):
    """Generate WAV audio from cobweb trajectory at given r value."""
    traj = logistic_trajectory(r_val)
    # Map all trajectory values to frequency indices at once
    indices = (np.clip(traj, 0, 1) * (len(FREQUENCIES) - 0.001)).astype(int)
    freq_array = np.array([FREQUENCIES[i] for i in indices])
    n_steps = len(freq_array)
    samples_per_tone = int(SAMPLE_RATE * TONE_DURATION)
    # Time array for one tone
    t = np.arange(samples_per_tone) / SAMPLE_RATE
    # Precompute envelope (same for every tone)
    envelope = np.ones(samples_per_tone, dtype=np.float64)
    attack_samples = int(ATTACK * SAMPLE_RATE)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    decay_samples = int(DECAY * SAMPLE_RATE)
    decay_start = samples_per_tone - decay_samples
    envelope[decay_start:] *= np.linspace(1, 0.01, decay_samples)
    # Vectorized: build a (n_steps, samples_per_tone) matrix of sin waves
    # freq_array[:, None] * t[None, :] gives the right shape for broadcasting
    phase = 2.0 * np.pi * freq_array[:, np.newaxis] * t[np.newaxis, :]
    all_sins = np.sin(phase)  # shape: (n_steps, samples_per_tone)
    # Apply envelope and flatten
    result = (all_sins * envelope[np.newaxis, :]).ravel()
    return result.astype(np.float32)


def combine_with_gaps(wav_files):
    """Combine multiple WAV files with silence gaps between them."""
    tracks = []
    sample_rate = None
    for path in wav_files:
        sr, data = wavfile.read(path)
        if sample_rate is None:
            sample_rate = sr
        tracks.append(data)
        # Add gap (except after last track)
        if path != wav_files[-1]:
            gap = np.zeros(int(GAPS * SAMPLE_RATE), dtype=data.dtype)
            tracks.append(gap)
    combined = np.concatenate(tracks)
    return sample_rate, combined


def main():
    import os
    os.makedirs("assets", exist_ok=True)

    wav_files = []
    for r_val, label, behavior in R_VALUES:
        print(f"Generating cobweb-r{label} (r={r_val}, {behavior})...")
        audio = generate_audio(r_val, label)
        wav_path = f"assets/cobweb-{label}.wav"
        wavfile.write(wav_path, SAMPLE_RATE,
                      (audio * 32767).astype(np.int16))
        duration = len(audio) / SAMPLE_RATE
        print(f"  -> {wav_path}  ({duration:.1f}s)")
        wav_files.append(wav_path)

    # Combine into one multi-track file
    print("Combining into single track with gaps...")
    sr, combined = combine_with_gaps(wav_files)
    out_path = "assets/cobweb-all.wav"
    wavfile.write(out_path, sr, (combined * 32767).astype(np.int16))
    print(f"  -> {out_path}  ({len(combined)/SAMPLE_RATE:.1f}s)")


if __name__ == "__main__":
    main()
