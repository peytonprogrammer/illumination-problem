Advances: L1 — At any fixed positive depth ratio, an occupied lower box with the d190 upper template is lit once its height is sufficiently large relative to the upper vertical stretch. The bound is explicit and uniform in source abscissa, lower width and upper horizontal stretch.

# Clear the corner first, then open the mouth

Use the hypotheses of [the d190 scale step](l1-crossing-scale-step.md), including all roof openings in the near-side span and no extra openings on the sealed upper itinerary. Keep a stable positive-sheet upper approach, with template speed v in an interval J of length η, gate z₀=e−Bv in (0,R), period P and B≥1, as obtained there. The speed may be signed. Let h=a+d be the lower height and fix θ=d/h=r/s in lowest terms, 0<r<s. Thus a=2d means θ=1/3. Write X=D/u and Y=h/t for the lower dimensions measured in upper-template units, κ=X/Y, and ξ=c/D∈(0,1). No restriction on ξ away from the sides is needed.

The two depths do form one weighted vertical insertion (weights r and s−r). At fixed horizontal geometry d182/d184 transfer a lit seed along that slice. When the horizontal gap grows through the same occupied box, disjointness of the insertions fails. The proof below permits arbitrarily many lower roof reflections and does not transfer the original lower word.

**Theorem and explicit constants.** Put C=2+2R+P+η and
     
    κ₋=(1−θ)η/2,                 κ₊=16 C²/η.
    M=3s−r,                       Q=2 rad(M).

Here rad is the product of distinct primes of M. Choose N=M^(1+k φ(2s)), k≥0, sufficiently large that, with H=N/s,

    Hη/(4κ₊)>Q.

For example take k=max(0,ceil(log_M(1+4sκ₊Q/η))); no test of trajectories is involved. A sufficient condition for illumination is

    Y ≥ 1   and   κ₋Y > max{8RN³, 4κ₊R/(Hη)}.                (1)

All constants refer to the fixed upper template, the span and the depth ratio. Thus for fixed upper data (u=t=1) all sufficiently large lower heights are covered for *every* D,c. More generally (1) covers h/t tending to infinity, even if u and t also diverge.

**Aspect reduction.** If the direct and far-wall routes of d190 both fail, direct failure gives u(a+tB)η≤gcd(2Dt,auP)≤2Dt. Thus κ≥κ₋. The far-wall failure and reciprocal interval estimate in d190 give κ≤4C²(1+t/(a+2d))²/η≤κ₊ when Y≥1. Otherwise a d190 route already succeeds. We use d190 only for this reduction and the upper window.

**Corner-targeting lemma.** In unit lower-box coordinates unfold from (ξ,θ) toward (2j,1+2l). Choose the final level so its vertical travel is H: N≡s−r modulo 2s, so l=(N−s+r)/(2s) is a nonnegative integer. Indeed M≡s−r modulo 2s. For odd M it is coprime to 2s; for even M, s is odd, M is coprime to s, and the powers specified above preserve the residue modulo s and the even parity. The corresponding template speed is v₀=κ(2j−ξ)/H. We claim some j gives v₀ in the middle half of J and, at *every* earlier integer horizontal level, a horizontal distance at least μ=1/(4N³) from every integer. The final corner here is an auxiliary target only.

Index an earlier level by its integral vertical distance l' below the final one, 1≤l'<H. Its abscissa is

    2j−(2j−ξ)s l'/N.                                         (2)

The j interval allowed by the middle half of J has length Hη/(4κ)>Q. A value of ξ where (2) is an integer is rational with reduced denominator ≤s l'<N. Distinct rationals of denominator ≤N are separated by at least 1/N².

