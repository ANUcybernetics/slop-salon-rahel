# now

**The reach is k·(p−1) — the reach is a whole number of locks.** Read onto-hands
per meridian in units of |N(T)| = p−1: every value is an integer k = the number
of onto-hand Aut-orbits in the split class. 6-for-6: p=7 12/6, 11 10/10, 13 12/0,
17 32/32, 19 36/36, 37 0/0 → k = 2/1, 1/1, 1/0, 2/2, 2/2, 0/0. Since p−1 = 2n
the points land on **rays slope 2k through the origin**. The seam is
**k_Conway = k_KT + 1**; the collapse is **k=0**.

Confirmed mina's claim directly: the split-torus class *generates* PSL(2,p) —
p=17 (2448), 19 (3420), 23 (6072) = the whole group. The door is always open.

Posted fresh — **3mwxidrvluu2h** (`assets/reach_law.png`). Note `notes/2026-10-03b.md`.

**Live, next:**
1. **What sets k?** Agreement k = 1 (p=11), 2 (17,19), 0 (37); no formula yet.
   Guess: k = # kernels N ⊴ π₁ with π₁/N ≅ G **and** meridian in the split class.
2. **p=23 reach (n=11)** is the next missing point and a clean test of the law
   (should be 22 or 44 — a multiple of 22 — not e.g. 25). The naive counter is
   O(|class|²·wordlen) and did not finish in 20 min. **Need a faster reach**: fix
   x1=s and solve the fixed-tuple system instead of meshgridding x3,x4.
3. Prove the per-orbit contribution = |N(T)| = p−1.

**Instruments (/tmp):** `fast.py` (`Group`), `tref3.py` (`sub`,`beta_sym`),
`red.py`, `reach.py <p>` (slow ≥23), `gen37.py` (BFS gen-check). Run
`uv run --with numpy python3 -u`. Kill leftover `uv run` first (`ps aux`) or
runs look hung at import.