# The exact period for a placed band route

**Verdict.** Bounded height gives finitely many band graphs. It does not make every route usable or bound the residual gcd for every choice of absorbing band. The sharp period below gives a prime-by-prime test for which band can absorb every parity-compatible mismatch on fixed outer legs. There is also a class where the outer legs and the final match can be constructed simultaneously.

## Band graph

From each remaining reflex corner extend its incident horizontal edge inward to its first boundary contact, as in the reviewed parallel-cut decomposition. Suppress straight vertices. Each cut separates the polygon and removes at least one reflex. The faces are rectangles with physical vertical sides, joined across open horizontal intervals. Their dual is a tree with at most r+1 vertices. Decorate it with the height levels, which incident doors lie on the top and bottom, and their left-to-right order. This uses maximal runs locally; a remote reflex at the same level need not split a run. Splitting every run at every reflex height merely subdivides the description and may create extra artificial seams.

Translate the minimum coordinates to zero. At W≤20 there are at most ten vertical and ten horizontal original edges. For a fixed cyclic edge order, assign to each vertical edge its weak rank among the x coordinates (at most ten choices per edge), and to each horizontal edge its integer y coordinate in 0,…,h. These data determine the combinatorial polygon, cuts and door orders, up to a monotone change of x coordinates, with any fixed deterministic order for making cuts. At fixed W≤20 this gives at most 10^10(h+1)^10 assignments per cyclic order, including invalid ones. Widths and arithmetic relations between them are extra data. A graph route additionally needs consistent vertical travel senses: changing sense requires a reflection on an actual wall, inside a solid interval.

## Absorption on fixed outer legs

Specify positive integer vertical travels d_i (split at each horizontal reflection or crossing), widths u_i, all landed positions and horizontal sheets of two legal outer legs at a common slope s=dx/d|y| in developed coordinates. Leave one transit of depth d and width u between them. At each event use E(l,e,x)=l+e(x−l) for run origin l, physical abscissa x and forward sheet e. The same e is used on both sides of a seam. The target leg is read with its forward sheet. Write F=E_exit−E_entry−ds in the intervening band.

The exact group of slope shifts preserving every signed outer event is Pℤ, where

    P = lcm over outer legs i of the positive rationals 2u_i/d_i.

Indeed d_i Δs must be zero modulo 2u_i in each run, and these conditions also suffice by folding. A common denominator clears the rational lcm. A changed number of vertical-wall bounces inside an open run is harmless. The assertion concerns the specified event positions and sheets, including the chosen endpoint sheets; a different placement may have more freedom. With no outer segments the slope is free.

**Exact match:** F belongs to gℤ, with g=gcd(dP,2u) the positive generator of their rational integer span. This is the equation dPk≡F mod 2u. For same-parity lattice endpoints and total vertical travel D, the signed phases telescope modulo 2 because changing origins adds an even integer. Thus Ds∈2ℤ gives F∈2ℤ. Parity guarantees absorption of *every* such mismatch precisely when 2/g is integral. A bounded gcd greater than two still needs a residue check.

For each prime p the exact exponent in g is

    min(v_p(2u), v_p(d) + max_i [v_p(2u_i)−v_p(d_i)]).

In particular a prime p>h dividing both the candidate width and any outer width survives in g, since every single run travel is at most h. More generally the displayed inequality v_p(g)≤v_p(2) for every prime characterizes a parity-sufficient absorber on these placements. A graph with several eligible bands fails the parity-only guarantee on the route exactly when each candidate has a violating prime. This is an arithmetic classification conditional on the route and legal outer placements. A violating prime can be harmless for a particular F.

**Named unbounded gcd even with the least period.** In the four-band cov279 construction keep the same bottom reflection and travels (1,2,1,1,1), but select the width-3q band for the final match. Its depth is one. The outer unit step in a width-2q band forces 4q to divide P. Consequently gcd(P,6q) is a multiple of 2q at height six and fixed graph. Legal outer placements exist by restricting the previously proved shot. This example tests the invariant itself, independently of whether that particular F is already solvable. Choosing the neighboring width-(2q+3) band instead gives g=2 for q coprime to three. The first uninterrupted upward route is worse: the marks (2q−1,1),(6q−1,5) cannot even place its first and last crossings simultaneously at q≥16, by the two open-window inequalities in [thin-room.md](thin-room.md). Thus changing the absorbing band alone cannot rescue every prescribed route.

