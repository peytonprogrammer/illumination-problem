# Fold-darkness minimum for all polygons (theory request)

You are a research collaborator on billiard illumination. Read-only: no
file edits, no searches of rooms, rays, or directions. Reply under 1,200
words. Mark each claim PROVED (give the proof), CITED, or GUESSED.

## Background
A pair (S, T) of points in a polygon is dark if no billiard path joins
them without hitting a vertex. The fold-back lemma: let P be a polygon
tiled by d reflected copies of a smaller polygon R, so the fold map
f: P -> R induces a branched cover DP -> DR of the doubled polygons
(spheres with cone points). Suppose every point of P that lies on a
straight path between lifts of f(S) and f(T) and maps to a vertex of R has
total angle 2 pi upstairs over an angle-pi cone point of DR (a "pole").
A geodesic through a pole folds back, so if f(S) != f(T) and the parity
structure forces every path to cross such points, (S, T) is dark.
Known: for orthogonal rooms (R = the 5-cell staircase Q), the smallest
dark rooms by folding are the 22-wall room (d = 3? check
`d4-monodromy-blocks/`), and the wall formula for glued rooms is
W(P) = d (W(R) - 4) + 4 + 2 n3, n3 = reflex corners of P over convex
corners of R. Triangle bases: (1,2,5) triangle exact 32 walls, 30-60-90
exact 27, 45-45-90 at least 22 (`d7-review/review.md`). Read
`d30-rigidity-proof/rigidity.md` sections 2 and 3 and
`d31-run-dark-min/README.md` for the precise fold-back lemma, the parity
property, and the glued-room enumeration. All paths are under
`.context/illumination-generalization-2026-11-06/fable/directions-2026-11-09/`.

## Questions
1. General fold inequality. For a strictly simple polygon P with n sides
   tiled by d reflected copies of a rational polygon R (angles pi p_i/q_i),
   derive from Riemann-Hurwitz on DP -> DR and Gauss-Bonnet an exact
   formula or sharp inequality for n in terms of d, the angles of R, and
   the ramification over each vertex of R. Generalize the orthogonal wall
   formula above.
2. Darkness condition. State the general parity property for R: which
   vertices of R must have which angles (pi/2? any pi/m?) for the fold-back
   lemma to apply, and what "a geodesic through a point over a vertex of
   angle pi/m folds back" requires. Is fold-back possible only over
   angle-pi cone points of DR (vertex angle pi/2 in R), or also over
   other angles?
3. Minimize. Using 1 and 2, find the smallest n for which a strictly
   simple polygon P can be fold-dark, over all rational bases R. Is 22 the
   minimum, or can a non-orthogonal strictly simple polygon be fold-dark
   with fewer sides? Either prove a lower bound of 22 for fold-darkness,
   or describe an explicit candidate (R, d, gluing) with fewer sides and
   the pair. Note the known non-strictly-simple examples: a pinched 22-gon
   and a slit 20-gon; explain why strict simplicity costs walls, if it
   does.
4. Scope check. A claimed reduction: for rational polygons whose unfolding
   is not a torus cover, every dark pair comes from a fold (a translation
   cover collapsing both points to one) or from periodic points, by
   Apisa-Wright, "Marked points on translation surfaces" (Thm 1.3), plus
   finiteness of periodic points on non-arithmetic Teichmueller curves.
   Is this a correct reading for illumination (not only finite blocking)?
   What is the precise gap, if any?

End with the single most promising next step and your probability that
"fold-darkness needs at least 22 sides for every strictly simple rational
polygon" is true and provable.
