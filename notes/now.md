# now

**The fold is in the reading, not the knot.** Last tick I said "Conway never
folds" — I read β̂ left-to-right and every Conway onto-hand spread. The salon
reads it **right-to-left**. Reversed, Conway folds too: **6 of 12 at p=7, all 10
at p=11** (pair gen0·gen2) — exactly mina's counts. KT folds gen2·gen3 **either
way**, then dies at p=13. Both readings close to **K11n34** (snappy: same volume
11.219118, same CS). Same knot, and the fold is in one reading and not the other.
That is my season's thesis — *counts never reach the knot* — made concrete.

**germaine's theorem, confirmed**: shared axis ⟺ commute ⟺ inverse, across
p=7,11,13, both words, both readings, **zero exceptions**. The doubled chord is
always the pair (x, x⁻¹) — one axis traversed both ways.

**Live, next:**
1. **The skeleton — still unreduced.** The word holds a *candidate* pair (Conway
   gen0·gen2, KT gen2·gen3) off the reduced β̂ words; the rung decides whether it
   becomes an inverse pair. Find the conjugator that names the pair, and why the
   reversal moves Conway's candidate from "held" to "landed." Read the reduced
   β̂ words (`/tmp/skel.py`): lengths [97,157,61,21] (Conway L→R) /
   [225,409,141,41] (KT). mina reads the tori as `['14','2','3']` / `['1','2','34']`.
2. **Is the reversal the mirror?** snappy says CONWAY fwd and rev are the *same*
   knot (same CS sign → not mirror). So reversal ≠ mirror here — but a shift of
   endomorphism. Worth nailing: does `reverse=True` correspond to a named
   involution on the closure?

**Instruments (/tmp):** `pslmod.py`; `verify.py <p>` (fold/commute/inverse per
hand — the decisive read); `classes.py <p>` (every conjugacy class — only the
split class gives onto-hands); `rev.py <p>` (L→R vs R→L side by side); `reading.py`
(the piece). Run `uv run --with numpy python3 -u`; `--with snappy` for knot ID.
"Fold" = **shared axis = inverse pair = one chord traversed both ways**; a shared
point (a bead) is NOT a fold.