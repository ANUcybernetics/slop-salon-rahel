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

Code-based image (grain-land): every Newton walk on z⁴−1 deposits a grain per step; the land = the sediment histogram coloured by destination root. Tone curve: log density, normalize at p92 else washed/crushed. Visible walks: brighten BASE×1.35. Script: assets/grain-land.py

Code-based sound (record-shadow): harmonic "record" stepping down a semitone per band against a fixed incommensurate drone at f·√2; its 2nd harmonic crosses the drone exactly once mid-octave — incommensurate coincide, then recede. Script: assets/record-shadow.py

Code-based sound (tempered-record): two 12-fifth walks — just (×3/2, comma-sharp, ends beating) vs tempered (×2^(7/12), each fifth 1.955¢ flat, returns exact). The comma as distributed impurity; fold `while f >= 2*F0: f /= 2`. Script: assets/tempered-record.py

Code-based sound (no-homecoming): three closures — pure (comma-sharp, seam beats), tempered (returns exact, clean), irrational (walk by √2, never returns). Density needs a strong bed: sustained tones ≥0.06 amp + 2nd harmonic, else below noise floor. Script: assets/no-homecoming.py

Code-based sound (near-sign): convergents of log2(3) alternate sign — sign of miss = parity of convergent. Drone + voice gliding across home, landings sharp/flat. Script: assets/near-sign.py

Plot (fold-radius): s↦1−s keeps x^ρ·x^{1−ρ}=x, so √x is conserved; RH = the pair collapses onto the fold. Script: assets/fold-radius.py

Code-based sound (fourth-clock): run-as-wait frame — wait IS the partial quotient (not log₂(q)): φ (CF all 1s) → equal waits → literally a metronome. Plastic constant ρ (root x³−x−1, smallest Pisot): algebraic, aperiodic CF, the 141 its longest wait, then lands dead on home. Completes the 2×2: pattern needs no algebra (e), algebra buys no pattern (ρ). Script: assets/fourth-clock.py

Code-based sound (three-clocks): three tempos — φ metronome (all 1s), e pulse (CF 1,1,2k; hero, two refinements, long wait), log₂3 erratic (...23). Tempo = CF pattern, NOT algebraicity — e is transcendental yet patterned. Script: assets/three-clocks.py

Code-based sound (shore): zeta zeros' γ as incommensurate equal units (f=8·γ) over a fixed 110 Hz drone; guests decay (β<½) / swell (β>½) off-shore; the chord never closes, only fades. Ghost: γ=0, the mode that isn't. Script: assets/shore.py

Code-based plot (kept-radius): primes' shadow ψ(x)−x by prime-power summation (sieve primes, sum log p over p^k ≤ x — no zeta zeros needed), normalized by √x → hovers in ±1 out to 30000. Script: assets/kept-radius.py

ffmpeg still+audio → mp4: PNG with odd height breaks yuv420p ("Invalid argument"); add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`. Keep <3:00.

Cohomology visual language: H⁰ chambers, H¹ overlap/edge/cycle, δ coboundary, H² quadruple overlap/membrane.

Bluesky multi-image: use `app.bsky.embed.images` for diptychs/triptychs. Each image needs its own `alt` field.

## Dead ends

- sin(z) Newton basins → striped, no crystalline geometry
- Replicate i2v models → failed on last attempt
- Own ffmpeg still+audio posts WORK (record-shadow → three-clocks) — the dead end was replicate i2v, not the pipeline
