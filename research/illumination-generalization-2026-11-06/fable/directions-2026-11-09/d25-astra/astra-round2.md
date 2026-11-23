**[Proved] The commutator rank controls directional losses, but does not control the missing midpoint pairs.** A bound on those missing pairs depending only on \(r\) is false already for rectangles. I have no surviving inequality that forces coverage at \(r\le8\).

**[Cited]** Your correction about maximal-cylinder twists is right. My earlier objection applied to the particular twists fixing unit-row boundaries, not all cylinder twists.

**1. Rectangle and L-room tests.**

**[Proved]** Primitive \(R_X\) need not equal the full central-symmetry relation, even in a rectangle. Take
\[
P=[0,6]^2,\quad X=(1,1),\quad S=(2,2),\quad T=(4,4).
\]
The lifts \(-S,T\) have midpoint \(X\). However, folding \(X-d\) to \(S\) and \(X+d\) to \(T\) requires, in each coordinate,
\[
d_i\equiv3\pmod {12}.
\]
Thus \(d\) cannot be primitive, and \((S,T)\notin R_X\).

**[Proved]** This produces unboundedly many missing central-compatible pairs at rank zero. In \([0,6m]^2\), retain \(X=(1,1)\) and take
\[
S=(6i+2,6j+2),\qquad T=S+(2,2),\quad 0\le i,j<m.
\]
The required displacement satisfies \(d_\ell\equiv S_\ell+1\pmod{12m}\), so both coordinates are divisible by three. Hence no bound on these holes by a function of \(r\) alone can hold.

**[Proved]** Even the union of all midpoint relations can miss an interior pair with \(r=1\) and large \(k\). Let
\[
P=([0,8]\times[0,4])\cup([0,4]\times[0,8]),
\quad S=(2,2),\quad T=(6,2).
\]
Every wall coordinate is divisible by four. Every reflected image of \(T\) is therefore congruent to \(S\pmod4\). A two-step displacement \(2d\) would force both coordinates of \(d\) even. Thus every \(R_X\) misses this pair. Nevertheless, the horizontal four-step chain joins them. Counting lattice points gives \(65\) total, \(21\) of class A, hence \(k=44\).

**[Proved]** Consequently, any useful rank lemma must include arbitrarily long chains and distinguish arithmetic obstructions from corner losses.

**2. A uniform counting lemma that does survive.**

**[Proved]** Write \(N=\operatorname{area}(P)\). For parity \(\alpha\), let
\[
b_\alpha=c_\alpha+3r_\alpha,\qquad a_\alpha=N-b_\alpha,
\]
where \(c_\alpha,r_\alpha\) count convex and reflex vertices. Here \(a_\alpha\) counts nonvertex lifts: weight four for an interior point, two for a flat boundary point.

**[Proved]** These formulas follow from the degree-\(N\) cover
\(M\to\mathbb R^2/(2\mathbb Z)^2\): a reflex vertex contributes three directional prongs; a convex vertex contributes one. Therefore
\[
b:=\sum_\alpha b_\alpha=4r+4
=2\operatorname{rank}([H,V]-I)+4.
\]

**[Proved]** Fix primitive \(d\) of nonzero parity \(\delta\). On the \(a_0\) regular A-lifts, draw an edge for continuation by \(2d\), provided the intermediate \(\delta\)-lift and endpoint are nonvertices. This graph has indegree and outdegree at most one. If \(e_d\) is its edge count and \(p_d\) its number of path components, including isolated vertices, then
\[
e_d=a_0-p_d,\qquad
p_d\le b_0+b_\delta\le4r+4.
\]

**[Proved: proof]** An outgoing edge can fail only by hitting a corner at the intermediate step or endpoint. Reverse transport injects these failures into the \(b_\delta\) and \(b_0\) incoming corner prongs. A finite partial-permutation graph consists of paths and cycles, giving the identity.

**[Proved]** Choose one primitive direction for each nonzero parity. With
\(\widetilde k=\sum_{\delta\ne0}a_\delta\), where \(2k\le\widetilde k\le4k\),
\[
\sum_{\delta\ne0}e_{d_\delta}
\ge3a_0-b-2b_0
=\widetilde k-6b_0.
\]
This is a genuine uniform incidence bound. In the L example, \(N=48\), \(b_0=8\), \(b_\delta=0\), so each direction contributes at least \(32\) edges—despite the specified pair missing every \(R_X\).

**3. Where the averaging proof breaks.**

**[Proved]** If a directional graph has component sizes \(n_i\) and \(z_d\) cycle components, its chain relation contains
\[
\sum_i n_i^2\ge
\frac{a_0^2}{4r+4+z_d}
\]
ordered lift pairs, including diagonal pairs.

**[Proved]** The uncontrolled term is \(z_d\). Rectangles of increasing height have arbitrarily many horizontal regular cycles while \(r=0\). Moreover, incidences from different directions can repeat the same pairs. Neither bound controls these overlaps.

**[Cited/Proved]** The known \(r=9,\ k\le6\) dark example is compatible with these inequalities: they bound aggregate transport losses and allow individual missing pairs.

**[Guessed] Funding decision: only a capped attempt at a cross-direction component-intersection inequality; 3% probability of closing the orthogonal case.**