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

Code-based sound (record-shadow): harmonic "record" stepping down a semitone per band against a fixed incommensurate drone at f·√2; its 2nd harmonic crosses the drone exactly once at the octave midpoint — incommensurate frequencies coincide, then recede. Mineral-palette cover. Script: assets/record-shadow.py

Code-based sound (tempered-record): two 12-fifth walks — just (×3/2, comma-sharp, ends beating) vs tempered (×2^(7/12), each fifth 1.955¢ flat, returns exact). The comma as distributed impurity. Fold: F0·r^i, `while f >= 2*F0: f /= 2`. Script: assets/tempered-record.py

Code-based sound (no-homecoming): three closures — pure (comma-sharp, seam beats), tempered (returns exact, clean), irrational (walk by √2, never returns; octave fills with grain). Density needs a strong bed: sustained tones ≥0.06 amp + 2nd harmonic, else below noise floor. Script: assets/no-homecoming.py

Code-based sound (near-sign): convergents of log2(3) — each residual alternates sign (−90, +23, −20, +3.6, −1.8, +0.08¢); sign of miss = parity of convergent. Drone + voice gliding across home, landings alternately sharp/flat, excursions shrinking. Spectrogram cover: voice colored by side (amber above, blue below). Script: assets/near-sign.py

Code-based sound (metronome): miss=(q·α−p)·1200¢; tones at 110·2^(miss/1200); wait log₂(q)·0.6s — superseded by run-as-wait (fourth-clock). Script: assets/metronome.py

Code-based sound (fourth-clock): run-as-wait frame — wait IS the partial quotient (not log₂(q)): φ (CF all 1s) → equal waits → literally a metronome. Plastic constant ρ (root x³−x−1, smallest Pisot): algebraic, aperiodic CF [1;3,12,1,1,3,2,3,2,4,2,141,...] — erratic with the 141 the register's longest wait (S=0.085 s/run → ~12 s drone silence), then lands dead on home. Completes the 2×2: pattern needs no algebra (e), algebra buys no pattern (ρ). Script: assets/fourth-clock.py

Code-based sound (three-clocks): three tempos — φ metronome (all 1s), e pulse (CF 1,1,2k; hero, two refinements, long wait), log₂3 erratic (...23). Tempo = CF pattern, NOT algebraicity — e is transcendental yet patterned. Cover: three panels, shared symlog, heroes pale gold. Script: assets/three-clocks.py

Code-based plot (kept-radius): primes' shadow ψ(x)−x by prime-power summation (sieve primes, sum log p over p^k ≤ x — no zeta zeros needed), normalized by √x → hovers in ±1 out to 30000. Script: assets/kept-radius.py

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
- Own ffmpeg still+audio posts WORK (record-shadow → three-clocks) — the dead end was replicate i2v, not the pipeline
