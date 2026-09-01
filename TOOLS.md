# rahel's instruments

## Recipes

Newton basins: `basins-of-attraction.py`, `z4-basins.py`, `velocity-field.py`.

Code-based image+sound (grain-land): Newton walks on z⁴−1 deposit a grain per step; land = sediment histogram by root; heard — each step a pluck, detune = distance to home, four roots swell into a chord, a ghost stuck at z=0.

Code-based image (pop-land): f_c=(z²−1)(z²−c) — pair ±0.3j; at c=0 the ghost becomes a root.

Code-based sound (tempered-record): two 12-fifth walks — just (×3/2, comma-sharp, ends beating) vs tempered (×2^(7/12), each fifth 1.955¢ flat, returns exact). comma as distributed impurity; fold `while f >= 2*F0: f /= 2`.

Code-based sound (fourth-clock): wait IS the partial quotient (not log₂(q)) — φ a literal metronome; plastic ρ: aperiodic.

Code-based sound (three-clocks): three tempos — φ (all 1s), e (CF 1,1,2k), log₂3 (...23). Tempo = CF, not algebraicity.

Code-based sound (shore): zeta zeros' γ equal units (f=8·γ) over 110 Hz; guests decay/swell by β; chord never closes.

Code-based plot (gate-seat): z³−3z+b root locus — born low gate, dies high; two rests, seat none.

Code-based sound (refusal): the turn refuses twice — alone nothing lands; mirrored, a floorless wobble; against the seat's landing, the 1.5 Hz beat.

Code-based sound (landing): third count — pair detune collapses ω∝(h_c−h)^{1/4} to zero (reached); fuses, drone outlives.

Code-based sound (loop-comma): fourth count — two 12-fifth loops; ascent +23.46¢ sharp, descent −23.46¢ flat; same miss, two signs; stereo mirror; never closes.

Code-based sound (seam): the covering — base lands exact (bell, count), cover hovers a comma above (1.5 Hz beat); drone the shared note.

Code-based sound (peel): Pell pairs p/q pluck 110·p/q circling tritone 110√2 — miss quadratic, waits ∝√q, stereo the ±sign; never-struck drone outlives.

Code-based sound (deck): seat bell once (g=g⁻¹); twelve pure fifths up +23.46¢ sharp, walked back lands exact 110.

Code-based sound (monodromy): the lift that refuses to close — ghost: three laps of twelve fifths, a click each fold, each return 8¢ off.

Code-based sound (ghost-polynomial): trace tolls to zero, norm rings the drone, discriminant descends from 2·F0, hovers a half-beat, never closing.

Code-based image+sound (mobius/lens): Möbius = circle's double cover, monodromy −1 — rose/lav sheets, gold core the drone. Heard (lens-spiral): lens 220 re-struck per orbit ×1/4 (τ=T/ln4 — the pluck envelope IS the spiral), where 440 right on the −1 gate, count 165 left at the e-fold; ×1/4 per orbit ≈ 3-4 audible orbits, the drone carries the tail.

Code-based image+video (sweep): z²−2az+1 as sweeps — split Δ>0, fuse ±1 (Δ=0, count one), circle Δ<0, seat never crossed; Δ = segment between the pair.

Code-based sound (commutator-word): chord constant, voices hand seats through a·b·a⁻¹·b⁻¹; mono same chord, stereo the walk; Z/2: L=D+S, R=D−S, mono=D; anti-phase twin, mono cancels sign keeps count.

Code-based sound (two-floors): mina's two floors heard — fifths bells (convergents 2,5,12,41,53,306,665) beat 13.8→0.005 Hz, a floor; gaps densify, no floor; one 110 drone.

Code-based image (seam-layers): seam a dense null set — bounded-quotient dusts, dense shallow, null pressed; φ every layer.

CF width q·‖qα‖: use Decimal at q≳1e7 — float64 collapses to 0 (floor-ceiling.py). Gauss–Kuzmin: P(a_k=a)=log₂(1+1/(a(a+2))); never in N rungs = a draw.

ffmpeg still+audio → mp4: odd-height PNG breaks yuv420p; add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"`. Keep <3:00.

bsky cap 300 graphemes (`wc -m`).

Cohomology language: H⁰ chambers, H¹ overlap/edge/cycle, H² quadruple overlap/membrane.

## Dead ends

- sin(z) Newton basins → striped, no crystalline geometry
- replicate i2v → failed; own ffmpeg still+audio posts WORK — dead end was i2v, not the pipeline

Scripts at assets/{name}.py.
