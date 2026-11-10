# Uniform independent-depth illumination for equal-height comb teeth

A30 strengthening, under the SAME original05:31:36Z aggregate deadline. This supplement preserves the frozen unequal-rate proof. Candidate for independent review; no ray search, finite control, reference trajectory or empirical rate inference is used.

## 1. The actual statement

Fix c,u,M_min>0 and interior offsets0<b_s,b_t<u. In ANY finite valid rectangular-spine comb, select two teeth of height u with lower/upper bands[l,l+u] and[l+H-u,l+H], where H>=2u+M_min. The spine has width c and contains those bands. Other teeth and spine ends are arbitrary consistent with a strictly simple comb. For actual marks

    S=(c+D_s,l+b_s), T=(c+D_t,l+H-b_t),

assume D_s,D_t>0 and their tooth right ends lie strictly beyond them. There is ONE finite D0 depending ONLY on c,u,M_min,b_s,b_t such that EVERY D_s,D_t>=D0 illuminates the actual pair. In particular D0 is independent of their ratio, H, intermediate teeth and both far-end margins. Rational listed data give a computable rational D0, though the procedure below can be enormous and is not claimed executed.

As in the independently reviewed direct comb construction, it suffices to find signs sigma_s,sigma_t, nonnegative integers k_s,k_t and tau>0 with

    r_s=sigma_s*b_s+D_s*tau-2u*k_s in(0,u),
    r_t=sigma_t*b_t+D_t*tau-2u*k_t in(0,u),
    r_s+r_t+2c*tau=H.                                      (1)

These equations construct actual tooth contacts at x>c, a protected two-leg spine path at x<c with one smooth actual x=0 reflection, and exact actual T. No artificial spine-end reflections occur. The source-sign and odd/even contact formulas of unequal-rate-comb-proof.md section4 apply unchanged once(1) is established.

## 2. A finite Fourier dichotomy, uniform in H and depth ratio

Put gamma=u/2, epsilon=gamma/8=u/16, beta=epsilon/(2u)=1/32 and mu=beta^2. Set

    t_min=M_min/(2c), d=min(t_min/4,gamma/(16c)), ell=2d.

For any current H use tau_center=(H-u)/(2c) and J=[tau_center-d,tau_center+d]. This interval has the SAME positive length ell for all H and lies above3t_min/4.

Let f be the product of two periodic tent functions of height1, centered at the zero phase with support[-beta,beta]. Its torus mean is mu; its Fourier coefficients are nonnegative and their absolute sum is1. In one variable the coefficients are beta*sinc(pi*n*beta)^2, with coefficient beta at n0. The sum of coefficients outside the square |h|,|k|<=K is at most4/(pi^2*beta*K). Choose a fixed integer K>16/beta^3; the omitted sum is then<mu/4 even using pi>1.

Choose C>8u/(ell*mu). Consider the phases

    theta_s=(b_s+D_s*tau-u/2)/(2u),
    theta_t=(b_t+D_t*tau-u/2)/(2u).

If EVERY nonzero integer pair(h,k) with |h|,|k|<=K satisfies

    |h*D_s+k*D_t|>C,                                       (2)

then its character average on J has magnitude at most2u/[pi*ell*|h*D_s+k*D_t|]<mu/4. Multiplying by the finite coefficients and summing keeps the entire nonzero retained contribution below mu/4, since their total absolute mass is at most1. The omitted contribution is below mu/4 as well. Thus the average of f on J exceeds mu/2, for EVERY such pair of depths and EVERY center of J. There is tau0 in J with f>0, hence integers k_s,k_t giving errors

    e_s=b_s+D_s*tau0-2u*k_s-u/2,
    e_t=b_t+D_t*tau0-2u*k_t-u/2,
    |e_s|,|e_t|<epsilon.                                   (3)

No limit in a varying depth ratio is used. This is a finite-frequency alternative.

If(2) fails and min(D_s,D_t)>C, the exceptional character must have both coefficients nonzero and opposite signs. Same-sign or one-zero characters have magnitude at least min(D_s,D_t)>C. Divide by their gcd and orient signs to get coprime positive integers m,n<=K with

    E=m*D_s-n*D_t, |E|<=C.                                 (4)

This is the bounded resonance case addressed next. The two alternatives exhaust ALL sufficiently large depth pairs.

## 3. Uniform strict portals in every bounded resonance tube

For fixed coprime1<=m,n<=K and E in[-C,C], put z=E/(2c). Let delta=m*sigma_s*b_s-n*sigma_t*b_t. Eliminating tau in(1) gives the weighted phase equation

    (m+z)r_s+(-n+z)r_t = delta+zH-2u*j,
    j=m*k_s-n*k_t in Z.                                   (5)

The image of(0,u)^2 under its left functional has length

    W=u*(|m+z|+|-n+z|)>=u*(m+n)>=2u.

If W>2u, every phase has a strict representative for either fixed sign choice. Equality W=2u forces m=n=1 and -1<=z<=1; changing sigma_s shifts delta by2b_s, strictly between0 and2u, so the two source signs cannot both lie in the excluded endpoint class. Thus for EVERY E and EVERY phase theta modulo2u replacing zH, one of the signs and some integer j yields a STRICT solution(r_s,r_t) in the open square.

