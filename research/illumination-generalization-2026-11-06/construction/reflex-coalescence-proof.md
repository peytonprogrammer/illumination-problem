# A two-reflection return resolves a reflex-coalescence stratum

A26 positive hand candidate, pending independent review. Original deadline is in reflex-coalescence-effort.json. No universal visibility assertion is assumed.

## Hypotheses

Consider a normalized affine orthogonal family P_epsilon, epsilon=1/L>0, with fixed wall pattern and vertices affine in epsilon. O_epsilon is a persistent reflex270 corner. After translating by O_epsilon and choosing axes, O=0 and the locally missing quadrant is x>0,y>0. The actual marks are

    S_epsilon=epsilon*(-a,b),  T_epsilon=epsilon*(c,-d),

with fixed a,b,c,d>0. They are actual distinct interior points. This describes opposite NW/SE approach arms. If both marks lie in a common local half-plane avoiding the missing quadrant, their direct segment is already legal; the opposite-arm case is the one addressed here.

Suppose a persistent convex90 corner p_epsilon=(-H_epsilon,-K_epsilon), with H_0,K_0>0, has its adjacent interior quadrant NE. The limiting open segment from O to p_0 is strictly inside P_0 and avoids the FULL limiting indexed boundary trace, except at the two specified endpoint corners. Assume all other limiting indexed segments and vertices are separated from that open segment and its endpoints, after excluding the incident wall pairs. The four incident walls have nonzero limiting lengths and no extra collapsing mirror is present near either corner.

More generally the segment may be an unfolded finite corner-to-convex billiard path: from O into the STRICT SW sector, with ordinary transverse corner-free intermediate reflections and endpoint p_0 approached in the interior of its convex sector. Unfold that finite prefix into the initial O chart; its image p_* must have two negative coordinates. All intermediate contacts obey full-trace strict guards. The construction below then uses that prefix, the two split corner reflections and its reversed prefix. The direct-segment version needs no intermediate wall word.

## Exact target image and positive contact order

Work first in the direct segment case, with H=H_epsilon>0,K=K_epsilon>0. Reflect the ACTUAL target in BOTH incident mirror lines x=-H and y=-K. The resulting image is

    T' = (-2H-c*epsilon, -2K+d*epsilon).

Join the actual source S to T' by a straight line. Its velocity displacement is

    (-2H+(a-c)*epsilon, -2K+(d-b)*epsilon).

The parameters at which that line meets the two unfolded mirror supports are

    t_x=(H-a*epsilon)/(2H+(c-a)*epsilon),
    t_y=(K+b*epsilon)/(2K+(b-d)*epsilon).

For sufficiently small positive epsilon, 0<t_x<t_y<1. In fact the numerator of t_y-t_x after multiplying its positive denominators is

    epsilon*[H*(b+d)+K*(a+c)] + epsilon^2*(b*c-a*d),

which is strictly positive for all sufficiently small epsilon, even when H,K vary affinely. The leading coefficient is positive. At the first contact (the vertical wall), its height above the convex corner is

    y(t_x)+K = (t_y-t_x)*[2K+(b-d)*epsilon] > 0.

After reflecting x, the horizontal-wall contact has physical abscissa to the RIGHT of p, at distance

    [2H+(c-a)*epsilon]*(t_y-t_x) > 0.

Both distances are O(epsilon), so both contacts lie in their persistent finite wall interiors for all sufficiently small epsilon. Neither is the actual corner. The two mirrors are met in the stated order. Folding the remaining segment ends EXACTLY at T, since T' was constructed from that actual point by these two physical reflections.

## Actual room and full boundary guards

Near O, the source leg initially has x<0 and travels SW; it remains on the allowed side of the vertical boundary ray until it leaves a fixed small corner neighborhood into the open SW quadrant. The final leg approaches T from SW while y<0, staying on the allowed side of the horizontal boundary ray. Near p both reflected legs lie in its NE interior quadrant, with the two positive wall distances computed above.

Away from small endpoint neighborhoods the limiting outward and return legs follow the same strict open segment Op in opposite directions. Compact trimmed pieces have positive distance from the full limiting boundary trace. Small affine changes preserve this distance, while the local corner calculations supply the guards at the two excluded endpoint neighborhoods. Thus the entire actual path is inside P_epsilon, touches only the two designated smooth mirrors, and avoids all other corners, walls and ghost traces. It has exactly two ordinary reflections unless an earlier actual target visit already supplies a shorter path.

For the finite-prefix generalization, unfold its ordinary mirror word first. Its persistent supports and transformed convex corner depend affinely on epsilon. The virtual source is still the actual S in the initial chart. The palindrome consisting of prefix, the two incident convex reflections and reversed prefix unfolds the actual T to the central inversion about the unfolded convex-corner image p_*. Orthogonal reflection matrices preserve the two local arm offsets at O under the reversed palindrome. Apply the SAME contact calculation at p_*, while the finitely many ordinary contacts before and after have strict trace margins by hypothesis. Refolding therefore yields a finite actual S-to-T path in this case too. No endpoint is replaced by a modulo or independently selected lift.

## Consequence and boundary

For every family satisfying these explicit hypotheses, the actual pair illuminates for ALL sufficiently large L. This resolves a class of REFLEX boundary coalescences excluded by the strict regular-contact limiting-witness theorem: the limiting double contact at the remote convex corner is deliberately split into two legal finite contacts.

It does not assert the required opposite-sector convex return exists in every polygon, even at W<=21. The separate visibility obligation must be proved, and a single visible corner is not assumed from wall count. Boundary traces with extra collapsed segments near O or p and non-affine endpoint approaches need separate analysis. This is a positive tail certificate, not the universal minimum.
