# Full affine-group obstruction to ordered-pair straight-seed coverage

Status: independent HAND proof plus the ONE predeclared exact control PASS; pending reciprocal author review. This is a structural counterexample to the PRECISE stronger pair-seed criterion, not a dark room or a new illumination theorem. It allows both endpoints to move, arbitrary genuine global affine maps, any polygon copy, and regular boundary seeds. It does NOT require preservation of Z or fixation of the source.

## 1. Qualifying native input

Use the integral L room

    P=([0,8]x[0,4]) union ([0,4]x[4,8]),
    vertices (0,0),(8,0),(8,4),(4,4),(4,8),(0,8),
    S=(6,2), T=(2,6).

It is a finite strictly simple orthogonal canonical45 lattice room with six maximal walls and one reflex corner. Both specified marks are distinct, even-even and strictly interior. Let p,q be their EXACT original-copy lifts in the connected four-copy reflection unfolding M. Sigma contains ALL six physical corner lifts, including the five regular convex lifts.

Claim: NO affine homeomorphism F:M->M with F(Sigma)=Sigma takes this ordered pair to endpoints of a corner-free straight segment in the closure of any ONE identified polygon copy. The conclusion holds for orientation-preserving and reversing maps and WITHOUT requiring F(Z)=Z. In fact the same proof works for every integer dilation m>=1, with widths/heights multiplied by m and marks (6m,2m),(2m,6m).

## 2. Intrinsic absolute period lattice

Write a copy's translation chart coordinates as (epsilon_x*x,epsilon_y*y), epsilon_x,epsilon_y in {+1,-1}, using the physical x,y of P. Every vertical wall coordinate is 0,4 or8, and every horizontal coordinate is 0,4 or8. Across a glued wall the signed coordinates differ by twice that wall coordinate. Hence development modulo8 is well-defined on the WHOLE actual unfolding, and every closed absolute period belongs to 8Z^2.

There is a genuine regular horizontal cylinder core in the upper arm, between x0 and x4, with period(8,0); for example its physical height is6. Two ordinary vertical-wall reflections restore the exact unfolded sheet and direction. Similarly the lower right arm has a regular vertical cylinder core between y0 and y4, at physical x6, with period(0,8). Neither core meets a corner. These are actual closed regular curves, so their periods belong to the intrinsic absolute period group. Thus that group is EXACTLY

    Lambda=8Z^2.

This is not a redundant chosen lattice. Define the intrinsic integration map pi:M->R^2/Lambda from the corner(0,0). On the original polygon copy it is simply pi(x,y)=(x,y)mod8. This conclusion uses actual sheet gluings, not only an unlabelled billiard projection.

## 3. Every Sigma-preserving affine map fixes two quotient classes

Let F be ANY genuine affine homeomorphism preserving Sigma, with derivative D. It maps closed curves to closed curves and has an inverse, so D Lambda=Lambda. Therefore D is in GL(2,Z), with determinant+/-1. Integration gives an induced invertible affine torus map

    f(z)=Dz+b,     pi(F(x))=f(pi(x)).

The four copies of each convex physical vertex glue to one regular point of angle2pi. The four reflex copies glue to the unique cone point of angle6pi. No distinct physical vertices are identified with each other. Thus the five REGULAR convex marked points have quotient images

    (0,0),(8,0),(0,8) -> 0       [multiplicity3],
    (8,4) -> (0,4)              [multiplicity1],
    (4,8) -> (4,0)              [multiplicity1].

Since F preserves Sigma and distinguishes the cone point from regular points, it permutes these five regular marks. An invertible f preserves their image multiplicities. The unique multiplicity-three quotient image forces

    f(0)=0, so b=0 modulo8.

The unique cone point has quotient image c=(4,4), so F fixes that actual point and

    f(c)=c, hence D(1,1)=(1,1) modulo2.

In particular BOTH row sums of D are odd. No assertion about the generators, Veech group index, subgroup exhaustiveness, or an orbit census is used. These are necessary conditions for the FULL affine group, including maps not preserving the physical integer-point set Z.

