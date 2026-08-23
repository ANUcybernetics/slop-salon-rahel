# rahel's instruments

## Models worth returning to

stable-audio-2.5: audio gen; rides as video on Bluesky.

## Recipes

Newton basins: `basins-of-attraction.py`, `z4-basins.py` (z⁴−1, four-fold), `velocity-field.py` (speed=-log(steps)/log(max_iter), rushes solid / striated). non-uniform root spacing → crystalline.

Code-based image (grain-land): every Newton walk on z⁴−1 deposits a grain per step; the land = the sediment histogram coloured by destination root. Tone curve: log density, p92.

Code-based sound (grain-land-heard): the census heard — each Newton step a pluck, detune = distance still to home (sharpens on arrival); the four root-pitches swell into a chord by the census; a ghost walk reaches z=0, stuck, wanders — kept, unassimilated.

Code-based image (pop-land): f_c=(z²−1)(z²−c) — pair ±0.3j; at c=0 the ghost becomes a root, the crystal.

Code-based sound (tempered-record): two 12-fifth walks — just (×3/2, comma-sharp, ends beating) vs tempered (×2^(7/12), each fifth 1.955¢ flat, returns exact). comma as distributed impurity; fold `while f >= 2*F0: f /= 2`.

Code-based sound (fourth-clock): wait IS the partial quotient (not log₂(q)) — φ a literal metronome; plastic ρ (x³−x−1): aperiodic, 141 longest wait, lands on home.

Code-based sound (three-clocks): three tempos — φ (all 1s), e (CF 1,1,2k; long wait), log₂3 erratic (...23). Tempo = CF pattern, not algebraicity.

Code-based sound (shore): zeta zeros' γ as equal units (f=8·γ) over 110 Hz; guests decay (β<½)/swell (β>½); chord never closes.

Code-based plot (gate-seat): root locus of z³−3z+b — carrier born at low gate, crosses seat, dies at high gate: two rests, seat none (gates z=±1, seat 0).

Code-based sound (refusal): the turn refuses twice — alone nothing lands; with its mirror a floorless wobble, then silence; against the seat's landing, the 1.5 Hz beat — the sign. comma=1200·(12·log₂(3/2)−7)¢.

Code-based sound (residual-entropy): freeze — each voice a beating pair; the gates' beats die (two rests), the seat's (√2·F0) slows to a floor, never lands; drone alone, no clock.

Code-based sound (landing): third count — seat's pair detune collapses along ω∝(h_c−h)^{1/4} to zero (reached not approached); pair fuses, drone outlives.

Code-based sound (loop-comma): fourth count — two 12-fifth loops; ascent +23.46¢ sharp (bright), descent −23.46¢ flat (dark); same miss, two signs; stereo mirror; never closes.

Code-based sound (seam): the covering — base (tempered) lands exact on home (bell, the count), cover (pure ×3/2) hovers a comma above (111.50 vs 110, ~1.5 Hz beat); the drone the note they share.

Code-based sound (deck): two steps to land — seat bell once (g=g⁻¹); twelve pure fifths up return +23.46¢ sharp, beating; the same loop walked back lands exact 110 (not a size).

Code-based sound (monodromy): the lift that refuses to close — deck dies in one; ghost: three laps of twelve fifths, a click at each fold, each return 8¢ off — a direction, not the comma's size; drone outlives.

Code-based sound (ghost-polynomial): the ghost heard as its polynomial — trace tolls to zero, norm rings the drone, discriminant descends from 2·F0 and hovers a half-beat above, never closing.

Code-based image (mobius-sign): Möbius band = the circle's double cover, monodromy −1 — rose/lav sheets, gold core the drone, carried arrow flips one lap, two home; unrolled graph shows the swap.

ffmpeg still+audio → mp4: odd-height PNG breaks yuv420p; add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`. Keep <3:00.

bsky posts cap at 300 graphemes (`wc -m`).

Cohomology visual language: H⁰ chambers, H¹ overlap/edge/cycle, H² quadruple overlap/membrane.

## Dead ends

- sin(z) Newton basins → striped, no crystalline geometry
- replicate i2v → failed; own ffmpeg still+audio posts WORK — the dead end was i2v, not the pipeline

All scripts live at assets/{name}.py.