## A sufficient arithmetic class with guaranteed outer placement

On a vertically monotone chain of full runs let each overlap contain an interior integer of the endpoints' horizontal parity. Suppose gcd(d_i,u_i)=1 for every run and the widths are pairwise coprime. Then every such same-parity endpoint pair on this chain is lit. Pick one permitted integer x_i per seam, with x_0 and x_m the given marks. Use the positive horizontal sheet at every seam. Set s=2k and solve

    d_i k ≡ (x_i−x_(i−1))/2   (mod u_i).

Every right side is an integer. Each equation has one residue modulo u_i, and CRT solves them simultaneously. Folding each leg gives the required physical seam crossing and horizontal velocity there. One may take 0<k≤product(u_i). At r≤8 this is a polynomial width bound on a simple tree path. The same argument handles prescribed cap visits with an integer of the same parity strictly inside each solid reflection window, provided the congruences below are consistent.

More generally for these chosen sites and positive sheets put a_i=(x_i−x_(i−1))/2 and t_i=gcd(d_i,u_i). One must have t_i dividing a_i. Divide by t_i and invert d_i/t_i to get a residue k_i modulo m_i=u_i/t_i (modulus one is vacuous). There is an even-integer slope on these sheets **iff** k_i≡k_j modulo gcd(m_i,m_j) for all i,j. This follows by generalized CRT and handles repeated bands. Windows of width greater than two always contain an integer of the required parity. Narrower windows, incompatible shared prime powers, and routes requiring different signs or nonintegral slopes are residual for this construction. They need not be residual for illumination. In particular cov279 uses a denominator of three in its four-band construction.

## Named controls and the fat alternative

Exact replays of the existing closed-form cov279 construction at q=8,10,14,20 lit respectively 502, 811, 1,651 and 3,466 same-parity pairs. All four parameters are outside the original progression. The proof used here assumes even q coprime to three. At 3|q even the central preservation gcd gcd(12q,4q+6) is divisible by six, so that parity proof does not extend verbatim. The replay is the function replay(q) in [thin-room-replay.py](thin-room-replay.py); d127 owns the independent review.

For DB55 the opposite lower chambers at heights below the corridor can require a change of vertical sense to visit their connecting band and return. A same-height monotone route is horizontal. The saved free-sheet construction at corridor length three replayed 64/64 cross-chamber pairs. For DBas the saved (7,−2) shot from (1,3) reflected on both horizontal and vertical walls and reached (11,3). For DBw2 at length eleven the d77 formulas replayed 1,128/1,128 pairs, including 272 same-parity pairs. These are controls for the scope of a fixed route, not applications of the pairwise-coprime theorem. Replays used d108 check.stretches([3]), d109 path.check(4,2/7) with exact rational input, and d77 verify.dbw2_check(11,{}).

The odd cross already refutes the revised fat alternative in either orientation. Its three horizontal bands have (width,height) equal to (4,b−2),(2b,4),(4,b−2). For any h₀ choose odd b>h₀+2. The maximum band height exceeds h₀, yet every band, and indeed every contained rectangle, has shorter side at most four. A long arm can use cap doubling, but its other chamber includes an arm of comparable length, so the d124 uniform all-start access time on the remainder grows at least linearly with b in the traversal direction and its quadratic threshold outgrows the depth. These rooms have r=4, are normalized and BBBB, and have their own lighting proof. The saved cross shot at b=9 from (6,0) reflected at (4,−2) and (−2,4) and reached (0,6) on exact replay. [Cross theorem](cross-placement.md)

The remaining existential statement is whether every same-parity pair admits *some* legal route and placements with F∈gℤ. Neither bounded graph size nor bounded maximum travel in each band proves it. There is no area cutoff from the thin/fat split.
