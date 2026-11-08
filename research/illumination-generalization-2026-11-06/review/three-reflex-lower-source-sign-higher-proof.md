# LS02: half-divisibility suffices for higher-valuation transport

Independent reciprocal review pending. This is a new quantified extension of LS01/EA06. It proves conditional lower/upper pair theorems at arbitrary positive valuation gap and, as a complete native consequence, the ordered equal-arm cap-depth-two family at a TWO-step gap. It does not prove arbitrary higher-gap rooms, all r3 or r<=8.

## Fixed geometry and marks

Retain the ORDERED actual spiral: positive integers P<L, L power of two, N>P+L; rational e>0; a=R=Pe,A=Ne,B=Le,l=A-B,w=A-a; integer heights 0<b<c<h<H with h even and c odd. Write p=nu2(P),t=nu2(N)>p. Actual rational-horizontal terminal marks have 0<s<a,l<target_x<A,0<v<c and even integer vertical marks. Put z=A-target_x, f=(h-v)/2,g1=h-c,d2=c-v. These are positive integers except rational z; g1,d2 are odd and 2f=g1+d2.

Claim L: for b<u<h, let alpha=(h-u)/2,beta=H-h. If beta is divisible by 2^(t-p-1), EVERY such actual pair illuminates.

Claim U: for h<=u<H, let n=(2H-h-u)/2>0. If n is divisible by 2^(t-p-1), EVERY such actual pair illuminates.

The exponent is nonnegative. At t=p+1 these divisibility conditions are vacuous, recovering the accepted lower and upper results. At larger gap they are genuine hypotheses; no unsupported residue-density statement replaces them.

## Strict lower seed is independent of valuation and beta parity

Use the exact two actual source images +s,-s and the same half-open basis as LS01. The coefficients lambda_sigma=-sigma*s/(2a)-alpha*N/(2Pbeta), mu=z/(2a)-f*N/(2Pbeta) give strict source and cap residuals for both signs. They have the SAME j,m=0 and Delta_i=i_plus-i_minus in {0,1}. Direct subtraction gives

    r_plus-r_minus=(d2/d)*(s-a*Delta_i), d=alpha+beta+f.

This is nonzero with absolute value less than 2a because 0<s<a and d2<2f<2d. Hence both seeds cannot be true right corners. The argument uses no assumption on nu2(N), nu2(P), or beta parity. Under the positive kernel H0=gcd(Nalpha,Pbeta,Nf), the full-period-fiber branch preserves the chosen safe source sign during finite positivity restoration. The non-full-period branch instead restores positivity then repairs a corner with at most one null. These are the exact physical strict seeds already hand-verified in LS01. The source sign remains the ORIGINAL S with its chosen initial horizontal velocity.

## Strict upper seed is independent of valuation

Set d=n+f,Hupper=gcd(nP,Nf). The accepted seed-existence portions of EA07, UE01 and SS01 exhaust dP greater than, equal to, or less than 2Hupper. Their arithmetic, exact integer preimages and simultaneous actual cap/right access do NOT use the one-step valuation premise. Specifically:

- In the greater branch, two strict cap columns and the exact vertical fiber give a safe right phase; the projection gcd is strictly less than 2Pd.
- At equality, n=f,Hupper=nP and P|N. A nonaligned offset has two columns. For an aligned single column z1=0 and integer full-period ratio Rf, r1/a=Rf*(2m+1)-(g1/(2n))*(s/a) is noninteger by its strict original-source offset in (0,1).
- In the reverse branch, Hupper=nP,n>f. Two actual SOURCE signs give nearest cap-index difference 0 or -1 and a right-phase difference which cannot be an even multiple of a. This supplies a safe sign. A non-full-period fiber instead permits usual null repair.

All cases have positive integer null increments to make actual m,q nonnegative and tau positive. Thus a physical strict upper seed exists without a valuation assumption; only target transport below needs the new divisibility. No upper source band or degenerate lower determinant is inserted at u=h.

## Why HALF the previous divisibility is enough

