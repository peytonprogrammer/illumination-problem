# R35 supplement: a whole alternating thin-comb family

This supplement preserves the frozen R35 packet. It adds its zero-depth midpoint-return case and joins accepted A35 with the author's separately requested A37 zero-depth supplement. The A37 zero-depth supplement is now independently accepted in mouth-endpoint-seam-independent-acceptance.json. The whole-family join itself awaits peer review. The universal W21 goal remains OPEN.

## Empty midpoint arms in the actual far-wall return

R35's opposite-side matching and its terminal smooth far-wall midpoint version remain valid when the lower source is its actual interior tooth-mouth midpoint: D_s=0. Its floor is identically0 and its residual is exactly u/2, so its arm is empty. The finite-output iteration still has Phi(0)>0 and bound H/c; the other target depth remains positive. There is no floor jump from the empty arm, no reflection at its seam and no division by its depth. The actual path starts at the seam moving into the core. Its next open point is inside the core, so it is a legal initial direction from the actual interior source.

For the symmetric same-side return, both selected source and target depths can therefore be zero. The half-path starts at one actual seam midpoint, travels across the protected core and within the centered opposite tooth to its smooth far-wall midpoint. The local J-reflected reverse ends at the other actual seam midpoint from inside the core. No selected source/target tooth wall is used in this case, so unequal selected widths cause no issue. The splice is the same actual vertical far-wall reflection (-vx,vy). All strict target, corner and first-arrival guards in R35 remain valid. This is an extension of its stated positive-depth domain, not a reinterpretation of a frozen assumption.

The analogous smooth opposite-wall construction also allows both depths0: its two arms are empty and it is simply S -> opposite wall at mean height -> T, with exactly one smooth reflection.

## The complete family and its proof

Take an integer rectangular spine [0,c] x [y_min,y_max] with POSITIVE EVEN integer c. Attach any finite collection of globally vertically separated left and right teeth. Each tooth has width1, height2 and ODD integer lower band edge. All bands lie within the spine's height range; either extreme may meet a global end. The side word can alternate arbitrarily. No wall-count, k, area, vertical-gap, diameter or tooth-count bound is used.

Claim, using the independently accepted A37 zero-depth supplement: EVERY distinct actual interior even-even A pair illuminates. In particular this covers every W<=21 member, including alternating side words not covered by A35's two-block theorem.

Every A point strictly between x0 and c is inside the spine. There is no integer abscissa strictly inside a unit-width tooth beyond a spine side. An A point on x0 or c is actual interior only inside a tooth mouth. Since its band endpoints are odd and two units apart, its only even ordinate is the exact midpoint. Consequently every actual A point is either a strict-core point or one of these midpoint seams. This classification is complete; it excludes actual boundary gaps and corners automatically.

If one point is strict-core, connect directly to the other strict-core point or seam midpoint inside the core rectangle. If both seams lie on opposite sides, the accepted A35 zero-depth opposite-side construction applies (a direct segment also works in the convex core). For two seams on the same side, order their even ordinates y_S<y_T and put

    mu=(y_S+y_T)/2, h=(y_T-y_S)/2.

The positive gaps between their height2 bands imply h>1. Both mu and h are integers. Exactly one of the following holds at the opposite core side:

1. The mean point is a smooth actual wall point. Use the one-reflection empty-arm path.
2. The mean is strictly inside an opposite tooth mouth. Its endpoints are odd and its height is2; hence mu is its unique integer midpoint. The zero-depth R35 actual far-wall return just proved applies.
3. The mean is an opposite mouth endpoint. Every such endpoint is odd, so mu and h are odd, since y_S and y_T are even. The selected teeth have w1,D0. Thus w1 and c even imply c does not divide h*w. This is also implied by gcd(c+D,2(w-D))=2 not dividing h for D0. The A37 zero-depth extension gives an actual nonresonant far twist on the smooth side of this endpoint. GLOBAL integer positive gaps preserve the needed open unit mirror interval. For a tooth ending at mu, reverse vertical orientation. If the selected side is left, horizontal reflection x->c-x preserves the even spine width and the same arithmetic c,w1,D0.

The mean is strictly between the global ends and cannot be a global floor/ceiling corner. Positive gaps exclude two different opposite bands sharing the endpoint. The three cases exhaust it. Every construction ends at the original actual target and avoids all actual corners.

All allowed integer spine widths and vertical gaps are covered directly. There is no unsolved small-parameter rectangle or seed witness hidden in this family claim. This does not cover teeth wider than1, non-midline marks, overlapping opposite bands, odd spine widths, arbitrary orthogonal rooms or the universal canonical45 W21 theorem. Even core width is used in the exact endpoint-case arithmetic; it is not an arbitrary normalization.

## Exact prescribed whole-room controls

The separate checker builds the fixed alternating R-L-R-L band pattern[1,3],[7,9],[11,13],[15,17], with unit tooth widths and global spine height18, at prescribed c2,4,6. It independently enumerates ALL actual interior A points by physical polygon membership and constructs a path for EVERY distinct unordered pair using the exhaustive classification above. No failed ray or direction enumeration is used. It includes the genuine mean-mouth-corner case for the two right seams and the actual far-midpoint return for the two left seams. Its results are finite controls of the general hand proof and its accepted A37 dependency, not proof of the universal W21 theorem.
