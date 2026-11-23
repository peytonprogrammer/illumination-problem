# A floor return in the ten-wall Ferrers room

Every distinct pair of real interior marks is lit if the bottom band has depth

    h ≥ max{d(W−u)/(u−w) − e, (d+e)(W−v)/(v−w)}.                 (A)

Here the four widths, from top to bottom, are w<u<v<W, all bands have left wall x=0, and their heights are c,d,e,h. This gives a tail in h for every assignment of the other dimensions, including every off-chord assignment. A second result below includes equality in the terminal rotation test. Both results await review.

## Place the first crossing, then reflect at the floor

By the [d169 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d169-review-d15r3/review.md), the only outstanding placement has source abscissa 0<x<w at distance a>0 above the first gate, and target abscissa v<z<W at depth 0<b<h below the last gate. Reflect the target in the full bottom floor. Its new depth below the last gate is B=2h−b>h. Put L=d+e+B. Choose the representative of x+az/L modulo 2w nearest zero and divide it by 1+a/L to obtain E. Launch in the developed chart with slope s=(z−E)/L per unit descent. The source coordinate E−as is congruent to x modulo 2w, so the line starts at a lift of the physical source. Its three signed gate coordinates are

    E,    ((e+B)E+dz)/L,    (BE+(d+e)z)/L.

The first has |E|<w. The second is strictly between −u and u because d(W−u)≤(u−w)(e+h). The third is strictly between −v and v because (d+e)(W−v)≤(v−w)h. These are exactly (A). At every gate the two band folds agree by absolute value, including reflection on the smooth common side at zero. In the bottom band the signed line interpolates from the third gate to z. At the floor the interpolation fraction is h/B>1/2. Since z>v and the third gate exceeds −v, the floor crossing is strictly positive and less than W. It is a legal reflection. Folding the remaining leg reaches the target.

## Equality in the terminal strip test

Let Pd/(2u) and Pe/(2v) be integers. Suppose the reduced denominator of Ph/W contains a prime power at least W/w. Then every pair is lit. Indeed, the two terminal rotations Pb/(2W) and P(2h−b)/(2W) sum to Ph/W. Either one is irrational or at least one reduced denominator contains this prime power. For the corresponding terminal travel B, the multiples of PB modulo 2W are dense or have spacing at most 2w. Choose M=kP and |Z|≤w with Z+MB congruent to z modulo 2W. The closed interval matters at equality.

Choose a representative X of one of ±x+Ma modulo 2w with |X|<w. At least one works because 0<x<w and the two representatives are distinct modulo 2w. Put D=a+d+e+B. Use the developed line from X−Ma with slope M+(Z−X)/D. At the three gates subtract the completed middle periods. The resulting gate coordinates interpolate strictly inside (−w,w), since each is attained before time D. The endpoint after folding is z. On the reflected itinerary, if the line was aimed exactly at a floor corner, stop earlier: in the formal rectangle unfolding, the two parts equidistant from that corner fold to the same physical point. At depth b on the incoming leg the path therefore already hits the target, before the corner. There is no other horizontal wall between entrance and floor. This proves the equality extension of the [terminal strip construction](ferrers-terminal-strip.md).

## Transpose and controls

In coordinates measured from the common bottom-left corner the isometry (x,y) ↦ (y,x) takes the staircase to widths (h,h+e,h+e+d,h+e+d+c) and heights (W−v,v−u,u−w,w). It exchanges vertical and horizontal reflections and preserves every forbidden vertex. Applying [d170's direct theorem](ferrers-two-windings.md) to this image gives the closed inequalities hu≤(e+h)(v−u) and (e+2h)wu≤v(u−w)(d+e+h). T1 gives 4≤16 and 36≤36. Equality is covered by the strict source correction in the direct theorem.

| Room | Whole-room verification | Prescribed shot, dx per unit descent | Target and reflection count |
|---|---|---|---|
| U1 | (A) gives 3≤4 and 2≤9 | 17/20 | (11/2,3/2), 3 |
| U2 | (A) gives 4≤5 and 3≤8 | 14/31 | (7/2,2), 5 |
| U2b | P=6, Ph/W=24/5, denominator 5=W/w | 1065/59 | (4,7/3), 57 |

Each replay used the named room's top-cell center as source. U1 and U2 use the far cell's center. U2b uses b=5/3, B=19/3, M=18, Z=0. D164's exact tracer returned each target. The inequalities and rotation argument establish the assertions for arbitrary marks.

## What remains

The symmetric Ferrers grid (0,10,11,13,N) in both axes illustrates the gap. For N=2860k and every positive integer k it has d=2,e=1,h=10 and w=10,u=11,v=13. The chord test fails (4>1), d170 fails (110>22), and (A) fails already at its first gate. The integer common period is 286 and Ph/W=1/k, whose denominator is less than W/w even before taking a prime-power factor. Symmetry repeats those failures in the other orientation. This is a residual of the displayed sufficient tests, not evidence for a dark pair.

For the pyramid follow-on, [the all-index obstruction](pyramid-sweep-obstruction.md) settles the proposed quantifier negatively. In mask 761, widths 2,V,4,2 from the bottom and horizontal lines at 0,1,65,67,69, take V any multiple of 192 greater than 192. The two forward gates require a signed first crossing simultaneously at most 1/4 and greater than 1, even allowing both terminal caps. The perpendicular shot given there lights the pair. The open whole-word question is whether the union of the two orientations and routes that revisit a gate suffices.

## What is the smallest W ≤ 20 room this result doesn't cover?

No ledger word changes status. Ferrers LLLLLRLRLR and pyramid LLLLRLLRLR remain PARTIAL. A smallest word still OPEN is the ten-wall LLLRLLLRLR, realized by (2,0), (4,0), (4,1), (3,1), (3,4), (0,4), (0,3), (1,3), (1,2), (2,2).
