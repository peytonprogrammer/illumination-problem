# A geometric invariant of strict whole-copy factors

R22 mathematical hand argument. Pending independent review. This packet does
not use an optical scan or a fixed-room computational check. It addresses the
precise Euclidean factor in fold-route-contract.md, including its proposed
similarity extension. The universal W<=21 objective remains open.

## 1. Hypotheses and normalized triangle count

Let B be a finite strictly simple canonical45 triangle disk, with w maximal
walls. Every noncorner integer point of B must be even-even (A). Let a,b be
two distinct smooth boundary A points. Assemble m whole copies by Euclidean
similarities g_i, with disjoint interiors, strictly simple disk union Q, and
literal equality of inverse maps at every contact. Actual distinct interior
S,T map to a,b. Maps agreeing only modulo a symmetry are excluded.

Literal agreement at two distinct points of a seam forces equal similarity
scales. Connected positive-contact adjacency forces one common scale. After
applying g_0^{-1}, the accepted seam-reflection normalization makes every
copy canonical and preserves A. Call this normalized room Qhat. The
similarity argument is also proved directly here: distance between two fixed
points forces the relative scale to be one, and relative seam maps are the
corresponding base-wall reflections. No affine normalization is assumed.

Write I for the number of interior A points of B, s for its number of smooth
boundary A points, and c for the sum of its A-corner triangle fan sizes.
In particular s>=2 and c>=0. The exact Euler and A-incidence identities are

    w-2 = 6I + 3s + c,
    N_B = 8I + 4s + c
        = (4(w-2)-c)/3 <= 4(w-2)/3.

These identities follow because every canonical triangle has one A vertex,
interior A points have eight incident triangles, smooth A points have four,
and all remaining integer points are genuine corners. This is independent
of the historical optical certificate theorem.

The accepted whole-copy assembly identity, including diagonal bases and
all seam junctions, gives

    W = m(w-4) + 4 + D,       D>=0.

Since w>=8, put M=floor((W-4)/4). Necessarily m<=M. Whole copies with disjoint
interiors give the exact normalized area identity N_Qhat=m N_B. Consequently

    N_Qhat <= (4/3)m(w-2)
           <= (4/3)(W-4+2m)
           <= (4/3)(W-4+2M).                 (1)

Every count is an integer. In particular:

    W<=21 => m<=4, N_Qhat<=33, area(Qhat)<=33/2;
    W<=22 => m<=4, N_Qhat<=34, area(Qhat)<=17.

The first line deliberately uses the conservative floor of 100/3; no claim
that the numerical upper bound is attainable is needed. Area here is in
the canonical base unit, with triangle area 1/2. An arbitrary physical
similarity can multiply it by any positive square scale.

## 2. Similarity-invariant geometric restrictions

A strictly simple finite canonical triangle disk has an edge-connected
triangle dual graph. To connect any two points, take a simple dual path,
choose points on its shared edges, and join consecutive points inside each
convex triangle. Each of at most N_Qhat triangles contributes at most its
diameter sqrt(2). Hence

    diameter(Qhat) <= N_Qhat sqrt(2).

Every actual corner of Qhat is an integer point: it is a copy corner or a
junction of canonical full seams. Thus every nonzero maximal wall has
length at least 1, while every wall has length at most diameter(Qhat).
The maximal-to-minimal wall length ratio R(Q) is invariant under every
Euclidean similarity, so (1) implies

    W<=21 => R(Q) <= 33 sqrt(2);
    W<=22 => R(Q) <= 34 sqrt(2).              (2)

This argument applies to diagonal and orthogonal bases alike and does not
assume the physical room uses the normalized canonical unit.

There is also a marked invariant. The actual normalized S,T are distinct A
points, so their distance is at least 2. Therefore

    area(Q)/|S-T|^2 <= N_Qhat/8.              (3)

In particular this ratio is at most 33/8 for W<=21. This is a necessary
factor condition, not a newly proved condition for darkness.

For each fixed W, there are only finitely many such normalized marked
rooms up to translation: the canonical triangle tiling is locally finite,
the edge-connected disk contains a bounded number of triangles, and each
has finitely many integer A marks. Translating one vertex to zero puts all
triangles in a fixed finite neighborhood. Hence there are only finitely
many similarity types of marked rooms in this precise factor class at
fixed W. No types are enumerated in this proof.

## 3. An actual dark room outside the unrestricted Euclidean factor class

Use the accepted 22-wall orthogonal room Q0 in research-note.tex, with
cyclic vertices

    (-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),
    (2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),
    (5,1),(4,1),(4,2),(3,2),(3,3),(1,3),
    (1,2),(0,2),(0,1),(-1,1),

