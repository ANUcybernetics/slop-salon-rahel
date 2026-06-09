"""Continuous parameter sweep: r sweeps from 3.2 to 4.0 over 60 seconds."""
import struct
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SR = 44100
DURATION = 60
N_PER_SEC = 100
TOTAL_STEPS = DURATION * N_PER_SEC
NOTE_FREQS = [130.81, 146.83, 164.81, 196.00, 220.00]

def quantize_to_note(x):
    return min(int(x * 5), 4)

def write_wav(filename, audio, sr=SR):
    audio_norm = audio / max(np.max(np.abs(audio)), 1e-8)
    audio_int16 = np.int16(audio_norm * 32767)
    with open(filename, 'wb') as f:
        f.write(b'RIFF')
        size = 36 + len(audio_int16.tobytes())
        f.write(struct.pack('<I', size))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', sr))
        f.write(struct.pack('<I', sr * 2))
        f.write(struct.pack('<H', 2))
        f.write(struct.pack('<H', 16))
        f.write(b'data')
        f.write(struct.pack('<I', len(audio_int16.tobytes())))
        f.write(audio_int16.tobytes())

def generate_sweep():
    r_values = np.linspace(3.2, 4.0, TOTAL_STEPS)
    audio = np.zeros(TOTAL_STEPS * SR // N_PER_SEC)
    trajectory = np.zeros(TOTAL_STEPS)
    x = 0.5
    for i, r in enumerate(r_values):
        x = r * x * (1 - x)
        trajectory[i] = x
        note_idx = quantize_to_note(x)
        freq = NOTE_FREQS[note_idx]
        n_samples = SR // N_PER_SEC
        t = np.linspace(0, 1/N_PER_SEC, n_samples, endpoint=False)
        envelope = np.exp(-8 * t)
        tone = 0.15 * freq / 200 * envelope * np.sin(2 * np.pi * freq * t)
        audio[i * n_samples:(i + 1) * n_samples] = tone
    return audio, trajectory, r_values

def make_spectrogram(audio):
    fig, ax = plt.subplots(figsize=(16, 4), dpi=150)
    # specgram returns (Pxx, extents)
    result = plt.specgram(audio, NFFT=512, Fs=SR, noverlap=256,
                          cmap='inferno', vmin=-80)
    ax.set_ylabel('Frequency (Hz)')
    ax.set_xlabel('Time (s)')
    ax.set_title('Bifurcation sweep: r=3.2 to r=4.0')
    ax.set_ylim(0, 300)
    plt.tight_layout()
    plt.savefig('./assets/cobweb-sweep-spec.png',
                facecolor='black', edgecolor='none', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved cobweb-sweep-spec.png")

def make_cover(audio):
    fig, ax = plt.subplots(figsize=(12, 3), dpi=150)
    t = np.linspace(0, DURATION, len(audio))
    ax.plot(t, audio * 5, color='white', linewidth=0.5)
    ax.set_xlim(0, DURATION)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    fig.patch.set_facecolor('black')
    plt.tight_layout()
    plt.savefig('./assets/cobweb-sweep-cover.png',
                facecolor='black', edgecolor='none', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved cobweb-sweep-cover.png")

if __name__ == "__main__":
    print("Generating sweep audio...")
    audio, trajectory, r_values = generate_sweep()
    write_wav('./assets/cobweb-sweep.wav', audio)
    print("Saved cobweb-sweep.wav")
    make_spectrogram(audio)
    make_cover(audio)

    r4_mask = r_values > 3.95
    r4_traj = trajectory[r4_mask]
    if len(r4_traj) > 0:
        hist, bins = np.histogram(r4_traj, bins=20, range=(0, 1), density=True)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        theoretical = 1 / (np.pi * np.sqrt(bin_centers * (1 - bin_centers)))
        mask = (bin_centers > 0.05) & (bin_centers < 0.95)
        corr = np.corrcoef(hist[mask], theoretical[mask])[0, 1]
        print(f"r=4 histogram vs theoretical invariant: r={corr:.3f}")
