Advances: L1 — Direct geometric test for the three aligned 3-by-3 chambers with two corridors of equal length.

Set D=3k+4, k≥1. Chamber i is [iD,iD+3] × [0,3] for i=0,1,2; the two corridors occupy 1<y<2. Interior lattice marks are exactly (iD+u,v) for u,v∈{1,2}. Normalize same-row placements to y=1 by vertical reflection.

**Result.** Every two distinct interior lattice marks are lit, for every k≥1. Same-row marks at equal offsets in the two outer chambers require at least two horizontal reversals. Every other pair admits a path with none. The requested exactly-one-reversal construction for the previously open equal-offset pair is impossible. The replacement below uses the part of the middle chamber above the corridor.

### The one-reversal test

Take the outer marks at (u,1) and (2D+u,1), u=1 or 2. Exactly one reversal of horizontal velocity must occur either left of the source or right of the target. The only possible vertical walls there are x=0 and x=2D+3 respectively. Unfold at that wall, and also unfold all horizontal-wall reflections. Integral horizontal walls preserve the parity of the target ordinate, so the ordinate halfway along the unfolded straight segment is integral. For a left reversal represent the source at −u: the midpoint abscissa is D. For a right reversal represent the target at 2(2D+3)−(2D+u): the midpoint abscissa is D+3. Since 0<D<D+3<2D+3, the left-reversal midpoint is after the reflection at 0 and the right-reversal midpoint is before the reflection at 2D+3; both are on the physical rightward pass through the respective open mouths. Refolding preserves integrality. This rules out one reversal.

For completeness, zero reversals give midpoint abscissa D+u. For u=1 the straight segment in the vertically unfolded middle chamber has integral ordinate m one unit after entry. The global and middle-chamber vertical coordinates differ by a composition of integer-wall reflections, hence by y ↦ ±y+2m′ with integral m′; integrality is preserved. If a,b are its unfolded mouth ordinates, b=3m−2a. Both ordinates must have residue modulo 3 in (1,2), since middle-chamber folds preserve that interval modulo 3. For a=3t+1+ε, 0<ε<1, the residue of b equals that of 1−2ε, outside this interval. Horizontal reflection of the whole room and path reversal exchange equal offsets 1 and 2. Thus zero reversals are impossible for both.

### Equal offsets: a path in the middle chamber's upper pocket

Set L=D−1/2. Start at (u,1) heading right and up with slope 1/L. Use accumulated absolute horizontal travel as parameter. The path has four legs of travel L each, with a single reversal of vertical velocity at the roof.

1. The first leg stays in the open corridor band until it reaches height 2 at x=D+u−1/2. This is inside the middle chamber. It clears both ends of the first corridor.
2. Above height 2 the middle chamber has reflecting sides at local abscissas 0 and 3. Start there at local abscissa a=u−1/2. Unfold the sides. After travel L the ray reaches the roof y=3 at unfolded abscissa a+L=D+u−1. Its residue modulo 3 is u, so it misses both roof corners. Reflect at the roof. Every intervening side contact is strictly between heights 2 and 3.
3. After another L the ray returns to height 2. Its unfolded local abscissa is a+2L=a+6k+7, congruent to a+1 modulo 6. Because 0<a+1<3, folding gives local abscissa u+1/2 and rightward velocity. Both transitions at height 2 are strictly inside the chamber. The upper excursion crosses exactly 2k+2 vertical-wall images: the positive multiples of 3 between a and a+2L.
4. Continue right and down for travel L, strictly in the corridor band until the target. The final height is 1 and the final abscissa is D+u+1/2+L=2D+u.

These are segments of one billiard trajectory: in the full unfolding its slope stays 1/L. Only smooth walls are used. This is a prescribed formula in k with no denominator cutoff.

### All remaining placements

* Marks in one chamber see each other directly. For different rows and different chambers the open straight segment stays in 1<y<2.
* Same-row marks in adjacent chambers: take one bounce at the opposite corridor wall at the horizontal midpoint. In local coordinates that midpoint is (D+u+v)/2, strictly between 3 and D for all offsets because D>4. The halves have opposite vertical slopes and lie in the open band.
* Same-row outer marks with distinct offsets u,v: put H=2D+v−u, which is odd. Use increasing horizontal travel t from 0 to H and unfolded ordinate f(t)=1+3t+t/H. In a chamber fold f into [0,3] by reflection; in a corridor fold it into [1,2]. These prescriptions join with equal height and velocity at every seam. Indeed each seam has integral t, and z=1+t/H lies strictly between 1 and 2 there. At even t the shift 3t is a period of both folds, so both give z with positive derivative. At odd t both give 3−z with negative derivative: the chamber shift is 3 modulo 6 and the corridor shift is 1 modulo 2. Thus every mouth is crossed transversely in its interior. All horizontal-wall hits between seams are smooth. At t=H the slow ordinate is 2 and the odd shift folds it to 1 in the last chamber, giving the specified target. There is no horizontal reversal. For comparison, an exactly-one-reversal path is available for (u,v)=(2,1): unfold the source to −2 and bounce at height 2 at x=D−1/2 in the first corridor. The reflection at x=0 is smooth; one reversal is optional in this placement.

Vertical reflection handles the second row. These cases exhaust the interior lattice pairs, including k=6 (area 65).

**Wall-budget check and scope.** The proof uses equal corridor lengths, aligned unit apertures, 3-by-3 chambers, and D≡1 modulo 3. In particular, the pocket has horizontal period 6 and its entry and exit differ by one unit on the rightward sheet. No step uses W≤20 as an inequality. D152's 22-wall R22 arm does not have this three-square, aligned-corridor decomposition; its known dark base pair does not contradict this family theorem. The construction supplies no general 8-versus-9 reflex threshold. Within the stated family there is no remaining interior lattice pair. The smallest spacing D=4, the other equal-length residue classes, and unequal lengths are addressed separately in the [pocket lemma](l1-pocket-lemma.md).
