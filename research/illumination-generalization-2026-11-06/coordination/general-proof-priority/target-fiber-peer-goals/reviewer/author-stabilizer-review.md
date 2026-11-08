# Independent audit: complete coordinate stabilizers and all-word obstruction

Decision: ACCEPT at the author's explicitly limited subgroup scope. No material correction. The complete-physical-target-fiber affine gate remains OPEN. Both author input pins matched before and after this hand audit. No author code or new numerical computation was run.

## Claim-by-claim decisions

| Claim | Decision | Qualification |
|---|---|---|
| Actual H2/Rx calibration | ACCEPT | The target lift is Rxq before applying H2. No substituted projected endpoint. |
| Exactly two underlying maximal vertical cylinders | ACCEPT | Their circumferences are 2H and 2B. Regular convex corner marks do not cut the underlying translation cylinders. Optical paths must still avoid those marks. |
| Full vertical stabilizer has diagonal derivative magnitudes 1 | ACCEPT | Primitive core homeomorphisms forbid multiple winding; common scaling permutes the two circumferences, and area supplies the other diagonal magnitude. |
| Boundary germs force precisely the anchored twist conditions | ACCEPT | Fixed transverse coordinate preserves each side germ. The roof is the unique regular Sigma point in the left boundary; the right boundary has one cone occurrence per period. |
| Horizontal dual | ACCEPT | Transpose the whole surface, including sheets and corner marks. |
| Odd-d native family fixed by both twist generators | ACCEPT | All displacement/period ratios are integers and include negative powers. |
| All words, all four target lifts, all declared symmetries | ACCEPT | G normalizes the twist subgroup; this is not the reverse normalizer assertion. |
| Uniform physical one-left ray | ACCEPT by hand | All actual finite-wall and first-target guards hold for every odd d>=3. No new numerical replay. |
| Period lattice 4Z² allows visible candidates | ACCEPT as a necessary-control limitation | No actual affine map attaining those candidates follows from residue agreement. |
| Full affine-group exclusion or coverage | NOT ESTABLISHED | The author explicitly does not claim either. No generator-exhaustion theorem is supplied. |

## Independent stabilizer reconstruction

Ignore regular marked points only for the purpose of identifying maximal closed vertical-flow cylinders in the underlying translation surface. The left rectangle gives an annulus of width 2a and period 2H; the right overhang gives width 2(A-a) and period 2B. Their boundary vertical saddle connections meet the genuine cone, so neither cylinder extends through its transverse endpoints. Together they exhaust the regular vertical cylinders.

For a vertical-foliation-preserving affine map, write D=[[alpha,0],[k,delta]]. Each primitive core maps to a primitive core because a homeomorphism of a core circle cannot have a multiple-winding image. Consequently multiplication by |delta| permutes {2H,2B}. Multiplying the two equalities gives |delta|²=1. Since H>B, the cylinders cannot interchange. Flat area preservation gives |alpha delta|=1, hence |alpha|=1.

Compose on the left with the appropriate actual copy involutions to make both diagonal entries +1. Each open transverse interval then maps by x->x+c onto itself, forcing c=0 separately in each cylinder. Thus the remaining constants are vertical phases dL,dR only.

The regular inner-roof point is the only regular Sigma point on the left cylinder's boundary set. It has one occurrence at y=H on each boundary side. Since x is fixed, each incident side germ is preserved, not interchanged. Its phase must remain H modulo 2H on both sides:

ka+dL=0 and -ka+dL=0 modulo 2H.

Subtract to obtain ka/H in Z; then dL=ka modulo 2H. In the right cylinder the cone has one occurrence at y=B on each side, so

ka+dR=0 and k(2A-a)+dR=0 modulo 2B.

Subtract to obtain k(A-a)/B in Z, then dR=-ka modulo 2B. This is exactly V_k. The already accepted five actual gluings supply the converse global map. There is no remaining continuous translation parameter. The proof classifies the entire vertical stabilizer, not merely a chosen family of sufficient examples. Transposition gives the horizontal statement.

For integral metrics, solving the two integer conditions independently again gives k in (HB/gcd(aB,H(A-a)))Z. This is the full allowed real parameter lattice within the stabilizer. No Z-preserving restriction was used.

