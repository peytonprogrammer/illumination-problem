# Request: new proof ideas for a wall-count minimality theorem (round 1)

You are a research collaborator. Another model (the coordinator) has run
this programme and is out of routes. Your job is ideas, not execution: read,
think hard, and propose. Do not run room, ray, or direction searches. Do not
edit any file. Reply in under 900 words.

## Target

Billiards with point light sources. A pair (S, T) of points of a polygonal
room is *dark* if no finite billiard path joins S to T without hitting a
corner. Conjecture: every strictly simple polygon with vertices on the
square lattice Z^2, sides axis-parallel or at 45 degrees, and at most 21
sides has no dark pair of interior points. A strictly simple 22-sided
orthogonal room with exactly one dark pair is known, so 22 would be the
minimum. The orthogonal case alone (W = 2r + 4 sides, r reflex corners,
r <= 8) would already be a real result.

## Established (AI-reviewed, not refereed)

- r <= 2 (at most 8 walls), any real side lengths: every pair is lit.
  Proof by corridor and door lemmas on position types
  (`d15-small-r/theorems.md`). The same method leaves 578 of 13,608
  position-type pairs open at r = 3; 96% are chains of corridors with
  resonance conditions such as "lit unless L h / (w D) is a positive
  integer" (`d17-r3/r3.md`).
- Real-to-rational: in an orthogonal lattice room, if all rational pairs
  are lit then all real pairs are lit (`d16-real-to-rational/reduction.md`),
  except possibly one-parameter families S = (x, y0), T = ((k - a x)/b, v0)
  (`d24-one-parameter/family.md`).
- Structure of the known example: the room's double D(P) is a sphere in
  Q(1^r, -1^(r+4)), a square-tiled pillowcase cover. The dark pair comes
  from a degree-5 factor cover onto a smaller pillowcase cover in which
  both points lie over one pole. "Same-fibre conjecture": for lattice
  points of corner parity class, dark iff the minimal such factor
  identifies or separates the points in a specific way.
- Parity: lattice points fall in four classes mod 2. k = number of
  non-corner-class lattice points that are not vertices ("transparent").
  Computer-assisted theorem: k <= 6 and W <= 21 implies all lit. The
  conjecture for orthogonal rooms is equivalent to: k >= 7 implies all
  same-class interior pairs are lit.
- Exhaustive censuses: all orthogonal rooms with area <= 20 (9.45e8 rooms)
  and all diagonal-wall rooms with <= 32 half-square tiles.
- Finiteness (`d19-finiteness/finiteness.md`, `d19-23-review/review.md`):
  the dark locus in the stratum with two marked points is closed and
  GL(2,R)-invariant, hence a finite union of affine invariant
  submanifolds (Eskin-Mirzakhani-Mohammadi). Dark families that fill a
  whole stratum of base surfaces are enumerated for r <= 8: three exist,
  none contains a room. Not covered: closed orbits (every lattice room
  with rational points is one), torus-cover families, proper subloci.

## Dead ends (do not re-propose without a new twist)

1. Bounded number of reflections: false. A thin L room needs > 95.
2. Proving the same-fibre conjecture through monodromy groups
   (2-homogeneity of a point-pair action for groups containing A_n): the
   cusp-based plan was refuted; the route is equivalent to classifying
   pure-braid orbits on permutation 4-tuples.
3. Finite-blocking theorems (Apisa-Wright, Lelievre-Monteil-Weiss,
   Hubert-Schmoll-Troubetzkoy): lattice rooms are torus covers, where
   every pair is finitely blocked, so these give no constraint.
4. EMM finiteness is ineffective, and the number of closed orbits
   (square-tiled surfaces) is infinite.
5. Enumeration beyond area 20: the count grows too fast, and there is no
   size bound that reduces the conjecture to a finite check.
6. Twisting a one-parameter family to contradict the rational-coordinate
   theorem: reflections conjugate a twist to its inverse.

## The coordinator's own candidate ideas (critique these)

A. *Semialgebraic cover.* Fix a combinatorial type (r <= 8). The lit set
   of a reflection word is an open semialgebraic set in (side lengths, S,
   T), cut out by quadratic inequalities. Cover the projectivised
   parameter space by finitely many *word families* w0 c^n w1 (c a
   cylinder core), each certified symbolically, with thin-corridor
   degenerations handled by the families. About 2r + 4 dimensions.
B. *Twist orbits and visibility.* Dark pairs in a normalised room lie on
   a grid (1/D) Z^2. Darkness is invariant under the horizontal and
   vertical multi-twists acting on lift pairs. A dark pair needs its
   whole twist orbit to avoid direct mutual visibility. Prove an
   expansion or equidistribution statement for this action on pairs that
   forces a visible pair once k >= 7.
C. *Counting lower bound.* For a dark same-class pair every unfolded
   segment from S to an image of T passes through a vertex image. Turn
   this into an inequality between the number of vertices (at most 20)
   and a density of primitive directions, giving a direct wall-count
   bound without classifying anything.
D. *Induction on r by surgery.* Cut along a chord from a reflex corner to
   get rooms with fewer reflex corners; relate dark pairs of P to dark
   pairs or blocked door configurations of the pieces.

## What to return

1. A verdict on each of A to D: promising, salvageable (how), or dead (why).
2. Up to four ideas of your own that are not in the lists above. For each:
   the key statement, why it could be true, the first lemma to try, and a
   cheap test that would kill it. Prefer ideas that use something the
   lists above never use (for example: the reflection group structure,
   Klein-group symmetry of the unfolding, hyperelliptic involution,
   Siegel-Veech or counting asymptotics, discrete harmonic or transfer
   operators, tropical or piecewise-linear arguments, proof by
   contradiction from a minimal counterexample).
3. Your single best bet and the honest probability that it closes the
   orthogonal case.

You may read the files named above under
`.context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/`.
Read sparingly. Mark every claim as proved, cited, or guessed.