and actual interior S0=(0,0), T0=(2,2). Define the one prescribed room

    Q100 = {(100x,y):(x,y) in Q0},
    S100=(0,0), T100=(200,2).

This is an explicit construction, not a searched candidate. The invertible
linear map A=diag(100,1) preserves strict simplicity, the 22 genuine turns,
interiority and actual distinctness. Its integer vertices and orthogonal
walls make Q100 a finite strictly simple canonical45 triangle disk; both
actual endpoints are even-even A points.

Here is the exact optical equivalence. For a horizontal wall, the velocity
reflection matrix is diag(1,-1); for a vertical wall it is diag(-1,1).
Both commute with A and A^{-1}. The corresponding affine position
reflections are conjugated to reflections in the image axial walls.
Thus a finite ordinary billiard path in either room maps bijectively to
one in the other, with its actual endpoints, contacts and ordered legs.
One may use a common affine time parameter: at axial reflections the
magnitudes of both velocity components stay fixed, so image speed is
constant as well. All corners and forbidden contacts map bijectively;
no boundary glide is created by an invertible linear map. Any earlier
actual target visit also maps to an earlier actual target visit.

Consequently the accepted exact darkness of S0,T0 implies exact darkness
of S100,T100, for all directions and all finite reflection counts. No
surface-lift darkness is substituted for physical darkness.

For clarity, the original darkness dependency can be checked by hand.
Q0 is three copies of the five-square staircase with cells
(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3), folded by identity,
(x,y)->(x,-y), and (x,y)->(4-x,-y). Its only noncorner integer base
points are a=(0,0), b=(2,-2). Unfolding an ordinary a-to-b path gives
an even-even endpoint; the first primitive integer step has non-A parity
and would fold to a true base corner. The four removable convex seam
endpoints only reverse the projected velocity, which retraces to the
last a visit before reaching a new b. All other base-corner preimages
are actual room corners. Axis-parallel physical paths cannot connect
S0 and T0, since they differ in both coordinates; all other paths cross
the axial seams transversely. Additional physical boundary preimages
of a,b obey ordinary reflection and are handled by last-a/first-b
truncation. This proves the physical claim used above without a ray cutoff.

Every horizontal wall of Q0 has length 1 or 2, and every vertical wall
has length 1 or 2, as read directly from consecutive displayed vertices.
Q100 therefore has longest wall length 200 and shortest wall length 1:

    R(Q100)=200 > 34 sqrt(2).

Equation (2) rules out ANY factor of Q100 satisfying section 1, even
with a different strict canonical diagonal base, different copy count,
arbitrary common scale, and different literal seam decomposition. It does
not merely show that the original stretched base fails the definition.

Thus the unrestricted statement that EVERY canonical45 dark actual pair
admits the specified Euclidean-similarity strict whole-copy factor is
FALSE, already at 22 walls. This does not refute H, which is restricted
to W<=21, and does not exhibit a smaller dark room.

## 4. Consequence for the central necessity question

A proof of H at W<=21 must exploit that wall threshold: the same
implication is false as an unrestricted geometric explanation of physical
darkness. In particular it would force all putative dark W<=21 inputs
into finitely many normalized similarity types and the explicit invariant
bounds (2)-(3). Existing arithmetic endpoint rationality gives no such
height or denominator bound. Local reversal or an individual surface-dark
lift supplies neither whole-copy multiplicity nor these metric bounds.

The counterexample still uses the original parity optical mechanism after
a reflection-preserving AFFINE change of coordinates. It does not prove
that all parity or all folding explanations fail. Orthogonal necessity
might instead allow independent axis units, but that is a different
factor class; its reduction and wall bound must be stated and proved.
For rooms with three mirror directions, the accepted affine rigidity
lemma disallows general anisotropic reflection-preserving normalization.

This packet supplies an invariant and an actual counterexample to the
unrestricted Euclidean converse. It neither resolves the uncapped W<=21
goal nor warrants marking it complete. The next distinct question is
whether a threshold-specific argument can force an affine-compatible
factor, or a different necessary global reversal structure, from physical
darkness without assuming the desired decomposition.

## Dependencies and verification boundary

Exact source hashes accompany the review request. Used mathematical inputs:
fold-base-incidence-supplement.md (Euler/A incidence),
fold-wall-bound-scope.md (whole-copy assembly with D>=0),
fold-normalization-supplement.md (canonical and actual-A normalization),
fold-similarity-supplement.md (also rederived in section 1),
orthogonal-affine-bridge.md (also rederived for this explicit map), and
research-note.tex sections 1-3 (explicit room and physical darkness,
reconstructed in section 3). No historical k<=6 optical theorem is used
in deriving the obstruction or transporting the 22-wall darkness.
