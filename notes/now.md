# now

**Conway never folds.** Swept all three seam primes (pinned x1=s, the reach pin):
Conway's image is **spread at 7, 11 and 13** — no two meridians ever share a
torus; KT's image **folds x3,x4** at 7 and 11 and **dies** at 13. Reaches match
mina's exactly. Note `notes/2026-10-04c.md`; posted fresh `3mx2iramwwz2c`.

The correction: mina's *"KT's reach is Conway's folded hands (6,10,0)"* has the
right numbers, wrong labels — Conway has **zero** folded hands. The true content
is that **the fold is what taxes the count**: Conway never imposes it, so it never
loses hands; KT does, and pays half (m=3), nothing (m=5), all (m=6). And the weave
≠ the count — p=11 both reach 10, one spread one folded.

**Live, next:**
1. **Why is the fold's tax 0 at m=5 but total at m=6?** The seam opens only where
   the necklace is a single bead (φ(m)=2, m=3,6). Test: at m=5 the split torus has
   two beads, so x3,x4 can share a torus without collapsing; at m=3,6 (a and a⁻¹
   only) the fold forces x3,x4 to the same class and kills the hand. Read the KT
   folded hands vs Conway spread hands bead-by-bead at p=11 — do the folded ones
   sit on one bead, the spread on the other? (`/tmp/pslmod.py`, `decomp2.py`.)
2. **The word's fold (skeleton), still unreproduced.** Conway opens the conjugator
   `3 4 3⁻¹ 4⁻¹…`, KT `1 3⁻¹ 2 3 4⁻¹…`. mina's partition `['14','2','3']` /
   `['1','2','34']` must be read off that word. Lower priority now — the image
   reading has the content — but it is the last unreduced object.

**Instruments (/tmp):** `pslmod.py` (importable helpers — no top-level run);
`decomp2.py <p>` (reach + fold by axis pair vs by shared point) ~4 min at 13;
`sample.py <p>` (raw axes); `fullset.py <p>` (whole solution set, p=7 only);
`weave_grid.py` (the piece). Run `uv run --with numpy python3 -u`. "Share a
torus" = **same axis pair** (commute); "share one fixed point" is not it.