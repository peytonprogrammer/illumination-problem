# Independent hand review of the eight-wall packet

Decision: no fatal mathematical gap found in the complete written proof chain after the corrections below. ACCEPT at the level of an independent AI hand reconstruction of the stated all-real orthogonal W<=8 theorem. This is not formal verification, external refereeing, a reflection bound, or any W10 extension. Original packet bytes are preserved in before/ and pinned in inputs.json. All frozen research proofs and historical acceptance receipts remain unchanged.

## Highest-priority mathematical steps

1. Roof corner / earlier target (Theorem 6.8 Step 4). On the actual upper strip write Beta=w+tau*h. At Beta=ja, periodic evenness gives F_a(Beta-sigma)=F_a(Beta+sigma). Setting sigma=tau*(H-y_t) identifies the ascending and nominated descending positions at the SAME actual height y_t. The ascending encounter precedes the roof because y_t<H. The lower two pieces already satisfy both strict portal guards; all upper contacts before y_t are between d and y_t, so the discarded roof corner is never reached. For y_t=d the identity reduces to F_a(w)=x_t and the path truncates at the second portal. Since 0<x_t<a, it is interior, not a corner or wall. No perturbation, target substitution or singular continuation is used.

2. Window amplification (Lemma 6.3 / Theorem 6.8 Step 1). The overlap of a radius-a window with a radius-R window, R=b+bg/H_s>b>a and center separation<=b, has length at least min(2a,a+bg/H_s). With H_s<c this implies ell>=min(2a,a+bg/c)=a*min(2,1+bg/(ac))=a Q_v. The original packet omitted the factor a in the denominator of its factored expression; the corrected inequality follows directly from its own lemma. Since T0<d and v>h>0, L=ell*(1+v/T0)>a Q_v*(1+h/d)>=2a. A target image therefore lies strictly inside the legal slope interval. The root retains the same tau and both original strict portal inequalities.

3. Exhaustion of staircase metrics (Proposition 6.10). For alpha=a/b,beta=c/d,p=alpha*beta,lambda=A/b,mu=H/d, failing F,Ft gives lambda>(1-p)/(1-beta), mu>(1-p)/(1-alpha). Outside the immediately sufficient Q=2 cases, either nonnegative E_lambda or E_mu yields Rh or Rv. Their sum is 2-s+p*(3s-4)-2p^2. The actual constraints give 2sqrt(p)<=s<1+p. If p>=1/3 its minimum occurs at the lower endpoint, with value 2(1-sqrt(p))^2*(1+sqrt(p)-p)>0. If p<1/3 its infimum at 1+p is (1-p)^2>0. Thus at least one E is positive. Equality in F/Ft is included directly; there is no missing limiting metric.

4. Floor chart and image choice (Theorem 6.5). An open interval longer than one complete period 2a of E={+/-x_t+2ma} contains two consecutive images: the sum of any two consecutive gaps is exactly 2a. Their slopes differ by less than 2a/D. Since D>c+y_s>2y_s, their developed floor coordinates differ strictly between 0 and a<A. They cannot both lie in AZ. At least one avoids a floor corner. Every other contact is inside a finite original vertical wall under the strict portal guards. No interpolation to the fixed target is being assumed.

5. L base/seam endpoints (Lemma 2.2 and its uses). The source-base variant has positive vertical height immediately after the start. At x=a it moves into the narrow column toward target t<a; at x>a the ordinary L arithmetic supplies q in (0,a) and lower x=0 contacts strictly above 0. In the wide-middle and staircase uses, that base or terminal seam is interior to the original room. The orientation-controlled path uses no artificial horizontal mirror, and added original corners are either outside the strict endpoint-height range or on an unused auxiliary wall. The whole actual ray is lifted without retuning.

