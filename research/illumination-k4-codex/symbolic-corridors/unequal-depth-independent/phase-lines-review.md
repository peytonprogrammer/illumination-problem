# Independent acceptance: every noncommensurable depth pair

Codex01a1a00f, 6 November 2026.

Verdict: ACCEPT the exact pinned phase-lines.md without mathematical correction.
For every permitted pair of independent horizontal positions s,t and all
positive dimensions/interior depths, illumination follows if a/g or b/g is
irrational. This includes all resonance cases under that hypothesis. It does
not cover the outstanding commensurable, unequal-depth, noncentered class.

The finite residual proof is a complete exact affine arrangement, not rational
sampling. I independently checked it using polygon subdivision, a different
method from the parent's vertical-slab decomposition.

## 1. Scope and exact rank alternatives

The accepted actual-mirror L reduction handles any s>d or t>d. Positive
axis scalings reduce d=g=1. Reflection about y=1/2 and time reversal
may order0<t<=s<=1, provided the depths and outer heights exchange too.
They do NOT permit an independent ordering of a,b.

For alpha=a/(a+1+b), beta=(a+1)/(a+1+b), the inverse formulas are
a=alpha/(beta-alpha),b=(1-beta)/(beta-alpha). Thus both alpha,beta
are rational if and only if both normalized a,b are rational. Under the
current theorem at least one phase is irrational.

If1,alpha,beta have no nontrivial integer relation, the separately accepted
finite-Fourier foundation already yields a common-chart path for every s,t.
Otherwise the rational span of1,alpha,beta has dimension2. Its rational
relation space is one-dimensional, and its integral vectors are exactly the
multiples of one primitive integer triple(m,n,r), gcd(m,n,r)=1, satisfying
m alpha+n beta=r. This does not mean gcd(m,n)=1: discarding that distinction
would lose disconnected orbit components. The normalization m>0, or m=0<n,
is legitimate and is used in the finite list.

## 2. Entire orbit closure, including every component

I checked the parent's residue-class proof in detail. If n!=0 and alpha
were rational, beta=(r-m alpha)/n would be rational too, contradicting the
hypothesis. Hence alpha is irrational. For each M congruent to j modulo|n|,
put z=M alpha/n. Its increments as M advances by|n| are +/-alpha,
so z is dense modulo1 by the independently audited irrational-circle lemma.
The orbit in that class has closure
 (n z, j r/n-m z) modulo1.
These curves lie in K={m x+n y integral}.

Conversely, given(x,y) in K and Z=m x+n y integral, solve
Z congruent to j r-m k modulo n. Bezout's identity and gcd(m,r,n)=1
guarantee a solution; reduce j modulo|n|. Then z=(x+k)/n gives
n z congruent to x and j r/n-m z congruent to y. Thus all components
of K occur. Negative n causes no problem: the congruence and signed dense
increment have exactly the same argument.

For n=0, m>0 and alpha=r/m, with gcd(m,r)=1. The first coordinates of
M(alpha,beta) run through ALL m values j/m, and on each residue class
modulo m the second coordinate is dense because beta is irrational.
This is again exactly K. No connected-kernel hypothesis is introduced.

I also independently derived a uniform check of the component bookkeeping.
Let g=gcd(m,n), m0=m/g,n0=n/g and choose p,q with m0p+n0q=1.
The integer matrix U with rows(m0,n0),(-q,p) has determinant1. It maps
the orbit increment to(r/g,theta), where theta=-q alpha+p beta is
irrational; otherwise the integer inverse matrix would make both phases
rational. Primitive gcd(m,n,r)=1 implies gcd(g,r)=1. Hence the first
coordinate cycles through all g components, while each fixed residue class
has dense second coordinate. The own checker verifies these Bezout and
component-cycle identities for all30 residual triples.

These elementary arguments justify the FULL closure claim, rather than
invoking an unproved torus-density theorem. An open box intersecting that
closure has a nonempty relatively open intersection and is visited by a
finite integer orbit index. Signed indices are permitted in all folds.

## 3. Translated phase level and open-box image

For a chosen u,epsilon, the developed portal vector is
E=s(1,1)+(u+epsilon*t-s)(alpha,beta)+4M(alpha,beta).
Applying the primitive relation gives exactly
m E1+n E2 congruent to C modulo4,
C=(m+n-r)s+r epsilon*t+r u.
The full-closure result proves equality with this entire level set after
translation and scaling by4. It is not merely a necessary congruence.

For each accepted four-chart box I1×I2, the image under m x+n y is the
OPEN interval(lo,hi) obtained by signed interval extrema. Every intermediate
value is attained inside the open rectangle, even if one coefficient is0.
Its width is |m|+|n|. The box therefore intersects the phase closure exactly
when lo<C+4k<hi for some integer k. Such a strict intersection supplies
actual portal values AND matching velocity by the separately accepted
four-chart geometry. Contacts are smooth actual walls, target is actual T,
y increases strictly and the reflection count is finite.

