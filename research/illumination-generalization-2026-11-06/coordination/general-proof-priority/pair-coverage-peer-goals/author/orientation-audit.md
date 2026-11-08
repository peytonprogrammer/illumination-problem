# Both orientation and parameter audit

These are partial ingredients, not full coverage. The full-group obstruction in obstruction.md supersedes the positive-coverage programme. Existing L illumination remains known and unchanged.

## Globally valid anchored shears

For P(A,a,B,H), the actual vertical cylinders are (-a,a) times R/(2H Z) and (a,2A-a) times R/(2B Z). V_k has shifts k(x+a) and k(x-a). Conditions ka/H and k(A-a)/B integral give pointwise boundary agreement, a common derivative, an inverse using -k, and preservation of all regular and singular physical corner lifts.

Put Gv=gcd(aB,H(A-a)). All REAL parameters satisfying these anchored full-twist conditions are exactly k=n*HB/Gv. Indeed write k=H*m/a; the second condition requires aB to divide H(A-a)m, hence m is a multiple of aB/Gv. This is a discrete rational parameter group, not a continuous choice.

Within this family Z preservation is equivalent to k being integral. Sufficiency follows from integral coefficients and chart offsets for the map and inverse. For necessity, ka is already integral. If a=1 this forces k integral. If a>=2, the integer smooth-floor point (1,0) has image vertical phase k(a+1); preserving integer lifts forces k integral after subtracting integer ka. The integral subgroup has minimum K_v=lcm(H/gcd(a,H),B/gcd(A-a,B)). No claim that these two parabolic directions generate the full affine group is made.

Transpose the WHOLE room. The parameters become (Anew,anew,Bnew,Hnew)=(H,B,a,A). Thus the horizontal cylinders are y in (-B,B), x modulo 2A, and y in (B,2H-B), x modulo 2a. H_l has shifts l(y+B) and l(y-B), with common derivative [[1,l],[0,1]]. Conditions lB/A and l(H-B)/a integral give the same gluing/corner proof. With Gh=gcd(aB,A(H-B)), the real anchored parameter group is l=n*Aa/Gh. Its integral Z-preserving subgroup has minimum K_h=lcm(A/gcd(B,A),a/gcd(H-B,a)).

## Actual target domains

The vertical all-real-source criterion requires the ACTUAL target (t,v) to satisfy 0<t<a,0<v<H, and v+k(t+a)=0 modulo 2H. It maps q to the original smooth bottom point (t,0). Sources in the vertical rectangle have identity seeds; other sources are in the bottom-right arm, where V_k or R_y V_k puts their images in the original closed lower rectangle. The r=0 and r=B cases are smooth floor/ledge seeds, not corners. The seed to (t,0) crosses x=a strictly below B.

The horizontal analogue requires target 0<v<B,0<t<A, and t+l(v+B)=0 modulo 2A. Transposition gives its all-real-source proof, mapping the target to the left wall (0,v). It cannot be applied directly to an upper-arm target.

A hidden pair has bottom-right S=(s,u), a<s<A,0<u<B, and upper-left T=(t,v),0<t<a,B<v<H. The vertical test can target T. The horizontal test must reverse the pair and target S, giving s+l(u+B)=0 modulo 2A. Both exact endpoint sheets are restored by inverse transport and reversal.

For all allowed real vertical parameters, the zero-floor equation is Gv*v+HB*(t+a)*n=0 modulo 2H*Gv. Its exact integer solvability condition is gcd(HB*(t+a),2H*Gv) dividing Gv*v. The dual horizontal condition is gcd(Aa*(u+B),2A*Gh) dividing Gh*s. These remain sufficient subfamilies only; failure is neither darkness nor a full-group obstruction.

## Abandoned weaker composition test

The originally declared A=H14,a=B6 control has minimal anchored real parameters 21Z in both directions; both exact endpoints S10,2,T2,10 are fixed by V21 and H21. That would defeat all their compositions, but not establish full-group failure. Its prescribed check was cancelled BEFORE implementation/run because the peer supplied the stronger L8 full-group invariant. Do not count the L14 control as executed. The L8 proof needs no generator list and directly resolves the intended criterion negatively.
