# Two growing equal-width necks: reduction to finitely many resonant ratios

Candidate theorem, Codex01a18403. Independent review pending. This treats simultaneous geometric growth, retaining the exact physical marks and the intermediate chamber phase. It is not the uncapped W<=21 theorem.

## 1. Fixed geometric data and quantified conclusion

Fix w,h>0 and three finite strictly simple orthogonal polygonal disks A,B,C. Put A in x<=0 with smooth mouth {0}x(0,w); B in 0<=x<=h with smooth mouths {0}x(0,w) and {h}x(0,w); and C in x>=0 with smooth mouth {0}x(0,w). Fix actual interior S in A and T in C. For L1,L2>0 join them in order by horizontal rectangular necks of width w and lengths L1,L2, translating B and C to their stated positions. Assume no additional contacts so the resulting room is a strictly simple disk. The physical target is the corresponding translate of the actual T.

There are constants a,b,d>0, a nonempty bounded signed slope interval I=(u,v) excluding0, and a nonempty circular phase arc J of length ell>0, depending only on the fixed chambers, mouths and marks, with the following consequence. Define

    D=L1+L2+a+b+d,
    rho=(L1+a)/D in (0,1),
    R={p/q in [0,1], reduced, q>=1, q<=1/ell}.

R is finite. For every open neighborhood U of R in [0,1], there is a finite D0 such that EVERY pair L1,L2 with D>D0 and rho outside U admits a finite actual corner-avoiding specular S-to-T connection.

In particular, if L1,L2 tend to infinity with L1/(L1+L2) tending to an irrational number, the actual pairs illuminate eventually. More generally any limiting ratio outside R has this conclusion. A dark sequence in this fixed family with D tending to infinity must have its ratio approaching R. No member of R is asserted dark or impossible to handle by a different itinerary.

The constants and D0 are chamber/mark dependent. There is no bound in W, exhaustive room decomposition, arbitrary-width-ratio extension, or diagonal-chamber assertion.

## 2. Common angular class and a first-transit middle beam

Use the independently accepted directional-minimality input of long-neck-proof.md: outside countably many magnitudes, the four-sign invariant surface of each orthogonal chamber is minimal. Also exclude the countable corner-hit directions from the fixed S,T, including removable corners. Choose one common positive magnitude m0. The finite FIRST-mouth paths from actual S,T exist by the accepted flow-box argument and are corner avoiding. Their finite words persist on an open interval of magnitudes.

We also need a genuine first transit of B from its LEFT mouth to its RIGHT mouth. At the same magnitude choose an inward left-mouth phase avoiding all corner-hit orbits. The excluded starting ordinates are countable, while the mouth interval is open. Its forward orbit in the CLOSED auxiliary B is complete and dense, so it reaches the right mouth in finite time. Before its first right-mouth hit, take the LAST left-mouth hit, or its initial left-mouth departure if there was no return. There are only finitely many wall hits in this finite segment. The portion after that last departure reaches the right mouth with no intervening hit of either mouth. Neither auxiliary mouth reflection belongs to the retained transit.

Thus some finite middle word is a legal first LEFT-to-RIGHT transit. All its non-mouth contacts are transverse and corner avoiding. There is a product of open intervals

    m in I_m,  z in J0=(zlo,zhi) strictly inside (0,w),

on which this SAME finite word takes an incoming left-mouth ordinate z and its fixed incoming vertical sign to the right mouth, with strict exit ordinate. Shrink I_m so the two end words remain valid there as well. Product openness follows from continuity of finitely many strict transverse contact and first-mouth guards; no infinite itinerary is assumed stable.

The minimality input is used only to obtain finite words and open beams. It is not an inference that a dense ray hits the exact target point.

## 3. Fixed affine charts and signs

Let the left and right end virtual marks in their final mouth charts be

    S*=(-a,alpha),  T*=(b,beta), a,b>0.

Let eS,eT in {+1,-1} be the vertical signs when their forward paths from S,T first reach their mouths. The horizontal signs are respectively +1,-1. Set the global signed slope tau=eS*m; its common interval is I=(u,v), of width delta>0. The reversed right-end word has physical slope -eT*m.

Let e0,e1 be the incoming and outgoing vertical signs of the middle transit, whose horizontal velocities are both positive. Unfold its finite word in the initial middle chart. The outgoing physical copy has affine coordinates

    (x,y) -> (x+d-h, kappa*y+c0),
    kappa=e0*e1,  d>0.

Indeed its derivative is diag(+1,kappa): both physical horizontal velocities are positive, while unfolding must match the initial direction. Its developed mouth is x=d; positive travel time and unit horizontal speed give d>0. The constants d,c0 and all signs depend only on the fixed word, not on m,z or the neck lengths. The transit satisfies

    kappa*z_out+c0 = z + e0*m*d.

Define

    sigma1=eS*e0,
    sigma_out=sigma1*kappa=eS*e1,
    sigma2=-eS*eT.

The normalized middle-entry phase must lie in

    J = (sigma1*J0)/(2w) modulo1,
    ell=|J0|/(2w) in (0,1/2).

This arc lies strictly in one half of the circle. Consequently membership gives a unique actual z in J0 and an integer first-neck period n1, with developed entry ordinate 2*n1*w+sigma1*z. The derivative of the first-neck fold there is sigma1, so its physical incoming slope is sigma1*tau=e0*m, exactly the middle beam's sign.

## 4. Exact endpoint equation and the intermediate phase

