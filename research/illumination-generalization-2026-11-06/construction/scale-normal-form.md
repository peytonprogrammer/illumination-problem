# Structural scale audit: two hand lemmas

Author: Codex01a18403, 2026-11-06. New hand argument, no enumeration or optical search. Independent review pending. The uncapped objective remains open.

## Missing implication and bounded test

Can ordinary similarity normalization reduce every <=21-wall marked canonical45 room to bounded k? Success would be a valid uniform bound, or an explicit obstruction that forces a different mechanism. Strongest objection: long primitive geometry has unbounded area relative to the endpoint-to-wall clearance. We test precisely this, not hypothetical-dark-room reduction by arbitrary surgery.

## Lemma 1: rational marked polygons are exactly the same quantified problem

Let D be a finite strictly simple polygon whose vertices have rational coordinates and whose walls have directions 0,45,90,135 degrees. Let S,T be distinct rational interior points. There is a positive integer L for which every coordinate of every L-scaled vertex and mark is even. For example take twice a common denominator. Then LD is a finite union of canonical45 triangles and LS,LT are interior A points. Its maximal wall count is unchanged, and illumination is preserved in both directions.

Proof. A horizontal or vertical edge of LD lies on an integer coordinate line. A diagonal edge lies on x-y=2m or x+y=2m. Each of these complete lines is a union of edges of the canonical tiling: along a diagonal, its integer vertices alternate even-even A and odd-odd B; along a coordinate line, successive integer vertices give triangle edges. Thus no triangle interior is cut by the boundary of LD. Select all triangles with interior in LD. Strict simplicity implies their closed union is exactly LD, a topological disk, and the bounded polygon gives finitely many triangles. The complete eight-triangle star around each interior A mark lies in LD: the mark is interior and no tile interior is crossed by the boundary. Positive similarity preserves specular angles, finite segment counts and corner avoidance; its inverse does as well.

Conversely, canonical triangle disks and their A marks have integer, hence rational, coordinates and the specified four unoriented wall directions. Consequently the requested uncapped theorem is EQUIVALENT to illumination of all distinct rational interior marks of all rational-vertex polygons in these four directions with W<=21. This is an exact equivalence, not approximation of real data.

Scope. This does not imply illumination for arbitrary real marks or offsets. Rational approximation need not produce a uniformly valid reflection word or positive clearance at a limit.

## Lemma 2: even the best similarity cannot uniformly bound k

For integer n>=1 let D_n=[0,4n] x [0,4], S_n=(2,2), T_n=(4n-2,2); use n>=2 for distinct marks. This is a canonical45 disk with W=4; the direct segment illuminates the pair. Suppose ANY Euclidean similarity of ratio r>0 maps this marked room to a canonical45 disk, with both marked images interior A points. Rotation, reflection and translation are allowed; the new canonical presentation may differ completely from the old one. Then its k is at least 2n-3. In particular no uniform similarity normalization can put every marked room into k<=6.

Proof of the scale lower bound. Every interior A point carries its full canonical star, the axis-aligned square of side 2 centered there. Its width in every direction is at least 2, since the width in unit direction (u,v) is 2(|u|+|v|)>=2. The narrow width of the similar rectangle is 4r. Containment of even one full star therefore forces r>=1/2. Its area is 16n r^2>=4n and its triangle count is N=2 area>=8n.

Proof of the exception lower bound. Every canonical triangle has exactly one C vertex. At an interior C there are 4 incident selected triangles; at a smooth boundary C there are 2; at a genuine C corner there are either 1 or 3. (The four available C triangles have angle pi/2.) Let k_C count the first two types. Then

    N = 4 J_C + 2 s_C + sum_(C corners) m_C
      <= 4 k_C + 3 W <= 4 k + 12.

Hence k>=(N-12)/4>=2n-3. All incidence counts refer to the NEW presentation, so this proves more than failure to divide out a common integer factor.

Consequence. The unbounded k is not only redundant dilation. A scale-invariant aspect/clearance ratio obstructs bounded k even after optimal similarity. These rectangles are illuminated; the lemma does NOT refute a normalization only of DARK pairs, or non-similarity surgery. Any such reduction must use actual darkness in an essential proved way.

## Strategy consequence

Retire the unconditional similarity-to-k<=6 route. Do not run k=7 solely to extend the cap. Remaining credible structural mechanisms are (i) a darkness-dependent metric simplification with a proved direction of implication, or (ii) a theorem on the boundary turn pattern/unfolding rather than cover degree. Lemma 1 means the latter must handle unbounded rational edge-length ratios and rational mark denominators.

## Independent review request

Check Lemmas 1 and 2, especially full-line membership in the checkerboard triangulation, full-star containment for interior A, the arbitrary-rotation width bound, and the C-incidence inequality. No computational run is needed. Do not interpret acceptance as an uncapped illumination theorem.
