# d37 brief: visibility-to-certificate (follow-up to d35 and d36)

Daniel approved one round, budget about 100k tokens. Theory only: no room,
ray, direction, or reflection-word discovery searches. Read-only checks on
the 22-wall room and P6 are allowed (cap: under 5 CPU minutes total).

## Task

Attack the step you named in d36 section 4, the one that decides the
target:

For an orthogonal lattice room with r <= 8 (W <= 20) and interior marks
S, T: if T is not illuminated from S, then some certificate exists, i.e.
a separating parity factor (common or per-class) or a rigid factor that
separates the pair.

Equivalently, the lit side: no separating certificate implies a legal
trajectory from S to T.

Your d35 reduction applies: the SL(2,Z) orbit of the marked square-tiled
surface is finite, and illumination becomes finitely many horizontal
visibility tests. The obstacle you named: partition closure combines
different monodromy words, but a trajectory keeps one direction.

## Ideas worth testing (pick, combine, or discard)

- Work direction by direction: for one primitive direction, the
  horizontal cylinder decomposition of the sheared surface decides
  visibility exactly. Characterize "no cylinder through both lifts" and
  ask whether, over all directions in one class, that forces a quotient.
- Use r <= 8: the bound on cone points limits how many cylinders can be
  blocked in each direction. The d25 counting lemma (path components
  p_d <= 4r + 4) may combine with the orbit's finiteness here.
- Use the d36 area bound (area <= 5r for a one-class separating quotient)
  and Theorem R (`d30-rigidity-proof/rigidity.md`) to restrict shape.
- If the full statement is out of reach, prove a named special case
  (for example, rooms whose SL(2,Z) orbit has one cusp, or r <= 5), or
  produce a concrete obstruction: an abstract configuration consistent
  with r <= 8 where visibility fails with no certificate.

## Deliverables

1. Proof, conditional proof with one named hypothesis, special case, or
   obstruction. Tag every claim PROVED / CITED / GUESSED.
2. Check on the 22-wall room and P6: the argument must produce their
   staircase certificates, and must not "prove" them lit.
3. Updated probability for the whole programme and the single next step.

State: `STATE.md`. Your replies: `d35-aw-torus/astra.md`,
`d36-amalgamation/astra.md`. Write to the -o file.