For Claim L, beta divisible by 2^(t-p-1) implies nu2(Pbeta)>=t-1. The Nalpha and Nf terms have valuation at least t. Hence nu2(H0)>=t-1. For Claim U, n divisible by that power implies nu2(nP)>=t-1 and nu2(Nf)>=t, so nu2(Hupper)>=t-1. Write Hstar for the relevant gcd in either case.

Set D0=gcd(g1*N,2Hstar),B0=2Hstar/D0. Since g1 is odd and nu2(Hstar)>=t-1,

    nu2(D0)=min(t,1+nu2(Hstar))=t.

The positive block of B0 null returns preserves all relevant literal signed residuals. Its actual increments are delta_j=2Nf/D0 and delta_k=g1*N/D0. Both are integers, since D0 divides 2Hstar and Hstar divides Nf. Their difference

    delta_M=N*d2/D0

is an INTEGER because 2Nf-g1N=Nd2, and is ODD because d2 is odd and nu2(D0)=t. D0 need not divide N. This holds exactly at nu2(Hstar)=t-1, where the individual null may be a full right period and EA06's original non-full-period repair alone was insufficient. The paired-source seed proofs supply the missing safe seed.

Let ell=log2(L),Lambda=lcm(P,N),Gamma=gcd(Lambda*d2,L)=2^min(t,ell). Since P<L and t>p, rho=Gamma/2^p is a positive power of two at least 2, potentially much larger than 2. Odd delta_M is a unit modulo this FULL rho. A finite 0<=b0<rho makes M=j-k divisible by rho, equivalently J=PM divisible by Gamma, retaining the odd part of P as an invertible factor. A subsequent finite common-period correction 0<=p0<L/Gamma makes J divisible by L because Lambda*d2/Gamma is a unit modulo L/Gamma. Final E=z modulo the TRUE period 2Le reaches the SAME actual T. No step replaces modulo rho by mere parity.

All updates are exact integer fold increments and choices of one final slope. Lower source/cap/right signs, or upper cap/right signs, remain literal and strict. Physical walls, finite mirrors, velocity matching, first target, lower roof exclusion and upper FINAL exact-S roof suffix retain the original accepted proofs. In particular these statements require only ordered widths and actual source/target placement, not N parity.

## Whole native TWO-step-gap cap-depth-two family

Now take e integral, H=h+2 and t=p+2, with all other ordered geometry and parity hypotheses unchanged. Every actual native terminal source has u<=h because h and H are even and differ by two.

For lower sources beta=2 is divisible by 2^(t-p-1)=2, so Claim L covers every one. At the mouth u=h, n=beta=2 meets Claim U. There are NO actual native upper levels h<u<H. Every bottom even v has odd d2. Thus all residual terminal pairs are covered, and accepted protected TR01/TR05 placement and legal reversal prove illumination of EVERY distinct actual native even-even pair in this entire family. Metrics, support, area and reflection count are unbounded. This is a new whole family beyond WJ01's valuation range, even though its cap depth is fixed at two.

## Prescribed actual rays and limits

Own two declared exact inputs have e4,P1,N12,L8,b1,c3,h6,H8,T=(20,2). Lower S=(2,4) gives H0=2=t-1 in valuation, selected source sign -1, final slope magnitude 779/5 and indices (39,6,74,58). Mouth S=(2,6) gives Hupper=2, equality cap spacing and final slope 621/4 with indices (m,j,k)=(6,74,58). Both require TWO positive blocks to correct modulo rho=4, then a nonzero full target-period shift. Both end at E=156=28 modulo 64, so actual target x=48-28=20. Exact original-wall first-hit replays pass a combined 347 reflections and 3490 finite wall/leg guards. No author code was run.

These finite controls corroborate the quantified proof, not a search or numerical coverage argument. No discovery, new clock, engine, census, fitting, worker, frozen edit or git mutation occurred. Arbitrary beta at gaps >=2, unrestricted upper n at those gaps, all larger unequal-arm/parity/type cases, all-r3 and r4..8 remain OPEN. Reciprocal independent review is required before acceptance.
