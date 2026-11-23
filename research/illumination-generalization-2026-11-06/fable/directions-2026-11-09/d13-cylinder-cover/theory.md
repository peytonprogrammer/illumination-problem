# Cylinder certificates beyond one-cylinder directions: theory

This file holds the proofs. Every statement carries one of these labels:

- **[Proved here, unreviewed]**: a proof written in this file that no other
  agent has checked.
- **[Standard]**: a known fact about translation surfaces, used without proof.
- **[Computed]**: an output of the scripts in this directory. For commands, see
  `README.md`.
- **[Interpretation]**: a reading of the results, not a proof.

## 1. Setting and notation

P is a strictly simple orthogonal lattice polygon made of unit cells. int P is
its interior. A lattice point of the boundary is a *convex corner* (one cell
around it), a *reflex corner* (three cells), or a *flat boundary point* (two
cells, side by side). A billiard path reflects specularly at walls. It must not
touch a corner. Passing through a flat boundary point is a legal reflection. S
*illuminates* T when a billiard path joins them. The relation is symmetric:
reverse the path.

**Surfaces.** M is the four-copy unfolding. Its squares are pairs (cell c,
sheet e), e in {±1}², with chart z = (e1 x, e2 y). M is a square-tiled
translation surface. The projection π : M → P forgets the sheet; it's the
quotient by the Klein group K = {(±1, ±1)} acting on sheets. Σ is the set of
lifts of corners.

A straight segment in M that avoids Σ projects to a billiard path, and every
billiard path lifts to such a segment [Standard: unfolding]. Across an edge
between two squares of one sheet, the projected path continues straight. Across
a fold edge, which joins two sheets, it reflects. A square corner that isn't in
Σ projects to an interior lattice point (the path continues straight) or to a
flat boundary point (a legal reflection).

**Directions.** θ = (p, q) with p, q >= 1 and gcd(p, q) = 1. On sheet e the
M-direction (p, q) is the room direction (e1 p, e2 q). So sheets (1,1) and
(-1,-1) carry the *plus family*, the room lines qx - py = k. Sheets (1,-1) and
(-1,1) carry the *minus family*, the room lines qx + py = k.

In a rational direction on a square-tiled surface, every leaf is closed or a
saddle connection. The leaves through Σ (*singular leaves*) are finitely many
saddle connections. Their complement is a finite union of open maximal
cylinders [Standard]. A regular closed leaf lies in the interior of its
cylinder.

**DP.** τ = (-1,-1) acts on M with derivative -1 and commutes with π.
DP = M/τ. τ maps leaves of direction θ to leaves of direction θ. A *DP
cylinder* D is the image of C ∪ τC for an M-cylinder C. A convex corner c lifts
to one point ĉ of M (four quarter squares glue to a disc of angle 2π); τ fixes
ĉ, so ĉ is a pole of angle π on DP.

**Labels.** For S in int P and a direction θ:

- Λ_θ(S) is the set of DP cylinders D such that some lift of S lies in the open
  M-cylinders of D.
- K_D is π(closure of the M-cylinders of D), a closed subset of P.

## 2. Lemma A' and the full-cylinder consequence

**Lemma A'.** [Proved here, unreviewed] Let S ≠ T be points of int P, θ a
rational direction, D in Λ_θ(S), and T in K_D. Then S illuminates T.

*Proof.* Pick an M-cylinder C of D and a lift s̃ of S in C. By definition of
K_D, some lift t̃ of T lies in the closure of C or of τC. In the second case
replace t̃ by τ t̃. It's again a lift of T, because τ is in K. So t̃ is in the
closure of C.

Develop C. There's a surjective local isometry φ from the open strip
R × (0, h) onto C, with φ(u + w, v) = φ(u, v) and direction θ horizontal. φ
extends continuously to R × [0, h], and the extension maps onto the closure of
C. Each boundary component of C is a closed chain of saddle connections, and
the boundary lines of the strip map onto it [Standard].

