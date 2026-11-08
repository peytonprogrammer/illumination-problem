# UP01 independent review

Decision: ACCEPT the restricted positive upper-source theorem, with the harmless inequality correction below. This does not prove all upper sources, all W10 rooms, or the native r<=8 target.

## Exact statement and inheritance

The room is the strictly simple ordered spiral with boundary
(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b),
where a=Pe,A=Ne,w=(N-1)e,l=(N-L)e, e is a positive integer, P odd>=5, N odd>N? precisely N>P+L, L a power of two **at least 2**, 0<b<c<h<H are integers, h even, c odd, and gcd(P(H-h),N)=1. L>=2 is inherited from l<w, not an extra restriction on a strictly simple original ordered spiral. S=(s,u), T=(t,v) are distinct actual even-even interior points with 0<s<a, u=h+2N*ell<H, ell>=1 integral, l<t<A and 0<v<c. The native parity hypotheses, including even v, are essential for d2=c-v odd and the final congruence.

All 72 author pins were checked before and after the independent checks. Previously accepted dependencies are reused at their recorded scopes; the new five-band transfer and existence steps were checked directly. The author checker was read but not executed. No discovery search was used.

## Claim decisions

1. **ACCEPT: actual five-band transfer.** The full initial cap has width A, with even-center left entry. Strict |zpre|<a makes its signed triangular fold match the actual width-a arm below h. The loop returns through that same mouth. The odd-A roof exit agrees with x=A-F_e on the true right arm, and the e-to-Le expansion matches signed derivatives at c. Each zero residual is a smooth outer vertical wall, not a corner. No width-a wall exists or is used above h. N>P+L ensures the two h mouths are disjoint and the displayed polygon has the required ordered inequalities.

2. **CORRECT a local displayed bound, ACCEPT four-seed availability.** The four predecessors satisfy U-4delta <= Y(q*-i) < U; the first inequality can be equality when Y(q*)=U and i=4. It need not be strictly greater as printed in section 3. The required window still holds strictly because 4delta<8e<2Pe. Thus this correction has no effect on the proof or final theorem. Clearing denominators gives the left bad event period PD/gcd(dpre+dleft,PD)>P>=5, so it removes at most one of four consecutive q. The cap event period D/gcd(dpre+dleft+C,D)>=2 removes at most two. Their union misses at least one of the four. This proves simultaneous existence in the same literal first-entry window.

3. **ACCEPT: preservation of both earlier passages.** For slope increment e*a0*M, dpre*e*a0*M=2A*ell*a0*M, preserving zpre literally, and dleft*e*a0*M is a multiple of 2a, preserving z0 literally. This uses the actual source-depth hypothesis dpre=2N*ell, not merely integrality. All affected indices are actual fold indices.

4. **ACCEPT: strict cap selection and right guard.** Since a0|P and gcd(P*epsilon,N)=1, epsilon*a0 is invertible modulo N. The cap orbit has spacing 2e, exactly the length of the open right mouth. Excluding the endpoint class ensures exactly one interior representative. Increment M by N preserves zpre,z0,z1 and adds odd e*g1*a0*N to the right phase, so at most one of the two choices is the true corner class. This is an arithmetic orbit argument with proved physical guards, not recurrence asserted as target attainment.

5. **ACCEPT: complete target identity.** Direct telescoping gives E=z+2e[q+D*a0*M/2-N*npre-P*nleft-N*m-k]. Both earlier indices must remain. The final slope increment 2e*a0*N*p preserves all four literal residuals and increments E by 2e*a0*N*d2*p. Its coefficient in target residue units is odd, hence invertible modulo L. The stated four index increments agree exactly with independent chart calculations. Folding E modulo 2Le reaches actual t, with the original source sheet and one common slope throughout.

6. **ACCEPT: final upper-S corner repair.** If the formal floor phase is ja, the left return residual is -zpre. After dpre of real full-cap ascent, the phase equals -s+2A*npre. Thus it reaches exact original (s,u), with signed velocity (-tau,+1), at elapsed 2(u-b). Because dpre<epsilon it is before the roof. Deleting the entire prefix leaves an ordinary original-room ray; no singularity is traversed. This dichotomy is applied at the final slope. Our conditional fixture explicitly crosses the artificial line x=a above h without reflection, which detects the old fake-wall error.

7. **ACCEPT: true-corner, finite-word and first-target guards; reject any broader reading.** A roof corner would force the descending h coordinate to equal the ascending h coordinate by triangular-fold symmetry. That contradicts the disjoint strict left/right mouths. Vertical hits inside each open band are ordinary. The only potentially singular horizontal contact is the floor, handled by claim 6. Before the final bottom descent, heights or left-arm x coordinates exclude T. The prescribed earliest-wall replay independently verifies first actual target arrival, original boundary intersections, ordinary specular reflection, absence of earlier corner hits, and every open segment inside the room. No bounded reflection assumption is used in the quantified proof.

## Independent prescribed evidence

`three-reflex-upper-floor-check.py` uses a separately derived direct modular inverse selector and the reviewer's existing exact earliest-original-wall verifier. It does not call the author checker.

- Author A reproduces slope 20225/38 and indices [266,160,556,133].
- Author B reproduces slope 5751/41 and indices [70,71,146,35].
- Two further checks select the first good predecessor independently on these same inputs, rather than prescribing the author's q.
- A separate conditional transfer fixture has e32,P3,L4,N9,b8,c24,h32,H40,S=(4,34),T=(208,16),tau22. Its residuals are (48,-48,16,0), E=176. The discarded formal floor is a true corner; the retained suffix lasts 30, starts at exact S with velocity (-22,+1), and meets the ordinary roof at (128,40). It is evidence for the general physical transfer lemma, **not** an arithmetic member of UP01, since P=3 and dpre=2.

All five checks pass, totaling 6456 actual reflections and 64610 exact wall-leg guards. These finite checks support the independently audited quantified proof; they do not establish its quantifiers by sampling.

## Next optical extension and open gap

The author's narrower-arm refinement UP02 is the next disjoint packet: the full-cap time inequality may replace P>=5 with a three/four predecessor argument. It does not remove the source-depth congruence. For arbitrary upper depth dpre, preserving both earlier literal residuals with slope step e*alpha requires alpha*dpre divisible by 2N and alpha*(h-b) divisible by P. Any cap rotation derived from such a step must retain its actual gcd with N; one cannot import UP01's invertibility automatically. This is a precise remaining obstruction to this selector, not darkness. Full ordered-spiral availability and all remaining r3 and r4..8 obligations stay open.
