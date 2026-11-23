# No uniform reflection bound at bounded thickness

**Thin theorem (negative).** R(6,6) does not exist. In the normalized, strictly simple 16-wall cov279 stretch with q=12j+4, the distinct same-parity interior marks (q/2,1) and (3q,3) are lit. Every shot between them with R physical reflections satisfies

    R+1 ≥ √q/12.

The bounding height is six, hence τ≤6, and the horizontal tree has four pieces. This is an immediate application of the independently reviewed d117 estimate 1≤48(R+1)²t with t=3/q. Its affine horizontal rescaling preserves the specular law on axis-aligned walls, corner avoidance and the number of reflections. The proof unfolds the first crossing of the narrow door and the target. At t=0 the determinant of their two displacement vectors from the source is odd in the chosen coordinates. At positive t it is zero. This comparison treats *every* slope and reflection word, including repeated visits to the door. For any proposed bound R choose q>144(R+1)² in the given progression. The two-band congruence in the same note constructs a legal shot. [Proof](component-ends.md) · [Independent review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d117-review-ends/review.md)

In particular no union of words of bounded length covers this family, regardless of how the word-legality inequalities are represented. Fixed-word development gives affine endpoint images. Testing collinearity or the order of crossings generally introduces determinants, hence polynomial rather than necessarily linear conditions in all varying parameters together. The explicit lower bound is the obstruction even if exact semialgebraic tests are available.

## Fat follow-on: lit marks deep in large squares

**Claim for review.** In the normalized six-reflex st279 end-square stretches there are lit same-parity lattice pairs requiring Ω(√m) reflections, with marks at distance Ω(m) from the boundary of their respective end squares of side m. This rules out a bound depending only on r and a fixed lower thickness threshold. It does not rule out a bound growing with the *actual* square size.

Use the four horizontal intervals (0,m), (m−1,m+2), (m,m+3), (m+2,2m+2) at successive vertical depths m,1,1,m, starting from y=0. The room is strictly simple and primitive in each axis. [Named room coordinates](stabilizer-orbits.md)

**Constructing lit marks.** Put m=144k², k≥16, and s=6k+3/2, the developed horizontal displacement per unit upward travel. Prescribe the physical abscissas m−1/2, m+1, m+5/2 at the three consecutive seams, all on the positive horizontal sheet. In each width-three middle run, adding s amounts to adding 3/2 modulo six. Thus the ray crosses exactly as prescribed and misses all lips.

Write fold(z) for folding modulo 2m into [0,m]. Extend the line down into the lower square by vertical travel a and up into the upper square by travel b. The endpoint coordinates are

    S=(fold(m−1/2−as), m−a),
    T=(m+2+fold(1/2+bs), m+2+b).

Choose a=m/2+1+4i and b=m/4+1+4j with i,j nonnegative. For each coordinate start at i=0 or j=0, take the directed distance modulo 2m to the desired phase m/2 in the direction of motion, then round that distance divided by 4s to the nearest integer. This places both folded abscissas within 2s of the respective square centers. Both extra travels above m/2 and m/4 are at most 2m/s+5. In particular the endpoints are strictly interior. Since a,b≡1 modulo four and 2s≡3 modulo four, both unfolded abscissas are even integers and both ordinates are odd. Folding in integral walls preserves that parity. The two end legs remain inside open height ranges of full rectangles, so all their side reflections are smooth. This proves lighting by construction.

**Lower bound for every shot.** Divide both axes by m. As k grows the source and target converge respectively to S₀=(1/2,1/2), T₀=(3/2,5/4), with coordinate errors O(1/√m) by the preceding bounds. The first mouth crossing converges to p=(1,1) with error ≤1/m. Every mirror line lies within 3/m of a line with integer coordinate. Replace every mirror in any proposed word by that limiting line, retaining its orientation, and use its prefix at the first passage. No legality at the limit is assumed.

In coordinates multiplied by four, the limiting mirrors have coordinates divisible by four. Any developed image of p has both coordinates 0 modulo four. The target image has even abscissa and odd ordinate, while the source is (2,2). Its displacement to the p-image has coordinates (2,2) modulo four. Its displacement to the target image has even first coordinate and odd second coordinate. Their determinant is therefore 2 modulo four. In scaled coordinates its absolute value is at least 1/8.

For a real shot with R reflections the corresponding developed vectors are collinear. Each coordinate has magnitude ≤3(R+1) by summing physical segment displacements in the scaled bounding box. Replacing one mirror contributes at most 6/m to either coordinate error because the linear parts of the reflections agree. The errors in the two displacement vectors are consequently at most δ=C/√m+6R/m in sup norm for an absolute C, including the endpoint errors. Bilinearity gives

    1/8 ≤ 12(R+1)δ + 2δ².

If (R+1)/√m tended to zero along any subsequence, the right side would tend to zero. Thus the minimum number of reflections is Ω(√m). This does not count artificial seam or grid crossings as reflections.

**Access versus matching.** For any prescribed fixed side K, center a K-square at T inside the upper end square for large m. Every point of that small square has scaled distance O(1/√m) from T₀, uniformly. The identical determinant proof shows that even *reaching that specified square from S*, with the landing point free, costs Ω(√m) reflections. This last claim is about a specified square deep inside the remote chamber. Merely entering the entire upper m-square at its near lip is a weaker task. Neither statement rules out certificates that encode an unbounded number of physical bounces in a single modular transit.

## Remaining complexity question

Both lower bounds concern the expanded physical word. The lit thin control uses two monotone rectangular legs; the constructed fat shot has four. Counting transitions between bands while treating all transverse reflections within each leg by one folding congruence is a different complexity measure. Neither example forces that count to grow. No general bound on it is proved here.