Unfold the middle with the affine chart above after its first-neck placement. At its right mouth the developed horizontal coordinate is L1+d, and the developed vertical chart has offset

    B0=2*n1*w+sigma1*c0,

and derivative sigma_out with respect to physical y. A second-neck reflected copy of the virtual target therefore has ordinate

    B0+2*n2*w+sigma2*beta,

where n2 is any integer. This is the standard period2w of that neck: if its physical period index is k, then n2=sigma_out*k, still an arbitrary integer. Its final fold orientation relative to the second-neck starting chart is sigma_out*sigma2, giving physical terminal slope sigma2*tau=-eT*m as required by the reversed target word.

Write N=n1+n2 and

    K=sigma1*c0+sigma2*beta-alpha.

The EXACT developed target image then gives

    tau_N=(K+2*N*w)/D,
    D=L1+L2+a+b+d.

The first middle-mouth developed ordinate is alpha+tau_N*(L1+a). Normalizing by2w gives its phase

    phi_N = alpha/(2w) + (K/(2w)+N)*rho  modulo1,
    rho=(L1+a)/D.

Thus it suffices to choose an integer N with BOTH tau_N in I and phi_N in J. If these hold, define n1 from the unique middle entry stripe and set n2=N-n1. The phase relation then determines the exact actual middle entry, follows its fixed finite transit to its strict exit, and matches the actual target word through the second neck. No target sheet is replaced and neither intermediate mouth coordinate is chosen freely after N is fixed.

For clarity, the second-neck physical fold is applied to sigma_out*(Y-B0). At its start this equals z_out in (0,w). At the far mouth it equals an integer period plus (sigma_out*sigma2) times the target word's actual mouth ordinate beta-b*sigma2*tau_N. It therefore returns that exact ordinate with physical slope sigma2*tau_N. This proves the splice with both possible orientations.

All source/middle/target words keep their strict finite guards. Each neck is traversed once and all its horizontal folds occur at smooth actual walls, strictly between its two joints; the selected phase arcs keep every mouth interior. Finite lengths and nonzero finite tau give finitely many contacts. These are genuine finite physical trajectories, not concatenations with independently chosen angles.

## 5. Elementary robust rotation-net lemma

For any open circular arc of length ell, a finite set of circle points with maximum circular gap less than ell meets EVERY translate of that arc. This property persists under sufficiently small perturbations of the finite points: a perturbation by at most epsilon increases the maximum gap by at most2epsilon.

If r is irrational, the finite initial orbit {0,r,...,m*r} has maximum gap less than ell for some finite m. Here is an elementary existence argument. Pigeonholing fractional parts produces an integer q with 0<||q*r||=gamma<ell/2. Multiples of either q*r or -q*r give a mesh with gaps at most gamma up to one turn. Their finitely many possibly negative indices can be shifted to nonnegative indices; the resulting translated mesh is contained in some finite initial orbit. Its largest gap remains less than ell. Irrationality prevents gamma=0.

If r=p/q is reduced and q>1/ell, its first q orbit points are an exact q-grid with gap1/q<ell. Hence the same finite-gap property holds. In both cases a neighborhood V_r of r retains the property for the SAME finite index bound m_r, because each of the first m_r points moves by at most m_r times the change in step.

Every r in [0,1] outside the finite set R therefore has a neighborhood with this robust finite orbit net. This is not an assertion that a changing rational step is automatically dense; it is a finite, uniform-in-starting-phase statement on a specific neighborhood.

## 6. Exact integer selection and uniformity off resonant neighborhoods

Let U be any open neighborhood of R. Its complement is compact. Choose finitely many of the neighborhoods V_r covering that complement and let m be the maximum of their finite orbit index bounds. For every rho outside U, the first m+1 rotation points have maximum gap less than ell. Every block of m+1 consecutive rotation points is a translate, so the same conclusion holds with ANY initial phase, including the length-dependent phase offset in phi_N.

The condition tau_N in (u,v) puts N in the OPEN real interval

    ((D*u-K)/(2w), (D*v-K)/(2w)),

of length D*delta/(2w). If this length exceeds m+2, that interval contains m+1 consecutive integers strictly inside it. Their phi_N values are a translate of the finite net, so one lies in the actual arc J. Choose it. Section4 then constructs the exact actual S-to-T trajectory.

Taking D0=2w*(m+2)/delta proves the uniform statement. In particular, along any sequence whose ratio tends to a number outside R, a neighborhood disjoint from R eventually contains the ratios; use the corresponding finite net and D tending to infinity. Finally rho and L1/(L1+L2) have the same limit because a,b,d are fixed and total neck length diverges.

## 7. What has and has not been reduced

Possible asymptotic failures in this fixed three-chamber/equal-width family are confined to a FINITE set of bounded-denominator rational ratios. They are not established failures of illumination. The set depends on a chosen actual middle transit beam; changing words may remove some or all of these residues. The earlier coupled-neck obstruction has limiting ratio1/2, necessarily in this possible exceptional set because ell<1/2. Its already-illuminated U8 rooms do not contradict this theorem.

No assertion handles the rational resonances, arbitrary moving/degenerating chambers, changing marks, shrinking or unequal apertures, more than two necks, diagonal-wall chambers, or rooms without this decomposition. There is no W-only bound on the finite net size, angular interval, threshold or denominator cutoff. No ray, direction, word or room discovery was performed. The full uncapped W<=21 objective remains open and this candidate requires explicit independent review.
