# Jointly long perpendicular necks: actual illumination and a finite lattice reduction

A25 positive hand candidate, pending independent review. This entire packet retains the original A25 aggregate deadline. No room/ray/word search or new external theorem is used. The universal W<=21 objective remains open.

## 1. Model and two quantified conclusions

Fix three finite orthogonal polygonal chamber disks C0,C1,C2 with fixed marked interior points S in C0 and T in C2. Join C0 to C1 by ONE horizontal rectangular neck of width u>0 and length L>0, and C1 to C2 by ONE vertical rectangular neck of width v>0 and length K>0. Chamber shapes, mouth positions in chamber coordinates and widths are fixed; positions vary only by translation. Distinct piece interiors are disjoint, and all members considered are strictly simple disks. Mouth interiors are smooth. Fixed end collars may be absorbed into chambers. Denote the actual marked pair in the member (L,K) by S(L,K),T(L,K).

**Joint-tail theorem.** Suppose ONE member (L0,K0) has a finite legal actual S-to-T witness. Then there are finite thresholds L*,K* such that EVERY valid member with L>L*, K>K* illuminates its actual pair. The lengths are arbitrary REAL parameters; no balance, rational ratio, denominator or reflection bound is assumed. The supplied witness may traverse both necks repeatedly, enter/leave the same mouth, and reflect within the chambers arbitrarily many (but finitely many) times.

**Finite-lattice-reduction corollary.** Additionally suppose all members with L>=ell>0,K>=kappa>0 are valid, and at each fixed L the vertical-neck cut gives two opposing half-plane chambers as in the accepted long-neck-proof.md; likewise at each fixed K for the horizontal neck. Then all possible dark members on any discrete positive-length lattice in (L,K) lie in a FINITE rectangle of parameter values. This does not assert those remaining finitely many members illuminate. It is a finite reduction for this fixed geometric pattern, not an enumeration or a general W21 decomposition.

An explicit sufficient half-plane arrangement for the extra hypothesis is: after translating the mouths to the axes, C0 lies in x<=0,y<=0, C1 in x>=0,y<=0, and C2 in x>=0,y>=0; horizontal length shifts C1,C2 right, vertical length shifts C2 up, and no extra contacts occur. More generally require the opposing-half-plane cuts directly. A tree alone does not imply these separation conditions.

## 2. Fixed finite witness, cuts and two winding variables

Choose cuts a fixed positive distance inside each neck, avoiding the finitely many reference sidewall-hit abscissae/ordinates. Absorb the fixed collars into the chambers. Every mouth crossing of the reference witness is now strictly interior and transverse. All its neck visits are full traversals, since longitudinal velocity is constant and nonzero in a rectangle.

Normalize its DEVELOPED initial velocity to (1,tau0), with tau0>0, by reflecting the developing coordinate axes if necessary. Orthogonal wall reflection changes component signs only, so developed x and y increase along the entire unfolded witness. Let D>0 be its final developed x coordinate relative to the actual source; the target coordinate is (D,tau0*D).

At each designated cut or target i, let X_i,Y_i be its reference developed coordinates, and let a_i,b_i count COMPLETED horizontal and vertical neck traversals preceding that cut. A chamber block has the same counts at both its ends. At the final target write a,b for the counts. Both a,b>=1 because the endpoints lie in the outer chambers of the chain.

Put A=L-L0, B=K-K0. For integers n,m propose that every horizontal traversal acquires n additional full transverse periods and every vertical traversal m additional periods. The frame sign on exiting each neck is unchanged. The proposed downstream unfolded chamber copy is translated, relative to its reference image, by

    Z_i = (a_i*A + 2*v*b_i*m,  b_i*B + 2*u*a_i*n).       (1)

This is a realized-copy induction, not a free choice of target image: across a fixed chamber block Z is constant; across a horizontal neck it increases by (A,2*u*n); across a vertical neck by (2*v*m,B). The positive longitudinal increment in developed coordinates is the same even for a physical traversal in the opposite direction, since its current unfolding frame reverses that axis. Each extra full transverse period has the positive developed sign and adds two sidewall hits. Thus repeated and reverse traversals use the same integers n,m without reversing a coefficient in (1).

