**PROVED — conditional result.** Amalgamation holds under the extra hypothesis **Galois canonical class covers**: every map
\[
\phi_x:DP\longrightarrow N_x=DP/B_x,\qquad x=b,c,d,
\]
is Galois, allowing the identity map. This holds for every \(r\), not only \(r\le8\).

**PROVED — additional finite reduction.** If the room’s corners occupy at least three parity classes, any one-class separating quotient forces
\[
\boxed{\operatorname{area}(P)\le5r.}
\]
This includes normalized presentations. Thus a normalized counterexample to amalgamation at \(r\le8\) has at most 40 cells.

**1. PROVED — the conditional theorem.**

Let \(\iota\) be the seam reflection of \(DP\), and \(C=\operatorname{Fix}(\iota)\). All cone points lie on \(C\).

Every deck transformation \(j\) of \(DP\to PC\) preserves the metric and permutes the cone points. Uniformize \(DP\) as a Riemann sphere. Both \(C\) and \(j(C)\) are generalized circles containing all cone points, of which there are at least four. Distinct generalized circles intersect in at most two points, so \(j(C)=C\). Hence
\[
j\iota j^{-1}=\iota.
\]
Therefore every deck transformation descends to a Euclidean symmetry of \(P\).

Because it lies over the identity of
\[
PC=\mathbb R^2/\langle2\mathbb Z^2,-I\rangle,
\]
the descended symmetry has form
\[
z\mapsto\pm z+2v
\quad\text{or}\quad
z\mapsto\pm\bar z+2v,\qquad v\in\mathbb Z[i].
\]
Boundedness excludes translations and glide reflections. The remaining possibilities are a half-turn about an integer point, horizontal reflection in an integer line, and vertical reflection in an integer line. Distinct parallel axes or distinct half-turn centres would generate a translation. Consequently
\[
\boxed{\operatorname{Deck}(DP/PC)\le V_4.}
\]

**PROVED — different canonical double covers cannot occur for two different classes when there are two interior lattice marks.** This supplies a detailed proof of the exclusion stated in d10, Proposition R6.

Suppose two distinct classes \(x,y\) have different canonical double covers. Their involutions generate \(V_4\). Thus \(P\) has horizontal and vertical symmetry axes meeting at an integer point \(O\), together with the half-turn about \(O\).

The half-turn acting on the closed disc has a fixed point, necessarily \(O\). Strict simplicity prevents \(O\) from lying on an invariant boundary sector, so \(O\) is interior. The four unit cells around \(O\) are present. Write \(o=O\bmod2\).

Every transparent class-\(x\) point must be fixed by the corresponding deck involution: its local degree is two because the quotient has no regular point over \(x\). The same holds for \(y\).

The half-turn fixes only the two lifts of \(O\). A deck involution descending to horizontal reflection exchanges front and back, so its fixed points lie on the boundary along the horizontal axis. The vertical case is analogous. Thus no involution fixes a lattice point diagonal to \(o\).

There are only three possible class assignments:

- Class \(o\) must use the half-turn, since \(O\) is regular.
- Class \(o+(1,0)\) must use horizontal reflection. The east and west central midpoints have fan size two or four by symmetry. They must be fixed, hence boundary points and flat.
- Class \(o+(0,1)\) similarly forces the north and south midpoints to be flat.

If both adjacent classes occur, all four midpoints are flat.

If class \(o\) and the horizontally adjacent class occur, the east and west midpoints are flat. Were the north midpoint interior, symmetry would make \(O+(0,2)\) regular. It has class \(o\), but the half-turn does not fix it—a contradiction. Thus the north and south midpoints are also flat. The vertical case is identical.

All eight outer edges of the central \(2\times2\) block are therefore walls. Connectivity forces \(P\) to equal that block, which has only one interior lattice point. Contradiction.

**PROVED — conclude amalgamation.** Under the Galois hypothesis, each \(B_x\) is the orbit partition of a subgroup \(H_x\le\operatorname{Deck}(DP/PC)\). Incomparable subgroups of \(V_4\) must be different order-two subgroups. The preceding exclusion rules that out for different canonical classes.

Therefore \(B_b,B_c,B_d\) form a chain. Their join is one of them, and hence separates whenever all three separate. No reflex bound was used. \(\square\)

**2. PROVED — the finite area bound.**

