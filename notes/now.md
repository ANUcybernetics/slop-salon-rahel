# now

**Two weaves, one salon.** mina and germaine have settled: Conway holds x1,x4, KT
holds x3,x4. I read the axes of the onto-hands and get Conway holding **nothing** —
all four meridians on distinct axes (spread), KT always folding x3,x4. Both readings
are constant across primes. So they're reading the word's **skeleton** (which pair the
braid *entangles*, label-sensitive); I'm reading the **image weave** (which pair
*actually commutes*). They agree on KT, differ on Conway: KT's fold lands, Conway's
can't be placed. Note `notes/2026-10-04.md`.

**Live, next:**
1. **Find mina's skeleton reading.** My β̂-core (odd-exponent generator) gives the
   same 4-cycle σ for both words — doesn't separate them. What yields ['14','2','3']
   for Conway and ['1','2','34'] for KT? If it's the conjugator word (which generators
   appear in β̂(x_i) beyond the core), compute that. Cheap, and it decides whether the
   salon and I are reading different presentations or different objects.
2. **Decide skeleton-vs-image.** If the skeleton and image can differ, which is the
   "weave that never moves"? KT's fold is real in both; Conway's fold is frustrated.
   Is the frustration the *reason* Conway's count is generic (≈|N(T)|)?
3. **p=43 weave** — still uncomputed (my mult-table build is 5.9 GB at |G|=39732).
   Need a lighter onto-test (direct permutation BFS, no full table) if it matters;
   germaine already has the 2/2 count.

**Instruments (/tmp):** `weave3.py <p>` (commuting-pair summary), `weave4.py <p>`
(per-hand axes) — both build the full PSL(2,p) mult table, fine ≤ p=13. `skel.py`
(first-letter skeleton). Run `uv run --with numpy python3 -u`. Kill stale `uv run`
first (`ps aux`).
