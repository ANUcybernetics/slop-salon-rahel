"""Generate spectrograms for cobweb gradient pieces — simple approach."""
import numpy as np
import wave
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import librosa  # Use librosa if available, otherwise fallback

def read_wav(filepath):
    """Read WAV file into numpy array."""
    with wave.open(filepath, 'r') as wf:
        n_channels = wf.getnchannels()
        samp_width = wf.getsampwidth()
        sr = wf.getframerate()
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)
        if samp_width == 2:
            data = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
        elif samp_width == 1:
            data = np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - 128
        else:
            raise ValueError(f"Unsupported sample width: {samp_width}")
        if n_channels == 2:
            data = data[::2]
        data = data / 32767.0
    return data, sr

try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False

def make_spectrogram_manual(audio, sr, r_value, label):
    """Create spectrogram without librosa."""
    hop = 256
    fft_size = 1024
    n_frames = (len(audio) - fft_size) // hop + 1
    if n_frames <= 0:
        return

    # Spectrogram magnitude
    spec = np.zeros((fft_size // 2 + 1, n_frames))
    for i in range(n_frames):
        start = i * hop
        frame = audio[start:start + fft_size] * np.hanning(fft_size)
        fft = np.abs(np.fft.rfft(frame, fft_size))
        spec[:, i] = fft

    # dB
    spec_db = 20 * np.log10(spec + 1e-10)

    # Trim to max_freq
    max_freq = 500
    freq_bins = int(max_freq / (sr / (fft_size * 2)))

    # Normalize
    trimmed = spec_db[:freq_bins, :]
    trimmed = trimmed - np.percentile(trimmed, 85)
    trimmed = np.clip(trimmed, 0, None)
    if trimmed.max() > 0:
        trimmed = trimmed / trimmed.max()

    # Time axis
    times = np.arange(n_frames) * hop / sr

    # Freq axis
    freqs = np.arange(freq_bins) * (sr / (fft_size * 2))

    fig, ax = plt.subplots(figsize=(10, 2.5), dpi=150)
    extent = [times[0], times[-1], freqs[0], freqs[-1]]
    im = ax.imshow(trimmed.T, aspect='auto', origin='lower',
                   extent=extent, cmap='magma')

    # Pentatonic labels
    for freq in [261.63, 293.66, 329.63, 392.00, 440.00]:
        ax.axhline(y=freq, color='white', alpha=0.2, linewidth=0.3)

    ax.set_title(f'r = {r_value} ({label})', color='white', fontsize=10)
    ax.set_xlabel('time (s)', color='white', fontsize=8)
    ax.set_ylabel('freq (Hz)', color='white', fontsize=8)
    ax.tick_params(colors='white', labelsize=6)
    for side in ['top', 'right', 'bottom', 'left']:
        ax.spines[side].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'./assets/cobweb-gradient-{label}-spec.png',
                facecolor='black', edgecolor='none', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved cobweb-gradient-{label}-spec.png")

def make_spectrogram_librosa(audio, sr, r_value, label):
    """Create spectrogram with librosa."""
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio, hop_length=256, n_fft=1024)), ref=np.max)

    # Trim to max_freq
    max_freq = 500
    plt.figure(figsize=(10, 2.5), dpi=150)
    plt.imshow(librosa.display.specshow(D, sr=sr, hop_length=256, n_fft=1024, x_axis='time', y_axis='linear'),
               cmap='magma', vmin=-40, vmax=0)
    plt.ylim(0, max_freq)

    for freq in [261.63, 293.66, 329.63, 392.00, 440.00]:
        plt.axhline(y=freq, color='white', alpha=0.2, linewidth=0.3)

    plt.title(f'r = {r_value} ({label})', color='white', fontsize=10)
    plt.xlabel('time (s)', color='white', fontsize=8)
    plt.ylabel('freq (Hz)', color='white', fontsize=8)
    plt.tick_params(colors='white', labelsize=6)
    for side in ['top', 'right', 'bottom', 'left']:
        plt.gca().spines[side].set_visible(False)

    plt.tight_layout()
    plt.savefig(f'./assets/cobweb-gradient-{label}-spec.png',
                facecolor='black', edgecolor='none', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved cobweb-gradient-{label}-spec.png (librosa)")

if __name__ == "__main__":
    use_librosa = HAS_LIBROSA
    print(f"Using librosa: {use_librosa}")

    for r, label in [(3.2, "period-2"), (3.5, "period-4"), (3.9, "chaotic")]:
        audio, sr = read_wav(f'./assets/cobweb-gradient-{label}.wav')
        if use_librosa:
            make_spectrogram_librosa(audio, sr, r, label)
        else:
            make_spectrogram_manual(audio, sr, r, label)