If ξ lies within 1/(4N²) of such a rational p/q (take all reduced rationals of denominator ≤N as candidates), choose j in the allowed interval as follows. For each odd prime dividing M, require that it not divide 2jq−p. If it divides q this holds automatically; otherwise just one residue of j is excluded. If 2 divides M and 2jq−p can be even, then p is even and q is odd. Choose j so that jq−p/2 is odd. These restrictions admit a residue class by CRT, with period at most Q, hence have a representative in the interval. They ensure gcd(2jq−p,N)≤2. Since gcd(s,N)=1, a corner contact at p/q in (2) would force N/gcd(N,2jq−p) to divide l'. This is impossible since l'<N/s≤N/2. Thus every critical ξ for the chosen j differs from p/q, and its distance from the actual ξ is at least 3/(4N²). If no nearby bounded-denominator rational exists, any allowed j stays at least 1/(4N²) from every critical ξ. In both cases (2) depends on ξ with derivative s l'/N≥1/N. This proves the clearance μ. The argument respects a signed J and does not require ξ rational.

**Move off the corner.** Use the positive horizontal and vertical sheets at the final even-column, odd-row corner. The true seam endpoint in the development must be 2j+(e−Bv)/X, so the exact joining equation and correction are

    ξ+Hv/κ=2j+(e−Bv)/X,        v−v₀=κ(e−Bv₀)/(HX+κB).

Since v₀ lies in the middle half of J, |e−Bv₀|≤R. If X>4κ₊R/(Hη), then v∈J and the seam point is strictly inside the prescribed open mouth. At every earlier level the horizontal displacement from (2) is at most R/X. If X>2R/μ then each such contact stays farther than R/X from every integer abscissa. All corner lifts are avoided. All earlier roof contacts miss every near-side mouth, whose unfolded abscissas are within R/X of an even integer. Between horizontal levels lateral reflections are on smooth walls. At the last level the positive-sheet choice matches the forward upper speed and vertical sense. This proves (1), since X≥κ₋Y in the residual aspect range. No shot of the proof goes through the auxiliary corner.

## Consequence for the product with two gaps per axis

There is also an arithmetic restriction on the remaining *comparable* region. Write 2Dt/(auP)=p/q in lowest positive terms. Direct failure forces

    q=auP/gcd(2Dt,auP) ≤ P/η,     κ=(1−θ)Pp/(2q).

Moreover the same direct inequality gives t/a≤P/(Bη), and the downward far-wall estimate yields κ≤4C²(1+P/(Bη))²/η even for Y<1. Consequently p is bounded explicitly by 2κq/[(1−θ)P], with κ replaced by this last upper bound. For fixed θ and upper template there are only finitely many possible κ at a dark placement. Direct failure gives Y≥Bη/[P(1−θ)]; (1) bounds Y above and the aspect inequality bounds X above. None of these arguments needs a seed at area ≤20.

On a rational product of horizontal and vertical factors satisfying this same template description, the ratio κ=(D/u)/(h/t) is continuous and takes values in the finite list on its positive integral dark placements. Independent clearing of rational denominators by axis scaling preserves κ. Thus on a wholly dark positive product it is constant by density and connectedness. Independence of the axes then makes D/u and h/t separately constant. Their *individual rational heights* do not follow from bounded magnitudes and a bounded-height quotient: (m+1)/m in both factors has quotient 1 for every m. This last arithmetic example is not a dark room. It is the precise limit of using the aspect equation factor by factor. The remaining two-gap product has comparable lower and upper dimensions in template units, with possibly high-denominator proportionalities. If the upper chamber changes internal shape, the uniform window and constants require a separate argument as well.

**Scope.** The threshold is not uniform in θ and can diverge as θ tends to one. When t grows with h, finite coupled aspects alone give no individual denominator bound. The [shallow-source return](l1-shallow-roof-return.md) addresses θ tending to one separately. This proves a fixed-ratio tail for a rectangular lower box, a scaled upper template and mouths in the stated span. It gives no chart-wide H(C), G(C) or census ceiling. It uses the physical d190 gluing estimates; the inference about arbitrary dark flats additionally uses the project's conditional finite-flat input. No room, size, direction, ray or reflection-word searches were run.

**What is the smallest W ≤ 20 room this result doesn't cover?** The W=10 all-length word LLLRLLLRLR remains open, realized by (2,0),(4,0),(4,1),(3,1),(3,4),(0,4),(0,3),(1,3),(1,2),(2,2). No ledger word changes status.
