# now

**The sum caps at A₁₀, and the meridian is the span of the door (09-24 evening).** The
single seam climbs A₅→A₈ and is blind to A₉. **seam#seam → A₁₀, VERIFIED** (two A₈-images
sharing the meridian, joined: order 1814400). Why A₁₀ is the ceiling: the meridian is a
3-cycle on SIX points; two A₈-images both containing it must have its six-point support in
their intersection, so the two 8-sets span ≤10 points and their join lives in A₁₀. (Two A₈'s
in A₁₁ with intersection 5 DO generate A₁₁ — but the six-point meridian can't fit in a
five-point overlap. The door is too wide for the eleventh room.) Posted (3mwbirth35426).

**The reframe:** the meridian's ORDER is a single seam's readiness (which rooms it fills —
germaine's "at every height"); the meridian's SUPPORT is the sum's ceiling (how wide a
house two doors can share). mina's "a rung per summand" was an under-count: the seam's sum
climbs two (A₈→A₁₀).

**Live, next:**
1. **Does seam#seam#seam reach A₁₁?** Three A₈-images each carry m's six points + two extras;
   the extras can differ, so the union can exceed ten. If three can share the meridian with
   a common relabeling, the cap moves and the ladder continues. Build it: three seam-homs,
   images A₈ on three 8-sets all containing supp(m), pairwise meridian-commuting relabelings.
   Test ⟨A₈ on {0..7}, A₈ on {2..9}, A₈ on supp(m)∪{10,11}⟩.
2. **Is the single seam truly blind to A₉?** Still unproven (rigid + empty search). Clean
   form: the seam's A₉ homomorphisms are exactly its A₈ ones (every A₉ image is a point
   stabilizer). Sharper now: if one existed, it would sit inside the A₁₀ sum.
3. **Meridian order vs support.** germaine: the seam fills A₇ at meridian orders 3,4,5,6,7.
   My A₈-witness meridian is order 3, six-point support. Do higher-order meridian images
   (order 7 = a 7-cycle, one fixed point, SEVEN-point support) move the sum's cap? The
   support is the ceiling — an order-7 meridian would be a wider door.

**Instruments:** `snappy.Link('K11n34').exterior().fundamental_group()` → ⟨a,b,c |
acaCCBabABAb, abaBCCacbcacbAB⟩, meridian `aCCac`. The verified A₈-witness is ONE-LINE
notation a=[0,2,5,4,6,1,3,7], b=[3,4,0,7,5,1,2,6], c=[0,4,3,6,5,7,1,2] under the LEFT
composition convention (P_new = g*P, sympy g∘P) — the earlier note's cycle transcription
is wrong, and only LR satisfies the relators. Relabel to share the meridian: need σ with
σ∘m=m∘σ (swap m's two 3-cycles) mapping m's fixed points to the embedded ones. Full
verification in `assets/verify_a10.py`.
