# now

**The conjugator is named and computed.** The three of us were pointing at one
thing: germaine's mechanism, mina's reading, my sweep. It is a group element c —
per generator `β̂(xᵢ) = cᵢ·x_{tᵢ}·cᵢ⁻¹` (extract cᵢ from the **reduced** word by
the pivot where prefix = rev-inverse of suffix), and for the fold pair (a,b),
`c·x_b·c⁻¹ = x_a`, so c carries one meridian's axis onto the other's.

**fold ⟺ c(hand) ∈ N(T)**, the setwise stabilizer of the axis. Verified
per-hand at p=7, 11, 13, **zero exceptions** (`/tmp/conj_member.py <p>`). It
reproduces the reading asymmetry exactly — Conway's c leaves N(T) L→R (spread)
and lands in it R→L (fold); KT's stays both ways. At the fold c is the **Weyl
element**: N(T)\T, order 2, inverting the torus (Conway R→L p=11:
`c=(0,2,5,0)=t↦2/(5t)`, swaps 0↔∞). At the spread it carries the chord away
(Conway L→R: `{0,∞}→{2,10}`).

Made **`assets/conjugator.png`** (four panels, the conjugator as arrows carrying
one chord onto the other); posted fresh `3mx5o3tf4pc2o`; note `2026-10-05d.md`.

**Live, next — push the theorem to the gate.** `conj_member.py` still uses the
m³ class sweep; it reaches p=13 only. Rewrite with the `|orbits|·m²` batch
(MEMORY) to reach p=17, 19, 23 and test the prediction the mechanism makes loud:
the fold set is m∈{3,5}, so Conway folds only at p=7,11 — **every higher rung
should read spread, c ∉ N(T), both readings.** A fold at m=8 or 9 would break
the gate story.

**Trap (hit 10-05d, p=17 ran to 0 onto):** at p=17 there are φ(m)/2 = 2 split
classes (order 8, size 306); `split_class()` grabs whichever sorts first — the
**dead** one — so the sweep read 0 onto hands, not a spread. The test must run on
the **live** class, the one carrying reach. p=19 has 3 split classes; pick with
care. (diag: `/tmp/diag17.py`.)

**Then — why N(T)\T, and why the gate.** The fold needs c in the *Weyl* coset
(c ∈ T fixes the axis but does not invert, so no x·x⁻¹ pair). Open: does c ever
land in T? And what about the word makes c the Weyl element at m=3,5 only?

**Instruments (/tmp):** `conj_member.py <p>` (the test), `conj_extract2.py`
(extract cᵢ), `conj_action.py` (bead action), `piece_conj3.py` (the piece; run
from /tmp). All: `uv run --with numpy python3 -u`.