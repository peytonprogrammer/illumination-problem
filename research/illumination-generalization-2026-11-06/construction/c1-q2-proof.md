# A48: entire core-width-one q=2, h>=3 branch illuminates

Status: author complete branch theorem, pending independent review. Original aggregate deadline2026-11-07T06:38:26.978013Z retained. Universal W<=21 objective remains OPEN.

## Domain and necessary entire-room reduction

Use the integer two-sided rectangular-spine comb model with core width1, every tooth width1/height2, same-side positive gaps, opposite-side overlaps allowed and W<=21. Suppose two actual interior A marks on the same seam have ordered floor-relative heights s<t. Put h=(t-s)/2 and q=min(s,G-t). This packet proves illumination whenever q=2 and h>=3. It does NOT cover q1 or h2.

Assume actual darkness. The accepted A38 four-level criterion forces every level h,mu,G-mu,G-h, mu=(s+t)/2, to be an opposite mouth endpoint. Because h>=3, all levels are in[3,G-3]. No height2 flush tooth can supply any of them. The two selected teeth are also nonflush because q2. Their charge in2N_nonflush+N_flush<=8 is4. There must be at least two opposite blockers (at least three distinct levels), all NONFLUSH; they consume the remaining4. The ENTIRE room therefore has precisely the two selected teeth and two nonflush opposite blockers. There is no unused attachment.

With d=|s-(G-t)| the sorted levels are h,h+2,h+2+d,h+4+d. Reflect vertically and exchange source/target if necessary to make s2. If d>0, each blocker must cover two levels exactly2 apart. Positive-gap disjoint bands force the lower pair and upper pair; pairing only inner levels would leave outer levels more than2 apart. Thus the room is precisely A1 below. If d0 there are three levels h,h+2,h+4; after vertical reflection one blocker is[h,h+2]. The second must extend OUTWARD from h+4 to h+6, since extending inward would touch the first. This gives A0 below. Nonflushness is exactly h>2. These normalizations preserve the actual pair under Euclidean isometry; they do not transfer illumination through deleting or adding a tooth.

All forms use core[0,1] x [0,G], selected LEFT teeth[-1,0] x [1,3] and[-1,0] x [2h+1,2h+3], actual S=(0,2),T=(0,2h+2).

A0: every integer h>=3, G=2h+4, RIGHT bands[h,h+2] and[h+4,h+6].
A1: every integer h>=3,d>=1, G=2h+d+4, RIGHT bands[h,h+2] and[h+d+2,h+d+4].

Each is a strictly simple20wall disk, all four teeth nonflush, and has exactly the two actual A points after the stated normalization. These are consequences of the reduction; no initial support cap was imposed.

## A1: variable-angle hand paths for h>=4

For h>4 use S,(1,2+h/2),(0,2+h),(1,2+3h/2),T. Every leg has absolute slope h/2, and all three contacts are smooth except possibly the second right turn. The first right turn is below h; the left turn is strictly between3 and2h+1. The second right turn is above h+2 and is outside the other opening unless2d<=h<=2d+4. All heights increase strictly inside the actual core's floor/roof range. These are ACTUAL vertical reflections.

On that exceptional strip with d>=5 use the seven-turn core path whose RIGHT turns are(1,2+(2j-1)h/4), j1..4, and LEFT turns are(0,2+jh/2), j1..3, interleaved between S,T. Every leg has absolute slope h/4. Since h>=2d>=10, the first two right turns lie below h, and the last two above h+2. The third is below h+d+2 because h/4<d. The fourth is above h+d+4 because3h/4>d+2. These strict inequalities follow from2d<=h<=2d+4 and d>4. All left turns lie strictly between3 and2h+1. This is the same explicit guarded mechanism as A44, with the core's horizontal scale changed but no tooth excursion involved.

For h4 and every d>=2 use the actual floor path

(0,2),(2/3,0),(1,1),(0,4),(1,7),(0,10).

All legs have absolute slope3. The actual floor contact lies strictly in0<x<1. Right heights1,7 avoid[4,6] and[d+6,d+8], because d+6>=8. The left contact4 lies strictly between selected left bands. Source and target are actual interior seams. Thus ALLh4,d>=2 are covered. Only h4,d1 is left in that row.

For h>=5 the exceptional strip with1<=d<=4 has EXACTLY16 integer cells: d1,h5..6; d2,h5..8; d3,h6..10; d4,h8..12. Their isolated exact certificates are in the table below. No parity restriction on h or d is imposed.

## A1: entire h3 row

For every d>=2 use this explicit actual path, initially(3,-4):