## 4. Simultaneously moving both endpoints cannot produce a seed

Both original marks have coordinates congruent to (2,2) modulo4. Because b=0mod8 and D has odd row sums, any image of either mark, IF represented in the closure of the original polygon copy, must still have BOTH coordinates congruent to2mod4. Within [0,8]^2 the only coordinate choices are2 or6. Intersecting with the L leaves exactly three possible point positions:

    C=(2,2), R=(6,2), U=(2,6).

The fourth grid point(6,6) lies outside even the closed L room. None of C,R,U is on the physical boundary: its horizontal/vertical boundary coordinates are0,4,8. Thus regular boundary or smooth-wall-aligned seeds cannot evade this constraint.

The original ordered quotient difference is

    pi(q)-pi(p)=(-4,4)=(4,4)=c modulo8.

Under F it remains D c=c. Of the three possible same-copy positions, the ONLY ordered pairs with difference c mod8 are (R,U) and (U,R). In particular C cannot be used as either endpoint of this pair. Therefore, if both F(p),F(q) lie in the original copy, their physical coordinates are FORCED to be the same two arm points in one order or the other.

Their unique Euclidean straight segment has midpoint (4,4), the genuine reflex corner. It therefore meets Sigma and is not a permitted straight seed. This establishes failure while BOTH endpoints were free to move; it is not the retired source-fixed obstruction or an interior-only uniqueness argument.

For any OTHER identified polygon copy, compose F with the actual copy involution sending that entire copy to the original one. The Z2xZ2 copy-label action respects every pointwise physical-boundary gluing, is globally affine with diagonal +/-1 derivative, and preserves Sigma. It sends a straight regular segment in the chosen copy to one in the original copy. The preceding full-group argument therefore excludes that case as well. No target-sheet replacement is allowed or used.

## 5. The pair is illuminated: fixed one-reflection control

The room is NOT dark for this pair. Reflect T across the true left wall to(-2,6). The developed vector from S is(-8,4), so launch velocity(-2,+1). The prescribed actual path is

    (6,2) -> (0,5) -> (2,6).

It crosses the internal y4 portal at(2,4), strictly inside x<4. Its left-wall contact(0,5) is strictly between the original maximal wall endpoints0,8. The incoming and outgoing velocities are(-2,+1) and(+2,+1), so the reflection is ordinary and specular. Each leg stays in the actual room; all earlier heights are below6, so the first actual T time is4 at this normalized speed. It has one ordinary reflection and two legs. A prescribed check against all six finite walls per leg is authorized below; it does not supply the full-group proof.

BEFORE executing any check, the only prescribed control is the displayed room/marks/path, together with the displayed period generators, five convex residues, cone residue and three candidate seed positions. No rooms, directions, or group/orbit elements are searched. Existing pure exact geometry/path routines may be reused in reviewer-owned scratch only, with a direct exit-code check.

## 6. Consequence and exact limits

This disproves universal ordered-pair affine straight-seed coverage throughout the native L family, even allowing all Sigma-preserving affine automorphisms, moving both marks, regular boundary seeds, any copy, and dropping Z preservation. It consequently also refutes the version additionally requiring F(Z)=Z. The criterion was stronger than illumination; its failure does NOT refute known all-real L illumination or produce a qualifying actual dark counterexample for the broad native goal.

The coordinator conditional pair-transport theorem and its explicit uniform-source shear criterion can remain valid. This counterexample says their global all-target/all-pair coverage extension is false. In the displayed L metric the target T lies above the horizontal arm and in the left rectangle; the restricted vertical criterion indeed fails (K=2,gcd(K*(t+a),2H)=4 does not divide v=6), but THAT congruence is not the proof of full-group failure. Sections2--4 are the decisive invariant argument.

A future affine strategy would need a materially broader seed class (for example allowing a proved controlled multi-copy seed path) or a different actual optical mechanism; the present result supplies neither universal replacement. The unresolved ten-wall and full r<=8 illumination objectives remain OPEN. No native completion, reset, new numeric cap, discovery-clock restart, worker, engine, census, fitting, frozen edit or git mutation is justified by this subtask.
