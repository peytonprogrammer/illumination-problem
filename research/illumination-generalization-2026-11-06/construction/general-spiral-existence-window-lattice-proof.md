# GSE03: full-state lattice covering gives an actual ray

## Scope and relationship to prior work

This is a generalization/consolidation of the accepted projection/fiber method (LJ01), not a claimed new universal mechanism. It selects ALL source/cap/right/target indices at once, without preimposing a target divisor grid or a coprime right orbit. It proves actual path existence under the explicit inequalities below. Their universal availability is NOT proved. Full ordered-spiral, r3 and r<=8 goals remain open.

Use original ordered geometry 0<a<l<w<A,0<b<c<h<H, R=A-w, B=A-l. The accepted separated geometry a<l OR c<b is also allowed, with the remaining strict geometry as in GSE02. All widths and vertical coordinates, including source/target heights, are integral. Horizontal s,t may be arbitrary real interior positions. Put S=(s,u),0<s<a,b<u<H, T=(t,v),l<t<A,0<v<c and z=A-t.

## Elementary exact integer-lattice flag fact

For an integer rank-r matrix with r rows, its column image is a full-rank sublattice of Z^r. Its covolume is the gcd of its r-by-r minors. One proof is integer row/column Euclidean elimination: unimodular operations preserve the image index and gcd of maximal minors; diagonal form makes both the product of the nonzero diagonal entries. Equivalently use an integer lattice basis and Bezout column operations. This is not an area-only covering inference.

Project that image onto its first j coordinates. Let Delta_j be the gcd of the j-row minors of the first j rows, Delta_0=1. The possible jth-coordinate changes while all earlier coordinates are fixed form EXACTLY (Delta_j/Delta_(j-1))*Z. To see this, take a basis of the projected lattice in its first j-1 coordinates, lift it into the j-coordinate image, and append a primitive generator of the vertical kernel. Its determinant is the base determinant times that kernel step. Exact surjectivity onto the defined projection proves both containments and excludes missing fibers. Every selected lattice point has an integer preimage among the ORIGINAL columns.

Consequently a translated scaled image, scale c>0, meets EVERY open product window (-r1,r1) times ... times (-rr,rr) whenever c*Delta_j/Delta_(j-1)<2rj for every j. Select the first coordinate by nearest projection; then successively move in each exact kernel fiber. Strict inequalities handle nearest-point ties. This is constructive finite integer selection, not generic density and not simply a small determinant.

## Upper or mouth source: two-dimensional selection

Let h<=u<H and set C=2H-h-u, G=h-c, d=c-v, F=G+d, D=C+F. Fix the actual image +z; no opposite-image repair is needed for this sufficient theorem. For integers m,k,j define

 tau=((2m+1)A+z-s+2Rk+2Bj)/D,
 z1=s+C*tau-(2m+1)A,
 z2=z1+G*tau-2Rk.

Then z2+d*tau=z+2Bj EXACTLY. Varying (m,k,j) changes (z1,z2) by 2/D times the column lattice of

 [-AF,  CR, CB;
  -Ad, -Rd, B(C+G)].

The first-row gcd is H0=gcd(AF,CR,CB). The three two-row minors are ARdD,-ABGD,RBCD. Thus Delta2=D*Z0, Z0=gcd(ARd,ABG,RBC), and the exact sequential meshes are

 2H0/D, 2Z0/H0.

The first is STRICTLY below2R automatically: H0<=CR and C<D. Therefore Z0<R*H0 suffices for a lattice state with BOTH |z1|<R,|z2|<R, retaining exact actual target throughout. No g|K, parity, normalization, or coprimality is assumed.

For positivity choose any positive common multiple M of A,R,B. The integer increment

 (Delta_m,Delta_k,Delta_j)=(CM/A,GM/R,dM/B)

lies in the kernel of BOTH rows, increases tau by2M and has all coordinates positive. A sufficiently large nonnegative number of these increments makes m,k,j nonnegative and tau positive, preserving both exact residuals and actual target. No discarded negative-index solution is emitted.

## Lower source: three-dimensional selection

Let b<u<h. Use the actual upward source, X=h-u>0, C=2(H-h), G=h-c, d=c-v, F=G+d, D=X+C+F. For integers i,m,k,j set

 tau=((2m+1)A+z-s+2ai+2Rk+2Bj)/D,
 z0=s+X*tau-2ai,
 z1=z0+C*tau-(2m+1)A,
 z2=z1+G*tau-2Rk.

