# Empty-triangle composition: hand audit and limits

2026-11-02. User-authorized bounded hand audit. No discovery searches,
implementation or new numerical runs. Local proof below awaits independent
peer review; it is not a proof of universal pocket detection.

## 1. Precise setting

Use the raw canonical room P, its marked D4 unfolding X, and the developing
cover pi:X->E=C/(2Z+2iZ). Every physical corner maps to an integer class
in E, and all branch values belong to those four classes. Keep physical
corner marks even when they are regular on the unmarked surface.

An AUXILIARY edge is a developed straight path between two specified
A-lifts, with full displacement 2w for primitive integer w, through one
physical B/C corner at its midpoint. Its two open halves avoid every
physical corner. A chosen embedded pi-sector specifies its continuation.
Auxiliary endpoints may themselves be physical A corners: such edges are
not counted as solutions to the S/T problem. Only a final edge with the
actual interior S,T endpoints is an admissible S/T event.

All vectors below use the same oriented translation charts on X. Let
u,v be integer vectors with det(u,v)=1. Put

    p=0, q=2u, r=2u+2v,
    Delta=conv(p,q,r).

Orient its boundary p->q->r->p counterclockwise. The first two edge
midpoints are u and2u+v; the third is u+v.

## 2. Empty-face check

Because (u,v) is an integral basis, an integer point of Delta has
coordinates au+bv with a,b integers and

    0 <= b <= a <= 2.

The six possibilities are (a,b)=(0,0),(1,0),(2,0),(1,1),(2,1),(2,2).
They are exactly the three vertices and the three side midpoints.
There is no integer point in the open triangle and no further lattice
point on its sides. The three midpoint classes modulo2 are u,v,u+v;
they are distinct and nonzero because u,v form a basis modulo2.
The vertices all project to0 in E.

The open triangle projects injectively to E: it lies inside one
fundamental parallelogram for the basis2u,2v. Its image contains no
branch value. Each component of its inverse image is consequently a
flat open triangle mapping isometrically to it. This is a covering-space
argument on this specific empty face, not an assertion about arbitrary
geodesic triangles.

Its closure must be understood as a map from the ABSTRACT closed
triangle. Different boundary points or vertices can become identified
in X. No global embeddedness of the closed triangle is assumed.
Locally, a lift of a sector at a boundary branch value has the same
angle as that sector and embeds in the corresponding cone.

## 3. Conditional triangle-closing lemma

Suppose supplied auxiliary edges e1:s->a and e2:a->t have full developed
displacements2u and2v, respectively. Require:

1. a is a REGULAR point of X, whether or not its physical A label is a
   boundary corner. The two supplied edges share this actual lift a.
2. At their B/C midpoints, their chosen pi-sectors are on the LEFT of
   the respective oriented edges, so they face Delta's interior.
3. Their directions are read in the common translation chart at a.
4. s and t are specified actual interior S and T lifts for the final
   S/T conclusion; there is no relabeling or replacement of t.

Then the remaining side gives an auxiliary edge e3:s->t of displacement
2(u+v), through its sole B/C midpoint, with an embedded pi-sector on
the RIGHT of the s->t orientation. It is an S/T event when item4 holds.
Retain u+v non-wall-parallel when using the opening proposition.

### Proof

Along e1, choose the left-hand half-disk at its midpoint specified by
item2. It determines one component above Delta's open interior. Continue
this lift throughout that open disk, which has no branch values.
Its first boundary edge is exactly e1: away from its midpoint this is
uniqueness of path lifting, and at the midpoint the selected half-disk
fixes which continuation is used. Its endpoint above q is therefore the
supplied a, not merely another point in the same torus fiber.

At the regular point a there is one ordinary2pi translation chart.
The triangle interior there occupies the sector between the reverse
incoming u direction and the outgoing v direction. Its angle is the
Euclidean interior angle of Delta at q, strictly between0 and pi.
Thus its next boundary germ in direction v is the supplied e2 germ.
That germ is unique at a. Uniqueness along its first open half and its
selected left pi-sector identify the entire next edge with e2. Its
endpoint above r is consequently the supplied t.

The third boundary of THIS SAME lifted triangle ends at s. This follows
from the extension at p of that component; it is not an inference that
an even developed lattice point has the desired label. At the third
midpoint, the triangle supplies a local half-disk of angle pi inside
the actual cone. Its two boundary germs therefore give the required
embedded pi-continuation, rather than a continuation with extra turns.
Reversing this boundary edge yields s->t with interior on its right.

