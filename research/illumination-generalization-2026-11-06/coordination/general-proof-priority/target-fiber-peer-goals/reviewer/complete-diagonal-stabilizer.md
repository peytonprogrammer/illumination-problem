# Complete diagonal stabilizer and a symbolic all-word residual

CONDITIONAL HAND result, pending independent review. The sole additional geometric dependency is the frozen two-cylinder decomposition in reviewer/diagonal-phase-lemma.md (SHA256 1f505b9fc60e3d7720d50637063c861f485eb0009e8b3bda7ebf9012bb819fef), itself awaiting peer review. The accepted full coordinate-stabilizer theorem and exact source/target conventions are unchanged.

This does not settle the full affine gate. It explains why the d=3 modulo4 residual cannot be eliminated merely by arbitrary compositions of the complete coordinate AND diagonal stabilizers and room symmetries. It is a symbolic proof for every stated d, not an orbit census or a proposed finite direction cutoff.

## 1. Full diagonal-foliation stabilizer

Use normalized A=2d+1,a=B=d,H=A and d odd>=3. The two maximal diagonal cylinders have flow-time periods T1=8d+2,T2=6d+2 and transverse parameter widths W1=2,W2=2d-2, with velocity (1,1). Their actual circumferences are sqrt(2)T1 and sqrt(2)T2. They are different.

Any affine homeomorphism preserving the unoriented diagonal foliation permutes the maximal diagonal cylinders. A primitive core maps primitively. Common longitudinal scaling must therefore permute this two-element circumference set. Taking products forces its absolute value to 1; differing lengths prevent cylinder exchange. Area preservation forces the transverse scaling absolute value to 1 as well.

The genuine symmetries J=RxRy and D:(x,y)->(y,x) realize all four independent choices of longitudinal/transverse signs: J changes both; D fixes the longitudinal direction and reverses transverse. After composing by a member of <J,D>, the derivative is a unit diagonal shear in the longitudinal/transverse frame. Each transverse interval maps by translation onto itself, so the transverse offset is zero.

The remaining local forms are exactly longitudinal shears with a common coefficient k, plus one constant longitudinal phase per cylinder. These phases must be constrained by actual marked boundary germs, not chosen freely.

## 2. Boundary marks remove the longitudinal phases

The five regular physical corner marks in the signed cross model are:

- O=(0,0), the original origin;
- the midpoint class represented by (A,0);
- the midpoint class represented by (0,A);
- the four outer-corner class represented by (A,d);
- the four outer-corner class represented by (d,A).

The sole cone is represented by the four inner corners (plus their edge-identification germs). The regular midpoint classes lie INSIDE cylinder1 at delta=1. The two outer-corner classes lie INSIDE cylinder2 at r=d+1. O is the only regular marked point on the diagonal critical boundary graph.

In cylinder1, O has one occurrence on each boundary circle: at cumulative time 7d+2 on delta=0 and at time 3d on delta=2 in the explicit return tables. Since normalized transverse orientation is positive, each cylinder side germ is preserved. O is uniquely characterized among regular Sigma on that boundary, hence fixed. On either side its longitudinal displacement must be a FULL multiple of T1. This forces the constant lower phase to zero modulo T1 and k*W1/T1 integral.

In cylinder2 each boundary circle has exactly one cone occurrence: for r=2 it occurs at cumulative time 2d+2, while for r=2d it is the initial cone. These assertions follow from the frozen first-return tables; the other contacts are ordinary identified edges, with no other cone in a full period. The map fixes the unique cone and preserves each side germ. Thus the lower longitudinal phase is zero modulo T2, and k*W2/T2 is integral.

Consequently the normalized map is exactly the already constructed boundary-fixing F_k, with no additional phase freedom:

k/(4d+1) in Z,
k(d-1)/(3d+1) in Z.

The allowed real k are precisely k0 Z, k0=(4d+1)(3d+1)/gcd(d-1,4). Therefore

Stab(diagonal)=<J,D> * {F_(n k0): n in Z}.

This is the complete foliation stabilizer, not a classification of all affine maps. The antidiagonal stabilizer is its conjugate by Rx. All actual phases/sheets have been included; Z preservation was not assumed.

## 3. Coordinate twists fix the entire relevant branch fiber

Let U be the actual fiber of the intrinsic period torus over the cone. In normalized coordinates the lattice is 2Z² and its cone class is (1,1). In the signed cross, every U point has odd integer coordinates, with the usual edge identifications. All such points remain odd in either coordinate-cylinder chart because chart translations are even.

The minimum coordinate coefficient is lambda=dA. In the left vertical cylinder, lambda(x+d) divided by its period 2A is d(x+d)/2, an integer for odd x,d. In the right cylinder, lambda(x-d) divided by 2d is A(x-d)/2, also integral. Boundary points are fixed by the admissibility condition. Thus EVERY vertical generator fixes ALL of U pointwise, not only the original source and target. The horizontal dual does too. Their arbitrary products K therefore act identically on U.

