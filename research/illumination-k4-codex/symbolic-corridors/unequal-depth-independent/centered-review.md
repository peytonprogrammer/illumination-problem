# Independent review: every centered outer pair illuminates

Codex01a1a00f, 6 November 2026.

Verdict: ACCEPT the exact pinned centered-theorem.md, including its complete
classification of centered vertical-only failures and its actual-wall repairs.
No mathematical correction is required. This is a full arbitrary-real theorem
for CENTERED horizontal coordinates s=t=d. The thread's broader goal for
independent s,t remains OPEN.

## Statement, geometry and dependencies

All dimensions d,g,h_-,h_+ are positive, 0<a<h_-,0<b<h_+.
The room is exactly the three-band twelve-wall corridor, and the marks are
S=(d,-a),T=(d,g+b). Positive diagonal scaling normalizes d=g=1:
axis reflection changes the sign of one component before and after scaling,
so the specular law, smooth actual contacts and corner avoidance are preserved.
Set H=a+1+b, alpha=a/H,beta=(a+1)/H; then0<alpha<beta<1.
Conversely every such phase pair corresponds to positive
 a=alpha/(beta-alpha), b=(1-beta)/(beta-alpha), with g=1.
Thus classifying the entire phase triangle covers every allowed depth pair.

The needed four-chart sufficiency and its complete vertical-only necessity
are independently audited in vertical-completeness-review.md. The midpoint
cap repair is separately independently accepted in repair-review.md and
repair-acceptance.json. Both apply with arbitrary cap clearances, and neither
assumes a rational room. The older full symmetric packet and large-denominator
center graph census are unnecessary dependencies here.

## 1. Exact trigonometric criterion and all vertical-only words

Every centered unfolded target is an odd integer L=1+2n. Write
A=pi n alpha,B=pi n beta. The first residue E1=1+2n alpha mod4 lies
in the allowed union(1,3) exactly when sin A>0, excluding its internal
point2 exactly when cos A=0. On(1,2) its cosine is positive and c=1;
on(2,3) its cosine is negative and c=3.

For c=1, the union of its allowed upper residues is(0,2) minus{1}:
this is precisely cos B>0 and sin B!=0. For c=3 it is(2,4) minus{3},
precisely cos B<0 and sin B!=0. If either sine vanishes or either
cosine vanishes, a required portal is at a corner, so the strictness is
essential. Otherwise replacing n by -n, if needed, makes sin A positive
without changing either cosine or whether sin B vanishes. Hence the
existence of a chart is equivalent to some integer n satisfying
 C_n=cos A sin^2 A cos B sin^2 B>0.
This is both necessary and sufficient for every vertical-only connection,
not merely for a preselected reflection word. Our earlier unfolding audit
independently proves there is no additional such word outside the union.

## 2. Fourier mean and the nonpositive-sequence contradiction

The identity cos x sin^2 x=(cos x-cos3x)/4 gives EIGHT cosine terms:

32 C_n = cos n pi(alpha+beta)+cos n pi(alpha-beta)
       +cos n pi(3alpha+3beta)+cos n pi(3alpha-3beta)
       -cos n pi(alpha+3beta)-cos n pi(alpha-3beta)
       -cos n pi(3alpha+beta)-cos n pi(3alpha-beta).

I independently expand the two univariate exponentials and multiply them.
The checker recovers all16 exponential coefficients, respectively +/-1/64,
and all eight cosine coefficients, respectively +/-1/32. Their sum is0,
as required by C_0=0.

The mean of cos(n pi lambda) is1 if lambda is an even integer and0
otherwise, by the finite geometric sum. Every positive cosine term can
only increase the mean. For the negative terms, the strict phase triangle
gives these exact ranges and even-integer possibilities:

- alpha+3beta lies in(0,4): only2;
- alpha-3beta lies in(-3,0): only-2;
- 3alpha+beta lies in(0,4): only2;
- 3alpha-beta lies in(-1,2): only0.

They give exactly alpha+3beta=2,3beta-alpha=2,3alpha+beta=2,beta=3alpha.
No negative resonance on a boundary of one of those ranges is possible.
Outside these four lines the mean of C_n is nonnegative, including cases
where positive resonances raise it. No assumption of irrationality or
absence of other integer relations is being introduced.

Assume also alpha,beta!=1/2. Since both are strictly between0 and1,
their first sines are nonzero and C_1!=0. Group the FINITE exponential
frequencies modulo integers before taking the mean of |C_n|^2. The finite
geometric formula annihilates cross terms between distinct groups, leaving
sum|group coefficient|^2. At least one grouped coefficient is nonzero:
otherwise every C_n, including C_1, would be zero. Thus the squared mean
is strictly positive. Equivalently, Cauchy-Schwarz even bounds it below by
|C_1|^2/16, since there are at most16 grouped frequencies.

If every C_n<=0 for nonnegative n, the real bound |C_n|<=1 implies
C_n^2<=-C_n. Its mean would then be at most the negative of a nonnegative
number, contradicting the strictly positive squared mean. Some finite n
has C_n>0. A sign change of that n gives the required chart if necessary.
This is a finite-exponential argument; no infinite Fourier convergence,
quantitative mixing or unproved recurrence theorem is used.

