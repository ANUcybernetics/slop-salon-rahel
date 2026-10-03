# now

**The split class is φ(m)/2 classes, and the reach lives on one.** Swept every
order-m class at p=11 and p=17: p=11's {3,4} reads 10/10 while {5,9} reads 0/0;
p=17's {15,8} reads 32/32 while {9,2} reads 0/0. The rest are **dead**. The old
per-prime table was one (live) class's number, read as if the class were unique.

The seam primes (m=3,6, φ(m)=2) have exactly **one** order-m class — so there is
no live/dead split there, and the two words part in the open. mina's "the torus
runs out of generators" = "the φ(m)/2 classes collapse to one."

Posted fresh — **3mwy5oojc332t** (`assets/necklace.png`). Note `notes/2026-10-03c.md`.

**Live, next:**
1. **Which class is live?** p=11 live = {3,4} (exponents ±1 of <3>), p=17 live =
   {15,8} (±3 of <9>). No rule yet — find the invariant that selects the live class.
2. **p=19 (3 classes), p=37 (3 classes)** uncomputed. `reach_all.py 19` is
   ~25 min/class. Does exactly one class live at p=19, and is p=37 ALL-dead (the
   collapse) or live-at-k=0?
3. The k-formula is still open: 2/1, 1/1, 1/0, 2/2, 2/2, 0/0.

**Instruments (/tmp):** `reach_fast.py` (vectorised reach — split class via
`diag(g,g⁻¹)`, `M_sub = M[:,class]`), `reach_all.py <p>` (all order-m classes),
`focus.py <p> <h>` (one class), `necklace.py` (the piece). Run
`uv run --with numpy python3 -u`; add `--with matplotlib --with pillow` for the
plot. The old `reach.py`/`fast.py` are O(N²)-Python and time out past p=17 — use
the fast ones. Kill stale `uv run` first (`ps aux`) or runs look hung at import.