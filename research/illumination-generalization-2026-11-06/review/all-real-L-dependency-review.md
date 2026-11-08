# Independent reuse audit: every six-wall orthogonal room illuminates

Verdict: ACCEPT the existing l-monotone-proof.md as an unconditional theorem for every distinct interior pair in every strictly simple orthogonal six-wall room, with arbitrary positive real dimensions. This is a historical dependency recovered and independently checked here, not a newly discovered theorem or a new census.

## Geometry and quantifiers

After a rigid change of coordinates, any strictly simple six-wall orthogonal polygon is an L. There is one reflex corner and five convex corners by the orthogonal turn identity. Its two horizontal levels on one arm and two vertical levels on the other give

    P=([0,A]x[0,c]) union ([0,a]x[c,C]), 0<a<A, 0<c<C.

The L has two overlapping convex rectangles H=[0,A]x[0,c] and V=[0,a]x[0,C]. If the distinct interior marks share either rectangle, their segment remains in the polygon interior. This includes internal portal lines and the internal seam x=a below c. Otherwise, after exchanging S and T, the pair has a<x_s<A, 0<y_s<c and 0<x_t<a, c<y_t<C. No endpoint placement is lost.

## Independent formula reconstruction

Put r=(y_t-c)/(c-y_s)>0 and E={epsilon*x_t+2ma}. Neighboring target images have gaps 2x_t and 2(a-x_t), both strictly less than 2a. Therefore there is an image x at nonzero distance delta=|x+r*x_s|<=a from -r*x_s. When the latter is an image itself, use a nearest distinct neighbor; delta<=a still holds, including the equality x_t=a/2.

Use (X_s,X_t)=(x_s,x) if x>-r*x_s and (-x_s,-x) otherwise. The symmetry E=-E makes both target choices legitimate. The segment meets the portal at q=delta/(1+r), so 0<q<a. Below the portal, the positive-source branch stays in (0,A); the negative-source branch stays in (-A,A) and folds once at x=0. That contact is strictly between y_s and c and is smooth. Above the portal, the period-2a triangular-wave fold gives the actual target x_t. Its finitely many reflection contacts lie strictly between heights c and y_t<C. Neither endpoint is a fold cusp, and neither portal endpoint is touched.

Both folds are the identity near q, so the physical velocities match at the transparent portal. The y component remains strictly positive. This gives an actual finite corner-avoiding connection using only vertical wall reflections. Transposing x and y gives another connection using only horizontal reflections, with the transposed dimensions (A',a',c',C')=(C,c,a,A), and reversing it gives the prescribed S-to-T order.

No local paths are concatenated with incompatible slopes: a single developed straight segment controls the entire constructed path. This is why the theorem is stronger than a generic local band-transfer atom. Finiteness is per input; no parameter-independent reflection bound follows.

## Consequence and limits

All canonical45 ORTHOGONAL rooms with W<=6 illuminate every distinct interior A pair, without a k bound. Four-wall orthogonal rooms are rectangles and convex; six-wall rooms are the L case above. In fact the result permits arbitrary real interior marks and arbitrary real L dimensions, including the noncommensurable examples that defeated affine rationalization.

The theorem also avoids every boundary blocker belonging to just one wall orientation by using the opposite-orientation path. It does not prove absence of mixed-orientation or interior finite blocking sets. It does not cover octilinear six-wall rooms with diagonal walls, or orthogonal rooms with two or more reflex corners. Those exclusions matter when using it as a foundation for W<=21.

## Verification level

The full historical written proof, old independent Opus hand-review receipt, and saved arithmetic control report were read. The argument above is an independent hand reconstruction of arbitrary-real cases, equality handling, actual target arrival, portal velocity, and corner avoidance. The old 972 controls and 7,132 wall contacts were not rerun or claimed as a new independent computation. Frozen source and receipt hashes are pinned in all-real-L-dependency-acceptance.json.
