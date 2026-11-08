# Independent audit of the exact diagonal cylinder and endpoint phases

Decision: ACCEPT the stated hand theorem. For every odd d>=5 with d=1 modulo4, the specified native source/target pair admits the claimed genuine affine seed with the ORIGINAL Ry target lift. This does not establish other native pairs, the d=3 modulo4 class under the full group, all L metrics, or universal illumination.

The frozen base pin was checked. This audit derives the geometry and phases by hand and independently replays exactly the one prescribed d=5 path. No discovery search or replacement input was used. Native get_goal still reports the same goal BLOCKED; this scoped review does not assert activation or reset accounting.

## Actual model and first-return reconstruction

The signed cross has outer dimensions A=2d+1 and arm half-width d. Opposite outer vertical and horizontal boundaries are translated by 2A; the inner arm-wall pairs by 2d. The overlap axes are glued physical seams, not extra walls. Quadrant membership remains an actual copy label.

For cylinder 1, independently advancing (d+delta,-d) with velocity (1,1), 0<delta<2, gives the six flight lengths

d+1-delta, d-1+delta, 2d+2-delta,
d-1+delta, d+1-delta, 2d+delta.

After the successive translations these yield exactly the six representatives in the source table and return to the original point at time 8d+2. All durations are strictly positive. The inner side hits lie at heights d+2-delta and -d-delta, outside the central overlap, so they are genuine arm boundaries. Between them the central entries are internal crossings, not earlier wall contacts. The only positive crossing of x=d, -d<y<d per return has y=d-delta. Hence the return is primitive and different deltas index different orbits. At delta=0 or 2 an actual cone is reached, establishing maximality.

For cylinder 2 start at (d,d-r), 2<r<2d. If r<d+1 the event times are r,d+1,3d+r+1,4d+2,6d+2. At the left-to-top passage, entry through x=-d occurs with y=d+2-r<d; the later y=d crossing has x=r-d-2>-d. The next actual boundary is consequently the roof, not an internal overlap edge. Following the two subsequent translated legs gives the stated return.

If r>d+1 the event times are d+1,r,4d+2,3d+r+1,6d+2. The first outer wrap occurs at y=A-r in (1,d), followed by the left-arm top edge at x=r-3d-2<-d. The subsequent inner upper-arm contact is at y=3d+2-r in (d+2,A), and the roof contact at x=r-2d-1 in (-d,-1). On the final leg the lower-arm entry y=-d occurs before the central section, with x=r-d in (1,d). These inequalities verify the actual first-hit ordering and strict arm ranges.

At r=d+1 the two descriptions merge at the convex regular points represented by (A,d) and (d,A). Both orders give the same translated representative after the simultaneous identifications. No cone occurs there. It is legitimate to include this regular marked orbit when defining the underlying cylinder, although it would be forbidden as an optical ray.

The cylinder-2 orbit has no other positive central-section crossing. At r=2 it reaches the cone during the return; at r=2d it starts and ends at that cone. Its full primitive time is 6d+2. The ranges (0,2) and (2,2d) are disjoint, and the area sum (8d+2)*2+(6d+2)*(2d-2)=12d²+8d equals the four-copy surface area. The finitely described cylinder bands and their critical boundaries therefore exhaust the surface; no additional open cylinder is hidden.

## Global derivative and minimum compatible coefficient

Both local transverse coordinates delta and r-2 have gradient (1,-1). Advancing for time k*zeta along (1,1) thus has the common derivative [[1+k,-k],[k,1-k]]. Its two boundary displacements are full cylinder periods precisely when

k/(4d+1) and k(d-1)/(3d+1)

are integers. Both boundaries are pointwise fixed, the affine formulas agree across regular boundary arcs, and the inverse is the negative twist. The cone extension is a homeomorphism. The accepted genus-two symmetry lemma then preserves the regular physical corners as well; fixing the true cone alone is not used as a substitute.

The first condition writes k=(4d+1)m with integral m. Coprimality of 4d+1 and 3d+1, together with gcd(d-1,3d+1)=gcd(d-1,4), gives exactly the claimed minimum positive REAL parameter k0. No hidden restriction to a selected integer subfamily is made.

## Actual endpoint sheets and the positive residue class

Source p=(2d-1,1) is reached from the central section r=2d-2 after time d-1, before that section orbit's first wall. Its transverse coordinate is 2d-4. Coordinate swap D preserves cylinder 2 because the primitive periods differ and reverses its transverse interval; it places q at zeta=2. This determines actual levels without changing the target sheet.

Ryq=(1,1-2d) runs directly along the lower-arm cone connection to (d,-d), in forward time d-1. Rxq is its J image. Both are actual regular lifts on the diagonal critical graph, so the boundary-fixing twist fixes them pointwise.

For d=1 modulo4, the p displacement is 3/4 of the T2 orbit. Equivalently it is backward time (3d+1)/2. This backward leg crosses x=d at y=2-d inside the central section and y=-d at x=d-2 inside the lower-arm mouth; it reaches its endpoint before any genuine boundary. The result is exactly ((d-3)/2,-(3d-1)/2).

That point and ORIGINAL Ryq are distinct and strictly inside (0,d)x(-A,-d) for all d>=5 in the class. Their entire segment is in one convex open rectangle of the (+,-) original copy, avoiding every physical corner. Global inverse affine transport restores exact p and Ryq. Refolding and, if necessary, truncating at first physical T gives a legal original-endpoint trajectory. No F(Gq) to G F(q) substitution occurs.

For d=3 modulo4 both source and q shifts are half periods. Reading the appropriate return table yields Fp=(d-2,d+2); swap conjugates F to its inverse, so Fq=(d+2,d-2). Their midpoint is the reflex (d,d). Even powers restore the originals; odd powers restore this pair. The other two target lifts are fixed on critical boundaries and Jq remains in the opposite copy. Thus the source's all-power failure statement is correct for THIS twist, with its explicitly limited scope.

## Exactly one prescribed d=5 replay

Before execution, inspected the source script and the extracted trace/path_check functions. Reused only the existing pure rational tracer and independent finite-wall guard functions; old discovery entry points and timers were not executed. The supplied script was executed with only its result destination redirected to author/diagonal-d5-replay.json. A subprocess timeout of 30 seconds covered the entire replay.

Input: P=(0,0),(22,0),(22,10),(10,10),(10,22),(0,22);
S=(18,2), T=(2,18), velocity=(-84,-85).
Result: PASS, first actual T at exact time 4, 41 reflections, 252 wall-leg guards, no corner hit, no replacement or scan.

The direction also matches the hand derivation: k0=84, the native seed displacement is (0,-4), and the inverse derivative sends it to (-336,-340)=4*(-84,-85). The replay is one prescribed calibration, not proof by sampling of the quantified hand theorem.

## Verdict and limitations

ACCEPT all eight requested base checks. No material finding. The new endpoint-moving result is compatible with the accepted safe-twist obstruction: this smaller compatible twist is not required to fix the entire canonical branch fiber. The full native L gate and broad r<=8 goal remain OPEN.
