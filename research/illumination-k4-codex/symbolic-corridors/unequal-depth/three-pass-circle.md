# Three traversals of the middle band repair the limiting circle windows

Codex01a18403. Candidate optical template and exact feasibility result. Independent review required. This is NOT a finite-rational-orbit illumination theorem.

## The optical template

Choose effective endpoint depths A,B on any of the four accepted cap sheets. Develop a line over virtual height -A<=z<=3+B:

    L=u+epsilon*t+4M, v=(L-s)/(A+B+3), X(z)=s+v(z+A),

with u=0or2, epsilon=+/-1, integer M. Let E=X(0). Use the lower and upper triangular horizontal folds from the accepted four-chart construction, and middle horizontal fold 1+F2(X-c), c=1or3.

In the middle interval0<=z<=3, fold the VERTICAL coordinate as

    Y=z for0<=z<=1,
    Y=2-z for1<=z<=2,
    Y=z-2 for2<=z<=3.

The entry is at the actual lower portal y0, the exit at the actual upper portal y1. Require the usual compatible strict portal intervals for E and E+3v: (u,c)=(0,1),(0,3),(2,1),(2,3) with boxes respectively (1,2)x(1,2), (2,3)x(2,3), (1,2)x(0,1), (2,3)x(3,4), all modulo4.

Additionally require the middle horizontal fold to lie STRICTLY in(2,3) at z1andz2. These are actual ledge reflections at the top and bottom middle walls. For c1 this means E+jv mod4 in(2,3)union(3,4); for c3 it means in(0,1)union(1,2), j1,2. The split excludes x3at a simultaneous right-wall corner. The open interval excludes the portal endpoint x2. Between these two heights, ordinary horizontal-fold kinks are smooth actual vertical-side reflections; none coincides with the two horizontal reflections.

Below0leave Y=z. Above3translate Y=z-2, so the effective target is at actual auxiliary height1+B. This gives an auxiliary outer-simple path of precisely the kind covered by accepted outer-leg-transfer.md. Its middle contacts are actual smooth walls and its outer developments are straight. That lemma transfers selected endpoint caps and removes bad cap-corner loops while preserving actual S,T. Hence every strict three-pass phase hit supplies a legal actual connection.

For example A=B1,s1/3,t2/3,u2,epsilon-1,M1,c1 gives v1,E4/3. Its two ledge residues are7/3and10/3, and its exit residue is1/3. It is the already accepted three-middle-reflection example; the actual unequal-depth five-bounce cap-transfer fixture is one physical instance of this template.

## Finite phase polygons

Take E in its entry interval and v mod4 in[0,4]. The two ledge guards and exit guard cut out finitely many open convex polygons in(E,v). The program enumerates every possible residue translate (0..3) at each intermediate level; their raw values are between0and15. It rejects zero-area closures. The strict conditions cannot hold solely on v0or4, since then ledge residues equal the disjoint entry residues. Exactly8nonempty phase polygons result, two for each compatible u,c row.

A nonzero linear form mE+nv has an OPEN interval image (lo,hi) on each open polygon, where lo,hi are the extrema on its closure. These extrema are exact rational numbers from the polygon vertices. A required relation level C modulo4 meets that polygon exactly when lo<C+4k<hi for some integer k. This tests strict line intersection, not a sampled E,v point.

## Circle relation for an affine depth family

Suppose effective depths vary as A=a1*lambda+a0,B=b1*lambda+b0. Put h1=a1+b1,h0=a0+b0+3, alpha=A/(A+B+3), delta=1/(A+B+3). The rational triple

    (m,n,r)=(h1,a1*h0-h1*a0,a1)

satisfies m*alpha+n*delta=r identically. Clear denominators and divide the common integer gcd to make it primitive. Cases where A,B are both constant need a separate finite-phase calculation; none of the16tested residual families uses that case.

At target shift/sign u,epsilon the finite/dense phase orbit has relation

    mE+nv = (m-r)*s+r*epsilon*t+r*u modulo4.

For irrational family parameter this is the full one-relation circle closure, provided no additional independent relation fixes the parameter. For rational parameters the orbit is FINITE: polygon-circle intersection alone does NOT guarantee a hit. No such density inference is made here.

## What the exact test establishes

The critical-line support rectangle classification records90one-parameter affine families. Twenty-four have a common limiting circle-blind endpoint corner for their four one-pass sheets; removing families with an identically equal effective-depth sheet leaves16. Those counts and the rectangle classification are separate pending proof dependencies.

For each of those16families and EACH recorded common blind endpoint corner, three-pass-circle.py derives the four three-pass relation triples from the affine depths and tests every phase-polygon normal interval. ALL16families have a strict hit on at least one cap sheet at every such endpoint limit. The JSON records an exact normal-level witness and polygon for each; there is no room, angle or word discovery search.

This removes the limiting feasibility obstruction for this particular template. It does not yet give a uniform sampling margin on the ENTIRE closed endpoint square, nor bound all rational denominators, nor complete optical closure of the families. The next proof question is to combine the existing one-pass circle guards with these three-pass guards into a quantitative closed-square affine cover. If that cover has positive uniform margin, the accepted-style finite circle spacing argument would bound the remaining rational denominators. A rigorous certificate is required before making that inference.

For rational effective depths, their one-pass and three-pass primitive joint denominators obey q3=q1+2D<3q1, where D is the least common denominator of A,B: write A=p/D,B=r/D with gcd(p,r,D)=1. Then qg=p+r+gD since gcd(p,D,p+r+gD)=gcd(p,r,D)=1. Thus q3>q1, which can be useful when converting a three-pass cutoff to a one-pass finite parameter list. This arithmetic observation does not replace the missing uniform cover.
