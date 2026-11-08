# Independent A26 review: reflex coalescence with a convex return

Verdict: ACCEPT the full stated conditional tail theorem, including its ordinary-prefix palindrome extension. The visible opposite-sector convex return and all full-trace hypotheses are essential; no universal visibility or wall-count consequence is accepted. Independent exact hand reconstruction only; no computation or discovery scan.

For the direct case set Dx=2H+(c-a)e and Dy=2K+(b-d)e. Both are positive at small e>0. The unfolded source-to-actual-target-image line is (-a*e,b*e)+t*(-Dx,-Dy). Its vertical-wall time is (H-a*e)/Dx and its horizontal-wall time is (K+b*e)/Dy. Both lie strictly between0and1. Their difference, after multiplying Dx*Dy, is exactly

    e*(H*(b+d)+K*(a+c))+e^2*(b*c-a*d).

This has positive leading coefficient even when H,K vary affinely. Hence the vertical wall is first. Its physical ordinate is above p by Dy*(ty-tx)>0. Reflecting x, the following horizontal contact is to the right of p by Dx*(ty-tx)>0. Both distances are O(e), so the two genuine finite mirror interiors are used and the actual corner is missed. The two perpendicular mirrors compose to central inversion about p, giving target image2p-T exactly. Reversing those actual reflections therefore ends at the actual T.

At the reflex source corner O the outgoing leg starts x<0 and travelsSW, so it cannot enter the missingNEquadrant. On return it approaches the actual T through y<0. At p, the entering, between-contact and outgoing segments are in its NEinterior. Strict separation of all nonincident indexed boundary pieces and nonzero incident lengths provide fixed corner neighborhoods with no extra mirror. On the compact trimmed portion of Op, the full limiting trace has positive separation; actual finite pieces converge and hence cannot create an unintended hit. Thus each entire actual leg stays inside, with exactly the intended smooth contacts. No convergence argument discards a thin slit or a created wall.

For the prefix extension, let h be the composition that unfolds the ordinary prefix into the initial O chart. Its linear part is an axial signed matrix and its translation depends affinely on e. The central pair of incident mirror reflections is Jp(z)=2p-z. The complete palindromic word acts on the actual target as

    h*Jp*h^-1(T)=2*h(p)-T.

This identity is valid for moving supports and preserves the actual target offset in the INITIALchart. The supplied unfolded corner h(p) has two negative coordinates, and the incoming reference segment approaches it in its convex sector, so its unfolded interior sector isNE. The same two-contact calculation applies there. Ordinary prefix contacts and their reversed counterparts retain their finite strict transversality/order/full-trace guards. Near O the initial and terminal arm argument is unchanged. This proves the claimed finite2k+2reflection construction (or a shorter prefix if the actual target is reached earlier).

All source hypotheses were retained: positive a,b,c,d,H0,K0; actual distinct interior endpoints; persistent reflex and convex corner walls; full trace excluding other endpoint collisions; strictlySWinitial prefix and a negative-coordinate unfolded convex corner. No proof of existence of that prefix/visible corner for arbitrary polygons is supplied or inferred. Boundary coalescences with other scales, extra collapsed mirrors or failure of this visibility premise remain unresolved. The universal W21 theorem is not accepted by this receipt.
