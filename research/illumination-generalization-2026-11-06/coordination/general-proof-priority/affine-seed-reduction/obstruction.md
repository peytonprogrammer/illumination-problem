# Native six-wall obstruction to affine reduction to a visible seed

Status: HAND proof plus prescribed exact check PASS. This obstruction is specifically to INTERIOR original-copy seeds. Smooth wall seeds are audited separately below.

## Fixed input and claimed implication failure

Let P have vertices (0,0),(28,0),(28,4),(16,4),(16,16),(0,16), with actual interior even-even source S=(26,2) and target T=(8,8). Let M be its actual four-copy reflection unfolding; Sigma is the full physical corner-lift set as in candidate.md.

Claim: NO globally affine homeomorphism of M preserving Sigma can send the original target lift to a directly visible interior point in the original polygon copy. This holds even without requiring the map to fix the source or preserve Z. Nevertheless the actual pair illuminates by one left-wall reflection, predicted below. Thus the universal affine orbit-to-visible-seed candidate is FALSE already for a six-wall L room.

## Primitive period lattice, computed by hand

All room wall coordinates are multiples of4. In reflected translation charts, transitions between copy coordinates differ by multiples of8 in each coordinate, because compositions of horizontal/vertical reflections translate by twice a wall-coordinate difference. Hence every closed absolute period belongs to8Z^2. Equivalently, global development modulo8 is well-defined on M.

There are regular horizontal cylinder core loops with periods (56,0) in the lower horizontal arm and (32,0) in the upper vertical arm. Their integral homology combination 56-2*32=-8 gives period (-8,0). There is a regular vertical cylinder core loop of period (0,8) in the right horizontal arm. Therefore the full absolute period lattice is EXACTLY Lambda=8Z^2. This is an intrinsic period lattice, not a chosen redundant lattice.

Define pi:M -> R^2/Lambda by integration, using the original (0,0) corner lift as origin, so pi on the original copy is simply (x,y) mod8. Since there is just one singular corner lift, the surface is connected of genus two, but no genus-two classification is needed below.

## Corner multiplicity invariant

Every affine homeomorphism F has one derivative A with A Lambda=Lambda. Thus it induces an invertible affine torus map f(z)=Az+b satisfying pi(F(x))=f(pi(x)). This follows by integrating the derivative along paths; the full period lattice makes the quotient intrinsic.

The five REGULAR convex corner lifts have these torus images:

- (0,0),(16,16),(0,16) all map to (0,0): multiplicity THREE.
- (28,0) maps to (4,0): multiplicity ONE.
- (28,4) maps to (4,4): multiplicity ONE.

The sole singular reflex lift (16,4) maps to (0,4). An affine homeomorphism preserves cone angle and hence permutes the five regular convex corner marks whenever it preserves Sigma. Since f is bijective, it preserves the multiplicity of their torus images. The unique multiplicity-three image forces f(0)=0.

The target T=(8,8) has pi(T)=0. Therefore pi(F(T))=0 for EVERY Sigma-preserving affine homeomorphism F, independent of its derivative or source behavior.

## Same-copy obstruction

The ONLY interior original-copy point with coordinates0mod8 is T itself. Indeed the lower arm has 0<y<4, so contains no positive multiple-of8 y-coordinate; the seam y=4 is not such a coordinate. In the upper arm, 0<x<16 and 4<y<16 force x=y=8. Boundary points are excluded from interior seeds.

The direct S-to-T segment reaches y=4 at x=20, outside the portal x<16. It is blocked by the actual wall. Consequently no Sigma-preserving affine image of T can be a same-copy directly visible interior seed. In particular G_p*T intersect V_p is empty.

## Actual illuminated pair and prescribed check

Reflect T across x=0 to (-8,8). The straight vector from S to that image is (-34,6), giving initial direction (-17,3). The predicted left-wall contact is (0,112/17), strictly between its endpoints (0,0) and (0,16). The entry at y=4 is x=44/3<16. Reflecting from that contact reaches T. Check the two legs against all six original finite walls with the existing exact checker; no ray search is needed.

This refutes only the sufficient orbit-coverage mechanism, not illumination. The conditional path-transfer proposition remains valid, as does its previous successful L calibration. Even replacing source fixation by preservation of the whole physical source fiber cannot repair THIS same-copy direct-seed obstruction; a materially broader seed condition would need a new proof.