Write s̃ = φ(u0, v0) with 0 < v0 < h, and t̃ = φ(u1, v1) with 0 <= v1 <= h.
For an integer n, let γ_n be the segment of the strip from (u0, v0) to
(u1 + nw, v1). Choose n so that the endpoints differ. If 0 < v1 < h, γ_n lies
in the open strip. If v1 is 0 or h, the relative interior of γ_n lies in the
open strip and only its endpoint is on the boundary line.

φ ∘ γ_n is a straight segment of M from s̃ to t̃. Its relative interior lies
in C, which contains no point of Σ. Its endpoints aren't in Σ, because S and T
are interior points. So it projects to a billiard path from S to T. ∎

**Boundary cases.** The proof covers each case the brief asked about.

- T on the boundary of K_D: on a singular line, on a saddle connection, at an
  interior lattice point, or on a cell edge. This is the case v1 = 0 or h.
- T at a flat boundary point: excluded, because T must be interior. The path
  itself may pass through flat boundary points; those are legal reflections.
- S on a regular non-generic line (the boundary between two open strips of one
  cylinder): S is in the open cylinder, so the lemma applies.
- S on a singular line of one family: that lift isn't in an open cylinder, so
  it contributes no label. The other family may still contribute one.
- S = T: excluded. Distinct room points have disjoint sets of lifts, so the
  choice of n above always exists.
- The path may pass through other lifts of S or T. That doesn't matter.

**Corollary A (full cylinders).** [Proved here, unreviewed] Call D *full* when
K_D = P. If D in Λ_θ(S) is full, S illuminates every T ≠ S in int P.

In a one-cylinder direction the single DP cylinder is full. Then Λ_θ(S) is
empty exactly when every lift of S lies on a singular leaf: S lies on a
singular line of both families. That is the candidate set X of Part A
(Lemma A and Theorem B). Corollary A is Lemma A.

**Theorem B'.** [Proved here, unreviewed] Let Θ be a finite set of directions.
Define the live set X'_Θ as the set of S in int P for which
Ill_Θ(S) (Section 3) doesn't contain int P. Every dark pair (S, T) satisfies
S, T in X'_Θ. If Θ contains a one-cylinder direction, X'_Θ ⊂ X.

X'_Θ is computable: `cover.c` returns it as a finite list of relatively open
cells, together with the uncovered region of each cell (Section 4).

## 3. Theorem C: the accumulated certificate

Full cylinders don't exist in the small class (iii) rooms: 0 of 102 rooms with
area <= 9, for every direction with p, q <= 9 [Computed, earlier session].
Theorem C uses every cylinder, full or not.

For a finite set Θ of directions, let

    Ill_Θ(S) = union over θ in Θ and D in Λ_θ(S) of K_D.

**Theorem C.** [Proved here, unreviewed]

1. S illuminates every T ≠ S in Ill_Θ(S) ∩ int P.
2. If (S, T) is a dark pair, then S and T are both in X'_Θ, T isn't in
   Ill_Θ(S), and S isn't in Ill_Θ(T).

*Proof.* Part 1 is Lemma A'. For part 2: if S isn't live, S illuminates T. If T
isn't live, T illuminates S, and illumination is symmetric. If T is in
Ill_Θ(S), S illuminates T by part 1. The last condition is symmetric. ∎

**Covering label sets.** Part 1 also gives the earlier "covering label set"
lemma: if the union of K_D over D in Λ_θ(S) is P for a single θ, then S
illuminates every T. That holds for points in two-cylinder directions whose
two labels together cover P.

## 4. Soundness of the exact computation (`cover.c`)

[Proved here, unreviewed] Each step of `cover.c` matches a statement below.

