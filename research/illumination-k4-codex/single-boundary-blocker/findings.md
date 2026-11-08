# A single smooth boundary blocker: cylinder removal and the remaining case

[done] Written partial reductions and 6,361 exact algebra controls.
[waiting on Claude] Independent proof review requested.
No universal removal theorem or counterexample is established here.

## Question and outcome

Let P be a bounded strictly simple orthogonal polygon, s and t distinct interior
points, and z strictly inside a maximal wall. Paths have finitely many ordinary
specular reflections and stop at every actual polygon corner. Suppose s and t
are connected when z reflects normally, but become unconnected if z absorbs.
Can this happen?

Two reductions follow below.

1. It cannot happen if some lifts of s and t share an open periodic cylinder
   that avoids every corner lift. This includes regular convex corner lifts.
2. If the unfolding is translation-primitive and is not a torus cover, such an
   example would require periodic lifts of both endpoints and at least one
   periodic lift of z, in the orbit-closure sense of Apisa–Wright.

The first statement is elementary and applies to torus covers too. The second
is a conditional application of an existing classification, not a theorem
about all orthogonal rooms. In particular it does not cover our lattice rooms.
Neither reduction proves the common-cylinder hypothesis for arbitrary marks.

## Follow-up reductions

[critical-leaf.md](critical-leaf.md) extends the criterion to ordinary
cylinders with one exact invariant-central-core exception. It includes a
prescribed six-wall positive control and shows why copy symmetry alone gives
no new physical connection. [genus-two.md](genus-two.md) applies Apisa's
published classification to exclude every finite blocker set between
distinct interior marks in a non-torus six-wall orthogonal room. Both
applications await independent Opus review. The global question remains open.

## 1. The involution records exactly the corners

Use the standard four-copy unfolding M. Label copies by
G = {1, H, V, HV}, where H and V are horizontal/vertical linear reflections.
A smooth wall point identifies two copies, so it has two lifts. An interior
point has four lifts. At either a convex right-angle or a reflex 270-degree
corner, the four copies form a single vertex lift, with cone angle 2pi or 6pi.

The copy action iota = HV has derivative −I and satisfies

    pi(iota(x)) = pi(x).

It has no fixed point over the physical interior: there are four distinct
copies. It has none over a smooth wall: its two lifts are interchanged.
It fixes every corner lift, since all four copies there are identified.
Thus its fixed set is exactly the set F of actual corner lifts.

This uses strict simplicity: unrelated physical boundary points are not
identified, and no slit or pinch creates additional stabilizers.
Regular convex lifts belong to F even though they are not zeros of the
Abelian differential. They must remain prohibited as ordinary path contacts.

For a check of the topology, if r is the number of reflex vertices, then
there are r+4 convex vertices, W=2r+4 and g=r+1. The fixed count W=2g+2
also follows from Riemann–Hurwitz for the genus-zero quotient. This count is
not used as a substitute for the explicit copy-stabilizer proof.

## 2. Corner-free cylinders cannot contain both lifts of z

A marked cylinder here is an embedded open Euclidean cylinder

    C = (R/LZ) x (0,h),       L,h > 0,

filled by periodic geodesics and containing no point of F. Maximality is in
its unoriented direction, with every point of F treated as an obstruction,
including regular convex lifts. It is not enough to exclude cone singularities.
A periodic leaf avoiding F has a neighborhood of this kind; cut any ordinary
cylinder further at the parallel leaves through its regular points of F.

**Lemma.** C and iota(C) are disjoint for a maximal marked cylinder C.

**Proof.** The derivative −I preserves the unoriented direction, and iota
preserves F. Therefore iota(C) is another maximal marked cylinder in that
direction. Distinct maximal cylinders in the same direction are disjoint:
if they overlap, their parallel periodic leaves give a single larger cylinder.
There are corner marks, so the whole unmarked flat torus is not an exception.
If C=iota(C), cylinder coordinates put the restricted map in the form

    (x,y) -> (−x+c mod L, h−y).

There are exactly two fixed points, at y=h/2 and
x=c/2, c/2+L/2 modulo L. They belong to F, contradicting C intersect F empty.
Thus C and iota(C) are disjoint. QED.