(0,2),(1,2/3),(1/2,0),(0,2/3),(1,2),(0,10/3),
(5/4,5),(2,4),(5/4,3),(0,14/3),(1,6),
(-1,26/3),(-3/4,9),(0,8).

The12 intermediate turns all obey the ordinary axial specular law, as recorded exactly in c1-q2-cap-check.json. That lower-cap verification included every cap wall, with an artificial roof used only as a REJECTION boundary and never reached. Maximum height is9, below the actual roof G=d+10 for every d>=2.

Here the first right tooth is[1,2] x [3,5], and the selected upper left tooth is[-1,0] x [7,9]. All tooth entries/exits are strict; the far right reflection at(2,4), far upper left at(-1,26/3), and upper-left horizontal reflection at(-3/4,9) are smooth. Floor contact(1/2,0) is strict. The source lower tooth is not entered: its seam is left behind along a core leg. Every core left mirror used lies outside its selected bands.

The only right CORE reflections above the first tooth are at(1,6); all others are below3. The added second right tooth starts at d+5>=7. It therefore removes no used mirror and introduces no corner on a leg: above6 every used open leg lies strictly at x<1 or inside the upper left tooth. Thus the SAME12reflection path is legal in EVERY full20wall A1 room for d>=2. This is a direct local guard, not a claim of monotone illumination under arbitrary attachment. Only the isolated h3,d1 requires the stored certificate below.

## A0: every h>=3

For every integer h>=9 the three-turn formula in the first A1 paragraph applies directly: its final right turn2+3h/2 lies strictly above h+6, and its first is strictly below h. It uses no altered end wall. The h4 floor path also applies to A0, because its second right opening starts8>7.

For h5,7 use the peer's frozen paths in c1-critical-final-check.json, independently checked in c1-variable-angle-prefix-independent.json:20+11actual reflections/660wallguards. A46 contains the accepted whole-odd-h join, but only these two prescribed prefixes are needed here. The remaining isolated h3,6,8 certificates are included below. This exhausts every integer h>=3.

## Isolated exact certificates

Every row here has a complete stored actual polygon, S,T, primitive velocity, rational path and actual wall indices in c1-q2-check.json. The first-candidate search stopped immediately on its first fully replayed actual path per prescribed input, with no replacement rooms. The physical Fraction checker guards every wall on every leg and rejects corner/tied contacts. Independent review must replay the certificates with its own code, not accept the discovery label alone.

| Family | h | d (0 denotes A0) | Actual initial velocity | Reflections |
|---|---|---|---|---|
| A0 | 3 | 0 | (-7, -4) | 30 |
| A0 | 6 | 0 | (-13, 5) | 38 |
| A0 | 8 | 0 | (-5, 8) | 22 |
| A1 | 4 | 1 | (-7, 11) | 28 |
| A1 | 5 | 1 | (-1, 4) | 13 |
| A1 | 6 | 1 | (-7, -4) | 45 |
| A1 | 5 | 2 | (-8, 13) | 17 |
| A1 | 6 | 2 | (-3, -7) | 14 |
| A1 | 7 | 2 | (-8, 3) | 37 |
| A1 | 8 | 2 | (-7, 3) | 48 |
| A1 | 6 | 3 | (-3, 10) | 22 |
| A1 | 7 | 3 | (-7, 3) | 48 |
| A1 | 8 | 3 | (-1, 4) | 12 |
| A1 | 9 | 3 | (-3, 11) | 18 |
| A1 | 10 | 3 | (-7, -3) | 48 |
| A1 | 8 | 4 | (-3, 5) | 25 |
| A1 | 9 | 4 | (-4, 7) | 25 |
| A1 | 10 | 4 | (-1, 4) | 13 |
| A1 | 11 | 4 | (-7, -12) | 116 |
| A1 | 12 | 4 | (-3, 5) | 25 |
| A1 | 3 | 1 | (-5, 2) | 28 |

The21 rows total672 actual smooth reflections and13860all-wall leg guards. They comprise A0h3/6/8, A1h4d1, the16 strip cells, and A1h3d1. The h3cap's12/208 and peer5/7's31/660 are separate evidence, not double-counted here. They are not a census or an inferred universal bound.

## Coverage and remaining obligation

The hand parameter inequalities plus exactly named isolated members cover ALLA0h>=3 and ALLA1h>=3,d>=1. The darkness-to-entire-room reduction above therefore closes the ENTIREq2,h>=3 branch atW<=21, once independently accepted. Combining with A47 would leave only q1 OR h2 in the c1 thin-comb model. The c2 complete theorem and c>=3 result are separate reviewed dependencies; wider/taller teeth and arbitrary canonical45 polygons remain outside this packet. The universal goal remains unfinished.
