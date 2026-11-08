# A57: a tooth-free periodic core path

Status: author proof, pending independent review. Universal canonical45 W<=21 objective remains OPEN. This is one entire four-tooth family, not a classification of all rooms.

## Exact room and endpoints

Let c,a,b,w_s,w_t be arbitrary positive REAL numbers. Take the rectangle [0,c]x[0,11], right teeth [c,c+w_s]x[1,3] and [c,c+w_t]x[7,9], and left teeth [-a,0]x[3,5] and [-b,0]x[6,8]. The union is a strictly simple orthogonal 20-wall disk: each tooth attaches along its full mouth, same-side mouths have positive gaps, and opposite interiors are disjoint. Let S=(c+D_s,2), T=(c+D_t,8), where 0<=D_s<w_s and 0<=D_t<w_t. Seam points with D=0 are actual interior points of this union.

## 1. Entire real seam family: five reflections

If D_s=D_t=0, the following path works for EVERY allowed choice of all five dimensions:

(c,2), (0,9), (2c/7,11), (c,6), (c/7,0), (0,1), (c,8).

Every leg has absolute vertical/horizontal slope 7/c. The successive genuine mirrors are left side, roof, right side, floor, left side. The left contacts 9 and 1 lie strictly outside both left mouths [3,5] and [6,8]. The right contact 6 is strictly between the selected mouths. The roof and floor abscissae lie strictly in (0,c). Every open leg lies in the open core rectangle; thus no tooth width affects any guard. At every mirror precisely the normal velocity changes sign. All five contacts are strict interiors of actual maximal walls. The only core-side contacts at the selected mouths are the actual endpoints. This proves illumination with five reflections, including first arrival at actual T.

## 2. Two infinite periodic core classes

For any positive integer beta congruent to 7 or 18 modulo 22, put tau=beta/c. Define F_L(q)=min(r,2L-r), r=q mod 2L. Develop horizontal distance z from 0 to 4c and fold

x(z)=F_c(c-z), y(z)=F_11(2+tau*z).

Insert every side-turn event z=c,2c,3c and every roof/floor event z=(11j-2)/tau in (0,4c). Consecutive events yield ordinary specular core segments. At z=c,3c the left heights are respectively (9,1) for beta=7 mod22 and (2,10) for beta=18 mod22. At z=2c the right height is always 6. At z=4c the target height is 8. None of 2+j*beta, j=1,2,3,4, is divisible by 11: reduction beta=7 or7 mod11 gives residues 9,5,1,8. Thus no floor/roof event coincides with a side event, including the endpoint. Every floor/roof contact has x strictly between 0 and c. The preceding mouth guards apply verbatim. Initial direction is up-left, final direction up-right (the terminal developed height is 8 mod22). Reflection count is

3 + floor((2+4*beta)/11).

For beta=7 this recovers the five-reflection formula. For beta=18 it gives nine reflections. The trajectory may intersect itself harmlessly; no earlier actual T occurs since the only intermediate right-side turn is at height 6.

## 3. Actual independent normal-depth arms

Assume additionally n_s=D_s*tau/2 and n_t=D_t*tau/2 are nonnegative integers, for one of the preceding beta choices. Each endpoint uses its OWN normal arm of depth D, independently of the other arm or the unused selected widths.

For the source arm let r increase from 0 to D, put sigma=(-1)^n, and use

x=c+D-r, y=1+F_2(1+sigma*tau*r).

Its initial height is 2; its terminal height is also 2 because tau*D=2n. Its terminal vertical velocity is upward: sigma times the folding derivative at the odd developed height 1+sigma*2n equals +1. Insert the horizontal-wall events at developed heights 2j. There are exactly n such events, each strictly between r=0 and r=D, hence at actual x strictly between c and c+D. Consequently every contact is inside a genuine horizontal tooth wall, away from both mouth corners and the unused far wall. If D=0 the arm is empty. The seam is not a mirror: its direction agrees exactly with the up-left initial core direction.

For the target arm reverse its OWN source-type depth-D_t prototype and reflect y to 10-y. It starts at (c,8) traveling up-right, matching the final core direction, and ends at actual (c+D_t,8). It has n_t legitimate reflections, with every internal abscissa strictly between c and c+D_t. All teeth retain their actual widths; no fictitious mouth reflection or changed target lift is used.

Concatenation gives an actual legal S-to-T path with n_s+n_t+3+floor((2+4*beta)/11) reflections. The source arm stays in the lower tooth, the core reaches its target seam first at its last event, and the target arm reaches its marked abscissa only at its endpoint. Thus first actual arrival is respected even when D_t=0.

## 4. Integer-core, independent integer-depth corollary

Suppose c>=1 is an integer, p=11^v_11(c), u=c/p, and D_s,D_t are nonnegative integers divisible by p. Choose the unique k in {1,...,10} with u*k=9 modulo 11. Set beta=2*u*k. Then beta=18 modulo 22 and tau=2*k/p; n_s=k*D_s/p and n_t=k*D_t/p are integers. Section 3 applies. Selected widths may be arbitrary independent positive reals exceeding the actual depths, and opposite widths are arbitrary positive reals.

In particular, if 11 does not divide c, EVERY independent nonnegative integer-depth pair is covered. When p fails to divide either depth, this corollary says nothing; it does not assert darkness. The more general sufficient condition is the beta congruence and the two integrality conditions in Section 3.

## Evidence and scope

The initial frozen seed used c=6, a=4, b=3, selected widths 6 and actual seams, with beta=18. The shorter beta=7 path and all quantified arguments above were derived by hand. No generic reflection-word cell theorem is needed or asserted. The prescribed checker constructs these formulas on original 20-wall contours using exact rational arithmetic. It reuses explicitly identified validator functions from review/resumed-exact-check.py; that reuse is not independent validation. Independent peer review of the mathematical argument remains required.

The result removes all horizontal width restrictions from the h=3,d=1 seam geometry, and adds the stated actual-depth class. It neither covers all four-band vertical parameters nor all core widths/depths nor arbitrary canonical45 disks. No uniform reflection bound is asserted for the independent-depth extension.
