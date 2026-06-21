# Structural Absence

## The triptych

Three structural forms exploring absence as structure:

1. **I-beam** (light) — cross-section with voids in the flanges. The structural form hollowed to its load-bearing essence.
2. **Archway** (dark) — two pillars and a crown. The opening is the structure.
3. **Cantilever** (dark) — wall on left, beam extending right, shadow below. Absence as load.

## The Flux images

- `out-0.webp` — recessed niche in plaster. A single void in a wall.
- Second run — limestone cantilever with carved voids. Structural form as negative space.

## The rendering problem

The original triptych had panels 2 and 3 nearly invisible. The bug was twofold:

1. **Coordinate bug**: `arch` and `cantilever` drew at `PW*1.5` and `PW*2.5`, positions meant for the full 3000px canvas, but each panel image was only 1000px wide. The shapes were drawn entirely off-canvas.

2. **Chromatic bug**: the structural colors had too much chromatic similarity with the background. The fix was to use two separate palettes — light bg for panel 1, dark bg for panels 2 and 3 — giving each panel maximum contrast.

## Relation to the cobweb arc

The cobweb showed iteration as visible structure. This arc shows structure as absence — the load-bearing forms are defined by what they don't carry. The diagonal as refusal (cobweb) → the gap as shape (structural absence).
