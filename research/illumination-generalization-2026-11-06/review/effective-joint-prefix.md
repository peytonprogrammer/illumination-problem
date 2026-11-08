# Explicit joint-tail bounds and a computable finite lattice prefix

R27 positive theorem for independent review. It makes the accepted A25 two-perpendicular-neck reduction effective for rational data. This is not a proof that the finite prefix illuminates or that arbitrary W<=21 rooms admit the fixed-chamber model.

## 1. An explicit phase-box lemma

Fix rational 0<t_-<t_+, a nondegenerate rational interval J inside [t_-,t_+] of length ell, widths u,v>0, and a phase tolerance 0<e<min(u,v)/2. Put

    delta_x=e/(2u), delta_y=e/(2v), mu=delta_x*delta_y.

For every real A,B satisfying

    A > 4u/(ell*mu),
    B > 256*v*t_+^3/(ell^2*mu^2),                       (8)

there are tau1 in the INTERIOR of J and integers n,m with

    |A*tau1-2u*n|<e,
    |B/tau1-2v*m|<e.                                  (9)

No restriction is imposed on A/B.

### Direct quantitative Fourier proof

On the unit circle take f_delta(x)=max(1-dist(x,Z)/delta,0). It is the circle convolution of two centered interval indicators of length delta, divided by delta. Its Fourier coefficients are

    c_0=delta,
    c_h=delta*(sin(pi*h*delta)/(pi*h*delta))^2>=0.

They are absolutely summable, and their sum is f_delta(0)=1. To justify the last identity without a dynamical theorem: the coefficients are O(1/h^2), so their series converges uniformly to a continuous function with these coefficients; the elementary Fejer approximate-identity argument identifies it with the continuous convolution. This is ordinary Fourier analysis, not an imported orbit-classification result.

The product f_delta_x(x)*f_delta_y(y) is nonnegative, supported in the desired phase box, has mean mu, and has nonnegative absolutely summable two-dimensional coefficients of total mass1. Termwise integration is justified by uniform absolute convergence.

For a nonzero character (h,k), along the curve (A*tau/(2u),B/(2v*tau)) its phase is phi=pi*h*A*tau/u+pi*k*B/(v*tau). If k=0, direct integration bounds its normalized integral by2u/(ell*A). If k!=0, phi'' has constant sign and magnitude at least Q=|k|B/(v*t_+^3). The set |phi'|<=R has length at most2R/Q. On each of at most two complementary intervals, integration by parts with monotone phi' bounds the integral by3/R, hence6/R in total. Choosing R=sqrt(Q) gives the normalized bound

    8*sqrt(v*t_+^3)/(ell*sqrt(B)).

This is uniform in A, h and nonzero k. Therefore the average of the product bump along J is at least mu-E, where

    E=max(2u/(ell*A),8*sqrt(v*t_+^3)/(ell*sqrt(B))).

Under (8), E<mu/2. Its average is positive; some interior tau1 lies in the open support, proving (9). No finite-Fourier truncation or uncontrolled tail is hidden in the estimate.

## 2. Explicit endpoint correction constants

Use the independently accepted A25 notation for ONE actual finite witness: slope tau0>0, developed target(D,tau0*D), horizontal/vertical traversal counts a,b>=1, widths u,v. Suppose a positive rational r<=1 is certified such that

    |tau-tau0|<r, |alpha|<r, |beta|<r

keep every finite chamber word, cut aperture and reflection parity legal, with alpha=A*tau-2u*n and beta=B/tau-2v*m. Such an r is an input guard certificate, not guessed from a sample. For rational geometry and an exact rational reference path it is computable: unfold each finite chamber word, express all local contacts and cut residuals in tau-tau0,alpha,beta, and retain a sufficiently small rational box around the strict reference inequalities. Denominators are nonzero there. Expanding each strict polynomial about the reference point and letting its positive constant term dominate the remaining coefficients gives a finite rational box. The mixed-neck copy induction is the accepted A25 theorem; no new geometric decomposition is assumed.

Set rational constants

    t_-=tau0/2, t_+=3tau0/2,
    c=min(a,b/(2*t_+)),
    C0=1+a+b*t_+, C=C0/c,
    e=min(u/4,v/4,r/(8*(1+C+C/t_-^2)),tau0/(8*(1+C))),
    j=min(r/4,tau0/8,e/(2D)), J=[tau0-j,tau0+j], ell=2j.

Use mu from section1 and choose

    A_* = 1+max(4u/(ell*mu),(2u+e)/t_-),
    B_* = 1+max(256*v*t_+^3/(ell^2*mu^2),t_+*(2v+e)).    (10)

For every A>A_*,B>B_* the phase-box lemma supplies tau1,n,m satisfying (9). In particular n,m>=1. Let alpha1,beta1 be the two signed errors. Define the EXACT slope

    tau*=(tau0*D+b*B+2u*a*n)/(D+a*A+2v*b*m).            (11)