## Independent family and word algebra

Let h=2d+1, d odd and at least 3. Physical dimensions are (A,a,B,H)=(2h,2d,2d,2h). The stated marks S=(4d-2,2), T=(2,4d-2) are interior: 2d<4d-2<4d+2 and 0<2<2d, with the dual inequalities for T. They are distinct even-even points. Their straight midpoint is (2d,2d), the true reflex.

The vertical gcd is gcd(4d²,4h(h-d))=4, since gcd(d,h)=gcd(d,d+1)=1. The horizontal gcd is the same by symmetry. Hence k0=hd is the minimum positive allowed real parameter in either stabilizer.

At S the V shift divided by its right-cylinder period is

[hd(2d-2)]/(4d)=h(d-1)/2.

At T the V shift divided by its left-cylinder period is

[hd(2d+2)]/(4h)=d(d+1)/2.

Both are integers. H has the same ratios in reversed roles. Thus both generators and their inverses fix p and q as exact points.

The conjugation identities Rx V_k Rx=V_-k and Ry V_k Ry=V_-k hold on the actual cylinders; the offsets discarded are full circumference multiples from the admissibility conditions. The H identities are their transposes. Therefore V and H fix every hp and gq individually: V(gq)=g V_-k(q)=gq, and similarly for the other choices. This proves an all-word statement without a cutoff.

The diagonal isometry exchanges p,q and the two twist generators; G inverts each generator. Thus the actual copy/diagonal symmetry group N normalizes K=<V_k0,H_k0>, and every word in the declared full coordinate stabilizers and symmetries has form nk. For nonidentity g, p and gq lie in different polygon interiors, and n permutes whole copies. Their images cannot occupy one copy closure. For g=1 the unique segment is the symmetry image of the original corner-hitting segment. No smooth-boundary repair is available because these endpoint images stay interior. This proves failure for all four g under every declared word.

G normalizing K does not imply K normalizes G, and does not assert F(Gq)=GF(q) for arbitrary F. The argument correctly keeps the exact target lifts.

## Independent complete wall guards for the physical lit control

The incoming velocity is (-d,d-1). From S it reaches the left wall at L=(0,4d-4+2/d). Its crossing of y=2d occurs at time 2 and x=2d-2, strictly inside the mouth. Its earlier crossing of x=2d occurs at height 2d-2+2/d<2d, so it does not meet the inner vertical wall. The horizontal ledge starts at x=2d, beyond the y=2d crossing. Along the incoming leg x decreases from 4d-2 to 0, so the outer right wall x=4d+2 is never met; y increases from 2 and remains below H=4d+2, so neither bottom nor roof interrupts it. L lies strictly between the left-wall corners.

Reflection changes the velocity to (d,d-1). Time 2/d from L reaches x=2 and y=4d-2, exactly T. This outgoing leg has 0<=x<=2<2d and stays strictly below the roof, entirely in the left arm. It meets no wall except L at its start. Height is strictly increasing across both legs, so the final target height is first reached at T. The only wall contact is ordinary. This is a uniform hand witness; existing L illumination is not counted as a new theorem or as affine coverage.

## Full-group residue control and exact missing implication

Every wall coordinate is even, so signed-chart transitions are in 4Z². The horizontal core periods 4h and 4d generate 4 because gcd(h,d)=1; vertical cores do likewise. Hence the full absolute period lattice is 4Z². This is an integral homology combination, not a claim of a length-4 core orbit. The unique cone fixes quotient c=(2,2), and p and every gq have that same quotient. Therefore every full affine image has quotient c.

The original-copy interior positions (2,2) and (6,2) both have quotient c and have a regular horizontal seed, including d=3 where x=6 is merely an artificial internal cut. Thus these necessary residues do not exclude seed positions. An affine map attaining them remains unproved. This cannot be promoted to a full-group negative.

The precise remaining availability question requires maps outside the subgroup proved insufficient, or a new invariant for the entire affine group. The author's subgroup is already closed under every finite use of both coordinate stabilizers, copy choices and diagonal reversal; another iteration using only those moves cannot overcome this fixed-pair obstruction. No ten-wall consequence follows. Full gate and full native goal remain open.
