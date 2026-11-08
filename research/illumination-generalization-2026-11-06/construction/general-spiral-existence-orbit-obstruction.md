# GSE01 premise audit: all nearest-cell preserving orbits can miss the actual target class

## Exact negative statement and its limits

The following common universal premise is FALSE:

> After choosing among the two real source charts, two real target-height charts, both initial horizontal signs and both actual target images, an AP01 nearest half-open source/cap seed at cap index zero always has a source/cap-preserving AP07 orbit that reaches a target-compatible strict right exit.

The proof below excludes every such seed and its ENTIRE integer orbit in an unbounded qualifying class. It is stronger than the failure of the sufficient test g|K: the source/cap seeds have ordinary strict right passages, but all their preserving orbits retain the WRONG target-index residue. It does NOT exclude other seed cells, other initial cap-index classes, repeated genuine horizontal contacts or all actual rays. No darkness is asserted.

## Qualifying room and original pair

For ANY odd integer K>=21, set e=1,P=8,N=3K and let L be the least power of two strictly greater than K. Then K<L<2K and N=3K>8+L. Use b=1,c=3,h=4,H=5, so a=8,l=3K-L,w=2K,A=3K are strictly ordered. The original ten-wall spiral is a finite strictly simple orthogonal lattice disk with three reflex corners.

Take actual S=(2,2) and T=(3K-3,2). Both are distinct interior even-even points: K odd makes the target abscissa even; 0<2<8,1<2<4 and 0<3<L,0<2<3. Every endpoint is in the actual room, not a projected sheet.

The source upward and real-floor times are X=2 and X=4. The cap time is C=2 and g1=h-c=1. The direct and actual-bottom-floor target durations are d=1 and d=5, with F=g1+d=2 or6. Both source signs sigma and actual target images epsilon are +/-1. There are16 declared combinations, with original horizontal s=2,z=A-t=3.

## Exact nearest seeds, without any sampling

For each combination put D=X+C+F and define

 M0=lcm(P/gcd(P,X),N/gcd(N,C)),
 g=gcd(M0*d,L).

Since N=3K is odd and L>=32,

 X=2: M0=12K,g=4;
 X=4: M0=6K,g=2.

Thus g<=P<K and the strict AP01 source/cap box exists. At initial cap index m=0 choose the SPECIFIED half-open indices

 lambda=-sigma*s/(2P)-XN/(2PC),
 mu=epsilon*z/(2g)-FN/(2gC),
 i=-floor(lambda+1/2), j=-floor(mu+1/2).

Let alpha=lambda+i and beta=mu+j; both lie in[-1/2,1/2). The literal root is

 q=Pi+gj,
 tau=(N+epsilon*z-sigma*s+2q)/D.

Expanding the two rounding errors EXACTLY gives

 tau=N/C+2(P*alpha+g*beta)/D.

Therefore |tau-N/2|<=(P+g)/D<=2, for ALL16 choices. The last bound follows from P8,g<=4,D>=6. Meanwhile the opposite-sign weighted residual basis gives the STRICT cap bound

 |z1|< [P*F+g*(X+C)]/D<=P=8.

These bounds are uniform over K and the actual source/target image signs; no finite list of K values is used.

Since g1=1, the right input is r=z1+tau. Hence

 |r-3K/2|<10.

For K>20 this implies the stronger interval

 K<r<2K.

Every seed therefore has actual centered right index k=1 and strict physical residual z2=r-2K in(-K,0). The source/cap guards and positive tau are real. The target congruence is the missing part.

## Every preserving orbit misses the correct target-index window

A source/cap-preserving step is Delta_tau=2M0*ell. Its actual right input changes by2M0*ell. A target-compatible index requires k in gZ because J=gj-Kk must be g-divisible and gcd(K,g)=1. The strict right inputs with such an index form

 union_{q integer}(2Kgq-K,2Kgq+K).

For X2,2M0=24K=3*(2Kg), becauseg4. For X4,2M0=12K=3*(2Kg),becauseg2. Thus the whole integer orbit is stationary modulo the target-aligned right period2Kg. Its initial r in(K,2K) misses that open window, and every integer null shift misses it as well. Equivalently k stays1 modulo g and J stays-K modulo g,neverzero.

This holds for both X, both d, both sigma and both epsilon. Allowing negative null indices only enlarges the attempted constructor; it still fails. Any actual positivity/corner guards can only remove candidates, not repair the target residue. The true target period is retained throughout the argument.

A formal source/bottom floor corner, if present in a chart, would require its own regular-prefix/suffix treatment; it does not change this negative claim about the specified nearest seed and preserving orbit. A repaired physical ray arising from another source programme is outside the excluded constructor. No arbitrary ray class is declared dark.

## Exact universal gap exposed

The AP07 coprimality identity cannot simply be dropped. Nor is considering both real floors and both actual endpoint images enough if the source/cap cell and initial cap index remain fixed by this nearest rule. A general proof must be allowed to change the source/cap lattice point inside its strict windows, change the initial cap-index class, or use repeated genuine horizontal contacts. The next existence lemma must control that choice jointly with the actual target residue.

The metrics above lie precisely in the accepted four-criterion high-source-valuation obstruction regime (nu2P3,oddK,N,c,b,evenh). This result strengthens its mechanism diagnosis: each of the16 proposed orbit constructors has a strict right passage but cannot reach the actual target class. It is still not a general optical obstruction or qualifying dark counterexample.

This is a symbolic hand proof. No numerical controls, search, census, new engine, workers, frozen edits, git changes or clock resets were used. Independent review is requested. The full ordered-spiral and r3/r<=8 objectives remain open.
