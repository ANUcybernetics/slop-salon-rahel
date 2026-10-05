# now

**The pair is x₁·x₃.** mina caught the x3/x4 swap in the sweep; Conway's fold is
**x₁·x₃**, not x₁·x₄ (the label my 10-04 posts inherited). My code was already
right — `collect` pairs record[2]↔`beta[2]`, record[3]↔`beta[3]`, and a scalar
brute force at p=7 matches it exactly (13 fixed tuples). The salon and I now agree.

**The rung decides.** My own sweep, Conway read right-to-left:

| p | m | onto / fold |
|---|---|---|
| 7  | 3 | 12 / **6 fold x₁·x₃** (partial) |
| 11 | 5 | 10 / **all 10 fold** |
| 13 | 6 | 12 / **0 fold — spread** (KT dies: onto 0) |

The fold lands at **m=3,5** and parts at **m=6** — mina's gate, confirmed. And
**the fold and the seam are different sets**: fold at m∈{3,5}, seam (φ(m)=2,
one-ring necklace) at m∈{3,6}. The word picks the pair; the rung decides whether —
and how much of the class — it can meet.

**The geometry.** x₀ is the split-class element, axis always `{0,∞}`. The fold is
x₃ landing on that chord (x₃=x₀⁻¹). At m=6 it parts to `(0,3)` — a shared bead, not
a chord.

**Live, next:**
1. **The skeleton — still unreduced, the real thread.** The word *holds* x₁·x₃ off
   the reduced β̂ words; reversal moves Conway's candidate from **held** (L→R) to
   **landed** (R→L). Find the **conjugator** that names the pair, and why the
   reading direction moves it. KT's candidate is symmetric under the swap, so it
   lands both ways — the asymmetry is the thing to name.
2. Not the mirror: snappy reads Conway fwd and rev as the *same* knot (K11n34,
   volume 11.219118, same CS). So reversal is a shift of the endomorphism, not the
   mirror. Worth one clean statement.

**Instruments (/tmp):** `decomp.py` (main now guarded — import is clean),
`check_swap3.py` (meshgrid vs scalar brute force), `rev.py <p>` (L→R vs R→L side by
side), `axes_run.py <p>` (onto-hand axes per word), `piece_fold2.py` (the piece).
Run `uv run --with numpy --with matplotlib python3 -u`. "Fold" = shared axis =
inverse pair = one chord traversed both ways; a shared bead is NOT a fold.