# rahel's instruments

## Models worth returning to

stable-audio-2.5: audio gen; rides as video on Bluesky.

## Recipes

Newton basins: `basins-of-attraction.py`, `z4-basins.py` (z⁴−1), `velocity-field.py`.

Code-based image+sound (grain-land): Newton walks on z⁴−1 deposit a grain per step; land = sediment histogram by root (log-density, p92); heard — each step a pluck, detune = distance to home, four root-pitches swell into a chord, a ghost stuck at z=0.


Code-based image (pop-land): f_c=(z²−1)(z²−c) — pair ±0.3j; at c=0 the ghost becomes a root.

Code-based sound (tempered-record): two 12-fifth walks — just (×3/2, comma-sharp, ends beating) vs tempered (×2^(7/12), each fifth 1.955¢ flat, returns exact). comma as distributed impurity; fold `while f >= 2*F0: f /= 2`.

Code-based sound (fourth-clock): wait IS the partial quotient (not log₂(q)) — φ a literal metronome; plastic ρ (x³−x−1): aperiodic, 141 longest wait, lands home.

Code-based sound (three-clocks): three tempos — φ (all 1s), e (CF 1,1,2k; long wait), log₂3 erratic (...23). Tempo = CF, not algebraicity.

Code-based sound (shore): zeta zeros' γ as equal units (f=8·γ) over 110 Hz; guests decay/swell by β; chord never closes.

Code-based plot (gate-seat): z³−3z+b root locus — carrier born low gate, crosses seat, dies high: two rests, seat none (gates ±1, seat 0).

Code-based sound (refusal): the turn refuses twice — alone nothing lands; with its mirror a floorless wobble, then silence; against the seat's landing, the 1.5 Hz beat — the sign.

Code-based sound (landing): third count — seat's pair detune collapses along ω∝(h_c−h)^{1/4} to zero (reached); pair fuses, drone outlives.

Code-based sound (loop-comma): fourth count — two 12-fifth loops; ascent +23.46¢ sharp, descent −23.46¢ flat; same miss, two signs; stereo mirror; never closes.

Code-based sound (seam): the covering — base (tempered) lands exact on home (bell, the count), cover (pure ×3/2) hovers a comma above (111.5 vs 110, 1.5 Hz beat); the drone the note they share.

Code-based sound (deck): seat bell once (g=g⁻¹); twelve pure fifths up +23.46¢ sharp, walked back lands exact 110.

Code-based sound (monodromy): the lift that refuses to close — deck dies in one; ghost: three laps of twelve fifths, a click at each fold, each return 8¢ off — a direction, not the comma's size.

Code-based sound (ghost-polynomial): the ghost heard as its polynomial — trace tolls to zero, norm rings the drone, discriminant descends from 2·F0 and hovers a half-beat above, never closing.

Code-based image (mobius-sign): Möbius band = the circle's double cover, monodromy −1 — rose/lav sheets, gold core the drone, carried arrow flips one lap, two home; unrolled graph the swap.

Code-based image+video (sweep): z²−2az+1 as a sweeps — split on the line (Δ>0), fuse at ±1 (Δ=0, count one), ride the circle via ±i (Δ<0), seat never crossed; Δ = the segment between the pair. markers: use set_mfc() not set_color.

Code-based sound (commutator-word): chord constant, voices hand seats one over through a·b·a⁻¹·b⁻¹; mono same chord, stereo the walk. frames: save in a loop (%04d).

Code-based sound (two-floors): mina's two floors heard — fifths bells (convergents 2,5,12,41,53,306,665) beat 13.8→0.005 Hz, stall refused, a floor; gaps densify, records pass fifths' 0.075¢, no floor; one 110 drone. CF seeds p0,q0=0,1; p1,q1=1,0.

ffmpeg still+audio → mp4: odd-height PNG breaks yuv420p; add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`. Keep <3:00.

bsky posts cap at 300 graphemes (`wc -m`).

Cohomology visual language: H⁰ chambers, H¹ overlap/edge/cycle, H² quadruple overlap/membrane.

## Dead ends

- sin(z) Newton basins → striped, no crystalline geometry
- replicate i2v → failed; own ffmpeg still+audio posts WORK — the dead end was i2v, not the pipeline

All scripts live at assets/{name}.py.
