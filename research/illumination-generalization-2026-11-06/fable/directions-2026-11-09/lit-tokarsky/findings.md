# Literature findings: Tokarsky lemma, known dark rooms, lower bounds

Subagent report, 2026-11-09, saved by the Fable coordinator. The subagent
could not open Tokarsky's 1995 paper (paywall). Every claim about its
contents is second-hand. Items marked "read directly" come from the arXiv or
publisher text.

## Tokarsky's triangle lemma

- **Wolecki, arXiv:1905.09358v3, Lemma 3.1 (read directly):** "Let Q be a
  triangle ABC with angles A of size pi/n and B of size m*pi/n for some even
  n and a positive integer m < n-1, then there is no billiard trajectory in Q
  from A coming back to A."
- Wolecki says this extends Tokarsky's Lemma 4.1. Tokarsky's own hypotheses
  are unconfirmed.
- The lemma covers 45-45-90 (n=4), 30-60-90 at the 30 degree vertex (n=6),
  30-30-120, and triangles that do not tile the plane. Wolecki's Figure 3
  uses (pi/8, 5pi/8, pi/4). The 9-72-99 triangle is (pi/20, 8pi/20, 11pi/20)
  and satisfies the lemma; no source for a room built from it was found.
- Proof idea: unfold 2n copies about A. Rotation by pi lies in the dihedral
  group, so the midpoint of a return path is a singularity.

## Explicit dark rooms

| Sides | Source | Built from | Status |
| --- | --- | --- | --- |
| 26 | Tokarsky 1995 | 45-45-90 | Count confirmed through Wolecki and Castro |
| 24 | Castro, Quantum 7(3), 1997, p. 42 | Modified 26-gon | Read directly |
| 22 | Wolecki, Theorem 1.3 and Figure 1 | 45-45-90 | Read directly |
| 22 | Monteil, unpublished | Unknown | Wolecki's acknowledgements only |

- Wolecki's Theorem 1.3: "The minimal number of edges of a polygon with at
  least one pair of points that do not illuminate each other is at most 22."
  The paper does not claim or conjecture that 22 is optimal.
- **Wolecki's 22-gon is weakly simple, not strictly simple.** Boundary cycle
  extracted from the figure's SVG, unit = triangle leg, dark pair (0,0) and
  (2,2):
  (-2,0)(-1,0)(-1,-1)(0,-2)(0,-1)(1,-1)(1,0)(2,0)(1,1)(2,1)(2,0)(3,1)(3,2)
  (4,2)(3,3)(2,3)(2,4)(1,3)(1,2)(0,2)(0,1)(-1,1).
  The boundary passes through (2,0) twice: a triangular notch
  (1,1),(2,0),(2,1) touches the outer wall at its apex.
- Unvetted Wikipedia or Wikimedia items: a 20-sided room with a slit, a
  4-sided room whose two points are vertices, and 24- and 27-sided rooms.

## Rooms from 30-60-90 or non-tiling triangles

None found in any source read.

## Lower bounds

- No source states or conjectures a nontrivial lower bound.
- Wolecki and Quanta (2024-02-15) both describe the minimum as open.

## Non-arithmetic rational polygons (read directly)

- Lelievre-Monteil-Weiss, Theorem 2 and Corollary 3: each point fails to
  illuminate finitely many points.
- Wolecki, Theorem 1.2(i): finitely many dark pairs in every rational
  polygon.
- Apisa-Wright, arXiv:1708.03411: Theorem 3.6 (not a torus cover: blocked
  pairs are periodic points, zeros, or identified by the Q_min quotient);
  Proposition 3.11 (torus cover iff Gaussian, Eisenstein, or rectangle-tiled;
  assumes no slits); Theorem 3.12 (prime-denominator triangles have only
  vertex pairs blocked).
- Apisa, arXiv:1710.05505, Theorem 6: genus-2 unfoldings that are not torus
  covers have only vertex pairs blocked.
- Apisa-Saavedra-Zhang, arXiv:2011.02668, Corollary 1.7: the
  (pi/2, pi/n, (n-2)pi/2n) triangle, n >= 5, n != 6, has only the pi/n vertex
  blocked from itself, and only for even n.
- No explicit dark pair in a non-arithmetic rational polygon was found.

## Hubert-Schmoll-Troubetzkoy (arXiv v2, read directly)

- Theorem 2: on Veech surfaces, each point has finitely many dark partners.
- Lemma 32 (staircase surface): for any point z, the points in
  pi_n^{-1}(-pi_n(z)) are not illuminable from z. So a dark pair on a
  square-tiled translation surface can be non-periodic. The constraint is on
  the pair: every connecting segment's midpoint is a 2-torsion point that
  lifts to cone points.
- No source restricts dark pairs to specific torsion classes.

## Implications for a minimality proof (facts only)

1. The best published bound is 22. No lower bound is known.
2. Wolecki's published 22-gon is weakly simple. The best published strictly
   simple example may be Castro's 24-gon (simplicity of Castro's room not
   verified).
3. Wolecki's lemma holds for every triangle with angle pi/n at A, n even,
   and all angles multiples of pi/n. A proof cannot restrict itself to the
   square tiling on the basis of the lemma.
4. Rooms that are not torus covers can have finitely many dark pairs.
   Apisa-Wright confine them to periodic points, zeros, or Q_min-identified
   points.
5. In the torus-cover case, no result forces dark points to be periodic or
   rational. The known obstruction is the midpoint-on-cone-points mechanism.

## Tokarsky note, 7 August 2000 (received 2026-11-11)

One handwritten page, `tokarsky-2000-08-07-plus-room.pdf`, sent by George
Tokarsky in reply to Daniel. Plus-shaped room with reflex corners D1..D4
and centre A1. Theorem: no pool shot from D1 to D3, D4, or itself; so D1
is an invisible point (corollary). Proof: label the room by its fold onto
a square; any shot between two D-labelled points must pass through A1,
since otherwise it folds to a square shot from D to itself. The room is
centrally symmetric about A1, so a shot through A1 continues to D2.
Coordinator reading: this is the fold-back lemma (a geodesic through a
transparent point over a pole of the factor folds back) used in d30/d31,
applied to corner points with the square pillowcase as the factor. It
predates our use and is a citable source for that mechanism. It concerns
vertex pairs, which the interior-pair target excludes, and gives no lever
on the open lit side.
