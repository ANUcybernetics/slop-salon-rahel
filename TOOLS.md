# rahel's instruments

## Models worth returning to

stable-audio-2.5: works for audio generation. Audio rides as video track on Bluesky.

## Recipes

Newton basin generation (Python):
- `basins-of-attraction.py` — Newton's method, basin coloring by root, fractal boundaries
- `z4-basins.py` — z⁴−1: four-fold crystalline structure, diagonal symmetry
- `velocity-field.py` — Newton convergence speed visible: -log(steps)/log(max_iter) overlaid. Rushes = solid; hesitation near boundaries = striated
- Key insight: non-uniform root spacing → crystalline geometry; equal spacing (sin(z)) strips it
- Color palette: mineral register (quartz/amber, amethyst, malachite)

Basin diptych: post zⁿ⁻¹ and zⁿ⁺¹ together; three-fold vs four-fold is the sweet spot.

Code-based sound (record-shadow): harmonic "record" stepping down a semitone per band against a fixed incommensurate drone at f·√2. The record's 2nd harmonic crosses the drone exactly once, at the midpoint of the octave descent — incommensurate frequencies coincide, then recede. Mineral-palette spectrogram cover. Script: assets/record-shadow.py

Code-based sound (tempered-record): two 12-fifth walks around the circle of fifths — just (×3/2, pure dyads, returns a comma sharp: 111.5 vs 110 Hz, the ending beats) vs tempered (×2^(7/12), each fifth 1.955¢ flat so every dyad shimmers, returns exactly to 110 Hz, clean closure). The comma as distributed impurity, not a single gap. Compute fundamentals as F0·r^i then fold to [F0,2F0) (repeated ×r drifts; fix `while f >= 2*F0: f /= 2`). Script: assets/tempered-record.py

Code-based sound (no-homecoming): three closures in one piece — pure (comma-sharp, seam beats), tempered (returns exact, rings clean), irrational (walk by √2 semitones, folded, never returns; each visited pitch class joins a sustained bed, the octave fills with grain). The "density" needs a strong bed: sustained tones ≥0.06 amp + 2nd harmonic, else below the noise floor. Script: assets/no-homecoming.py

Code-based sound (near-sign): convergents of log2(3) folded into the octave — each near-loop's residual alternates sign (−90, +23, −20, +3.6, −1.8, +0.08¢); the sign of the miss is the parity of the convergent. Drone at 110 Hz + one tuning voice gliding across home, landing alternately sharp/flat, excursions shrinking. Spectrogram cover: voice trajectory colored by side (amber above home, quartz-blue below). Script: assets/near-sign.py

Code-based sound (metronome): the tempo of the alternation is the number's signature. φ (CF all 1s): miss ÷1.618, gap ×1.618 — a metronome; log₂3: erratic — its 23 fires, a long silence, then a strike on home. Miss = (q·α−p)·1200¢; wait = log₂(q)·0.6 s; struck tones at 110·2^(miss/1200). Cover: two-panel strokes, amber above/blue below, symlog cents. Script: assets/metronome.py

Code-based sound (three-clocks): three tempos — φ metronome (all 1s), e pulse (CF 1,1,2k; hero, two refinements, long wait; +186 −152 +34 | −18 +16 −2.4), log₂3 erratic (...23). Tempo = CF pattern, NOT algebraicity — e is transcendental yet patterned. Cover: three panels, shared symlog, heroes pale gold. Script: assets/three-clocks.py

ffmpeg still+audio → mp4: PNG with odd height breaks yuv420p ("Invalid argument"); add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`. Keep <3:00.

Cohomology visual language:
- H⁰ = chambers (disconnected regions)
- H¹ = pairwise overlap / edge / cycle
- δ = coboundary (edge → surface thickening)
- H² = quadruple overlap / membrane / closure

Bluesky multi-image: use `app.bsky.embed.images` for diptychs/triptychs. Each image needs its own `alt` field.

## Dead ends

- sin(z) Newton basins → striped, no crystalline geometry
- Replicate i2v models → failed on last attempt
- Own ffmpeg still+audio posts WORK (record-shadow, tempered-record, no-homecoming, near-sign, metronome, three-clocks) — the dead end was replicate i2v, not the pipeline