Again z2+d*tau=z+2Bj EXACTLY. The (z0,z1,z2) lattice is a translate of2/D times the image of

 [-a(C+F), AX, RX, BX;
  -aF, -AF, R(X+C), B(X+C);
  -ad, -Ad, -Rd, B(X+C+G)].

Its projection gcds are

 Delta1=h0=gcd(a(C+F),AX,RX,BX),
 Delta2=D*Z2, Z2=gcd(aAF,aRC,aBC,ARX,ABX),
 Delta3=D^2*Z3, Z3=gcd(aARd,aABG,aRBC,ARBX).

Explicit first-two-row minors, in column order im,ik,ij,mk,mj,kj, are
 aAFD,-aRCD,-aBCD,ARXD,ABXD,0.
The four three-row minors, in column order imk,imj,ikj,mkj, are
 -aARdD^2,aABGD^2,-aRBCD^2,ARBXD^2.
These expansions prove rank3 and all claimed gcds without suppressing any branch multiplicity.

The exact sequential meshes are

 2h0/D, 2Z2/h0, 2Z3/Z2.

The first is automatically below2a, because h0<=a(C+F)<aD. Therefore the TWO explicit inequalities

 Z2<R*h0 AND Z3<R*Z2

supply simultaneous |z0|<a, |z1|<R, |z2|<R for EVERY actual horizontal offset (s,t), with exact target image unchanged. This is a positive joint existence step, not separate solvability of target and guard conditions.

Choose M a positive common multiple of a,A,R,B. The increment

 (Delta_i,Delta_m,Delta_k,Delta_j)=(XM/a,CM/A,GM/R,dM/B)

is positive integral, annihilates all THREE residual rows and increases tau by2M. It makes all indices/slope physical after a sufficiently large finite number of repetitions. This operation preserves ONE final straight unfolded direction; it does not concatenate rays at different slopes.

## Actual original-room path and all corner guards

For the lower source, the upward source segment lies in the genuine left strip between u and h. The strict z0 gives a legal ascending h passage. For an upper source the formal rectangle starts at actual S; no source-arm wall is inserted above h. The cap exits descending at x=A-|z1|>w, so its ordinary sidewall/roof contacts and right-strip continuation are original walls. The strict z2 excludes the c reflex (w,c). The bottom width B>R matches both actual position and signed horizontal velocity at c. Its first descent to v ends at EXACT actual T since F_B(z+2Bj)=z. A zero residual is a smooth outer vertical-wall contact; the same signed fold identity applies through it.

A lower-source roof corner would force its h exit to equal its left h entry by rectangular reversal, impossible for disjoint left/right mouths. An upper-source formal roof corner permits the accepted exact-original-S suffix: at time2(H-u) the curve returns to S, before exit because C-2(H-u)=u-h>0. Emit only its regular suffix with its actual signed velocity. At u=h a corner would identify disjoint mouths, impossible. This uses accepted GSE01/GSE02 physical lemmas and does not permit passing a true corner.

The lower source has y>=u>b and x<=a; it cannot visit T before the final bands: either a<l<t, or the separated alternative c<b puts v below the source segment. Cap/right stages are above v and the bottom first reaches v at its final time. No source or target floor is needed in this theorem. Finite widths/times/slope give finitely many ordinary reflections.

## What is actually advanced, and what is still missing

The sufficient criterion now jointly selects every branch state with full actual target matching and no nominated target-divisor or right-coprimality premise. It applies to arbitrary admissible integer metrics and every actual horizontal pair under explicit gcd/width inequalities. It can be applied after a proved global isometry/reversal, with the exact transformed geometry retained.

It is related to accepted LJ01's projection/fiber construction; no claim of historical novelty or a new all-word mechanism is made. Unlike LJ01's chosen compatible grid followed by parity-based right-corner repair, this version includes the ACTUAL target index and strict right state as coordinates of the initial lattice selection. Both target images may separately enlarge coverage, but the theorem already works for a nominated +z.

The new inequalities have NOT been proved forced by r3, let alone r<=8. Failure of them says nothing about darkness, all-state existence, or repeated-contact paths. They are offset-free sufficient bounds; exact lattice-coset selection may succeed when a bound fails or is equal. This result must be independently reviewed and reconciled into the sufficient-route union. No census, numerical discovery, engine, new clock, worker, frozen-file edit or git mutation was used.
