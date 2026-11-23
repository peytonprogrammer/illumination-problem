Advances: L1 — Two cap reflections give an effective finite residual for an occupied crossing with a single mouth, fixed end depths and one upper run, across all ratios of the two growing lengths.

# Crossing strips with one open mouth

**Theorem.** Let the lower rectangle be [0,D] × [0,h], with solid sides and floor. Its roof opens only at I=(i,i+w). The attached upper rectangle has width W and solid sides from this mouth to the target level. Take interior lattice marks S=(c,d) in the lower rectangle and T at height h+b in the upper run, with 0<c<D, d,b>0 and a=h−d>0. The proof also applies at an artificial terminal cut if T is interior to the room and the last leg reaches it from the run. All dimensions are integral. Hold i,w,W,b,d fixed. Both a and D may vary independently, as may c and the target abscissa.

Choose an unfolded positive-sheet target abscissa e<0 modulo 2W so far to the left that (i+w)b/(i−e)<1. Put δ=b/(i−e)−b/(i+w−e)>0. Every dark placement satisfies

    a ≤ max{d, 4dW(2d+1)/w, 64bdW/(w²δ)},
    D ≤ 4(a+d)/δ.

This is uniform in the target abscissa if desired: take e in [−B−2W,−B) with integer B>b(i+w)+1, and replace δ by bw/[(i+B+2W)(i+w+B+2W)]. The result concerns these mark placements. Extra structures above the target level do not affect the shots.

## Direct and floor-return routes

Write v=dx/dy in the vertical unfolding with time increasing along the path. The travel to the seam is A=a for a direct ascent and A=a+2d for an initial descent reflected at the floor. At a positive-sheet seam crossing z in I, the two leg equations are z≡c+Av modulo 2D and z≡e−bv modulo 2W. Eliminating v gives precisely

    (A+b)z ∈ bc+Ae+2g_A ℤ,     g_A=gcd(bD,AW).

Thus (A+b)w>2g_A gives a strict gate solution. With no floor return this suffices. On the capped route the only extra obstruction is c+dv∈Dℤ at the floor. For fixed z, increasing v by 2DW/g_A preserves both equations. If g_A>2dW, two successive choices cannot both hit a floor corner. If g_A≤2dW, a corner hit has v=(jD−c)/d. The residue of j modulo 2d determines z modulo 2D. There are at most 2d such gate heights in I. If (A+b)w>4dW(2d+1), the open window contains more than 2d solutions, so at least one is legal.

Consequently, once aw>4dW(2d+1), failure of both routes forces (A+b)w≤2g_A for both travels. The gcd of the two g values divides W gcd(a,2d) and their lcm divides bD. Multiplication gives

    D ≥ (a+b)(a+2d+b)w²/(8bdW).                 (1)

## Far-wall return

Use horizontal travel as time and positive slope magnitude s in (b/(i+w−e), b/(i−e)). The reverse target leg reaches z=e+b/s strictly inside the mouth. Launch S rightward and upward, reflect at x=D, and return leftward to z. In the vertically unfolded lower rectangle this is an upward arrival at the roof exactly when

    d+s(2D−c−e)−b = (2j+1)h.

Before reaching the far wall, any part of the shot under the opening has risen by less than (i+w)s<1≤a, so stays below the roof there. On the return, successive roof visits are separated horizontally by 2h/s>i+w. Hence there is no earlier escape. A far-wall corner requires d+s(D−c)∈hℤ. Between consecutive roots of the endpoint equation this quantity increases by 2h(D−c)/(2D−c−e), strictly between 0 and h. Therefore two consecutive roots suffice. They exist when (2D−c−e)δ>4h, in particular when Dδ>4h.

Combining the last inequality for failure with (1), and using a+d≤2a when a≥d, proves the stated bounds. The geometric point is that the two short routes can miss only in a box wide enough for the third route. No wall-count estimate enters.

## Named crossing and scope

For the st279 placement in the [crossing-strip note](l1-crossing-gap-transfer.md), take horizontal coordinate 5−x. Then c=d=b=w=1, i=0, W=3, h=a+1. A floor-corner hit forces integer v and hence integer z, impossible in (0,1). So (1) holds on failure at every a. Taking e=−1 gives δ=1/2 and coefficient 2D in the far-wall equation. Failure now forces

    (a+1)(a+3)/24 ≤ D ≤ 4(a+1).

Only a≤93 and D≤376 remain. These are necessary bounds for a dark placement. The residual has not been enumerated. Prescribed controls in original room coordinates were replayed by the d109 polygon-edge tracer:

| a | D | launch velocity | route | smooth reflections before T |
|---:|---:|---|---|---:|
| 7 | 21 | (−23/5,−1) | floor | 5 |
| 7 | 35 | (−1,4/7) | far wall | 5 |
| 101 | 303 | (−2753/52,−1) | floor | 37 |

**First open structural case.** A second opening on the swept roof can intercept the far-wall excursion before its intended return. Alternatively, a second gate on the upper leg restricts the allowed s before that excursion begins. The proof needs a positive interval of legal return slopes in the resulting chart. No bound in W alone or general semilinearity conclusion follows.

**What is the smallest W ≤ 20 room this result doesn't cover?** As a whole-word ledger result it leaves the W=10 word LLLRLLLRLR open, including its realization (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2). No word changes status.
