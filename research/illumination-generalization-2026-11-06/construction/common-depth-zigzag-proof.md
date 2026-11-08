# A51: exact multibounce matching at arbitrary common actual depth

Author theorem pending independent review. Conservative ORIGINAL effort start06:35/deadline06:49Z includes preliminary mental algebra; no deadline renewal. No discovery search was used. Universal canonical45W21 remains OPEN.

## 1. The matching lemma

Let a finite two-sided rectangular-spine comb have core[0,c]x[0,G], c>0. Two selected right teeth have height2, centers s<t, and actual middle-row marks S=(c+D,s), T=(c+D,t), D>=0. Their independent actual widths w_s,w_t are strictly greater thanD; no equality of unused far widths is assumed. Set h=(t-s)/2>1. Fix any positive integer m. Choose

n=floor(D*h/(2*m*c)+1/2),
tau=(h+2*n)/(m*c+D),
delta=D*tau-2*n=(D*h-2*m*c*n)/(m*c+D).

Then tau>0 and |delta|<1. ForD>0, nearest-integer rounding bounds the numerator bymc and mc/(mc+D)<1. ForD0,n0,delta0. No first-stationary or commensurability assumption is needed. Also h=delta+m*c*tau.

The lower selected tooth admits an actual finite prefix fromS to its mouth at(c,s+delta), leaving with horizontal velocity toward the core and UPWARD vertical velocitytau. To verify parity, measure height phase from its bottom wall, so the mark starts at phase1 in a height2 strip. Start with horizontal component-1 and vertical component(-1)^n*tau. After horizontal distanceD, the unfolded height phase is1+(-1)^n*(2n+delta). Folding modulo4 into[0,2] gives exactly1+delta, with UPWARD derivative. It yields exactlyn horizontal-wall reflections. Every such contact has c<x<c+D<w_s+c; every portal is strict since|delta|<1. Thus no far wall or corner is used. AtD0 this prefix is empty, beginning at the actual interior seam, with no seam reflection.

From the lower portal run2m straight core legs, each horizontal lengthc and vertical incrementc*tau, with successive side contacts at heights

y_j=s+delta+j*c*tau, j=1,...,2m-1.

Oddj contacts the opposite side x0; evenj contacts the selected side xc. The final mouth point is(c,s+delta+2mc*tau)=(c,t-delta). Every open core leg has0<x<c and every turn is specular at its designated vertical wall, PROVIDED each y_j is a smooth actual mirror point. There is no artificial reflection at either mouth.

Append the reversed lower prefix reflected byJ(x,y)=(x,s+t-y). This starts at(c,t-delta) with horizontal velocity toward the target and upward vertical componenttau, then reaches the ACTUALT. Only the selected target's portion0<=depth<=D is used, so w_t may differ arbitrarily fromw_s. Itsn horizontal contacts remain smooth. If another actualT is encountered earlier, truncate there. The finite path has2n+2m-1 ordinary reflections. This lemma is conditional ONLY on its explicitly computed side contacts being actual smooth mirrors; the next sections verify those mirrors for whole parameter families.

## 2. Arbitrarily wide/deep A1 family with a uniform vertical cutoff

For positive REALc,w_s,w_t,w_1,w_2 andD>=0 withw_s,w_t>D, use the actual room consisting of

core[0,c]x[0,G], G=2h+d+4;
selected RIGHT teeth of widths w_s,w_t at bands[1,3],[2h+1,2h+3];
opposite LEFT teeth of widths w_1,w_2 at bands[h,h+2],[h+d+2,h+d+4].

Here h,d are INTEGERS withh>=5,d>=1. Marks areACTUALS=(c+D,2),T=(c+D,2h+2). All four teeth are nonflush; the room is strictly simple with20 maximal walls. The horizontal data are arbitrary and independently unbounded, includingD/c. No original ray or finite seed is supplied.

For m2, the opposite contacts computed by section1 are

2+h/2+delta/2, 2+3h/2-delta/2,

and the selected-side contact is2+h. Since|delta|<1 andh>=5, the first opposite contact lies strictly belowh and the second strictly aboveh+2. The selected-side contact is strictly in(3,2h+1). The second opposite contact also avoids the second closed band whenever