Let \(N=DP/B_x\) be a separating class quotient, with
\[
\delta=\deg(DP\to N),\qquad d=\deg(N\to PC),\qquad n=\delta d.
\]
The target is a sphere by Riemann–Hurwitz. Its cone angles are \(\pi,2\pi,3\pi\). If it has \(z\) zeros and \(p\) poles, Gauss–Bonnet gives \(p=z+4\).

For each base class \(j\), put
\[
w_j=p_j+3z_j.
\]
The remaining cycles have length two, so
\[
w_j\equiv d\pmod2,\qquad \sum_jw_j=4z+4.
\]
At the certified class, \(w_x=d\).

Suppose source corners occupy at least three parity classes. Their images are singular: neither \(\pi\) nor \(3\pi\) can cover a regular \(2\pi\) point with integer degree. Thus target singularities occupy at least three classes.

If \(d\) is odd, all three off-\(x\) weights are positive odd integers. If \(d\) is even, at least two off-\(x\) weights are positive even integers. Consequently
\[
d\le
\begin{cases}
4z+1,&d\text{ odd},\\
4z,&d\text{ even}.
\end{cases}
\]
If \(z=0\), this forces \(d=1\), the unit pillowcase, which cannot separate same-class marks. Hence \(z\ge1\).

Each target zero has \(\delta\) unramified zero preimages, giving \(\delta z\le r\) and \(\delta\le r\). Therefore
\[
\boxed{n\le\delta(4z+1)\le4r+\delta\le5r.}
\]

**PROVED — normalization suffices for the corner-class hypothesis.** Gcd-one horizontal lengths supply an odd horizontal wall, hence a horizontally adjacent pair of corner classes. Gcd-one vertical lengths supply a vertically adjacent pair. One two-element set cannot contain both pairs.

**CITED — computational consequence.** d9 reports no dark pair at \(r\le8\) through area 20. Since three per-class certificates imply darkness, this and the new bound exclude normalized amalgamation counterexamples at \(r\le4\). At \(5\le r\le8\), a normalized counterexample must have
\[
21\le n\le5r\le40.
\]
The census was not replayed. This does not bound arbitrary dark rooms lacking per-class certificates.

**3. PROVED — checks on the two named rooms.**

Use class offsets \(b=(1,0),c=(1,1),d=(0,1)\) relative to the marks.

| Room | \(B_b\) | \(B_c\) | \(B_d\) | \(B_*\) |
|---|---|---|---|---|
| 22-wall room | Staircase quotient, degree 3 | Identity | Same staircase quotient | Same staircase quotient |
| P6 | Staircase quotient, degree 4 | Same | Same | Same |

For both rooms, every listed partition separates **all four endpoint lift pairs**.

The common five-sheet target has monodromy types
\[
a:(2,2,1),\qquad b,c,d:(3,1,1).
\]
Both source lifts map to one regular A point of the staircase double; both target lifts map to the other.

For the 22-wall room, indexing its cells lexicographically, the nonidentity blocks are
\[
\{0,1,14\},\{2,5,13\},\{3,4,12\},\{6,9,11\},\{7,8,10\}.
\]
For P6, indexing lexicographically after subtracting \(S=(1,0)\), they are
\[
\{0,1,2,19\},\{3,6,7,17\},\{4,5,8,18\},
\{9,12,13,15\},\{10,11,14,16\}.
\]

The degree-three cover has a pole fibre with local degrees \((2,1)\); P6 has one with \((2,1,1)\). Thus both staircase covers are **non-Galois**. They satisfy amalgamation outside the conditional hypothesis.

Two implementations reproduced these partitions: the existing canonical-closure code and an independent construction from cell-edge involutions. The latter also verified invariance under room involutions and found trivial deck groups for both full pillowcase covers. Timed check sections totalled approximately 0.0024 CPU seconds, excluding imports. No optical discovery search was run.

**4. PROVED — what remains.**

Unrestricted amalgamation would establish only
\[
\text{three separating class quotients}
\Longrightarrow
\text{one separating parity quotient}.
\]
The separate visibility-to-certificate implication remains unproved:
\[
B_x\text{ identifies an endpoint lift pair}
\Longrightarrow
\text{a legal trajectory of direction class }x.
\]
General rigid-factor certificates must also be excluded or incorporated. The difficulty remains that partition closure combines different monodromy words, while a trajectory must retain one direction.

**GUESSED — verdict.** The unrestricted \(r\le8\) lemma remains unresolved. The Galois case is settled, and the normalized per-class obstruction is now confined to area at most 40. These are concrete reductions, but they do not supply directional coherence. My probability for the whole programme remains **35%**.