**PROVED — conditional result.** The visibility-to-certificate implication holds under a named **classwise joint-majority hypothesis**, defined below. The proof uses affine return maps and genuine straight trajectories; it never substitutes arbitrary monodromy words for trajectories.

**GUESSED — scope.** I have not proved that \(r\le8\) forces this hypothesis. The unrestricted visibility-to-certificate statement remains open.

**1. PROVED — the exact directional object.**

Work with the same-class interior lattice marks of d35–d36. Put \(Q=DP\), and let \(V\) be its regular points over the A pillowcase pole.

For a primitive direction of class \(x\in\{b,c,d\}\), lift the corresponding pillowcase arc \(A\to x\). Delete every vertex of cone angle \(\pi\) or \(3\pi\), retaining only regular \(2\pi\) vertices. The remaining graph has degree at most two.

Two regular A points are joined in that direction exactly when they belong to one component of this regular graph.

*Proof.* Following consecutive edges is straight continuation through regular points. Poles and zeros are precisely physical corner lifts and stop the trajectory. A component is a path or cycle, along which any two A vertices connect.

This also explains why “a cylinder through both points” needs care. On the unfolding, ordinary cylinders can contain removable corner blockers. Moreover, a valid segment can lie on a critical leaf between blockers. The regular lift graph handles both issues.

**2. PROVED — the affine averaging lemma.**

Let a finite group \(H\) act on a finite set of regular A points through affine return maps preserving physical corner lifts and direction class \(x\). Let \(O_i,O_j\) be two \(H\)-orbits.

Suppose one regular directional component \(C\) satisfies
\[
\boxed{\frac{|C\cap O_i|}{|O_i|}
      +\frac{|C\cap O_j|}{|O_j|}>1.}
\]
Then every distinct pair \(p\in O_i,q\in O_j\) is \(x\)-illuminated.

*Proof.* For uniformly chosen \(h\in H\),
\[
\Pr(hp\in C)=\frac{|C\cap O_i|}{|O_i|},
\qquad
\Pr(hq\in C)=\frac{|C\cap O_j|}{|O_j|}.
\]
The strict inequality forces some \(h\) with both images in \(C\). They connect along one straight trajectory. Pulling it back by \(h^{-1}\) gives a straight, corner-avoiding trajectory from \(p\) to \(q\). The direction remains in class \(x\).

Here \(H\) means the finite **point-permutation image of affine return maps**, not the sheet monodromy group.

**PROVED — useful consequences.**

- If \(H\) is transitive and \(|C|>|V|/2\), every pair in \(V\) illuminates.
- In a transitive orbit of size two or three, one visible pair suffices.
- For a specified dark pair in orbits \(O_i,O_j\), every directional component must satisfy the reverse inequality, with sum at most one.

An exact refinement uses unordered-pair orbits: if a component contains one pair from an \(H\)-orbit of pairs, every pair in that orbit illuminates. Thus a dark pair-orbit makes every directional component an independent set in its orbital graph.

**3. PROVED — conditional visibility-to-certificate theorem.**

For each \(x\), form the canonical quotient
\[
\phi_x:Q\to N_x=Q/B_x.
\]
Partition \(V\) into fibres \(F\) of \(\phi_x\).

Every regular \(x\)-directional component lies within one such fibre.

*Proof.* Its odd checkpoints map to poles of \(N_x\): they cannot map to zeros because they are regular upstairs. At a pole the projected trajectory folds back. Consecutive even A checkpoints therefore have the same image. Repeat along the component.

Define the **classwise joint-majority hypothesis**:

> For every class \(x\) and every fibre \(F\), choose a subgroup of affine return maps preserving \(F\) and direction class \(x\). For each pair of its point-orbits \(O_i,O_j\), some regular component \(C\subset F\), in a direction of class \(x\), satisfies the boxed density inequality.

This is a finite group-and-component condition. It asks for component sizes and orbit intersections, rather than a trajectory for every endpoint pair.

Under this hypothesis,
\[
\phi_x(\sigma)=\phi_x(\tau)
\quad\Longrightarrow\quad
\sigma,\tau\text{ are }x\text{-illuminated}.
\]
This follows directly from the averaging lemma.

Consequently, if the physical pair is dark, \(B_x\) separates every source/target lift pair for **each** \(x\). The three canonical quotients therefore supply per-class parity certificates.

No amalgamation assumption is used. Under this hypothesis, rigid certificates are unnecessary.

**4. PROVED — a non-vacuous geometric special case.**

Consider the rescaled L-room already used in d25:
\[
P=([0,4]\times[0,2])\cup([0,2]\times[2,4]).
\]
Its odd-odd interior points are
\[
S=(1,1),\quad T=(3,1),\quad U=(1,3),
\]
with front/back lifts \(s_\pm,t_\pm,u_\pm\) in \(Q\).

The horizontal decomposition has circumferences \(8,4\) and heights \(2,2\). A horizontal multitwist of shear four fixes the boundary saddle connections and acts on these six points as
\[
h=(s_+\ t_-)(s_-\ t_+).
\]
The analogous vertical multitwist acts as
\[
v=(s_+\ u_-)(s_-\ u_+).
\]
Both preserve direction parity classes.

