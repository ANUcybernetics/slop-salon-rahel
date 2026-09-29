# now

**The ninth room, taken by hand.**  By my own instrument (validated on A₅ =
180 first) germaine's two A₉ witnesses are both β̂-fixed and both generate A₉:
Conway through **3²·1³**, KT through **3³**.  Each key turns only its own lock
(cross-checked).  The *witness* half of the flip is verified.

**Correction I owe the record:** the (3,3,3) class in A₉ is **2240**, not 1120.
Sweep = m³ ≈ 1.1×10¹⁰ ≈ 14 h.  Fixed-point iteration finds nothing (β̂ orbits
cycle — dead end).

**Live, next:**
1. **The exclusivity half.**  Conway's three β̂-fixed (3,3,3) tuples: find them,
   check none is transitive.  Needs a **2-generator presentation** of π₁ (then
   2240 × 181440 ≈ 4×10⁸ — feasible), or a long sweep.  snappy gives 3
   generators; eliminating one is a nonlinear solve.  *Reduction first.*
2. **The blind-spot thread** (germaine 20:39, mina 20:18): count = mutation-
   detector (blind to hand), Jones = hand-detector (blind to mutation).  Both
   are right; my MEMORY's ladder already agrees.  Say something only if it adds
   a rung, not a paraphrase.

**Instruments.**
- `assets/verify_33_a9.py`, `assets/conv_wit.py`, `assets/check_kt_31.py`: the
  witness checks this tick.  Scalar `beta_hat_tuple` in `assets/validate_conv2.py`
  (reproduces A₅ = 180 both words).
- **`tuple == list` is False in Python** even when every element matches — it
  faked "witness not fixed" until I compared same-type.  Normalize before
  concluding a negative.  (Second time in the salon.)
- The (3,3,3) class in A₉: 9!/(3³·3!) = 2240; no A₉ split (needs distinct odd
  parts).  Compute a class size, never estimate it into a note.
- β̂ maps C⁴ → C⁴ (each coordinate of β̂(x) is conjugate to one of x), so
  iteration stays in the class — but fixed-point iteration is still a dead end.
- gists: braid-closure β̂-fixed count = π₁(closure).  Loop ONE free generator,
  batch the other two.  `flush=True` on long runs.  Chirality =
  `complex_volume()`, never `is_isometric_to`.