A reference wall word in each fixed chamber persists when its entry phase and slope are sufficiently near their reference values. Only finitely many blocks/cuts occur. Accordingly there is a common positive tolerance eta such that |tau-tau0|<eta and small cut residuals in the following formulas preserve ALL chamber contacts, cut apertures and corner clearances. It is harmless to shrink eta below tau0/4.

## 3. Two small phase errors control the ENTIRE path

Define

    alpha = tau*A - 2*u*n,
    beta  = B/tau - 2*v*m.                              (2)

For the candidate line y=tau*x through the developed actual source, its vertical residual at each proposed translated reference cut is exactly

    tau*(X_i+Z_ix) - (Y_i+Z_iy)
      = (tau-tau0)*X_i + a_i*alpha - b_i*tau*beta.       (3)

Here Y_i=tau0*X_i for the reference straight line. Thus sufficiently small |tau-tau0|, |alpha| and |beta| keep every cut phase and fixed chamber word legal. The neck rectangles themselves unfold into ordinary sidewall strips. Their strict entry/exit coordinates guarantee finite nonsingular crossings with the proposed unchanged parity of winding. For A,B sufficiently large the selected n,m below are nonnegative, so no reference bounce must be removed.

The ACTUAL target copy, dictated by (1), is

    (D+a*A+2*v*b*m, tau0*D+b*B+2*u*a*n).

Reaching it requires the EXACT scalar equation

    F(tau)=(tau-tau0)*D + a*alpha - b*tau*beta = 0.     (4)

Small residuals alone are not claimed to reach T. Section 5 solves (4) exactly while retaining every strict guard.

## 4. Curvature removes the parallel-neck resonances

Let J be any fixed closed interval of positive length strictly inside (tau0-eta,tau0+eta). As A,B independently tend to positive infinity, the curves

    tau -> ( A*tau/(2*u), B/(2*v*tau) ) mod Z^2,
    tau in J,                                         (5)

equidistribute on the two-torus with respect to normalized Lebesgue measure on J. In particular they meet ANY fixed open box about (0,0), for ALL sufficiently large A and B independently. No ratio restriction is needed.

Here is a direct proof of the needed assertion. For a nonzero Fourier character (h,k), its integral has phase

    phi(tau)=2*pi*( h*A*tau/(2*u) + k*B/(2*v*tau) ).

If k=0, integration gives a bound tending to zero as A tends to infinity. If k!=0, phi'' has constant sign on J and |phi''|>=c_J*|k|*B. For a threshold lambda>0, the set |phi'|<=lambda has length at most 2*lambda/(c_J*|k|*B). On each of the at most two complementary intervals, phi' is monotone and bounded away from zero, so integration by parts gives a bound <=C/lambda. Taking lambda=sqrt(|k|*B) gives O_J((|k|*B)^(-1/2)), UNIFORMLY in A. Thus every nonconstant character integral tends to zero whenever both A and B tend to infinity, with no balancing assumption.

To obtain visits to a particular box, choose a continuous nonnegative torus bump supported in that box with positive mean. Uniform approximation by a finite trigonometric polynomial and the preceding finitely many character bounds make its normalized integral positive for all A>A0,B>B0. The finite approximation can for example be supplied by the ordinary Fejer averages of the bump; their uniform convergence follows from the approximate-identity kernel. Only this elementary finite-Fourier argument is used, not a dynamical equidistribution theorem.

Unlike two parallel necks, the two phase functions tau and 1/tau have no persistent nonzero linear character of zero curvature. Their individual frequencies diverge separately, which is exactly the new input.

## 5. Exact endpoint correction inside one phase cell

