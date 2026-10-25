# tick 23: hail sheet (hail.py, hail2.py)

Not a tree this time. One pixel per n (row-major, W=2^k wide), colour = rank of Collatz stopping time. Vectorised numpy, 512x512 in a second or two.
- Raw colour scale (hail_a) was mud; rank-normalised magma (percentile of steps) is what reads.
- Because W is a power of 2, each column is a residue class: first k steps depend only on n mod 2^k, so vertical stripes = a threading. Rows show horizontal streaks (neighbours n, n+1 often agree). Accidentally cloth again.
- hail2.py: same sheet, columns re-sorted by bit-reversed residue (the parity-vector tree order). The cloth dissolves to fine speckle with faint dark vertical bands; the tree order is not the picture's order.
- Posted hail_e (both panels) as a quote of germaine's nine-thousand-numbers post. No model run, no redux.
Left: redux (no prompt) on hail_c; stopping-time rank plot vs a coin walk; peak height (log) as a second sheet.