This argument is exact period arithmetic; it does not enumerate U. Genuine affine maps preserve U because the period torus is intrinsic and the unique cone is fixed. Hence after any other affine move, K still fixes the resulting U points.

## 4. Uniform residual for d=3 modulo4

Let d=3 modulo4 and put, in the original normalized polygon,

p=(2d-1,1), q=(1,2d-1),
p1=(d-2,d+2), q1=(d+2,d-2).

All four are odd-odd, strictly interior, and satisfy x+y=2d. At d=3 the two ordered phases (p,q) and (p1,q1) are reversed rather than disjoint; the argument does not require them to be distinct sets.

Let F=F_k0. The frozen half-period calculation gives

F(p)=p1, F(p1)=p,
F(q)=q1, F(q1)=q.

The second equalities follow because the first points lie in the same cylinder at half-period phases, so a second application returns to the original actual point. Centrality of J gives the same toggles in the opposite (--)-copy.

For every z among p,q,p1,q1, the original reflected lift Rxz has signed x-y=-2d, and Ryz has x-y=+2d. Those diagonal lines are parts of the genuine cone saddle-connection boundaries shown in the frozen tables. Therefore F fixes ALL those (-,+) and (+,-) lifts pointwise. This is a boundary-point statement on the underlying surface; the marks themselves are interior physical endpoints and do not become forbidden corners.

It follows that on the finite SYMBOLIC set of copy-lifts of p,q,p1,q1, F preserves each quadrant copy separately. It toggles the pair phase 0<->1 in the (++),(--) copies and does nothing in the other two copies. No element of this set is on a physical wall, so its copy membership is unique.

The room symmetry group N=<G,D> permutes whole copies; D exchanges p with q and p1 with q1, while G only changes copy labels. K fixes all these points because they belong to U.

Consider ANY finite word in K,N,F, with arbitrary signed powers. If the initial target label g is nonidentity, p and gq begin in different copies. Each generator preserves the relation of unequal copy labels: K is pointwise identity here, F does not change either label, and N applies the same whole-copy permutation to both. Thus they remain in distinct copy interiors and cannot define a one-copy seed.

If g=1, both endpoints begin in the same copy with ordered physical pair (p,q). At every step they remain in one copy and in one of the two pair phases, allowing reversal of order: (p,q),(q,p),(p1,q1),(q1,p1). F toggles BOTH phases together when active on that copy; N swaps roles or copies, not phase; K does nothing. Every such pair has the physical reflex (d,d) as its midpoint. Hence its segment hits Sigma.

Therefore the ENTIRE group generated by the complete horizontal, vertical, diagonal and antidiagonal foliation stabilizers and all original copy/diagonal symmetries fails ALL FOUR target-lift choices on EVERY d=3 modulo4 control pair. This includes arbitrary alternations, not just powers of one diagonal map.

This is still a subgroup theorem. It asserts neither that these four directions exhaust affine behavior nor that the full gate is false. No new direction search or finite orbit traversal was used: invariance follows from symbolic generator identities.

## 5. A full-group direction-matching restriction

The coordinate foliation cylinder ratio is

Raxis=A/d=(2d+1)/d.

The diagonal and antidiagonal ratio is

Rdiag=T1/T2=(4d+1)/(3d+1).

An affine equivalence between two periodic foliations must scale all primitive core circumferences by a common positive factor. Their ordered circumference ratios must agree. Here their cross-product difference is

(2d+1)(3d+1)-d(4d+1)=2d²+4d+1>0.

Thus NO affine map on these surfaces can take a coordinate foliation to a diagonal/antidiagonal foliation, or vice versa. This is a necessary full-group condition based on actual cylinder lengths, not failure of one matrix test.

A map sending a coordinate foliation to a coordinate one is in the previously excluded coordinate/symmetry subgroup. A map sending a diagonal/antidiagonal foliation to either diagonal one is, after copy conjugations, in the complete diagonal stabilizer just classified, hence in the excluded enlarged group. Therefore on the d=3 modulo4 control pair, ANY successful affine map must send EACH of the four controlled projective directions {horizontal,vertical,diagonal,antidiagonal} outside that four-element set.

This is necessary, not sufficient: many words in the already excluded group also send those particular directions outside the set. It is NOT a finite direction list for a proof or search and does not justify adding directions one by one as a completion strategy. The full-group endpoint action/availability obligation remains unchanged.

## Status and coverage

The positive d=1 modulo4 affine seed in the prior packet is preserved. This conditional addendum isolates why merely using the entire minimal-diagonal stabilizer cannot settle the other residue class. It gives no new metric class, dark pair, reflection bound, ten-wall consequence or full-native-L coverage. The complete diagonal geometric dependency and this addendum both require independent review before acceptance. Frozen peer/coordinator files and previous receipts are unchanged; no new computation, census, worker, engine, git mutation or discovery-clock restart occurred.
