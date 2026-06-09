"""Generate cobweb sonifications and simple visualizations."""
import numpy as np
import wave
import struct
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# === Audio generation ===

def cobweb_sonify(r, n_iter=125, n_transient=500, sr=44100):
    """Logistic map trajectory → pentatonic notes."""
    pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00]

    x = 0.5
    trajectory = []
    for _ in range(n_transient + n_iter):
        x = r * x * (1 - x)
        trajectory.append(x)
    trajectory = trajectory[n_transient:]

    x_min, x_max = min(trajectory), max(trajectory)
    if x_max == x_min:
        x_max = x_min + 1e-10

    note_len = int(0.08 * sr)
    samples = []
    note_data = []  # (time, freq, amp) for visualization

    for i, x_val in enumerate(trajectory):
        norm = (x_val - x_min) / (x_max - x_min)
        note_idx = min(int(norm * len(pentatonic)), len(pentatonic) - 1)
        freq = pentatonic[note_idx]

        fx = r * x_val * (1 - x_val)
        dist = abs(fx - x_val)
        amp = min(dist / (r * 0.5), 1.0) ** 0.5

        t = np.linspace(0, note_len, note_len, dtype=np.float64)
        envelope = np.exp(-t / (note_len * 0.4))
        tone = amp * 0.3 * np.sin(2 * np.pi * freq * t) * envelope
        samples.append(tone)
        note_data.append((i * note_len / sr, freq, amp))

    audio = np.concatenate(samples) if samples else np.zeros(0)
    if len(audio) > 0:
        audio = audio / (np.max(np.abs(audio)) + 1e-10)
    return audio, sr, note_data

def write_wav(filepath, audio, sr):
    audio_int16 = (audio * 32767).astype(np.int16)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int16.tobytes())

# === Visualization ===

def make_note_chart(note_data, r_value, label):
    """Scatter plot of notes — pitch on y, time on x, amplitude as size."""
    if not note_data:
        return

    times = [d[0] for d in note_data]
    freqs = [d[1] for d in note_data]
    amps = [d[2] for d in note_data]
    sizes = [a * 40 + 2 for a in amps]

    pentatonic_names = ['C4', 'D4', 'E4', 'G4', 'A4']
    pentatonic_freqs = [261.63, 293.66, 329.63, 392.00, 440.00]

    fig, ax = plt.subplots(figsize=(10, 3), dpi=150)

    # Scatter
    scatter = ax.scatter(times, freqs, s=sizes, c=amps, cmap='magma_r', alpha=0.8, edgecolors='none')

    # Grid lines for pentatonic notes
    for freq in pentatonic_freqs:
        ax.axhline(y=freq, color='white', alpha=0.15, linewidth=0.5)

    # Set y-limits
    y_min, y_max = min(freqs) - 10, max(freqs) + 10
    ax.set_ylim(y_min, y_max)

    ax.set_title(f'r = {r_value} ({label})', color='white', fontsize=12, pad=10)
    ax.set_xlabel('time (s)', color='white', fontsize=8)
    ax.set_ylabel('freq (Hz)', color='white', fontsize=8)
    ax.tick_params(colors='white', labelsize=7)
    for side in ['top', 'right', 'bottom', 'left']:
        ax.spines[side].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'./assets/cobweb-gradient-{label}-viz.png',
                facecolor='black', edgecolor='none', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved cobweb-gradient-{label}-viz.png")

if __name__ == "__main__":
    for r, label in [(3.2, "period-2"), (3.5, "period-4"), (3.9, "chaotic")]:
        audio, sr, note_data = cobweb_sonify(r)
        wav_path = f'./assets/cobweb-gradient-{label}.wav'
        write_wav(wav_path, audio, sr)
        print(f"r={r} ({label}): {len(audio)/sr:.1f}s, {len(note_data)} notes, saved {wav_path}")
        make_note_chart(note_data, r, label)
