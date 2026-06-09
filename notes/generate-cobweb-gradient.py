"""Generate cobweb sonification across parameter space — r=3.2 (period-2), r=3.5 (period-4), r=3.9 (chaotic)."""
import numpy as np
import wave
import struct

def cobweb_sonify(r, n_iter=125, n_transient=500, sr=44100):
    """Logistic map trajectory → pentatonic notes.

    C major pentatonic: C4(261.63), D4(293.66), E4(329.63), G4(392.00), A4(440.00)
    Trajectory x → normalized position → note index
    Distance from diagonal → amplitude
    """
    # C major pentatonic frequencies
    pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00]

    # Generate trajectory
    x = 0.5
    trajectory = []
    for _ in range(n_transient + n_iter):
        x = r * x * (1 - x)
        trajectory.append(x)

    trajectory = trajectory[n_transient:]

    # Normalize to [0, 1] → note index
    x_min, x_max = min(trajectory), max(trajectory)
    if x_max == x_min:
        x_max = x_min + 1e-10

    samples = []
    note_len = int(0.08 * sr)  # 80ms per note

    for x_val in trajectory:
        # Normalize
        norm = (x_val - x_min) / (x_max - x_min)
        note_idx = int(norm * len(pentatonic))
        note_idx = min(note_idx, len(pentatonic) - 1)
        freq = pentatonic[note_idx]

        # Distance from diagonal
        fx = r * x_val * (1 - x_val)
        dist_from_diag = abs(fx - x_val)
        amp = min(dist_from_diag / (r * 0.5), 1.0)
        amp = amp ** 0.5  # soften the dynamic range

        # Generate tone with exponential decay
        t = np.linspace(0, note_len, note_len, dtype=np.float64)
        envelope = np.exp(-t / (note_len * 0.4))
        tone = amp * 0.3 * np.sin(2 * np.pi * freq * t) * envelope

        samples.append(tone)

    # Concatenate
    audio = np.concatenate(samples) if samples else np.zeros(0)

    # Normalize
    if len(audio) > 0:
        audio = audio / (np.max(np.abs(audio)) + 1e-10)

    return audio, sr

def write_wav(filepath, audio, sr):
    """Write audio as 16-bit PCM WAV."""
    audio_int16 = (audio * 32767).astype(np.int16)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int16.tobytes())

if __name__ == "__main__":
    for r, label in [(3.2, "period-2"), (3.5, "period-4"), (3.9, "chaotic")]:
        audio, sr = cobweb_sonify(r)
        path = f"./assets/cobweb-gradient-{label}.wav"
        write_wav(path, audio, sr)
        print(f"r={r} ({label}): {len(audio)/sr:.1f}s, saved to {path}")
