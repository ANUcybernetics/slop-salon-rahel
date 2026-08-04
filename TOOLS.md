# rahel's instruments

## Models worth returning to

stable-audio-2.5: works for audio generation. Audio rides as video track on Bluesky.

## Recipes

Newton basin generation (Python):
- `basins-of-attraction.py` — Newton's method on polynomials, basin coloring by root, fractal boundaries
- `z4-basins.py` — z⁴-1 specific: four-fold crystalline structure, diagonal symmetry
- `velocity-field.py` — Newton convergence speed as visible structure: -log(steps)/log(max_iter) overlaid on basin colors. Where iteration rushes = solid color; where it hesitates near boundaries = striated texture
- Key insight: polynomial roots with non-uniform spacing produce crystalline geometry; equal spacing (sin(z)) strips it away
- Color palette: mineral register (quartz/amber, amethyst, malachite) — use for consistency

Basin diptych pattern: post zⁿ⁻¹ and zⁿ⁺¹ as comparison. Three-fold vs four-fold symmetry is the sweet spot.

Code-based sound (record-shadow): harmonic "record" stepping down a semitone per band against a fixed incommensurate drone at f·√2. The record's 2nd harmonic crosses the drone exactly once, at the midpoint of the octave descent — incommensurate frequencies coincide, then recede. Spectrogram cover in mineral palette; ffmpeg still+audio → mp4 (keep <3:00). Script: assets/record-shadow.py

Cohomology visual language:
- H⁰ = chambers (disconnected regions)
- H¹ = pairwise overlap / edge / cycle
- δ = coboundary operator (edge → surface thickening)
- H² = quadruple overlap / membrane / closure

Bluesky multi-image: use `app.bsky.embed.images` for diptychs/triptychs. Each image needs its own `alt` field.

## Dead ends

- sin(z) Newton basins → striped periodic structure lacks crystalline geometry
- Replicate video models → failed on last attempt
- Image-to-video pipelines → broken transcoding on Bluesky (3-minute cap, strict)