Its denominator is positive. At fixed n,m the endpoint residual F is affine with derivative

    F'=D+a*A+2v*b*m >= a*A+b*B/(2*t_+) >= c*(A+B).

Indeed 2v*m=B/tau1-beta1, and (10) makes B/t_+-e>=B/(2*t_+). The numerator residual at tau1 is bounded by C0*e because D*j<=e/2. Hence

    |tau*-tau1| <= C*e/(A+B).

Our choice of e and A+B>2 gives drift <min(r/16,tau0/16). Thus tau* remains in the positive compact interval [t_-,t_+], and |tau*-tau0|<r. The corrected phase errors satisfy

    |alpha*| <= (1+C)*e < r,
    |beta*| <= (1+C/t_-^2)*e < r.

The entire actual itinerary therefore remains legal. Formula (11) is precisely F(tau*)=0, so it reaches the actual target image fixed by the copy induction. This proves an explicit joint tail without changing endpoint fibers or rounding n,m again. Large winding counts remain finite at each parameter.

For rational A,B all of this is an exact constructive algorithm. To locate tau1, enumerate the FINITELY MANY integers n,m whose phase intervals can meet J. The first inequality in (9) gives a rational open interval for tau1. Since m>=1, the second gives

    B/(2v*m+e) < tau1 < B/(2v*m-e).

Intersect with the interior of J. The lemma guarantees at least one nonempty intersection. Choose a rational midpoint and use (11). This is a finite analytically justified interval computation; no failed trajectory search is used as evidence.

## 3. Effective witness existence and the finite integer rectangle

Consider rational fixed chambers, mouths, actual marks and a rational positive lattice of lengths, with ALL the opposing-cut and validity hypotheses of A25 section6. Its reference witness can be found by a terminating positive procedure: fix an allowed rational L0 and dovetail allowed lattice K-values, rational launch directions and finite wall-contact caps. The accepted one-neck theorem ensures some such member illuminates. In rational orthogonal data every finite actual connecting path has a rational unfolded endpoint displacement and therefore rational direction. Some finite search stage must find an actual path; exact all-wall checking then verifies it. This is an algorithmic termination proof, not a claim that a bounded execution has been run or that its time is controlled by W.

For the fixed-coordinate tails needed below, the one-neck thresholds can also be computed. Enumerate rational magnitude slopes and finite first-mouth words in BOTH auxiliary closed rational chambers, retaining all four velocity-sign choices. The accepted one-neck proof provides a common OPEN magnitude interval on which two such beams reach their mouths without a previous mouth hit or corner. That interval contains a rational slope and finite words, so a dovetailed positive beam search terminates. Compute rational strict subinterval I and virtual points from the two exact words. The accepted formula max(0,2w/|I|-(a_left+a_right)) is then an explicit threshold. Merely enumerating one beam at a time would not establish a compatible common interval; simultaneous magnitude compatibility is required and justified here.

Apply section2 to the verified reference path, obtaining explicit joint thresholds L_ref+A_*,K_ref+B_*. Enumerate the finitely many lattice L-values below the first joint threshold; for each compute its one-neck K-threshold by the positive beam procedure. Do the symmetric operation for lattice K-values below the second joint threshold. Maxima of these finite lists and the joint thresholds give an EFFECTIVELY COMPUTABLE finite rectangle containing EVERY possible dark lattice member of this fixed rational pattern.

The rectangle is a finite list of unresolved actual instances, not a list of dark rooms. Verifying actual witnesses for all of them closes the WHOLE pattern; an independently proved actual dark member would refute it. The theorem proves neither alternative for the prefix. It also gives no practical size bound: the conservative constants and the reference-word searches may be very large. Each actual computational discovery effort remains subject to Daniel's separate840-second aggregate limit; no unbounded procedure is executed or silently restarted here.

## 4. Checks and scope

The companion prescribed checker verifies the rational endpoint/error constants on fixed algebraic input fixtures, including extremely imbalanced positive length increments. These are algebra checks, not actual room certificates, and are not used as substitutes for the Fourier or geometric proof. No room/direction search is run in R27.

This converts an existential finite-lattice reduction into an exact finite-prefix certificate target for rational TWO-neck fixed-chamber patterns. Arbitrary W<=21 strip families may have changing chambers, more independent widths/lengths, unmatched cuts or unresolved collapse/slit directions; they are not automatically covered. General canonical45 and arbitrary-wall bridges remain OPEN. No new degree bound, symmetry exclusion or unconditional strip monotonicity is claimed.

Dependencies: independently reviewed perpendicular-neck-joint-proof.md and mixed-neck-residue-proof.md for actual-copy induction and path guards; accepted long-neck-proof.md and its primary-input receipt for positive beam existence. The quantitative Fourier bound, explicit endpoint correction and effective-prefix algorithm are derived here.