Because iota swaps the two lifts of a smooth z, a marked cylinder contains at
most one of them. This is the additional restriction missing from an argument
about two arbitrary regular blockers on a translation surface.

## 3. Two winding connections remove that one blocker

**Cylinder theorem (written proof; independent review pending).** If lifts x of s and y of t lie in a common open marked
cylinder, then some ordinary billiard connection from s to t avoids z.

**Proof.** Enlarge to a maximal marked cylinder C. It contains at most one
lift b of z. If it contains none, any straight cylinder connection works.
Choose coordinates x=(a,u), y=(d,v). First suppose u!=v. For n in Z, the
straight segment in the cylinder universal cover from (a,u) to (d+nL,v)
projects to a connection entirely inside C.

A blocker can lie on this segment only if its transverse coordinate w is
strictly between u and v. Put lambda=(w−u)/(v−u), so 0<lambda<1. Its horizontal
coordinate must then satisfy

    b_x = a+lambda(d−a+nL) mod L.

If both n and n+1 met b, subtraction would imply lambda L is an integer
multiple of L, hence lambda is an integer. This is impossible. Consequently
at least one of the n=0 and n=1 segments avoids b.

If u=v, x!=y because their physical projections s,t are distinct. The two
complementary arcs of that periodic core circle have disjoint interiors;
a single b can belong to at most one. One arc avoids b.

Every constructed segment stays inside C, hence avoids all of F. Folding
produces a valid billiard connection; if it reaches the physical target early,
truncate there. It is finite: the compact segment has a positive distance
from the finite marked set and has only finitely many transverse seam
crossings. Axial seam coincidence would project onto a physical wall, whereas
both endpoints are interior, so it is not an exception here. QED.

This is a sufficient criterion. It does not say that a lit pair necessarily
has lifts in a common marked cylinder. A path can run along a critical leaf
bounded by marked corners while connecting its interior points.

## 4. What remains for rational-grid limits

Suppose, after an independent scaling of the axes, the room vertices and both
marks are rational. Any valid unfolded s-to-t connection has rational direction:
its developed endpoints are rational, since every reflection has rational
coefficients. Any reflection of it at z has rational coordinates. Thus an
essential z in this setting is rational as well.

Such a room unfolds to a square-tiled surface after a further common scaling.
In a rational direction, each nonsingular leaf is periodic or terminates at
singularities in both directions. Adding the finite rational corner marks cuts
some periodic leaves into finite marked segments. This follows directly from
the finite permutation of square-edge states in that direction, or by changing
an integral primitive direction to horizontal in the square tiling.

If a connection were carried by a periodic leaf avoiding F, its source/target
lifts would lie in a marked cylinder, contradicting essentiality by the theorem.
Therefore every ordinary connection in an essential-blocker example must lie
on a finite leaf segment whose two extensions end at actual corners.
It must pass through z once and nonaxially by the earlier no-repeat theorem.

This is a reduction to critical leaves, not a construction or their exclusion.
It supplies no new room, direction, word, reflection bound or ray catalogue.
The rational-grid assumption need not hold at a real degeneration limit.

## 5. A separate non-torus, primitive obstruction

Assume additionally that the translation surface M has genus at least two,
is not a torus cover, and admits no translation covering onto a surface of
smaller genus. Thus M=X_min in the notation of Apisa–Wright. Their Section 3
and Theorem 3.6 require the non-torus-cover hypothesis.

The canonical iota negates the differential. In this primitive case it is the
unique such involution and Q_min=M/iota (their Lemma 3.3). A fiber of Q_min
contains x and possibly iota(x), which both project to the same physical point.
Hence lifts of distinct physical s,t are never in the same Q_min fiber.

If z blocks the pair, the finite regular set

    B_all = {convex corner lifts} union pi^(-1)(z)

blocks every pair of lifts x of s, y of t. Reflex corner lifts are zeros and
are automatically prohibited. Apisa–Wright Theorem 3.6 now forces x,y to be
orbit-closure periodic points. Choose x,y joined by a corner-free path in the
undecorated room; such a lift pair exists by the question's premise. Any
inclusion-minimal blocking subset of B_all must contain a z lift, because that
path misses every convex corner lift. Their Theorem 3.16 forces every point in
this minimal blocker to be periodic. Thus at least one z lift is periodic.