There is a uniform rho>0 for these solutions, independent of E, theta, m,n and H. Here is the complete compactness justification. At any chosen solution at least one functional coefficient is nonzero: m+z and -n+z cannot both vanish. Hold one portal coordinate fixed and solve for the other while E and a LOCAL real lift of theta vary. The resulting solution varies continuously, with the same signs and j, and remains strictly inside the square in some open parameter neighborhood. This gives an open cover of the compact set[-C,C] times the phase circle. A finite subcover and the minimum of its positive portal margins give rho for that m,n. There are finitely many m,n, so take the minimum again. Different charts may use different signs, j and portal points; no continuous global choice is assumed. Translating theta by its period merely changes j. Therefore for each ACTUAL H choose a solution of(5) with

    rho<=r_s*,u-r_s*,r_t*,u-r_t*.

Set tau*=(H-r_s*-r_t*)/(2c)>t_min. This lower bound is uniform even though H and tau* may be arbitrarily large.

For rational fixed data this uniform margin is COMPUTABLE, not only abstract. Represent theta by[0,2u]. Enumerate rational fixed portal coordinates, rational candidate margins, signs and integers j. Solving for the other coordinate gives a rational function of E,theta with linear denominator. On a fixed denominator sign, the inequalities that both portals have the candidate positive margin define open rational polyhedral chart domains. These charts cover the closed rational rectangle[-C,C]x[0,2u]: strict feasibility at every point persists, and rational choices can approximate the fixed coordinate. Coverage by any finite list is decidable by its finite rational-linear sign arrangement. Enumerate until it covers; compactness guarantees termination. The minimum of its stored positive margins works. Repeat over the finitely many m,n. No such enumeration is executed here, and no practical complexity or small threshold is asserted.

## 4. Exact target correction in the nonresonant case

At the integers selected in(3), set

    F(tau)=b_s+D_s*tau-2u*k_s
           +b_t+D_t*tau-2u*k_t+2c*tau-H,
    A=D_s+D_t+2c.

F is affine of derivative A>0. At tau0 its magnitude is at most2c*d+2epsilon<=3gamma/8. Define tau'=tau0-F(tau0)/A. Then F(tau')=0 EXACTLY. Each portal changes by at most |F(tau0)| because0<D_s/A,D_t/A<1. Its total distance from u/2 is therefore less than epsilon+3gamma/8=gamma/2. Both corrected portals are strict.

Choose D0 additionally so3gamma/(8A)<t_min/4 whenever D_s,D_t>=D0; D0>3gamma/(4t_min) suffices. Since tau0>=3t_min/4, this gives tau'>t_min/2. The indices remain fixed during correction. Finally use the exact equations themselves to obtain

    2u*k_s=b_s+D_s*tau'-r_s> -2u+D_s*t_min/2,

and likewise for k_t. D0>4u/t_min makes both integers positive. Thus the phase selection has become an ACTUAL path certificate(1), not just an approximate or chosen-sheet connection.

## 5. Exact weighted rounding in the resonant case

Use the selected strict portal pair from section3. Choose Bezout integers alpha*m+beta0*n=1. The index solutions are

    k_s=alpha*j+n*h, k_t=-beta0*j+m*h.

Set C0=H-sigma_s*b_s-sigma_t*b_t+2u*(alpha*j-beta0*j). Choose h nearest to[A*tau*-C0]/[2u*(m+n)] and define

    tau=[C0+2u*(m+n)*h]/A.

The sum/target equation is EXACT and |tau-tau*|<=u*(m+n)/A<=2u*K/A. At this tau the portals are ALSO exactly

    r_s=[nH+delta-2uj+(E-2nc)tau]/(m+n),
    r_t=[mH-delta+2uj-(E+2mc)tau]/(m+n).

Their tau derivatives have absolute value at most B=C+2c. Put eta=min(t_min/2,rho/[2(B+1)]). Choose D0>u*K/eta; then A>2u*K/eta and the rounding error is<eta. Thus tau>t_min/2 and both portal margins remain>rho/2. This is independent of H, the Bezout representative and the aspect ratio. Positivity of the two actual winding indices follows from

    2u*k_s=sigma_s*b_s+D_s*tau-r_s> -2u+D_s*t_min/2>0

under D0>4u/t_min, and similarly for k_t. An H-dependent index base never needs a separate bound.

A single D0 exceeding C, u*K/eta,4u/t_min and3gamma/(4t_min) satisfies BOTH branches. For rational fixed data choose it rational, using the terminating chart-cover procedure for rho. All constants depend only on the stated fixed data. Equations(1) now hold for every depth pair beyond this threshold.

## 6. Physical realization and scope

The exact direct realization is the SAME independently accepted construction in unequal-rate-comb-proof.md section4: signed initial tooth legs with ordinary horizontal-wall contacts strictly x>c, strict actual mouth crossings, two central legs at x<c with one actual smooth left-wall hit, and the reversed upper tooth leg ending at ACTUAL T. Its mirror word and number of bounces can vary with every parameter; neither is uniformly bounded here. Other teeth and their created corners are untouched. No bound on area, k, number of extra teeth or actual separation H is used beyond H>=2u+M_min.

This proves a uniform entire two-independent-depth tail for equal-height selected teeth, with arbitrary aspect ratio and a vertical-separation-uniform threshold. It is stronger than eventuality on each fixed ray, and was not inferred from raywise coverage or a compactness assumption on rate ratios. The finite Fourier/resonance split supplies the missing uniformity.

It does NOT illuminate the region where one depth stays small, the finite prefixes of a chosen lattice family, unequal selected heights or arbitrary noncomb rooms. Coupling those remaining axes to literal neck theorems requires its own actual geometric proof. The universal W<=21 theorem remains OPEN. This supplement is a hand proof candidate pending independent review, not formal verification.
