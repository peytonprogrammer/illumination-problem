# A44: variable-angle closure of A1 for h >= 4

Status: author proof, pending independent review. Universal W<=21 objective remains open.
Original aggregate effort deadline: 2026-11-07T06:27:19.007644Z. The earlier fixed-q pack failed and is retired; no additional discovery was used for this argument.

## Quantified statement and geometry

For every EVEN integer h>=4 and EVEN integer d>=2, let P be the union of the closed core [0,2] x [0,G], G=2h+d+4, right teeth [2,3] x [1,3] and [2,3] x [2h+1,2h+3], and left teeth [-1,0] x [h,h+2] and [-1,0] x [h+d+2,h+d+4]. Then the actual interior marks S=(2,2) and T=(2,2h+2) illuminate each other by a finite corner-avoiding specular path.

Every tooth has positive height and width. Same-side bands have positive gaps; opposite-side overlaps are allowed. All teeth are nonflush. The boundary is a simple orthogonal polygon with20 maximal walls. Both marks have full interior neighborhoods supplied by the core and their right teeth. The accepted A42 classification identifies precisely this family, but the paths below need no classification assumption. Reflection at x=0 is legal exactly outside both closed left bands; reflection at x=2 is legal outside both closed right bands. A path strictly inside 0<x<2 cannot meet any tooth wall or polygon corner.

## 1. Three-reflection variable-angle path

Assume h>4. Use the interleaved vertices

S, (0,2+h/2), (2,2+h), (0,2+3h/2), T.

All legs have absolute slope h/4, strictly increasing y, and alternating horizontal velocity. Thus each designated vertical-wall collision is specular. The right turn has height 2+h strictly between3 and2h+1. The first left turn lies below h because h>4. The second left turn lies above h+2. It lies strictly outside the other left band precisely when h/2<d or h/2>d+2. The entire path is strictly between floor and ceiling. Consequently this actual path works unless

2d <= h <= 2d+4.                                      (E)

No missing mirror is used at an endpoint: S and T are actual interior seam points, and their adjacent legs immediately enter the open core.

## 2. Seven-reflection path on the exceptional strip

Suppose (E) and d>=6. For j=1,...,4 put L_j=(0,2+(2j-1)h/4); for j=1,...,3 put R_j=(2,2+jh/2). Use

S,L_1,R_1,L_2,R_2,L_3,R_3,L_4,T.

All eight legs have absolute slope h/8, strictly increasing y; all turns are actual vertical specular reflections if their heights are smooth. Here h>=12>8. The first two left heights lie strictly below h: the larger is2+3h/4<h. The last two lie strictly above h+2. Moreover L_3 lies strictly below h+d+2 since h/4<d, a consequence of h<=2d+4 and d>2. The last left height lies strictly above h+d+4 since3h/4>d+2, a consequence of h>=2d and d>4. Thus the two upper left turns lie on opposite sides of the entire second opening, with neither on an endpoint. Every right height is strictly between3 and2h+1 since h>2. All path heights lie between those of S,T, strictly inside [0,G]. This proves legality for the whole stated strip, without a parameter bound.

## 3. The entire h=4 row

For every d>=2 the following four-reflection path works:

(2,2), (2/3,0), (0,1), (2,4), (0,7), (2,10).

Initial velocity is proportional to(-2,-3). Reflection at the actual floor changes only the vertical sign; subsequent vertical reflections change only the horizontal sign. The floor contact has0<2/3<2. Left heights1,7 avoid [4,6] and [d+6,d+8], the latter starting at least8. The right height4 lies strictly between [1,3] and [9,11]. Each open leg lies in the open core, apart from its permitted boundary contact. The endpoint is the actual T. There are no corner continuations or fictitious mirrors.

## 4. Five isolated exact exceptions

After sections1-3 the remaining EVEN parameter pairs are precisely

| h | d | Initial actual velocity | Reflections | All-wall leg guards |
|---|---|---|---|---|
| 6 | 2 | (-1,-3) | 5 | 120 |
| 8 | 2 | (-2,3) | 8 | 180 |
| 8 | 4 | (3,1) | 21 | 440 |
| 10 | 4 | (-3,1) | 27 | 560 |
| 12 | 4 | (3,1) | 33 | 680 |

These are exact stored paths, not inferred from sampling: each row is retrieved by (h,d) from the frozen c2-A1-below-check.json. That file gives the full actual polygon, S,T, Fraction collision coordinates, wall indices and velocity. Its checker tests every polygon wall on every leg, chooses the first positive collision, rejects tied or endpoint collisions, and terminates only on the actual T strictly before the next wall. The five rows total94 reflections and1980 all-wall leg guards. Independent review must replay these prescribed certificates with its own checker; author execution alone is not independent acceptance.

Exhaustion: for h>=6 outside (E), section1 applies. Inside (E), d>=6 is section2. For d=2, the even h>=6 possibilities are6,8. For d=4 they are8,10,12. Section3 covers all h4, including its equality cases. Hence every h_even>=4,d_even>=2 is covered. The h2 row is intentionally excluded and remains a separate obligation.

## Dependencies and limitation

The hand paths in sections1-3 are self-contained. Section4 relies only on the five specified exact physical path certificates and their exact wall checker; it does not rely on completeness of any ray pack or origami search. No failure-to-find result proves darkness. This establishes an entire unbounded two-parameter A1 subfamily once independently accepted, not all canonical45 rooms, not all two-sided combs, and not the universal22-wall minimum.
