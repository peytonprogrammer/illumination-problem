# Independent bridge analysis — initial derived lemmas

The uncapped canonical45 theorem remains OPEN. The implications below are independent of any peer normal-form implementation; derived before inspecting that implementation.

## B1. Similarity reduction for rational octilinear data — PROVED, conditional only on the target theorem

Let P be a strictly simple polygon with rational vertex coordinates, all wall directions in {0,pi/4,pi/2,3pi/4}, and let S,T be distinct rational interior points. Choose a positive even common-denominator multiplier L making every vertex AND both marks even-even. Then LP has the same maximal-wall count and topology. Every horizontal/vertical wall is a union of canonical tiling edges. Each diagonal wall has slope +/-1 and even coordinate intercept, so it too follows canonical AB edges. A canonical triangle cannot straddle the polygon boundary without crossing one of these tiling edges; the bounded closed polygon is consequently a finite edge-to-edge union of full canonical triangles. Both marks are interior A points. Similarities preserve actual corners, specularity and the marked pair. Thus a proof of the uncapped canonical45 theorem implies illumination for EVERY such rational octilinear polygon/pair with W<=21. Conversely a dark pair in that rational class would scale to a counterexample to the target. There is no k bound needed or claimed in this embedding.

A common global rotation can be applied first if all directions share that rotated octilinear set and coordinates in that frame are rational. Rational slopes in arbitrary directions are not covered merely by being rational.

## B2. Wall count cannot bound exception count or lattice diameter — PROVED

For n>=3, [0,2n]^2 is a canonical triangle disk with W=4 and interior A pairs. Direct counting gives I=(n-1)^2, J=3n^2-2n, s_N=4n, k=3n^2+2n, N=8n^2. Thus any assertion W<=21 implies uniformly bounded k, I, N or raw lattice diameter is false. Similarity does preserve illumination but can change lattice presentation and its k.

Removing a common integer dilation does not itself bound geometry: rectangles [0,4]x[0,2n+1], n>=2, have primitive integer vertex coordinates, W=4, marks S=(2,2),T=(2,2n), and aspect ratio tending to infinity. Here I=n,J=5n,s_N=2n+5,k=7n+5,N=16n+8. These are illuminated convex examples, not dark pairs. They refute a raw finite-coordinate/exception bound, not a possible illumination-preserving normal form with a proved pair-preservation rule.

## B3. Affine mirror-preservation rigidity — PROVED

For an invertible linear map A, let Q=A^T A. For a wall with normal n, Euclidean specular reflection R_n is conjugated to the Euclidean reflection in the image wall for ALL incident directions iff Q commutes with R_n, equivalently n is an eigenvector of Q. Necessity: A sends the wall tangent to the image tangent; to send the reversed normal eigenvector to the image normal, its image must be perpendicular to that tangent, giving n^T Q t=0. Sufficiency follows from the two perpendicular eigenlines. A symmetric non-scalar positive 2x2 matrix has exactly two perpendicular eigenlines. Thus two nonparallel, nonorthogonal wall directions force Q scalar, so A is a similarity. Orthogonal rooms admit independent axis scaling; an octilinear room with an axis wall and diagonal wall generally does not. Hence the completed orthogonal corridor normalization is not a general canonical45 or arbitrary-polygon normalization.

In particular no Euclidean similarity maps a polygon whose pairwise wall angles are not multiples of pi/4 to canonical45 directions. A rational 3-4-5 right triangle supplies rational coordinates and slopes violating that angle condition. An affine map can change those angles but then fails B3 unless it is already a similarity. This refutes a blanket affine/similarity bridge to arbitrary rational slopes.

## B4. Stability gives openness, not the needed closedness — PROVED local implication; limit bridge OPEN

A finite corner-avoiding transverse specular trajectory is stable under sufficiently small perturbation of the polygon vertices and interior endpoints with fixed wall combinatorics. Unfold its fixed finite reflection word. The target image and segment depend continuously on the data; all finitely many intended line intersections stay transverse, correctly ordered, and strictly inside their edges. Compact subsegments away from bounces have positive clearance from other walls. Local transverse contacts retain the same actual mirror side. Therefore nearby data still have that legal word. Thus illuminated configurations form an open set. Dense illumination on rational inputs alone does NOT prove illumination at all limiting real inputs: this would need closedness or a quantitative compactness argument.

A sufficient compactness bridge would bound reflection count and supply uniform positive clearance/transversality/flight-length margins along an approximating sequence. Finite wall words could then be fixed on a subsequence and their nondegenerate paths passed to the limit. Neither the uncapped target nor the existing corridor theorem asserts those uniform bounds. No limit bridge has been established. A literature-backed actual example of failure of general closedness is a separate pending check, not assumed here.

## Scope still unresolved

[open] Uncapped canonical45 W<=21 target, including unbounded primitive aspect ratios and all marked pairs.
[open] Arbitrary real endpoints in a rational octilinear room; rational marked-pair density is insufficient without a new argument.
[open] Arbitrary real octilinear wall lengths/coordinates.
[refuted mechanism] A single affine/similarity reduction for arbitrary rational slopes using ordinary Euclidean reflection.
[open] Any materially different bridge to arbitrary polygon geometry and universal wall minimality.

## B5. General limit-closure bridge is actually false — PROVED using an accepted example and a primary theorem

Wolecki, Illumination in Rational Billiards, arXiv1905.09358v3, Definition1.1, Theorem1.2(i) and Lemma2.1: rational means angles in Q*pi; trajectories stop at polygon vertices; only finitely many point pairs fail to illuminate. This includes the already accepted orthogonal22wall room with distinct rational interior S,T. Fix that S and choose rational targets T_n->T avoiding its finite dark-target set. Each pair S,T_n illuminates, but S,T does not. Thus billiard illumination need not be closed even for a fixed rational orthogonal polygon and rational approximating endpoints. This directly refutes an unconditional inference from nearby illuminated data to the limiting pair. It does not supply a W<=21 counterexample or rule out a stronger low-wall compactness theorem.

Primary source: https://arxiv.org/html/1905.09358v3 (Definition1.1;Theorem1.2(i);Lemma2.1;Remark2.2 for removable vertices). Earlier fixed-source finiteness also appears in Lelièvre–Monteil–Weiss, Everything is illuminated, Corollary3: https://www.math.tau.ac.il/~barakw/papers/illumination.pdf . No new dark-pair construction is involved.

## B6. Arithmetic endpoint bridge independently accepted

[done] dark-endpoint-rationality.md WITH dark-endpoint-rationality-supplement.md is independently ACCEPTED; see its acceptance.json and construction peer full hand review. In rational-coordinate four-direction rooms, all distinct dark interior endpoints are rational. This removes the arbitrary-endpoint arithmetic gap CONDITIONAL on proving the uncapped canonical45 theorem. The k<=6 baseline is insufficient because endpoint-denominator scaling can change k. Irrationalwalls/arbitrarydirections remain open; no universal minimum inferred.