**4.1 Labels.** In cell (a, b) the open plus strips are k < qx - py < k + 1 and
the open minus strips are k < qx + py < k + 1. The program forms strip slots of
M, follows the permutation of slots, and merges slots across regular leaves by
union-find. That gives the M-cylinders. It then merges the two sheets of each
room strip, (1,1) with (-1,-1) and (1,-1) with (-1,1), which is the τ-quotient.

The lift of S on sheet (1,1) lies on the plus leaf through S. That lift is in
an open M-cylinder exactly when the leaf is regular. Then its cylinder is the
leaf's cylinder, which is also the label of the adjacent open strips. The lift
on sheet (-1,-1) is τ of the same leaf, so it gives the same DP label. The
minus family works the same way. So Λ_θ(S) is the plus label of S (absent on
a singular plus line) together with the minus label (absent on a singular
minus line).

**4.2 K_D.** The plus and minus lines cut each cell into closed faces
F(i, j): the closure of {i < qx - py < i + 1, j < qx + py < j + 1} within the
cell. π(C) is a union of open strips and the regular lines between them. π is
continuous and the closure of C is compact, so π(closure C) = closure π(C).
So K_D is the union of the closed faces whose plus or minus label is D.

**4.3 Cells.** Start from the relatively open cells that partition int P: open
squares, open interior edges, and interior lattice points. For each θ, split
every live cell by the singular lines of θ that cross its relative interior.
Inside a resulting cell no singular line of θ crosses, so the plus label is
constant along the cell. Adjacent open strips separated by a regular line carry
one label by construction. A cell that lies on a singular line has no label from
that line. So each Λ_θ, and hence Ill_Θ, is constant on each cell. The program
reads Λ_θ at one point of the relative interior: the centroid of up to three
hull vertices.

**4.4 The uncovered region.** For a cell, let U = int P \ Ill_Θ(S), the same
for every S in the cell. Each live cell carries Q, a finite list of closed
convex polygons of dimension 2. The invariant has two parts:

- (I1) U ⊂ union of Q.
- (I2) The interior of each polygon of Q lies in U.

Initially Q is the list of closed cells, and U = int P. For a new direction θ
with labels Λ = Λ_θ(S), the update replaces each W in Q by the 2-dimensional
pieces W ∩ F over the closed faces F of W's cell whose plus and minus labels
are both outside Λ.

- (I1) holds after the update. A point x of U that isn't in any K_D, D in Λ,
  lies in some closed face, and every closed face that contains x has both
  labels outside Λ. Otherwise x would be in that K_D. So the new U lies in the
  union of all pieces W ∩ F. The new U is open: int P minus a closed set.
  Pieces of dimension < 2 have empty interior, and a finite union of segments
  and points contains no nonempty open set. So dropping them keeps (I1).
- (I2) holds after the update. The interior of W ∩ F is int W ∩ int F. The
  first lies in the old U. The open face int F meets no closed face other than
  F, so it misses every K_D, D in Λ.

So Q is nonempty exactly when U is nonempty, and the union of Q equals the
closure of U. The computed live set is exactly X'_Θ, not an
over-approximation.

The program clips by maximal runs of consecutive kept strips instead of single
faces. Within a cell the union of the kept faces equals the union, over runs
[i1, i2) of kept plus strips and [j1, j2) of kept minus strips, of the closed
parallelograms i1 <= qx - py <= i2, j1 <= qx + py <= j2. The two sets are
equal, so the invariant is unchanged.

**4.5 Pairs.** For a room where every live cell is a point, `cover.c` lists
the pairs (s, t) of live points with t in the union of Q(s) and s in the union
of Q(t). By Theorem C every other pair is lit. Pairs of interior lattice
points are already decided by the Part A census. The rest are shot exactly
(Section 6).

**4.6 Arithmetic.** Every vertex is the intersection of two lines among
x = n, y = n, and qx ± py = k with p, q <= B. Its denominator divides
2pq <= 2B². Points are reduced triples of 64-bit integers, and products use
128-bit integers. The program aborts if a vertex denominator exceeds 10^9,
which never happened. Representative points have denominators up to 3(2B²)³
and are only used to read labels.

