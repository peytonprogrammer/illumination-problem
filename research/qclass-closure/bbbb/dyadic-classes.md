# Which 2-adic classes can a billiard path realize?

**Verdict.** In cov4181, a normalized orthogonal room with eight reflexes and 20 walls, a same-parity interior pair realizes exactly **one** of the three odd-coordinate parity vectors used in R22's proof. This rules out requiring each class across strictly simple normalized orthogonal lattice rooms with r≤8 (W≤20). Cov4181 has a corner-only class, so the BBBB-only version remains open.

## The dyadic point in R22

Take the source as origin in the development. For distinct same-parity interior lattice marks a legal orthogonal billiard path has nonzero displacement D with both entries even. Write D=k v, where k>0 is the gcd of its absolute entries and v is primitive, and put j=ν₂(k). The displacement to R22's intermediate point is

    D/2ʲ = (k/2ʲ)v,         (D/2ʲ) mod 2 = v mod 2.

Thus the parity of the odd-coordinate vector is **exactly the primitive direction parity**, at every valuation j≥1. The point can be several primitive steps along the trajectory. Its absolute parity after folding is a+v mod 2 for a source of parity a, since reflection in an integer-coordinate wall preserves coordinate parities. Only when j=1 does the halving procedure terminate at the temporal midpoint. R22 uses the absence of regular sites in all three off-source classes on the staircase together with its separate seam-reversal lemma. It does not require a fixed point in the source fiber. [R22 proof](../../illumination-publication/repository/preprints/twenty-two-wall/manuscript.tex)

## A 20-wall pair that realizes precisely one class

Use the named cov4181 pair S=(2,3), T=(4,3), source parity a=(0,1). I checked the regular lattice sites directly from the 28 cells printed in d66. A site is regular if its cell star consists of four cells or two edge-adjacent cells. The respective numbers of physical regular sites in absolute parities (0,0), (0,1), (1,0), (1,1) are 10, 8, 0, 11.

| Primitive parity v mod 2 | Absolute parity of the dyadic point | Verdict |
| --- | --- | --- |
| (1,0) | (1,1) | The direct horizontal chord realizes it at (3,3), with j=1. |
| (1,1) | (1,0) | Impossible. Every lattice site of this parity in the closed room is a corner. |
| (0,1) | (0,0) | Impossible for this pair despite ten regular sites. D66 first established this orbit exclusion. It has no recognized parity certificate. D144 independently reproduced the exclusion on all source and target lifts. |

For the last row, the first primitive step projects to the straight embedded pillowcase arc from a to d=(0,0). Each further step traverses the same arc in reverse or forward. A corner-free trajectory would give a live walk in the arc graph, regardless of how many steps separate the endpoints. All arcs of this parity are among the tested pure mapping-class states, by extending each primitive direction to a unimodular basis with a prescribed reduction mod 2. This invokes the complete saved orbit verdict, not the independent direction traces truncated at height 60. [Named-room data and verdict](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/README.md) · [Arc dictionary and implication](per-class-converse.md)

The independent d144 replay used 3,888 marked-origami states and confirmed that (1,0) has exactly the valuations {1,2}. Its 341 cov4181 direct-tracer comparisons agreed state by state. [d144 independent check](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d144-review-dyadic/review.md)

If “each class” also prescribes the valuation j, even the rectangle [0,2] × [0,4] fails: from (1,1) to any developed image of (1,3) the vertical displacement is 2 or −4 modulo 8. Therefore j≤2. Both values occur on vertical paths, directly to y=3 or via reflection through y=0 to y=−3. Neither path meets a corner. This rectangle example concerns the given lattice scale. Cov4181 already excludes two primitive parities at *every* valuation in normalized coordinates.

## The full valuation spectrum for a fixed room

For a same-parity lattice pair in an orthogonal room of n cells, fix a primitive parity c. The attainable j form a finite set, possibly together with an upper tail. More precisely, **if any j>⌊log₂(4n−1)⌋ occurs in c, then every j>⌊log₂(4n−1)⌋ occurs in that same c**. Also, if c occurs at all, it has a witness with j≤⌊log₂(4n−1)⌋.

To prove this, work on the four-copy translation unfolding with an oriented primitive direction v. Cut trajectories at all physical corner lifts. This includes convex-corner lifts even though their cone angle is 2π. Successive regular lattice hits form chains or cycles under the one-step partial bijection. There are at most 4n regular lattice states, because there are 4n squares and each regular state consumes four square corners. From a fixed source lift to a distinct target lift a chain supplies at most one travel count k<4n. On a cycle the counts are h+ℓC, ℓ≥0, where 0<h<C≤4n. The first arrival therefore proves the small-witness claim. Write b=ν₂(C). If ν₂(h)<b, every count has valuation ν₂(h). Otherwise the counts divided by 2ᵇ form a progression with odd difference. For any j≥b a nonnegative index can be chosen to make that quotient congruent to 2^(j−b) modulo 2^(j−b+1). Hence every j≥b occurs. A valuation above the stated cutoff must be in the latter cycle case, and a single direction v then realizes the entire upper tail. Every isolated valuation is attained by a count h or k at most 4n−1. In the tail case 2ᵇ divides the positive h<C, so b≤⌊log₂(4n−1)⌋ as well. Taking all directions and lift choices preserves the conclusion. This bounds the number of halving depths to consider for a fixed room; it gives no width-independent direction or area bound.

**What remains.** For the lighting goal it suffices to realize *one* primitive parity at *one* depth for each pair. BBBB guarantees regular sites in all three off-source classes. What it does not supply is an uninterrupted trajectory through one of those sites with the prescribed target downstream. The exact test is a common leaf through a regular relay; passing to deeper dyadic coordinates alone does not force one. [Relay criterion](per-class-relay.md)
