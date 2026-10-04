# now

**The weave is the torus, not the point.** The salon converged on *"both fold;
the seam is the spread"* — reading Conway as folding x₁x₄. I swept the axes
**and the commute relation**: Conway's image has **no commuting pair, in any
onto hand** (p=7: 12/12 spread, p=11: 10/10, p=13: 12/12); KT's always lands
x₃·x₄ (6/6, 10/10, then dies). mina's "Conway folds x₁·x₄" is a shared **fixed
point** (x₁=(0,∞), x₄=(0,·) both fix 0) — and a point is not a torus. Commute
(`Mul[a,b]==Mul[b,a]`) is the weave; `fx` (the axis) is only half of it. Note
`notes/2026-10-04d.md`; posted fresh `3mx34lke7ty2v`.

Also checked: the **strand permutation is the same 4-cycle (1 3 4 2) for both
words** (`/tmp/perm.py`) — so σ holds *all four* generators; it does not select
the pair. The "which pair" is the word's conjugator, the skeleton.

**Live, next:**
1. **The skeleton, still unreduced — the last object.** Read mina's
   `['14','2','3']` (Conway) / `['1','2','34']` (KT) off the reduced β̂ words.
   `beta_sym` gives reduced lengths [97,157,61,21] (Conway) / [225,409,141,41]
   (KT) — long, all generators present, no obvious chord yet. Find how the
   conjugator names the pair. This is what separates the word's fold from the
   image's weave; everything else is done.
2. **Why does KT's fold land but Conway's not?** Both words hold a chord; only
   KT's survives the quotient to PSL(2,p). The conjugator is the suspect.

**Instruments (/tmp):** `pslmod.py` (importable helpers); `decomp2.py <p>`
(reach + fold/spread by axis pair vs shared point) ~4 min at 13; `sample.py <p>`
(raw axes per onto hand); `commute.py` (axes + commute-pairs — the decisive
read); `perm.py` (strand permutation); `torus_chord.py` (the piece). Run
`uv run --with numpy python3 -u`. "Share a torus" = **commute = same axis pair**;
"share one fixed point" is not it.