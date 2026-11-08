# A58: independent actual depths on complete zigzag parameter families

Author theorem pending independent review. Universal canonical45 W<=21 remains OPEN. Original conservative effort07:39Z to07:53Z, including preliminary two-residual algebra. This is a new independent-depth implication, not an enlargement of a search count.

## 1. Independent-depth matching lemma

Let two right teeth in a finite rectangular-spine comb have height2, centers s<t with h=(t-s)/2>1, positive real core width c, and arbitrary independent actual depths 0<=D_s<w_s,0<=D_t<w_t. Set actual S=(c+D_s,s),T=(c+D_t,t). Fix a positive integer m, E=D_s+D_t, L=2m*c+E. Define on nonnegative integers

F(N)=floor(D_s(h+N)/L+1/2)+floor(D_t(h+N)/L+1/2).

Iteration from N0=0 is nondecreasing. The bound F(N)<=E(h+N)/L+1 shows every integer B>=(hE+L)/(2mc) is a supersolution. Thus iteration stabilizes at a finite least fixed value N. Define tau=2(h+N)/L, n_i=floor(D_i*tau/2+1/2), delta_i=D_i*tau-2n_i. Then N=n_s+n_t, -1<=delta_i<1 and

2mc*tau=2h-delta_s-delta_t.                       (1)

Both lower inequalities are strict. If delta_i=-1, that floor argument is integral; at N-1 it decreases by D_i/L>0, so its floor drops by at least one and the other floor cannot increase. Hence F(N-1)<=N-1, contradicting the iteration's least fixed value. N0 cannot have such an equality since a threshold with positive D_i implies n_i>=1. Therefore delta_s,delta_t are BOTH in(-1,1).

The actual source arm has x=c+D_s-r and y=s-1+F_2(1-2n_s+tau*r),0<=r<=D_s. It begins at original S, ends at strict mouth (c,s+delta_s), and exits up-left. Exactly n_s horizontal reflections occur at strict positive depths below D_s, so the actual far wall is never touched. For D_s=0 the arm is empty and delta_s=n_s=0. Construct the target arm by reversing its OWN analogous prototype centered at s, then reflecting y to s+t-y. It begins at (c,t-delta_t) traveling up-right and reaches original T, with n_t legitimate selected horizontal reflections. Unused selected widths may differ arbitrarily.

Between these portals take 2m core legs, each of horizontal run c and upward vertical increment c*tau. The intermediate side heights are

y_j=s+j*h/m+(1-j/(2m))*delta_s-(j/(2m))*delta_t,
                    j=1,...,2m-1.                 (2)

Odd j meets x0, even j meets xc. Every error in (2) lies STRICTLY in(-1,1), because its absolute coefficient sum is one and both residuals are strict. If every indicated side contact lies on a smooth actual mirror, the concatenation is a legal finite actual path. Its reflection count is n_s+n_t+2m-1. All open core segments have0<x<c and heights between the two strict portals. There is no seam mirror or target-image substitution. The target tooth arm's marked abscissa is first reached at its endpoint; earlier actual target arrival elsewhere, if any, can be truncated.

This generalizes the accepted A51 COMMON-depth lemma. Its old half-unit error margins CANNOT be used for independent depths: formula(2) can have a full-unit error. The following cutoffs account for this larger error.

## 2. Literal four-band rooms

A1: core[0,c]x[0,G],G=2h+d+4; selected right bands[1,3],[2h+1,2h+3]; opposite left bands[h,h+2],[h+d+2,h+d+4]. Here h,d are integers,h>=6,d>=1. All four tooth widths are independently arbitrary positive REAL numbers, selected widths exceed their own independent actual depths. Marks S=(c+D_s,2),T=(c+D_t,2h+2). These are strictly simple20-wall rooms. No horizontal metric, endpoint-depth, ratio, diameter or supplied-witness restriction is imposed.

A0: same selected bands and actual marks, G=2h+4 and opposite bands[h,h+2],[h+4,h+6], integerh>=10. Again all real horizontal dimensions and depths are independent. The selected and opposite bands lie strictly within the vertical core range.

## 3. Full A1 coverage outside forty vertical cells

Use m2 first, recomputing the least index in Section1. The left heights are2+h/2+e1 and2+3h/2+e3 with both errors in(-1,1). Since h>=6, the first is strictly below h. The second is strictly above h+2. The intermediate right contact2+h+e2 is in(3,2h+1), hence in the smooth selected gap.

The second left contact avoids the ENTIRE second opposite band if either

h<=2d-2 OR h>=2d+6.

Indeed its difference from the second band's lower endpoint is h/2-d+e3, strictly negative in the first case. Its difference from the upper endpoint is h/2-d-2+e3, strictly positive in the second case. Strictness holds also at displayed equality cutoffs.

It remains to handle2d-1<=h<=2d+5. If d>=8, use m4 and recompute ALL indices/residuals at that new m. In particular h>=15. Odd side contacts are2+j*h/4+e_j,j1,3,5,7, all errors strict(-1,1). The lower two are strictly below h, since the larger is<3+3h/4<=h for h>=12. The upper two are strictly above h+2, since the smaller is>1+5h/4>h+2.

The j5 contact is strictly below the second band's lower endpoint: its difference is h/4-d+e5 < h/4-d+1 <= (2d+5)/4-d+1 = 9/4-d/2 <0 for d>=8. The j7 contact is strictly above the upper endpoint: its difference is3h/4-d-2+e7 >3h/4-d-3 >=3(2d-1)/4-d-3 =d/2-15/4>0 for d>=8. Thus these two contacts straddle the entire second opening. The three even right contacts2+j*h/4+e_j,j2,4,6, lie strictly in(3,2h+1), because h>=15. All intermediate heights are between strict selected portals and therefore away from floor/roof; these are actual vertical mirrors only.

Consequently A1 is completely illuminated for EVERY allowed real horizontal metric and independent actual depths, except POSSIBLY the following forty vertical cells:

d1: h6..7;
d2: h6..9;
d3: h6..11;
d4: h7..13;
d5: h9..15;
d6: h11..17;
d7: h13..19.

These cells are explicit unproved exceptions to this theorem, not dark rooms and not a finite room inventory: each has unbounded continuous horizontal data. In particular EVERY A1 with h>=20,d>=1 and EVERY A1 with h>=6,d>=8 is covered. A1 with h3,4,5 is outside this theorem; A57 separately covers h3d1 at ALL independent real depths.

## 4. Full A0 coverage for h>=10

Take m2. As above the first left contact is below h, the second above h+2, and the right intermediate contact is in its smooth gap. For A0 the second left contact is also strictly above h+6: its difference from this upper opening endpoint is h/2-4+e3 > h/2-5>=0 for h>=10. Thus all three core mirrors are actual and Section1 yields illumination for the entire arbitrary-horizontal-data A0 family at every h>=10, with arbitrary independent actual depths. No reflection bound independent of those depths is asserted.

## 5. Exactness, dependencies and remaining scope

The actual finite matching lemma and physical mirror guards above are the proof; controls test their prescribed formulas. They use rational arithmetic and disclosed reuse of the earlier audited all-wall validator. No discovery inventory or failed path search is used. No computation can substitute for the all-real inequalities.

The theorem keeps actual S/T and independent selected widths. It removes the former common-depth restriction on complete large-vertical families and leaves finite VERTICAL patterns, not bounded horizontal samples. It does not prove all endpoint placements, all four-band patterns, all combs, taller teeth, diagonal geometries or universal canonical45 W21 illumination. Independent peer acceptance is required before calling this milestone verified.
