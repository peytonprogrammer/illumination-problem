# d36 brief: per-class amalgamation (follow-up to your d35 reply)

Daniel approved one round, budget about 100k tokens. Theory only: no room,
ray, direction, or reflection-word discovery searches. Small checks on the
two named rooms below are allowed (read-only, cap: under 5 CPU minutes).

## Task

Attack the lemma you proposed in d35 section 4:

For interior marks and r <= 8 (orthogonal lattice room, W = 2r + 4 <= 20):
if each class partition B_b, B_c, B_d separates the pair, then
B_* = B_b v B_c v B_d separates it.

You showed pure monodromy invariance can't prove it (12|34 vs 13|24).
Use the geometry: room involutions (the pillowcase reflections), planarity
of the room, a reflex-corner charge, or the band lemma / Theorem R
(`d28-band-stabilization/`, `d30-rigidity-proof/rigidity.md`).

## Deliverables, in order

1. Either a proof, a proof under one clearly named extra hypothesis, or a
   concrete obstruction (an abstract configuration consistent with
   r <= 8 and all known constraints where amalgamation fails).
2. Test against the two known dark rooms:
   - the 22-wall room (W = 22, r = 9; exactly one dark pair), and
   - P6 (W = 28, `d30-rigidity-proof/`, `d31-run-dark-min/found.json`).
   For each, compute or describe B_b, B_c, B_d, B_* and say whether the
   lemma's conclusion holds there. A lemma that fails on them must use
   r <= 8 explicitly.
3. State what remains between amalgamation and "dark implies separating
   parity factor" (the visibility-to-certificate step), with your
   updated probability for the whole programme.

Tag every claim PROVED / CITED / GUESSED as before. Write to the -o file.
State repo is in `STATE.md`; your d35 reply is `d35-aw-torus/astra.md`.
