# A29: positive U matching does not automatically transfer to inner teeth

Status: the proposed all-depth long-vertical-gap shortcut is RETIRED. This is an exact obstruction to one prescribed mechanism, not a dark room and not a universal illumination obstruction.

## The part that works

For selected tooth heights a,b, spine width c and gap M, set actual source offset b_s from its lower floor and target offset x_t from its lower floor. The U phase ladders are P_s=a-b_s or a+b_s, and P_t=x_t or2b-x_t. At tau>=0 choose the first P_s+2an> D_s*tau and P_t+2bm>D_t*tau. Iterating tau_new=(L+R+M)/(2c+D_s+D_t) from0 is monotone, bounded and finite-valued, hence terminates at a fixed point. At the first stationary iterate neither ladder jumps, so ell_s=L-D_s*tau and ell_t=R-D_t*tau are strictly between0 and their respective2a,2b periods. The matching identity is2c*tau=M+ell_s+ell_t. If M>=2max(a,b), both portal x coordinates c-ell_s/tau,c-ell_t/tau lie strictly in(0,c).

## Missing actual-mirror guard

If ell_s=a, the source arm meets its outer mouth endpoint at x=c, an actual reflex corner when the selected tooth is internal. If ell_s>a, the last outer arm reflection occurs at x<c on the auxiliary spine cut y=l_s. That cut is NOT an actual mirror. Thus positive portals and exclusion of equality alone are insufficient. For the protected monotone central construction with no physical spine-end reflections one needs the stronger0<ell_s<a and0<ell_t<b. The target has the identical issue.

## Exact failure of ALL four phases and ALL arm windings

Take c=a=b=1, D_s=D_t=1/2, b_s=x_t=1/3 and M=5. The phase ladders are P_s in{2/3,4/3} and P_t in{1/3,5/3}, each with period2.

For any proposed legal monotone one-left-wall-bounce path, the strict residual requirements imply

    5/2<tau<7/2,     5/4<D_s*tau<7/4.

Thus L must lie between D_s*tau and D_s*tau+1, and can only be4/3 or8/3 from the two source ladders. Similarly R can only be5/3 or7/3 from the two target ladders. The exact matching equation is3*tau=L+R+5. These four possibilities are:

    L4/3,R5/3: tau8/3, ell_s0 (inner-corner equality);
    L4/3,R7/3: tau26/9, ell_s-1/9 (not a forward valid arm);
    L8/3,R5/3: tau28/9, ell_s10/9>1 (artificial-cut reflection);
    L8/3,R7/3: tau10/3, ell_s1 (outer-corner equality).

None is legal. This excludes every arm winding for these FOUR phase ladders under this prescribed central mechanism, not merely the first fixed points found by iteration.

The failure persists for M=5+8q, q>=0 integer: replace tau by tau-4q and subtract2q from L,R. The phase ladders and strict residual inequalities reduce exactly to the same four cases. Hence making only this vertical gap arbitrarily large does not repair this particular construction.

For an actual strictly simple canonical control, choose the spine[0,1]x[0,11] and four teeth[c,2] on bands[0,1],[2,3],[8,9],[10,11], marks(3/2,7/3),(3/2,25/3). Scaling by12 gives a strict sixteen-wall canonical45 room with actual even-even marks(18,28),(18,100). The prescribed obstruction still holds under similarity. This is not a dark-pair assertion. A valid path may use the actual spine ends, tooth roofs, or additional visits.

## Computation and decision

The first bounded discriminator checked only residual equality and was too weak; no proof claim came from its15552 controls. The corrected guard test stopped after four prescribed rational parameter patterns with the displayed exact counterexample. The hand enumeration above independently excludes all winding indices for that input and its8q translates; computation is not the proof. No general room/ray search was performed. No associated process remains.

Do not continue expanding this false long-gap k0 premise. The next positive obligation is to combine the peer's new no-supplied-witness marked-comb horizontal-tail result with the accepted mixed-neck joint-growth theorem on a literal disjoint H/V strip decomposition. That addresses two-parameter atlas fibers with actual paths, not another k0 phase variant.