6. U fixed point (Theorem 3.1). The functions L,R are nondecreasing step functions, including the zero-depth constant cases. Choosing B>2c*tau0 makes the first iterate strictly larger; tau_max is an invariant upper bound. A bounded interval admits only finitely many L,R values, so the increasing iteration terminates rather than merely converges. If the terminal value were a jump, the preceding L or R would be at least a full period smaller, contradicting the fixed-point equation. Hence both portal remainders are strict. The floor coordinate lies inside kA+(M/2,A-M/2), excluding both convex floor corners. The contacts of x=a before exit lie above c; x=0 contacts may be below c but remain on its genuine maximal wall. This distinction is corrected in the packet.

7. Remaining chain. Independently checked the six normal forms, their closure/positivity and k4 nonintersection condition; L target-image construction and its transpose; T endpoint placement/orientation lifts; wide-middle interval inclusion, target spacing and signed seam agreement; staircase placements and seams; and the main theorem's assembly. The proof is an exact finite case analysis for all real parameters. Its examples are controls, not an exhaustive numerical proof.

## Applied packet corrections

- Fixed the factored Q_v bound as detailed in item 2.
- Made the U high/seam endpoint case explicit by using y>=c in the opposite-arm branch; Theorem 3.1 already covers it.
- Corrected the U contact-height sentence: only inner-wall contacts must be above c; left-wall contacts can lie anywhere above the positive exit height.
- Allowed the wide-middle seam x=A equality when w=0; this is the same smooth original wall contact already covered by the local fold formula.
- Corrected six/eight-edge wording in the W6 classification paragraph.
- Fixed reproduce.sh to capture each Python exit code before truncating output. Its former python|head pipeline could report success despite Python failure.
- Corrected reproduce.md's claim that every command runs a scratch copy; the figure and manifest commands intentionally rewrite packet outputs in place.

These are explicit corrections to the derivative manuscript and its runner, not retrospective edits to frozen proofs. No new all-metric optical theorem is claimed from them.

## Verification and remaining review limits

The corrected runner executed all 12 existing prescribed checks successfully. An injected scratch-only Python failure with exit code 19 caused the runner to exit 19, with no success marker. This checks failure propagation, not mathematics. The independent ST10-E calculation is recorded separately in central-strip-check.json.

The theorem remains an AI-reviewed draft awaiting external mathematical review. The existing proof convention permits revisiting the source; reaching the target earlier allows truncation. No upper bound on U reflections is needed because finite iteration is proved per input. No source is inferred from an independently accessible target state. No claim about

## Mathematical referee addendum

This review gives a mathematical judgment. My
judgment is that the corrected eight-wall theorem is proved by the supplied
constructive chain. This is my own assessment, with the same AI-review limits,
not a claim of independent human refereeing.

I reconstructed the U construction's termination quantitatively. At every
strict update after the first, at least one nonnegative winding index must
increase, because the update is determined by their sum plus B. On the
bounded slope interval the selected indices satisfy

    n_L <= floor((y_s-c)*tau_max/(2a))+1,
    n_R <= floor((y_t-c)*tau_max/(2b))+1.

Thus at most 1+n_L(tau_max)+n_R(tau_max) updates reach the fixed point.
The selected value cannot be a discontinuity by the preceding strict-jump
contradiction. The complete physical ray then has exactly
2*n_L+2*n_R+2*k+1 reflections, with the finite upper bound inserted in the
packet. All contacts are still ordinary; this adds no new path selection
hypothesis and uses no rationality assumption. It makes the alleged
finite-iteration mechanism directly auditable rather than relying on a
limit of trajectories.

I also separated closure, positive lengths and simplicity in the U normal
form. Positivity gives H_L,H_R>c but does not alone imply c>0. With H_L>0
and 0<a<A, c<=0 makes the inner wall x=a meet the non-adjacent floor y=0.
The Jordan-boundary hypothesis excludes this. The manuscript now states
that necessary simplicity argument explicitly. This repairs an omitted
justification, not an excluded admissible room.

These are analytic proofs, not extrapolations from fixtures. No new
trajectory search or computational evidence was needed for the addendum.
The per-room reflection bound concerns opposite-arm U pairs; it is not a
uniform bound for all metrics or a ten-wall extension. The full proof's
quantifiers remain every orthogonal Jordan polygon with at most eight
maximal walls and every two distinct interior real points.