h<=2d-1 OR h>=2d+5.

For the first inequality, its difference from the lower band edge h+d+2 is h/2-d-delta/2<=-1/2-delta/2<0. For the second, its difference from the upper edge h+d+4 is h/2-d-2-delta/2>=1/2-delta/2>0. These inequalities are strict even whenh is odd and at either displayed equality. All core turns are therefore actual mirrors.

Only the strip2d<=h<=2d+4 remains. Ifd>=6 choose m4 and recompute n,tau,delta with THISm; do not reuse m2's phase. Its four opposite heights are

2+(2j-1)*h/4 + delta*(1-(2j-1)/4), j1..4.

The lower two lie belowh because their larger height is2+3h/4+delta/4<h, usingh>=12 anddelta<1. The upper two exceedh+2. The third lies below h+d+2 becauseh/4-delta/4<d/2+5/4<d ford>=6. The last lies aboveh+d+4 because3h/4-3delta/4>3d/2-3/4>d+2 ford>=6. Thus the two upper contacts straddle the entire second opening strictly. The three selected-side contacts have heights2+jh/2+delta*(1-j/2), j1..3. They all lie strictly in(3,2h+1) sinceh>=12 and|delta|<1. All portals remain within the selected mouths and every open core leg stays strictly between the physical floor and roof. Section1 gives the actual finite path.

Therefore this WHOLE arbitrary-horizontal-data A1 family illuminates for every h>=5,d>=1 EXCEPT possibly the following21 vertical cells:

d1:h5..6; d2:h5..8; d3:h6..10; d4:h8..12; d5:h10..14.

In particular, ALLh>=15,d>=1 and ALLh>=5,d>=6 are completely covered, with a cutoff INDEPENDENT ofc,D and all tooth widths. The21 remaining vertical cells each still have arbitrary real horizontal data; existing unitwidth seam certificates do NOT close them. Alsoh3/4 lies outside this theorem. No finite-remainder completeness claim is being substituted for the actual proved region.

## 3. Arbitrary-horizontal-data A0 family

Use the same selected teeth and marks, core heightG=2h+4 and opposite bands[h,h+2],[h+4,h+6], for every integerh>=9. All horizontal data remain arbitrary as above. For m2, its first opposite turn is belowh, and the last exceeds h+6 because

2+3h/2-delta/2-(h+6)=(h-8-delta)/2>0.

The selected-side turn2+h lies in the smooth gap. Thus the same direct matching gives an actualS-to-T path for EVERYh>=9 and everyc,D/independent width. The floor and roof never participate. This is a whole all-parameter family, not propagation from a seam witness.

## 4. Relation to the W21 reduction and evidence

The accepted A38 criterion already permits equal actual depthD and DIFFERENT unused selected widths. Its integerheight2 dark-level/charge argument in the accepted A48 proof therefore still forces an allegedq2,h>=3 same-abscissa dark pair atW<=21 onto precisely the four-band A0/A1 patterns, even with arbitrary tooth widths: both selected teeth are nonflush, all blockers lie away from the flush endpoints, and the remaining wall charge forces two opposite nonflush blockers and no unused attachment. This packet supplies explicit actual witnesses on the large vertical-parameter portion of those patterns with NO horizontal metric bound. It does not settle their remaining finitely many vertical patterns or general unequal-depth endpoint pairs.

Four PRESCRIBED rational formula controls in common-depth-zigzag-check.py/json exerciseD0,n0; nonzero depths; odd/even prefix parity; m2/m4; unequal selected/opposite widths; and nonintegralcorec. All68actual reflections and1440finite-wall leg guards pass. They are exact checks of the displayed formula, not discovered directions or samples proving the quantifiers. The algebra and strict inequalities above prove the complete stated coverage.

The source/target names never replace their physical endpoints by a reflected lift. No far wall is invented inside a wider tooth. The older finite unitwidth example tables are not used as proof of this new unbounded depth/width scope. General mixed unequal depths, higher teeth and arbitrary canonical45 geometry remain OPEN, and the native objective remains unfinished.