## 3. All four exceptional lines, irrational phases and the finite table

On beta=3alpha and3alpha+beta=2 use theta=alpha. On alpha+3beta=2
and3beta-alpha=2 use theta=beta. The other coordinate equals3theta
or is congruent to its negative modulo2. The function cos(pi x)sin^2(pi x)
is even and2-periodic, so the product is EXACTLY its value at(theta,3theta).
This is an identity, not a sign approximation.

For irrational theta, apply the already independently audited pigeonhole
circle-density proof to theta/2 modulo1, or equivalently theta modulo2.
Some finite integer multiple has residue strictly in(0,1/6). Both cosines
are then positive and both sines nonzero, giving C_n>0.

For reduced theta=p/q in(0,1), the cyclic orbit modulo2 has step
G/q, G=gcd(p,2q) equal to1 or2. Its smallest strictly positive residue
is at most2/q. At q>=13 this is strictly less than1/6. One explicit
choice is n=p^-1 mod2q when p is odd, giving residue1/q; when p is
even, q is odd and n=(p/2)^-1 modq gives residue2/q. This proves the
entire large-denominator branch. The checker's44 prescribed inverse controls
are arithmetic checks of this formula, not its universal justification.

The leftover reduced theta values have q<=12. Denominator1 has no value
strictly between0 and1, so starting at q=2 is exhaustive. The peer table
filters exactly0<alpha<beta<1 and removes alpha or beta=1/2, which have
the separate argument below. My own checker independently regenerates all
40 rows from all reduced p/q and all four line equations. It compares
every entry with BOTH the written proof table and the parent JSON receipt.
All40 agree exactly. There are34 success rows and6 failure rows; the
latter represent only the THREE phase pairs
(1/4,3/4),(1/5,3/5),(2/5,4/5), each lying on two lines.

For successful rows I verify an exact positive cosine-sign witness using
rational residues only, choose its sign, reconstruct c,u and the actual
target lift, and check the whole physical path. For failure rows the ENTIRE
period n=0,...,2q-1 contains no positive C_n. This is the complete finite
residual proof after the hand reduction; it is not extrapolation from a
sampled denominator cutoff.

If alpha=1/2, even n have sin(pi n alpha)=0 and odd n have
cos(pi n alpha)=0, so every C_n=0. The same argument applies to beta=1/2.
Under the inverse phase-depth map, these lines are a=b+1 and b=a+1;
the three isolated phase pairs give(a,b)=(1/2,1/2),(1/2,1),(1,1/2).
Thus the claimed failure classification is exact for all real depth pairs.
The strict edges alpha=0,beta=1,alpha=beta are excluded by the stated
positive/interior hypotheses rather than omitted cases.

## 4. Actual repairs and final centered theorem

The two midpoint lines have the independently accepted two-reflection cap
repair and its reflected/time-reversed partner. Its hypothesis h_+>b,
or the reversed lower-cap version, is exactly the interior-mark condition;
there is no additional cap-clearance assumption.

For each of the three isolated depth pairs use v=4/(a+b+3),
p=1+(a+1)v,p'=1+(b+1)v,eta=1-(3-p)/v. I independently derive
and verify every value in the second written table. They give
1<1+av,1+bv<2;2<p,p'<3;0<eta<1;p+p'+v=6.
The path S -> (p,1) -> (3,eta) -> (p',0) -> T has directions
(v,1),(v,-1),(-v,-1),(-v,1), up to positive scale.
The first/last legs cross strict portals at1+av and1+bv. The three
contacts lie strictly inside the actual upper ledge, right wall and lower
ledge of the middle band. The middle legs remain in its open rectangle
until their listed first walls. The final leg reaches actual T for the
first time; its y increases from0 to1+b. No exterior cap is reached,
so arbitrary h_->a,h_+>b suffice. Every reflection and length is legal.

Every depth pair now has either a successful vertical chart or one of these
verified repairs. Undoing the positive diagonal scaling proves the full
centered theorem with arbitrary positive real dimensions and independent
a,b. There is no uniform reflection bound in this argument.

## Reproducible checks and remaining full-thread scope

Run `python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/centered-check.py`.
It imports only my own frozen independent geometry implementation, never
executes peer code, and does no parameter-discovery sweep. Its exact proof
checks cover16 exponential coefficients,8 cosine terms,40 residual rows,
all written table entries and44 inverse-formula controls. It additionally
checks122 prescribed actual paths and296 wall contacts, including all34
successful residual rows, all3 core repairs, three off-line charts, scales,
reversals and two exact irrational Q(sqrt(2),sqrt(3)) paths. All PASS.
These path counts support the hand proof; they do not prove arbitrary-real
coverage on their own. The separately frozen midpoint repair acceptance
supplies the other two infinite exceptional lines.

All source hashes were checked before and after the run. The exact theorem,
parent checker and parent receipt are pinned in centered-check.json.
No claim is made here about independent horizontal s,t, the complete cap-sheet
cover, all interior pairs, other room families, historical novelty or a
universal polygon wall minimum. The full native review goal remains ACTIVE.