Their finite permutation image has two orbits:
\[
O_1=\{s_+,t_-,u_-\},\qquad
O_2=\{s_-,t_+,u_+\}.
\]
One horizontal regular component contains
\[
C=\{s_+,s_-,t_+,t_-\}.
\]
It contains two-thirds of each orbit. Every orbit-pair density sum is therefore \(4/3\). The averaging lemma proves that all six regular A points pairwise illuminate, using directions of horizontal parity.

This example uses a return subgroup with **two** point-orbits. It does not assume the abandoned pair-transitivity lemma. It is an analytical construction, not a computational search.

**5. PROVED — why the cone count does not establish joint majority.**

Let
\[
w_y=p_y+3z_y
\]
count corner prongs over class \(y\). Then \(\sum_yw_y=4r+4\).

For one arc \(A\to x\), every path component of the regular graph has two missing edge incidences. Deleting corner vertices supplies at most \(w_A+w_x\) such incidences. Therefore
\[
p_x\le\frac{w_A+w_x}{2}\le2r+2
\]
for the number of regular path components in \(Q\), including isolated vertices. This is the doubled-polygon version of d25’s unfolding bound.

But cycle components remain uncontrolled. Rectangles already have arbitrarily many discrete regular-leaf cycles as their dimensions increase. Thus this inequality does not force one component to occupy a majority of a return orbit.

Likewise, one cusp controls direction orbits, not automatically the action on endpoint fibres. A separate point-action argument is still needed.

**6. PROVED — strengthen the d36 area reduction, but keep its direction straight.**

Assume the corners occupy at least three parity classes, as in normalized presentations.

The d36 proof actually establishes:
\[
N_x\ne PC\quad\Longrightarrow\quad n\le5r,
\]
whether or not \(N_x\) separates the chosen pair. Separation was used only to exclude \(N_x=PC\).

Indeed, writing \(\delta=\deg(Q\to N_x)\), \(d=\deg(N_x\to PC)\), and \(z=z_{N_x}\), that proof gives
\[
d\le4z+1,\qquad
N_x\ne PC\Rightarrow z\ge1,\qquad
\delta z\le r.
\]
Hence \(n=\delta d\le5r\).

Therefore
\[
\boxed{n>5r\Longrightarrow B_b=B_c=B_d=\text{one-block partition}.}
\]
Each canonical rigid partition \(R_y\) is coarser than \(B_y\), since it merges all cycles over \(y\), not merely 2-cycles. Thus all \(R_y\) are also one-block partitions in this range.

For normalized \(r\le8\), rooms of area greater than 40 are consequently **certificate-free for these canonical parity/rigid mechanisms**. The area bound does not eliminate them; the proposed theorem must prove them illuminated.

Conversely, a proper one-class quotient has \(\delta\le r\le8\). Its regular A fibres have at most eight points; fibres over target poles have at most four regular preimages. This supplies a bounded fibre problem in the proper-quotient branch.

**7. PROVED — the two named dark-room checks.**

Using \(b=(1,0),c=(1,1),d=(0,1)\) relative to the marks, the fixed computations give:

| Room | \(B_b\) | \(B_c\) | \(B_d\) | \(B_*\) |
|---|---|---|---|---|
| 22-wall room | Degree-three staircase quotient | Identity | Same staircase quotient | Same staircase quotient |
| P6 | Degree-four staircase quotient | Same | Same | Same |

Every listed partition separates all four endpoint lift pairs.

The common target has types
\[
a:(2,2,1),\qquad b,c,d:(3,1,1),
\]
so it is the staircase double. Both source lifts map to one regular A point and both target lifts to the other. The canonical rigid partitions have one block in both rooms.

Thus the certificate-producing procedure returns their staircase certificates immediately. It never invokes a majority argument between points in different fibres.

The static visibility checks also show:

- In the 22-wall room, the common regular A fibres have sizes \(3+3\). The original basis gives a two-point component in one fibre at \(b\), and in the other at \(d\).
- In P6, the fibres have sizes \(4+4\). The checked original-basis components have size at most two in either fibre. Exactly half is insufficient for the strict majority argument.

These figures are not a verification of the joint-majority hypothesis over their return actions. No such verification is needed for their already separating certificates.

The checks used only the original three arc graphs and canonical partition closures. Their timed sections totalled under 0.003 CPU seconds, excluding imports. No modular-orbit, ray, direction, or reflection-word discovery search was run.

**CITED — existing closed branch.** d2-review and the \(k\le6\) theorem already illuminate the \(r\le8\) case with a non-unit common parity factor. The unresolved cases therefore have \(N_{\min}=PC\). A proper *one-class* quotient may nevertheless remain; this is distinct from that closed common-factor branch.

**GUESSED — verdict and next step.** The joint-majority theorem gives a genuine conditional solution, with a geometric example and no word-to-ray substitution. I have not derived its hypothesis from \(r\le8\), and it is only sufficient.

The single next step is the **degree-three one-class fibre lemma**: prove that every affine-return pair-orbit in a three-point fibre meets a regular visibility component, or yields a rigid certificate. This isolates at most three pair-orbits and targets a proper one-class quotient rather than repeating the already closed common-factor case.

My probability for the whole programme is **30%**.