# A literal two-strip comb family has a computable finite lattice remainder

A31 candidate for independent review. This proves the previously conditional geometric application of the H-uniform horizontal theorem. A finite possible-dark remainder is NOT illumination of that remainder or completion of the W21 goal.

## 1. Exact initial data and two independent insertions

Fix one finite rational-coordinate rectangular-spine comb P0: spine[0,c]x[y_min,y_max] with c>0, plus finitely many right rectangular teeth[c,R_j]x[l_j,u_j]. Every tooth has positive width/height and different bands have positive separating gaps. Fix actual interior marks S,T STRICTLY in two DIFFERENT teeth, S in the lower band and T in the upper. Their horizontal depths from x=c are d_s,d_t>0 and their offsets from the lower selected floor/upper selected ceiling are b_s,b_t. Assume all tooth heights are commensurate; for canonical integer data this is automatic.

Choose one bare-spine gap(y_-,y_+) BETWEEN the two marked tooth bands, containing NO tooth band and no actual mark height. Put G=y_+-y_->0. For L,M>=0 define P(L,M) by:

* extend EVERY tooth right end by L and move each selected mark right by L;
* translate EVERY tooth band and actual mark above this bare gap upward by M, and extend the spine top by M, leaving lower data fixed.

The two operations act on separate x/y coordinate ranks and commute. The selected separation H is H0+M, where H0>u+v and u,v are the selected tooth heights. The offsets c,d_s,d_t,b_s,b_t,u,v do not vary. Other tooth positions change only by the same indicated upper translation.

For every L,M>=0 this is a finite strictly simple comb disk. Tooth bands remain positively separated, the spine remains a positive rectangle, and no tooth collides with another or crosses the spine. Every nonzero maximal boundary segment remains positive. Coordinate ranks and all existing boundary mergers at the global spine floor/ceiling are preserved, so the maximal wall count is exactly the original count. The actual marks remain distinct interior points in their respective teeth.

For integer canonical P0 with even-even marks, taking L=2n,M=2m, n,m>=0 integers, preserves every integer axial boundary coordinate and both even-even actual marks. Therefore the whole grid is a family of canonical45 triangle disks with the SAME W, including W<=21 whenever the starting comb has that property. No k, area or diameter bound is imposed.

## 2. Exact vertical neck at each fixed horizontal coordinate

Choose cuts at

    a=y_-+G/3, b=y_+-G/3, so ell0=b-a=G/3>0.

For fixed L, take C_-(L) to be the part below y=a, capped there by[0,c]x{a}. Take C_+(L) to be the part above y=b, capped by[0,c]x{b}, translated down by b-a so its mouth is aligned at y=a. Both are finite rational orthogonal Jordan chamber disks: cutting the spine in a tooth-free slab separates it into two rectangles with attached disjoint teeth. Each chamber contains its corresponding actual mark strictly in its interior. Both selected marks lie outside the two retained bare-spine collars.

Insert the rectangle[0,c]x[a,a+ell0+M] and translate the aligned upper chamber by ell0+M. The resulting union is EXACTLY P(L,M), not a substitute subroom. Piece interiors are disjoint, only the two intended mouth contacts occur, and each relative-interior mouth is locally two sided. The two vertical neck sidewalls are the actual spine walls x=0,c throughout the inserted bare gap. Every nonmouth chamber boundary remains an actual wall of the union. There are no hidden contacts with any tooth, because the entire slab was chosen tooth free. This geometry is admissible for ALL M>=0.

After a fixed axis swap/translation this is the accepted one-neck model with width c and length ell0+M, with FIXED chambers/actual marks for each fixed L. The caps are auxiliary boundaries only. The accepted first-mouth construction reaches their strict interiors before any cap reflection and explicitly excludes both mouth endpoints, even if smooth before gluing. Thus neither a cap reflection nor a created-corner equality is mistaken for a physical path. It applies here to actual S,T.

For comparison with the literal mixed-neck program, choose two vertical cuts strictly inside(c,c+epsilon) with epsilon<min_j(R_j-c),d_s,d_t. Across that slab each tooth is a separate fixed-height horizontal neck; the marked right pieces lie beyond the cuts. These horizontal cores are disjoint from the vertical spine core, which lies at x<=c. Cutting them together yields a tree consisting of the two spine pieces joined vertically and one right leaf per tooth. All remaining blocks and mouths are fixed; only the common horizontal lengths and the one vertical length change. Thus this is a literal disjoint H/V neck family, not an assertion that arbitrary intersecting atlas strips have fixed chambers.

## 3. A uniform horizontal tail

Apply the independently accepted H-uniform comb theorem with M_min=H0-u-v>0. It supplies an explicit rational L_bar such that EVERY P(L,M), M>=0, illuminates its actual pair whenever L>=L_bar. Its constants do not depend on H0+M or on the intermediate tooth translations. The selected right ends remain beyond the transported marks, as required.

Choose N=max(0,ceil(L_bar/2)). Then every integer n>=N is illuminated for ALL m>=0. This is the step that a separate fixed-H tail alone would not justify.

## 4. Each remaining horizontal coordinate has a computable vertical tail

For each of the finitely many integers n=0,...,N-1 fix L=2n. Section2 gives rational fixed chambers and actual rational marks, joined by a width-c neck of length ell0+2m. The accepted effective rational one-neck construction gives a computable finite V_n such that every neck length strictly above V_n supplies an actual finite corner-avoiding S-to-T path.

Its constructive procedure uses a fixed irrational slope in Q(sqrt(2)) on each capped rational chamber, stopping at the FIRST strict mouth hit. Rational corners/mouth endpoints cannot be hit in that direction; minimality supplies finite termination. It then extracts a rational open common direction interval and picks an exact integer neck phase. The accepted theorem includes these dependencies and endpoint exclusions. No new first-witness search or assumed seed trajectory is required here.

Set

    M_n=max(0, floor((V_n-ell0)/2)+1).

For m>=M_n the actual neck length ell0+2m is strictly greater than V_n, hence the corresponding P(2n,2m) illuminates. The strict inequality is retained even at an integral cutoff.

Let M_star=max_{0<=n<N} M_n, taking M_star=0 if N=0. Any dark member of this entire integer two-parameter family must therefore satisfy

    0<=n<N, 0<=m<M_n,

and in particular lie in the computable finite bounding rectangle

    0<=n<N, 0<=m<M_star.                                   (1)

The rational constructions terminate for each of finitely many n. This proves computability of the finite remainder, without claiming a practical complexity bound or that any of those routines was executed in this effort. An actual bounded computation stopped after840seconds would remain incomplete; the mathematical termination theorem is not a runtime promise.

## 5. Contribution and unresolved obligations

This verifies an actual joint parameter reduction on a concrete family inside the geometric atlas: every chosen rational comb, transported marks in different teeth, one common horizontal extension and one bare vertical separating-gap extension. It allows arbitrary unequal commensurate selected heights, unequal actual depths and offsets, arbitrarily many extra teeth, and arbitrarily large independent n,m. Neither a supplied finite witness nor an aspect-ratio restriction is assumed.

Every point OUTSIDE(1) is rigorously illuminated by the accepted constructions. Entries INSIDE(1) still require actual illumination proofs or rigorously verified darkness certificates. A finite geometric list or failure to find a ray does not decide them. No all-comb result, many independent gap uniformity, moving mouth-height assertion, arbitrary nonrectangular chamber family, diagonal strip reduction or universal W<=21 conclusion follows.

The proof imports published minimality through previously reviewed one-neck work. No external expert verification is claimed. It closes the conditional literal-decomposition/joint-tail implication, not the main illumination goal.