Its half-vector u+v is primitive: a common divisor of its coordinates
would divide det(u,u+v)=1. Section2 shows that its midpoint is the only
integer point between its endpoints. Rawness makes that B/C lift a
physical corner, and all other physical corners project to integer
classes. Neither open half can therefore meet a physical corner.
For non-wall direction, ordinary mirror crossings are transverse and
fold back to legal specular reflections. The prescribed interior
endpoint labels are unchanged. This proves the conditional claim.

The proof uses only the torus covering and marked-corner facts, not the
full planar fan tree. This is both a virtue (precise local control) and
a limitation (no new global endpoint-selection mechanism yet).

## 4. Exact limitation at a singular A intermediate point

If a is a zero of cone angle2pi*n, there are n germs with the same
ordinary developed direction. The holonomy vectors alone no longer
identify the outgoing e2 germ with the edge of the selected face.

One may replace regularity by an EXPLICIT angular compatibility condition.
Let alpha be the interior angle of Delta at q. The oriented sector from
the outgoing v germ to the reversed incoming u germ on the triangle side
must have intrinsic angle exactly alpha, with no additional2pi turns.
It must be the sector selected by the first face lift. A sector of
alpha+2pi*j, j!=0, fails the claim's identification premise. The same
pi choices are still required at both edge midpoints.

With that exact sector supplied, the proof extends. Merely matching the
directions modulo2pi, or having a connected endpoint graph, does not
supply it. No universal compatibility theorem is proved.

## 5. Two-interior-mark circularity and a possible auxiliary vertex

If P has exactly two interior A labels S,T and a is required to be an
interior A point, its physical label must be S or T. If it is S, the
input edge a->t already joins S to T. If it is T, input s->a already
does so. Different copy labels do not change this fact. Therefore
triangle closure using only interior A vertices cannot establish the
FIRST S/T seed in the important two-full-fan case.

The local lemma does allow a different sort of auxiliary vertex. A
physical45degree A tip is regular on X: its eight reflected sectors
have total angle2pi. It can be the intermediate a even though ending
an auxiliary edge there is not an ordinary optical S/T connection.
The final third side avoids that tip, and its endpoints remain S,T.
A regular boundary A vertex is therefore a genuine way to avoid the
interior-label circularity in the local construction.

What is NOT proved: that the two actual marks admit auxiliary edges to
one such a with determinant-one half-vectors, correct common lift and
compatible pi sides. Existence of arbitrary topological paths to the tip
or separate connections in unrelated directions would not suffice.
No auxiliary paths, directions or triangle chains were searched.

## 6. Pocket response is a second, independent requirement

Transport the abstract closed face with the material marking through the
pocket slide; do not assume its sides remain straight or its midpoints
remain geometric midpoints. Pull back the actual derivative differential
to that abstract disk. It has a vector-valued primitive F there, unique
up to an additive constant. Write c1,c2,c3 for the three actual midpoint
corner lifts, and set

    D1 = F(s)+F(a)-2F(c1),
    D2 = F(a)+F(t)-2F(c2),
    D3 = F(s)+F(t)-2F(c3).

These are exactly the relative midpoint-event defects of the three
oriented edges, from main26.1/31.1; reversing an edge does not change
its sum-of-arms event class. Fixed PHYSICAL endpoints do not imply their
F values coincide in this developed face. Corner-motion and accumulated
mirror terms are already included by the material differential.

Subtracting gives the exact relation

    D1+D2-D3 = 2*(F(a)-F(c1)-F(c2)+F(c3)).

Closedness of the differential does NOT force the right-hand discrete
second difference to vanish. Thus triangle closure supplies no automatic
additivity of the three event defects and does not imply D3!=0 from
detecting auxiliary edges. A genuine detection argument must evaluate
the actual collar crossings of the third edge (or prove a new geometric
constraint on these values). No arbitrary endpoint offsets are omitted.

## 7. Assessment and cost gate

The bounded local admissibility test has a complete hand proof, pending
independent review. It preserves the actual endpoint labels, primitive
halves and exactly a pi-sector under explicit compatibility hypotheses.
It does NOT prove global existence or nonzero response.

The next mathematical obligation, before any broader investment, is:
Does the planar raw-room structure force a compatible pair of auxiliary
edges through a regular boundary A point for the specified S,T, with a
third edge having nonzero actual collar count? This is still an unproved
assertion, not a result of the lemma or a new authorization for a search.

Two warning signs have been identified early: restricting to interior
auxiliary vertices is circular when I=2; and defect does not propagate by
simple edge addition. Do not expand into a triangle catalogue, general
path-shortening campaign, or implementation. Independent audit first.