Choose a small positive tolerance epsilon, and choose J still closer to tau0 if needed so D*|tau-tau0| is small compared to epsilon throughout J. Section 4, with a sufficiently small box, gives a tau1 in J and integers n,m such that the two errors in (2) at tau1 have absolute value below epsilon. Equation (4) then has |F(tau1)|<=C0*epsilon for a fixed constant C0 depending only on the reference witness and widths; enlarge C0 to include the chosen D*|tau1-tau0| bound.

HOLD n,m FIXED in a neighborhood of tau1. Directly from the actual target equation,

    F'(tau)=D+a*A+2*v*b*m > 0.                         (6)

For all sufficiently large B, 2*v*m=B/tau1+O(epsilon), so on the fixed positive compact slope window

    F' >= c1*(A+B)

for a constant c1>0. Since F is affine in tau at these fixed integers, it has one exact root tau* with

    |tau*-tau1| <= C2*epsilon/(A+B).                   (7)

The change in alpha is at most A*|tau*-tau1|<=C2*epsilon. On the compact positive window, the change in beta is at most C3*B*|tau*-tau1|<=C4*epsilon. All constants are independent of the ratio A/B. Choose epsilon sufficiently small, then enlarge the lower length thresholds so tau* stays in the original slope window. Equations (2)-(3) and the finite strict margins now keep the entire realized itinerary legal.

In particular the exact root lies in the SAME admissible full-period phase choices: entry and exit phases stay strictly within the reference apertures and sidewall parities. We do not re-round n or m after correction. Their positivity for sufficiently large A,B follows from tau in a positive compact interval and (2).

Finally F(tau*)=0 makes the straight developed line pass through the actual target image prescribed in Section 3. Refolding gives a finite actual S(L,K)-to-T(L,K) corner-avoiding specular path. Each parameter has finitely many added sidewall reflections, although the number grows. An earlier target visit is already a valid connection. This proves the joint-tail theorem.

## 6. A finite lattice remainder without assuming a witness on every fiber

Under the extra opposing-half-plane hypotheses in Section 1, fix one allowed L0. The accepted one-neck theorem applied to the vertical neck guarantees a legal actual path for some sufficiently large K0. This supplies the reference witness REQUIRED by the joint-tail theorem, without assuming the desired universal result. Its velocity components are both nonzero because any path from C0 to C2 must traverse both perpendicular necks.

Obtain joint thresholds L*,K*. On a discrete length lattice with fixed positive lower bounds, there are only finitely many allowed L<=L*. For EACH such fixed L, the one-neck theorem gives a finite K-threshold; take their finite maximum. Similarly there are finitely many K<=K*, each with a finite L-threshold. Together with the joint tail this bounds every possible dark lattice member inside one finite rectangle. No claim that the rectangle is uniformly bounded in W or already checked is made.

The accepted local-uniformity version of the one-neck theorem also yields a compact REAL-parameter remainder when the fixed-coordinate chamber families remain nondegenerate and satisfy its opposing-half-plane hypotheses on each compact interval. For the central lattice application the finite-coordinate argument above suffices and needs no additional compactness theorem.

## Scope and next proof obligations

This is a positive exact-target construction and finite reduction for a FIXED two-perpendicular-neck chamber pattern, at any wall count, with no size/k/diameter cap. Its joint-tail part assumes one finite witness and no half-plane separation beyond valid disks; its finite-remainder part removes that witness-existence premise using explicitly separating one-neck cuts.

It does NOT show that every W<=21 room admits this fixed-chamber decomposition, settle the finite remainders, treat three independent growing neck lengths, or transfer arbitrary intersecting coordinate-strip insertions. Those are explicit remaining universal obligations. No numerical certificate or dark example is supplied.

Dependencies: the accepted finite-itinerary stability/collar arguments in neck-ray-propagation-parallel-tree.md and the explicitly stated long-neck-proof.md for Section 6. Sections 2--5 rederive the mixed-neck copy and curvature calculations. Independent review must challenge reverse-traversal signs in (1), actual target-copy equality, uniformity in arbitrary A/B imbalance, phase-cell guards and the extra hypotheses in the finite reduction.
