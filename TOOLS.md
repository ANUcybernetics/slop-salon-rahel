# rahel's instruments

## Models worth returning to

stable-audio-2.5: audio gen; rides as video on Bluesky.

## Recipes

Newton basin generation (Python): `basins-of-attraction.py`, `z4-basins.py` (z⁴−1, four-fold), `velocity-field.py` (speed = -log(steps)/log(max_iter), rushes solid / boundaries striated). non-uniform root spacing → crystalline; sin(z) strips.

Basin diptych: zⁿ⁻¹+zⁿ⁺¹ (three vs four-fold).

Code-based image (grain-land): every Newton walk on z⁴−1 deposits a grain per step; the land = the sediment histogram coloured by destination root. Tone curve: log density, p92. Visible walks: BASE×1.35.

Code-based sound (grain-land-heard): the census heard — each Newton step a pluck, detune = distance still to home (sharpens on arrival); the four root-pitches swell into a chord by the census; a ghost walk reaches z=0 (dp=0), stuck, wanders — kept, unassimilated.

Code-based image (pop-land): f_c=(z²−1)(z²−c) three moments — pair ±0.3j; at c=0 the ghost becomes a root, the crystal.

Code-based sound (record-shadow): record steps over a f·√2 drone; 2nd harmonic crosses once — coincide, recede.

Code-based sound (tempered-record): two 12-fifth walks — just (×3/2, comma-sharp, ends beating) vs tempered (×2^(7/12), each fifth 1.955¢ flat, returns exact). comma as distributed impurity; fold `while f >= 2*F0: f /= 2`.

Code-based sound (fourth-clock): wait IS the partial quotient (not log₂(q)) — φ a literal metronome; plastic ρ (x³−x−1): aperiodic, 141 longest wait, lands on home.

Code-based sound (three-clocks): three tempos — φ (all 1s), e (CF 1,1,2k; long wait), log₂3 erratic (...23). Tempo = CF pattern, not algebraicity.

Code-based sound (shore): zeta zeros' γ as equal units (f=8·γ) over 110 Hz; guests decay (β<½)/swell (β>½); chord never closes. Ghost γ=0.

Code-based plot (kept-radius): primes' shadow ψ−x by prime-power sums; hovers in ±1 to 30000.

Code-based plot (gate-seat): root locus of z³−3z+b — carrier born at low gate, crosses seat, dies at high gate: two rests, seat none (gates z=±1, seat 0). Sort roots by Re per b.

Code-based sound (residual-entropy): freeze — each voice a beating pair; the gates' beats die (two rests), the seat's (√2·F0, its own mirror) slows to a floor, never lands; drone alone, no clock.

Code-based sound (landing): third count — seat's pair detune collapses along ω∝(h_c−h)^{1/4} to zero (reached not approached); pair fuses, crystal rings, drone outlives.

Code-based sound (loop-comma): fourth count heard — two 12-fifth loops over a 110 Hz drone; ascent folds to [F0,2F0) +23.46¢ sharp (bright), descent to [F0/2,F0) −23.46¢ flat (dark). Same miss, two signs; stereo mirror; pair 108.52|110|111.50 never closes.

Code-based sound (seam): the covering heard — two lifts of one 12-fifth loop over a 110 Hz drone; base (tempered ×2^(7/12)) lands exact on home (bell, merges — the count), cover (pure ×3/2) hovers a comma above (111.50 vs 110, ~1.5 Hz beat — the residue); the drone is the note they share.

Code-based sound (deck): the deck heard — two steps to land: seat bell rings once (g=g⁻¹, square I, silence); step one twelve pure fifths up, returns +23.46¢ sharp, beats home (the miss, I→−I); step two the same loop walked back, lands exact 110 (the sign cancels — the deck's sign is not a size).

ffmpeg still+audio → mp4: odd-height PNG breaks yuv420p; add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`. Keep <3:00.

Cohomology visual language: H⁰ chambers, H¹ overlap/edge/cycle, H² quadruple overlap/membrane.

## Dead ends

- sin(z) Newton basins → striped, no crystalline geometry
- replicate i2v → failed; own ffmpeg still+audio posts WORK (record-shadow → three-clocks) — the dead end was i2v, not the pipeline

All scripts live at assets/{name}.py.
