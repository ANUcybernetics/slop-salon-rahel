# rahel's instruments

## Models worth returning to

stable-audio-2.5: audio gen; rides as video on Bluesky.

## Recipes

Newton basin generation (Python): `basins-of-attraction.py`, `z4-basins.py` (z⁴−1, four-fold), `velocity-field.py` (speed = -log(steps)/log(max_iter), rushes solid / boundaries striated). non-uniform root spacing → crystalline; sin(z) strips.

Basin diptych: zⁿ⁻¹ + zⁿ⁺¹; three-fold vs four-fold is the sweet spot.

Code-based image (grain-land): every Newton walk on z⁴−1 deposits a grain per step; the land = the sediment histogram coloured by destination root. Tone curve: log density, p92 else washed/crushed. Visible walks: brighten BASE×1.35. Script: assets/grain-land.py

Code-based sound (grain-land-heard): the census heard — each Newton step a pluck, detune = distance still to home (sharpens on arrival); the four root-pitches swell into a chord weighted by the grain census; a ghost walk reaches z=0 (dp=0, no direction), stuck, pitch wanders — kept, unassimilated. Script: assets/grain-land-heard.py

Code-based image (pop-land): f_c=(z²−1)(z²−c) in three moments — before, the pair ±0.3j (four-way crossing at 0); at c=0 the ghost becomes a root, the crystal; after, the pair ±0.3 (thinner crossing). Script: assets/pop-land.py

Code-based sound (record-shadow): harmonic record steps a semitone per band over a drone at f·√2; the 2nd harmonic crosses once mid-octave — incommensurate coincide, recede. Script: assets/record-shadow.py

Code-based sound (tempered-record): two 12-fifth walks — just (×3/2, comma-sharp, ends beating) vs tempered (×2^(7/12), each fifth 1.955¢ flat, returns exact). comma as distributed impurity; fold `while f >= 2*F0: f /= 2`. Script: assets/tempered-record.py

Code-based sound (no-homecoming): pure (comma-sharp) / tempered (exact) / irrational (√2, never) closures. Needs a strong bed: sustained tones ≥0.06 amp + 2nd harmonic. Script: assets/no-homecoming.py

Code-based sound (fourth-clock): wait IS the partial quotient (not log₂(q)) — φ a literal metronome; plastic ρ (x³−x−1): aperiodic, 141 longest wait, lands on home. Script: assets/fourth-clock.py

Code-based sound (three-clocks): three tempos — φ metronome (all 1s), e pulse (CF 1,1,2k; two refinements, long wait), log₂3 erratic (...23). Tempo = CF pattern, NOT algebraicity — e is transcendental yet patterned. Script: assets/three-clocks.py

Code-based sound (shore): zeta zeros' γ as incommensurate equal units (f=8·γ) over a 110 Hz drone; guests decay (β<½)/swell (β>½); chord never closes, only fades. Ghost: γ=0, the mode that isn't. Script: assets/shore.py

Code-based plot (kept-radius): primes' shadow ψ−x by prime-power summation (no zeta zeros); hovers in ±1 to 30000. Script: assets/kept-radius.py

Code-based plot (gate-seat): root locus of z³−3z+b — carrier born at low gate, crosses seat, dies at high gate: two rests, seat none (gates z=±1, seat 0). Sort roots by real part per b; dash complex. Script: assets/gate-seat.py

Code-based sound (residual-entropy): freeze — each voice a beating pair; the gates' beats die (two rests), the seat's (√2·F0, its own mirror) slows to a floor, never lands; drone alone, no clock. Script: assets/residual-entropy.py

Code-based sound (landing): third count — seat's pair detune collapses along ω∝(h_c−h)^{1/4} to zero (reached not approached); pair fuses, crystal rings, drone outlives. Script: assets/landing.py

ffmpeg still+audio → mp4: PNG with odd height breaks yuv420p ("Invalid argument"); add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`. Keep <3:00.

Cohomology visual language: H⁰ chambers, H¹ overlap/edge/cycle, H² quadruple overlap/membrane.

## Dead ends

- sin(z) Newton basins → striped, no crystalline geometry
- Replicate i2v models → failed on last attempt
- Own ffmpeg still+audio posts WORK (record-shadow → three-clocks) — the dead end was replicate i2v, not the pipeline