When |m|+|n|>=5, this open interval has length>4 already in the common
box(1,2)^2. Every residue modulo4 is attained. This proves the entire
large-normal branch for every horizontal endpoint pair, without a bounce
cutoff, a coordinate grid or a parameter sampling premise.

## 4. All primitive short relations and the finite period-index bound

On the strict phase triangle0<alpha<beta<1, the linear form m alpha+n beta
has open range with endpoints min(0,n,m+n),max(0,n,m+n). It is a
nonconstant linear functional because(m,n)!=(0,0); every strictly intermediate
value is attained in the open triangle. Thus these strict r bounds remove
no possible primitive relation. Enumerating the sign-normalized normals
with0<|m|+|n|<=4 and gcd(m,n,r)=1 gives precisely30 triples.

Also |r|<|m|+|n|<=4, so |r|<=3. On the closed endpoint triangle,
|C|<=|m+n-r|+|r|+2|r|<=|m+n|+4|r|<=16.
Inside any of the four phase boxes, |m x+n y|<16. A successful equality
m x+n y=C+4k therefore implies |4k|<32, hence |k|<8. My own checker
uses ONLY k=-7,...,7, independently confirming the parent's wider-9...9
window contains every possible success. These are integer guard translates,
not discovered reflection words or an unproved finite ray cutoff.

Endpoint reversal maps the relation to(-n,-m,r-m-n), followed if necessary
by a simultaneous sign change. This preserves the L1 norm and primitiveness.
The own checker confirms the full30-triple list is closed under that map,
so ordering s,t while exchanging depths loses no relation case.

## 5. Independent continuous affine-cover certificate

For each triple and each of the four boxes, both target signs and all k
in the proven range, I independently construct the two exact affine guards
C+4k-lo>0 and hi-C-4k>0. An affine guard's maximum on the closed triangle
is its largest value at(0,0),(1,0),(1,1). A clause discarded because one
maximum is nonpositive cannot hold anywhere in the triangle. Positive
constant guards introduce no line; nonpositive constants correctly remove
their impossible clause. No approximation or numerical tolerance is used.

The parent checks vertical slabs. My implementation instead starts with
the CLOSED triangle and repeatedly cuts every convex polygon by every
nonconstant guard-zero line, using exact rational half-plane intersections.
It retains the closures of all positive-area faces. After all cuts:

- The vertex-average of each convex face lies in its open two-dimensional
  sign cell, because it is a strict positive combination of its vertices.
- Every open edge is checked at its midpoint.
- Every vertex is checked separately.

Each affine guard has constant sign, including zero when appropriate, on
every such relatively open face, edge and vertex. All boundary crossings
have become vertices or split edges in the subdivision; finite line
arrangements have no other cell types. The domain's s=1 and t=s boundaries
are polygon edges, and their intersection is explicitly a vertex. Only
s=0 or t=0 points are excluded by the true domain0<t<=s<=1.
Discarding zero-area polygon pieces does not discard lower-dimensional
cells: they remain boundaries of adjacent positive-area pieces, or of the
original domain, whose edges and vertices are checked.

This proves that checking the resulting representatives is a complete
continuous-domain proof, not sampling that domain. The two methods agree
on every retained clause count and every uncovered endpoint set. They
also agree with EVERY entry of the written proof table.

Exact independent results:30primitive relations,94open polygon faces,
374admissible sign-cell representatives. There are28 completely covered
relation rows. The only uncovered cells are the single point(s,t)=(1,1)
in each of(0,2,1) and(2,0,1). Every equality edge and isolated intersection
has been included, so no limiting or generic-position argument is used.

## 6. Close the exceptional cells and state the remaining full goal

The two residual relations are beta=1/2 and alpha=1/2. At their sole
uncovered horizontal pair s=t=1 they are the already independently accepted
centered midpoint lines b=a+1 and a=b+1. The actual two-reflection cap
repair works for every positive original exterior clearance. Thus these
cells are illuminated too. Every noncommensurable depth pair and every
permitted independent horizontal pair is covered.

Run `python3 .context/illumination-k4-codex/symbolic-corridors/unequal-depth-independent/phase-lines-check.py`.
It imports or executes no peer program, performs no room/orbit/ray discovery,
and writes only its own receipt. The30 residual cases are the complete
finite mathematical reduction just proved. All finite guards, written table
entries, reversal transforms and component-cycle identities pass exactly.
Source hashes match the frozen request and are checked before and after.

The broader native goal remains OPEN: commensurable normalized a/g,b/g,
unequal depths, both horizontal positions in the left portions, not both
centered. Rational phase orbits are finite and do NOT have the closure used
here. No claim about their coverage, a complete cap-sheet theorem, arbitrary
interior pairs, another room family or universal wall minimality
follows from this acceptance. The real-parameter proof is independently
AI-reviewed and computer-assisted in its finite residual cover; it is not a
formal proof assistant certificate or external expert refereeing.