## Boundary-seed qualification, declared before computation

The word "inside" in the previous candidate must be interpreted explicitly. The proof above excludes interior seeds. The transfer proposition also works for a seed on a smooth physical wall, as long as the segment approaches it through the original copy and the seed is not in Sigma. That broader sufficient condition is NOT refuted by the interior-point uniqueness argument: the distinguished torus fiber has smooth boundary points, including (8,0), (16,0), (24,0), (16,8), (8,16), and (0,8).

Indeed, for this same room the vertical cylinder charts have a central cylinder (R/32Z in y) at -16<x<16, and a right cylinder (R/8Z in y) at 16<x<40. Define V by (x,y)->(x,y+x+16) in the central cylinder, and (x,y)->(x,y+x-16) in the right cylinder. It is identity on all vertical boundaries (shifts0,32 or0,24), shares derivative [[1,0],[1,1]], preserves integer points, and preserves the corner marks: the two central-axis corners x0 shift by16 and swap; rightmost x28 shifts12mod8 and swaps its two corners; reflex seam and x16 roof corner remain fixed. Thus V maps T to the smooth bottom point (8,0). It does NOT fix the prescribed S=(26,2): that point maps to (26,4).

As a separate symbolic calibration, choosing source S0=(24,2) makes V fix the exact source (shift8mod8). Then V maps T to visible (8,0), while the direct S0-to-T segment is blocked (portal56/3>16). This explicitly shows why boundary seeds cannot be silently discarded in the broader mechanism. Prescribed checks may verify these formulas and the direct seed segment; they do not decide the enlarged source-fixed criterion for S=(26,2).

## Obstruction to an all-real source-fixed version

A further hand argument excludes universal coverage for arbitrary real endpoints, even allowing smooth boundary seeds. For a fixed finite translation surface with a finite invariant corner set containing a regular corner, its corner-preserving affine automorphism group is countable. Choose two nonparallel relative holonomy vectors based at a marked corner. Their images lie in the countable set of relative homology holonomies, so there are countably many possible derivatives. The image of that corner has finitely many choices, and a derivative plus its value at a regular point determines an affine map on the connected surface.

For a nonidentity affine map, its fixed set in a regular translation chart has area zero: it solves (A-I)x=-b, giving a line, point, or empty set when A differs from I. When A=I, a fixed regular point would make the map the identity by continuation. Thus the union of fixed sets of all nonidentity maps has area zero. Almost every interior source has trivial stabilizer. Choose such a source in an open set from which a given target is hidden in a nonconvex L room. Its target orbit is a singleton, and no visible seed of any allowed kind exists in that orbit.

This argument concerns arbitrary REAL endpoints. It does not refute the native integer endpoint criterion, whose sources occupy a special arithmetic set. It must not be used to claim a native lattice counterexample to the enlarged boundary-seed criterion.

## Verification receipt and final scope

`python3 -B obstruction-check.py` passed. It checked the fixed room's strict simplicity and actual even-even interior marks, the explicit period generators, all corner residues and their multiplicities, the direct portal failure, the one-reflection actual path against all twelve leg/wall pairs, the six smooth boundary candidates, and the explicit V boundary calibration. No alternate ray or affine orbit was enumerated. The global affine/period implications and the generic-real fixed-set theorem are hand arguments above, not formal proof-assistant output.

The preceding candidate.md said "inside" without explicitly distinguishing an interior seed from a smooth boundary seed. We must not use that ambiguity to claim the broader mechanism has been refuted. The precise conclusions are:

1. Universal reduction to an INTERIOR original-copy visible seed is false for native pairs already at W=6.
2. Reduction to an interior OR regular boundary visible seed remains unresolved for native pairs; it is strictly stronger in scope than the interior-only version, and the explicit S0 calibration shows the difference is substantive.
3. A universal source-fixed affine reduction fails for arbitrary REAL endpoints, with either seed convention, by the area-zero stabilizer argument.
4. The conditional transfer proposition remains valid whenever an appropriate affine map and legal seed segment actually exist.

For this route to contribute to the native universal theorem, it now needs a positive ARITHMETIC result including regular boundary seeds and exact source fixation. The all-real theorem cannot be obtained from this source-fixed mechanism. Further isolated successful paths do not prove that arithmetic result.
