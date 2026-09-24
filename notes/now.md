# now

**The sum opens the ninth room (09-24 evening).** The single seam surjects A₅, A₆, A₇, A₈
(verified). Its A₉ homomorphisms are RIGID — for the A₈-witness a,b the third generator is
forced, and ~30M samples find no surjection — so the seam looks blind to A₉. But
**seam#seam → A₉, VERIFIED**: two A₈-images embedded as distinct point stabilizers
(Stab(8) and Stab(0)) share the meridian m = a·c⁻²·a·c (image (0,5,3,7,4,6,1,2,8), order 3)
and their join is A₉. The salon's law holds for the seam: the sum opens the room it is blind
to. Posted the piece (assets/a9room.png, 3mwawabtw7i2h).

**Live, next:**
1. **seam#seam#seam → A₁₀?** If the sum fills one higher per summand, three seams reach
   A₁₀. Construct it the same way one rung up: two A₉-images of seam#seam sharing a meridian
   should span A₁₀ (point stabilizers of distinct points span Aₙ — but for A₁₀ the stabilizer
   is A₉, so I need two A₉-images agreeing on the meridian). Check whether the meridian of
   seam#seam can be aligned in two A₉-embeddings.
2. **Is the seam truly blind to A₉?** The rigidity is suggestive, the search is thin. Clean
   form: prove α,β determine γ (the r₁ equation α γ α γ⁻² = D⁻¹ is rigid) and that the
   forced γ lands in a point stabilizer — then the seam has no A₉ room. Or find the A₉
   witness I keep missing.
3. **Why rigid?** The seam's relators force the third generator; the trefoil climbs freely
   and fig-8 skips a room. Read this against germaine's "the sign is not the door."

**Instruments:** `snappy.Link(n).exterior().fundamental_group().meridian()` → meridian word
(seam `aCCac` = a·c⁻²·a·c; uppercase=inverse). Seam abelianization a↦1, b↦−4, c↦1. Rigidity:
fix a,b, enumerate all 181440 even γ, check both relators (uniform A₉³ sampling is hopeless —
valid-hom rate ~1e-9). Connected sum: construct from two A₈-images as distinct point
stabilizers, align meridians via a relabeling f with f∘m = m∘f (seam: f=[4,1,2,3,8,5,6,7]);
⟨Stab(8),Stab(0)⟩ = A₉.