In particular, if the only regular periodic points are corner lifts, no such
essential z exists, and no distinct interior pair can be finitely blocked.
The hypothesis on periodic points is an extra condition to verify, not a
classification asserted here. Nonprimitive coverings can identify distinct
physical points in Q_min, and square-tiled surfaces cover tori. Neither case
is covered by this argument.

## 6. Prescribed-point cylinder literature and limits

Nguyen–Pan–Su prove dense directions and dense union of closed geodesics through
a point that has one, and finiteness of points having none (Theorems 1–2).
Neither statement ensures a common cylinder for two prescribed points. Their
Theorem 3 applies to the specified hyperelliptic stratum components, not every
hyperelliptic Riemann surface with an Abelian differential. General orthogonal
unfoldings with r reflex corners lie in H(2^r); for r>=3 that is outside the
listed H(2g−2) and H(g−1,g−1) components. Regular corner stops are another
condition to retain.

Their Proposition 3.1 already uses the two-fixed-points obstruction for an
involution on a closed geodesic. The symmetry step in Section 2 above is related
to this published argument; no novelty claim is made. Adelstein–Desai–Ji–Zdeblick
construct oblivious points also on square-tiled surfaces. These abstract examples
do not supply an orthogonal billiard realization or an essential boundary blocker.

Primary sources: [Nguyen–Pan–Su, v3](https://arxiv.org/html/1712.09066v3);
[Adelstein et al., v2](https://arxiv.org/html/2008.08494v2).

## 7. Literature boundary and research decision

Wolecki Remark 2.2 distinguishes smooth reflections from continuation through
pi/n corners: the latter retraces the physical trajectory. It supports dropping
regular convex corner stops for connections between distinct physical marks,
but does not remove an arbitrary smooth boundary blocker. His finite-pair
results likewise do not imply removability. The cylinder proof above keeps all
corner stops explicitly, so it does not need that convention simplification.

Sources: [Wolecki, v3, Remark 2.2 and Lemma 2.1](https://arxiv.org/html/1905.09358v3);
[Apisa–Wright, Section 3, Lemma 3.3, Theorems 3.6 and 3.16](https://websites.umich.edu/~alexmw/ApisaWright.pdf).

Next useful target: can an essential boundary blocker persist when every
connection is on a critical marked leaf? A proof that one such pair has a
connection in a corner-free periodic cylinder would remove it immediately,
but that existence statement is still unproved. Alternatively, prescribe a
critical-leaf configuration and check whether all four target lifts can remain
blocked; two arbitrary point blockers alone are not enough evidence.

## Verification receipt

`check.py` passes 6,361 prescribed exact Fraction/copy-group controls: 5 lift
stabilizers, 18 invariant-cylinder charts, 3,168 consecutive-winding identities,
3,080 complementary-arc cases, 49 evaluations of the arbitrary-two-blocker
negative control, and 41 topology identities. These are algebra controls; the
written proof supplies the geometric and global implications. Run:

    python3 -B .context/illumination-k4-codex/single-boundary-blocker/check.py

## Subsequent resolution of the six-wall singleton remainder

The general question in this document is still open for higher-genus orthogonal rooms. Its entire six-wall L subclass, including rational/torus-cover shapes, is now settled by the elementary construction in `l-monotone-proof.md`.

Every interior pair has a corner-free connection using only vertical-wall reflections, and another using only horizontal-wall reflections. The target-image spacing argument forces a strictly interior portal crossing with q=distance/(1+r). A boundary blocker on a horizontal wall is avoided by the first connection, and one on a vertical wall by the second. The same proof avoids any boundary blocker set contained in one wall orientation. No monodromy assumption, rationality restriction or primary classification theorem is needed.

The separate Opus adversarial review accepts the proof, and the exact formula controls pass. The new statement rules out decorated dark six-wall limits with one retained smooth boundary blocker under our existing Jordan/mark/persistence hypotheses, including isolated8-to6 smooth-step limits. It does not settle mixed-orientation multiple-blocker sets, interior blockers, contacts/slits, boundary or merged marks, or higher genus. No novelty claim is made.
