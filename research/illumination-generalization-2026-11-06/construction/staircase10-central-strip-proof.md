# ST10-E: exact central-strip reduction and obstruction to a crossing proof

## Decisions and scope

PROVED here, pending independent review: every pair not covered by the four accepted L placement lifts can be moved by a WHOLE-ROOM transposition and endpoint reversal into the central-strip target domain stated below. These are actual isometries/reversals, with unchanged endpoints under the isometry, not a geometric filling or a choice of another target preimage.

NOT PROVED: all such pairs have the proposed one-left-excursion path. The physical endpoint fan is discontinuous at genuine reflex hits. The explicit frozen-control calculation below refutes the naive continuous-crossing premise, not the entire class. It is a concrete instance of the already recognized singular-fan difficulty; it is not claimed as a new theorem about darkness.

## 1. All-metric actual endpoint normalization

Use the accepted cross-placement S=(s,u),T=(t,v): s>=w2,0<u<y2,y2<=v<H,0<t<the actual width at v<=w2. ML01 leaves precisely

 (u<y1 OR v>y3) AND (t<w3 OR s>w1).

If t<w3, retain the original orientation. If t>=w3, actual interior membership forces v<y3: at or above y3 every actual interior x is strictly less than w3. The residual then forces s>w1, and hence u<y1. Transpose the entire room and exchange the endpoint names. The new data are

 (w0p,w1p,w2p,w3p)=(H,y3,y2,y1),
 (y1p,y2p,y3p,Hp)=(w3,w2,w1,w0),
 Sp=(v,t), Tp=(u,s).

All strict width/height orderings hold. Source satisfies sp=v>=y2=w2p and 0<up=t<w2=y2p. Target satisfies vp=s>w1=y3p and 0<tp=u<y1=w3p, with vp<Hp by actual source membership. Both are actual interior points under the isometry. Thus in BOTH cases one obtains

 s>=w2, 0<u<y2, y2<=v<H, 0<t<w3.       (CS)

Equalities s=w2 and v=y2 are retained; t=w3 in the old orientation goes into the transposed case, and no limiting argument is used. Integral geometry and even-even marks stay integral/even-even under transposition. Billiard reversibility restores the requested original order.

Consequently, a universal optical existence result on (CS), combined with the accepted L lifts, would cover all original four-band metrics and endpoint placements. This is a sufficiency reduction, not such an existence result.

## 2. Precise widening-only mechanism

Let x decrease from actual s to0 with horizontal velocity -1 and initial vertical velocity lambda, where lambda is any finite real. Reflect vertically once from the ORIGINAL maximal left wall x=0, then let x increase to actual t. Because t<w3, the full returning segment remains in the genuine central rectangle (0,w3) times (0,H). Along the outward segment the ceiling height is nondecreasing as x decreases: y1,y2,y3,H, skipping all columns right of the actual source. Every ceiling and floor segment used is a true original horizontal wall. Arbitrarily many such contacts are allowed. This is the one-left subfamily of the already admitted transposed outer class, not a new claim of class completeness for all rays.

At a widening vertical section x=wj the incoming strip has height h and the new strip height hnew>h. Write W_h(z)=z-2h*floor((z+h)/(2h)) with values in [-h,h); at its upper-cusp values use one-sided limits. An incoming signed phase r is propagated across horizontal distance d by r+lambda*d. If the old folded coordinate is below h, the unique signed residual W_h(r+lambda*d) lies strictly between -h and h. The new fold locally agrees with its absolute value, preserving position AND signed vertical velocity. The value zero is a legal smooth original floor reflection, since (wj,0) is not a polygon corner. Values plus/minus h are the genuine reflex corner (wj,h) and must be excluded. No extra mirror is inserted at the vertical section.

In the final height-H strip, the actual endpoint ordinate is F_H(r+lambda*l), where l is the remaining horizontal travel to0 and back to t and F_H(z)=distance(z,2H Z). The left-wall contact must also avoid the true corners (0,0),(0,H). If a putative matched path hits such a left corner, the final-strip symmetry F_H(B-z)=F_H(B+z) at B in H Z gives the SAME actual T at the earlier outward crossing x=t. Truncating before that corner is legal provided all earlier guards hold. This is the transposed earlier-target argument, not a continuation through a corner.

The exact global obligation remains: find ONE lambda with all encountered true reflex guards and endpoint equation F_H(r+lambda*l)=v, or earlier actual T. The signed residual r depends on the same lambda through every preceding widening. Local maps alone do not establish that obligation.

## 3. Actual endpoint-fan discontinuity on the frozen lit control

Use ONLY the already frozen geometry widths(40,12,8,4), heights(0,12,16,20,40), actual S=(38,2), and target abscissa t=2 (the specified frozen target is (2,38)). Take lambda0=5/13. The first widening, at x=12 after distance26, meets phase2+26lambda0=12, exactly the genuine reflex corner (12,12). It is forbidden.

For lambda just below lambda0, there is no initial ceiling contact and the signed phase entering the height16 column tends to +12. For lambda just above, one ordinary contact with the REAL ledge y12 at x>12 occurs before the widening; the signed residual tends to -12. No source or sheet is changed.

Subsequent limits are as follows; all lie strictly within the indicated next strip, so no second critical event coincides at lambda0.

| Position | Phase from below | Phase from above | Genuine ceiling after entry |
|---|---:|---:|---:|
| x=12 | 12 | -12 | 16 |
| x=8 | 176/13 | -136/13 | 20 |
| x=4 | 196/13 | -116/13 | 40 |
| x=0 | 216/13 | -96/13 | 40 |
| x=2 after left reflection | 226/13 | -86/13 | 40 |

Each horizontal distance from12 to8,8 to4,4 to0 is4; the returning distance0 to2 is2. Thus these entries follow by adding20/13 or10/13 respectively. At x8 both incoming height16 phase magnitudes are strictly below16; at x4 both incoming height20 magnitudes are strictly below20. At x0 both folded heights are in (0,40), so the left reflection is ordinary. All these inequalities persist in one-sided open slope neighborhoods.

The two ACTUAL limiting endpoint heights at x2 are therefore226/13 and86/13, distinct by140/13. Even modulo the final height40 billiard circle, the two signed phases differ by24, which is not a multiple of80. The endpoint fan has a genuine jump. Its branch equation has nonzero slope, and it has a positive-length terminal central corridor, but neither fact supplies the missing intermediate-value or degree assertion.

This does NOT exclude an endpoint at height38 at other slopes, does NOT refute the full one-left family or ST10-A, and does NOT describe a dark pair. The already independently accepted16-reflection ray illuminates the specified pair. It only makes precise why a continuity-through-reflex proof for ST10-E cannot be used.

## 4. Frontier and stopping decision for this hand attempt

The endpoint normalization is a reviewable all-metric reduction. The physical transfer is a prerequisite, not a positive intersection theorem. The proposed continuous-crossing proof fails on the original frozen control. An all-branch union or discrete arithmetic invariant might still force target attainment, but none has been proved here; generic recurrence, average angular drift and finite residue counts cannot replace that missing implication.

There is currently no justified general nonemptiness argument for either this class or the complete five-programme union, and no complete failure of either class has been shown. Repeating the conditional folds would not be progress. Do not count this limitation as full-goal completion. No new ray/direction/room discovery, new clock, engine, census, fitting, worker, frozen edit or git action. All staircase10, all-r3 and r<=8 remain OPEN.