## 5. Obstructions

**Proposition O (pole pairs).** [Proved here, unreviewed] Let c1 ≠ c2 be
convex corners and Θ a finite set of directions. For θ in Θ, let D_θ(c) be the
DP cylinder whose closure contains the pole ĉ. Suppose D_θ(c1) ≠ D_θ(c2) for
every θ in Θ. Then there's r > 0 such that T isn't in Ill_Θ(S) for all S, T in
int P within distance r of c1, c2 that lie off the singular lines of Θ.

So no certificate built from Lemma A' with directions in Θ covers any
neighbourhood of (c1, c2), and X'_Θ has points arbitrarily close to c1 and c2.

*Proof.* Fix θ. Only finitely many singular leaves exist, and those that miss
ĉ have positive distance from it. Take a small disc around ĉ in M. The
separatrix through ĉ cuts it into two half-discs, and no other singular leaf
meets it. Each half-disc is connected and consists of regular points, so it
lies in one open M-cylinder. τ swaps the two half-discs, so both give one DP
cylinder, D_θ(c). A point S of int P near c, off the line through c, has all
four lifts in this disc. So Λ_θ(S) = {D_θ(c1)} for S near c1.

The same holds for T near c2: every lift of T lies in the open cylinders of
D_θ(c2). The open set D_θ(c2) is disjoint from D_θ(c1), so it is disjoint from
the closure of D_θ(c1). So no lift of T lies in that closure, and T isn't in
K_{D_θ(c1)}. Take r as the minimum of these radii over the finite set Θ. ∎

`poles.py` and the pole test in `cover.c` read D_θ(c) as the label of a strip
of c's cell that touches c.

**Proposition O' (corner and flat point).** [Proved here, unreviewed] Let c be
a convex corner and f a flat boundary point. Let A_θ(f) be the set of labels of
the open strips that touch f inside its two cells. Suppose D_θ(c) isn't in
A_θ(f) for every θ in Θ. Then the conclusion of Proposition O holds for (c, f).

*Proof.* f has two lifts f+ and f- = τ f+, each a regular point of M. Near f+
only the singular leaves through f+ can meet a small disc around it. So the
lifts of a point T near f, off the singular lines, lie in open cylinders whose
DP labels are in A_θ(f). Then argue as in Proposition O. ∎

**Remarks.** [Interpretation]

- Unmarking convex corners doesn't help. A merge across a leaf through convex
  corners stays inside one DP cylinder, because the pole has angle π.
- No one-sided chain of saddle connections joins c1 to c2 in the obstructed
  rooms tested. Pairs near (c1, c2) would need paths whose directions
  depend on S and T without bound. Deciding them is a renormalization problem.
  This directory doesn't solve it.

## 6. Exact shooting and its re-check

`shoot.py` decides a single pair (s, t) of rational interior points. Every
billiard path from s to t unfolds to a straight segment from s to an image
t' = (e1 t_x + 2m, e2 t_y + 2n). The script tries the images by distance up to
radius R. For each image it runs two independent exact tracers on the
direction v = t' - s for time in (0, 1]:

- a room tracer with specular reflection, failing at convex or reflex corners;
- a tracer on M, following the square gluings of `cyl.Surface`, failing at
  lifts of corners.

A pair is LIT when both tracers find t. The script aborts if they ever
disagree. A LIT result is a proof that the pair is lit, independent of
Sections 2 to 5.

## 7. What is unreviewed

Every result in Sections 2 to 5 is new and unreviewed: Lemma A',
Corollary A, Theorem B', Theorem C, the soundness argument of Section 4, and
Propositions O and O'. They rely on the [Standard] facts above and on the
Part A census for lattice pairs. Section 6 is a direct computation and doesn't
depend on them.
