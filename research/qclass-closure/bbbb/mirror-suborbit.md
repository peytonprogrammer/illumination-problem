# A full-stabilizer obstruction using just one endpoint

**Decision: retain B′ as a one-mark test.** For a regular interior room point S let s be either lift on Q and let ι be the physical mirror. With G the orientation-preserving affine group of Q preserving its corners, define

    e(S) = |G_s · ιs|.

This is the number of different images of the *other lift of S* while s is held fixed. The definition is independent of which lift is called s: conjugation by ι normalizes G and interchanges the two actions. On a normalized lattice room the relative period lattice with the corner lifts marked is Z²: the wall vectors generate it by the separate axis gcds, and all developed corner displacements are integral. Affine maps preserve this lattice and send corners to corners, hence permute the lattice points. Thus these orbit sizes are finite for lattice marks.

**Theorem for review.** If S has a distinct dark physical partner T, then both endpoints satisfy

    2e(S) ≤ B(r)(B(r)−1),       2e(T) ≤ B(r)(B(r)−1),

where B(r) is the uniform bound on ordinary hidden regular Q targets from a specified Q source. Consequently a mark with e(S) above this threshold illuminates **every other distinct interior physical point**. No comparison between the absolute orbit sizes of S and T is needed. This is a restriction on one mark of a dark pair, independent of who the other mark is. It uses the ordinary shadow theorem reviewed in d86, without any transfer of midpoint candidates to ordinary shadows. [Shadow theorem](shadow-budget.md) · [D86 review](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d86-review-shadow/review.md)

## Proof and quantitative full-group mechanism

Use distinct left and right copies of the point set of Q. Start with the four edges from {s,ιs} on the left to {t,ιt} on the right and take all their simultaneous G-images. Each vertex on either side has degree at most B(r) if the physical pair is dark: every edge joins distinct points which cannot illuminate each other on Q, and this property is symmetric and affine invariant. Keeping the sides separate also works if the two G-orbits overlap.

For every s′ in G_s · ιs, choose g fixing s with gιs=s′. The two vertices s and s′ are distinct and share **both** gt and gιt as neighbors. Count length-two walks from s ending at a different left vertex. There are at most B(r)(B(r)−1) walks, and each of the e(S) endpoints contributes at least two. Exchange the sides for the second inequality.

The same count works **before assuming darkness**. Let M be the largest of the source-fixing orbits on the opposite mark among the four lift pairs in either orientation. Each of the four seed-edge orbits contributes at most M neighbors at any vertex, by conjugacy of point stabilizers. Hence, for every pair of distinct interior lattice marks,

    2 max(e(S),e(T)) ≤ 4M(4M−1).

In particular, if the mirror suborbit at one endpoint grows, at least one of the full stabilizer orbits relevant to the *actual marked pair* grows at least on the order of its square root. This implication does not require a dark pair, an effective value for B(r), or transitivity on lattice points. It concerns the genuine orientation-preserving group; the mirror is used to name endpoints and conjugate maps, not counted as an orientation-preserving generator.

## A nonaxial certificate for the one-mark hypothesis

Let F be any corner-preserving affine map in G and F*=ιFι. At a given lattice lift s compute u=period_F(s) and v=period_F*(s). Since F and F* act by mirror conjugacy, period_F(ιs)=v and period_F*(ιs)=u. Powers fixing s yield

    e(S) ≥ max(u,v)/gcd(u,v).

For a certified parabolic F, this compares the same marked point in a direction and its **mirror direction**, including the correct cylinder height and winding multiplier in each. For a twist fixing its rims the period at height h in a circumference-C cylinder is the denominator of λh/C in lowest terms; a point on a pointwise fixed rim has period one. No independent choice of an unrelated twist on the second cylinder is justified: it must be F*. If the reduced ratio grows in any sequence, this proves full-group orbit growth for every putative physical partner along that sequence, and eventually ordinary illumination for all partners at fixed r. An axial twist satisfying F*=F⁻¹ always gives ratio one. Even equality of this ratio in every checked direction gives no upper bound on the full-group orbit. [Parabolic period formula](stabilizer-orbits.md)

There is also a purely permutation-theoretic sufficient condition. Enlarge G by ι to the extended group E, of index at most two over G. If E acts doubly transitively on a finite orbit of m points containing s, then ιs is in that orbit and E_s · ιs has m−1 points. Since [E_s:G_s]≤2 and G_s is normal in E_s, this orbit splits into at most two equal-size G_s-orbits. Thus e(S)≥(m−1)/2. Double transitivity here concerns affine maps on *regular point lifts*, not the reviewed sheet monodromy of the pillowcase cover. The argument gives no implication from high marked sheet valency to double transitivity.

## What this rules out and what it leaves

A hypothetical same-parity dark pair in the large-area range must now have bounded mirror suborbits at **both** marks under the full group, in addition to high sheet valency and the d82 unrealized midpoint count. In particular the reduced period ratios above must have bounded numerator and denominator at each mark for every parabolic and its mirror. To prove a room-size cutoff by this route it would suffice to show that outside an explicit area range one endpoint of every nondirect pair has a large mirror suborbit, or else prove illumination for pairs in the remaining bounded class. B(r) itself is presently ineffective, so merely proving growth with no effective ordinary shadow estimate yields at most an ineffective cutoff unless there is also a direct visibility argument.

The mirror suborbit can be genuinely bounded under the **full** group. If ιs=k s for some projective-derivative-kernel element k, normality gives G_s · ιs ⊆ K s, and s itself cannot occur, giving e(S)≤|K|−1≤3. For interior S this happens exactly when S lies on a physical horizontal or vertical symmetry axis: k must exchange halves and its physical reflection must fix S. In particular in the previously studied cross the two marks (6,0) and (0,6) lie on different symmetry axes, so both pass the bounded-mirror-orbit obstruction at every size despite being lit. This is a test of the criterion, not a conclusion about the two cross-mark full stabilizers. [Kernel classification](stabilizer-orbits.md)

**Verdict.** The new mechanism converts an asymmetry of the nonaxial periods of a *single* mark into growing full stabilizer orbits and eventual illumination, without requiring information about the partner's cylinder. I have not proved that such asymmetry occurs in every large room, or that the symmetry-axis points exhaust the bounded mirror-suborbit cases. A bounded suborbit gives no dark pair. The general same-parity lighting and off-class reachability questions remain open. No direction, room, word, or ray search was run.
