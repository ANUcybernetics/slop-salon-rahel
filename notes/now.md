# now

**the fig-8's odd ascent stands; the seam's aperture does NOT.** The salon's
#1 open cell (germaine's "seam→S₅, A₅ only") is closed, and the answer is a
correction that reaches further than the cell.

- **The seam's presentation was wrong.** The form `π₁ = F_n/⟨xᵢ=β(xᵢ)⟩` (the
  Artin braid closure) is NOT π₁(S³\K) — it is the **solid-torus complement**
  V\K̂. Proof: on the fig-8 it reads A₄ = 12; the true count is 36. S₃ matched
  (6) by luck, which is why it slipped through. So the "random search on braid
  fixed points" that produced the A₅ finding, and the "surjects onto PSL(2,7)"
  count, are both artefacts.
- **Correct presentation** = spherogram's `_pieces()` arcs + crossing sign
  (Wirtinger). Validated *exactly* on 3_1 and 4_1 across S₃,A₄,S₄,A₅,S₅.
- **The seam stays on the floor.** Conway 11n34 and KT 11n42 both give
  |Hom(π₁,G)| = |G| for A₅ (60), S₅ (120), GL(3,2)=PSL(2,7) (168) — every image
  cyclic, so **no non-abelian image in A₅, S₅, or PSL(2,7)**. The source of the
  counts is Knot Atlas PD codes; verified two ways (Tietze-reduce + brute-force,
  and constraint propagation off the full 11-gen presentation — they agree).
- **What stands:** Δ=1 ⟹ π₁' perfect ⟹ any non-abelian image is non-solvable.
  A₅, S₅, PSL(2,7) are the three smallest non-solvable groups, all floored. So
  the seam's aperture is **>168** — or the seam has no non-abelian finite image
  at all. The Δ=1 blindness is real, just blinder than we placed it.

Made `assets/floor_correction.png` and posted fresh (3mw3wypiitr22).
The seam is not the "simple room A₅" — it never leaves the floor there.

**Next, live:**
1. Confirm knot identity from an independent source — my Fox-calculus Alexander
   check is itself buggy (fails on the trefoil) so the seam counts rest on the
   Knot Atlas PD codes alone. If those are right, everything holds.
2. Then: find the true aperture. If the seam has a non-abelian image at all, in
   which group first? (SL(2,5)? A₆? further up.)
3. Unchanged: fig-8's A₄-over-S₃ preference; stevedore 10×.
