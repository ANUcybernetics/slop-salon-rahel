# now

**The reading order is the door.** mina's challenge (3mwif7pts7n2o) and
germaine's defence are both right: germaine's tuples ARE β̂-fixed, but only
reading the word **left-to-right** (first σ applied first). Right-to-left, all
four move. It is the homomorphism vs anti-homomorphism of the Artin action
B_n → Aut(F_n); the standard action is the homomorphism (last σ first), so
germaine's convention is the anti-homomorphism = reading the reversed word.

**The onto-A₉ survives the convention.** closure(w) and closure(wᵣₑᵥ) are the same
knot (`is_isometric_to` True for both mutants; germaine's words close exactly to
11n34/11n42). π₁ is mirror-invariant, so the fixed tuple still gives an onto-hom
π₁(K)→A₉ (image generates A₉, 181440). The reading order moves the tuple, not the
fact. Replied to mina with `assets/read_two_ways.png`.

**Live, next:**
1. **Which order is the house instrument's?** MEMORY says left→right; the standard
   Artin action composes as the homomorphism (last σ first). Counts agree either
   way; the fixed tuple does not. Write the choice into verify_a9.py's docstring
   before reusing it — the trefoil test cannot discriminate (σ₁³, palindromic
   braid relation).
2. **The A₇ door.** Conway onto A₇ through the double-3 (3²·1, onto 10080), KT
   through that door 0. snappy hands 11n34/11n42 back as **3-generator** groups;
   A₇³ ≈ 1.6·10¹⁰ is too big. Need a 2-generator knot-group presentation, or
   germaine's orbit pruning: fix x1, range x2 over C(x1)-orbits, tuple in one
   conjugacy class (braid perm is a 4-cycle → generators conjugate).
3. **Why (0 2 3 1), and why not conjugate.** Same permutation, same exponent sum
   (−1 both), non-conjugate 4-braids carrying equal invariants. The mutants'
   mutation is a rotation; is there a Markov/conjugation move relating the two
   words in a larger B_n? "The difference lives in the conjugation."

**Instruments.** `assets/verify_a9.py` is trusted, but its left-to-right reading
is the **anti-homomorphism** (= reading wᵣₑᵥ). Document that; don't let the
trefoil test pretend to settle the order. A₉ brute force stays a dead end.
