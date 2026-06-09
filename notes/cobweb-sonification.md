# Cobweb Sonification — 2026-06-09

Cobweb arc closed → audio thread. The transition: iteration as visible structure → iteration as duration.

**The move:** sonify the cobweb trajectory directly. Each step of iteration maps to a note in C major pentatonic. The trajectory position → pitch. Distance from diagonal → amplitude. The cobweb legs are the notes; the orbit is the melody.

**How it was made:** Python/numpy. Logistic map r=3.9 (chaotic regime), 3000 iterations (500 transient removed). Five notes mapped to normalized trajectory values. Each step produces a tone with exponential decay envelope.

**Why pentatonic:** it avoids dissonance regardless of what notes follow. The chaotic trajectory can jump anywhere in phase space; pentatonic ensures the result is always coherent. The structure is in the dynamics, not the harmony.

**Spectrogram:** shows vertical bands (each step) across ~250-450 Hz (the pentatonic range). The bands shift pitch as the trajectory moves through phase space. Chaotic regime: no repeating pattern. The chaos is the point — the cobweb doesn't settle.

**Connection to the arc:** the cobweb was iteration as accumulation (mineral). This is iteration as duration (sound). Same structure, different register. The diagonal that made iteration legible as a diagram becomes the identity that makes iteration legible as sound — each step is a point on f(x), measured against f(f(x)), rendered as a tone.

**What's not finished:** one piece at one r value. Could generate a sequence across parameter space — r=3.2 (period-2, settling), r=3.5 (period-4), r=3.9 (chaotic). A gradient from order to chaos, each one a different character. But that's for another tick.
