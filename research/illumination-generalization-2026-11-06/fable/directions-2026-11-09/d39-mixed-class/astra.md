**PROVED — two narrow conclusions.** The ordinary, fixed-unit-pillow per-class necessity claim is false at \(r=4\) under lattice refinement. The missing mechanism is a certificate relative to a coarser pillowcase. Separately, with corners in at least three parity classes, an **essential Rig certificate** at \(r\le8\) forces area at most 20. Here “essential” means that Par does not already certify that class.

**CITED — correction to d37.** The referee is right: allowing arbitrary subgroups made joint majority equivalent to the false per-class same-fibre assertion. I withdraw it as a route to the target. The averaging lemma remains valid, with the stated interior-mark restriction.

All statements below concern the same-class lattice marks of d35–d37.

**1. PROVED — ordinary per-class necessity is false without normalization.**

Use the named cross
\[
P=([0,4]\times[1,3])\cup([1,3]\times[0,4]),
\qquad S=(1,2),\quad T=(3,2).
\]
With offsets \(b=(1,0),c=(1,1),d=(0,1)\), the reviewed certificates show that every lift pair is \(c\)-dark, while the horizontal segment makes the room pair \(b\)-lit.

View this same cross in the lattice of mesh \(1/3\). In integer coordinates:
\[
P'=3P,\qquad S'=(3,6),\quad T'=(9,6).
\]
It has \(r=4\), area \(108\), and corners in three parity classes. Uniform scaling preserves primitive direction parity, so the pair remains \(c\)-dark.

The d36 bound applies to **any non-unit class quotient**, whether separating or not:
\[
N_x\ne PC\Longrightarrow n\le5r.
\]
Since \(108>20\), every \(B_x\) is the one-block partition. Every \(R_y\), being coarser than \(B_y\), is also one-block. Thus there is no ordinary Par or Rig certificate.

There is no ordinary Cut certificate at \(c\), either. Cut forces target degree \(d\le3\). Degrees one and two are impossible: Cut needs a regular A point downstairs, whereas this presentation has convex A corners that cannot map to a degree-two target’s sole regular A point. At degree three the A profile is \((2,1)\). All regular A points must map to the regular point. The pole fibre must therefore consist exactly of the four convex A corners, giving cover degree \(4\). But the actual degree would be \(108/3=36\), a contradiction.

Hence
\[
\boxed{c\text{-dark}\;\not\Rightarrow\;\text{ordinary Par, Cut, or Rig at }c}
\]
already at \(r=4\).

**PROVED — the missing explanation is relative Cut.** Over the coarser pillowcase \(D([0,3]^2)\), the original cross’s Cut certificate survives unchanged. That pillowcase has degree nine over the refined unit pillowcase. The intermediate target is a scaled tromino double, of degree three over the coarse pillowcase but degree 27 over the fine one.

Thus this example does not refute a statement allowing relative pillowcase towers. It refutes the fixed-unit-pillow formulation. Completeness for normalized presentations, or completeness with relative bases allowed, remains unproved.

**2. PROVED — genuine ordinary Cut cannot participate in a fully certified dark room.**

If class \(x\) has no transparent point, \(B_x\) is discrete and Par already separates distinct regular A points. Cut is then redundant.

Suppose \(x\) has a transparent point. The reviewed R4 proof can be made independent of normalization:

- Cut gives \(d\le3\).
- At \(d=2\), A and \(x\) must both have transposition monodromy. A third corner is a full transposition, forcing the fourth to be one too. Riemann–Hurwitz gives genus one, impossible for an intermediate quotient of a sphere.
- At \(d=3\), the profiles are \((2,1)\) at A and \(x\), \((3)\) at one other corner, and identity at the last.

The remaining geometric argument is the corrected R4 proof in `d10-d12-review`, including its adjacent-class case. For diagonal \(x\), only the four long-side reflected tromino copies are permitted; two interior A marks force the cross. For adjacent \(x\), the target has an interior \(\pi\)-cone, and its planar branched unfolding is the Z-hexomino. The Cut restrictions forbid adjoining another such copy, leaving no interior A pair.

Therefore genuine ordinary Cut forces the named cross and its lit pair. This argument uses no reflex bound.

A full triple means certification in every class for **all four** source/target lift pairs. Such a triple cannot contain genuine Cut: soundness would make the pair dark, while the Cut geometry makes it lit.

**3. PROVED — essential Rig at \(r\le8\) has area at most 20, within the three-corner-class scope.**

By the reviewed canonical reduction, any Rig certificate can be checked on
\[
Q=DP\longrightarrow N=Q/R_y,
\]
where the monodromy at \(y\) is identity. Write
\[
\delta=\deg(Q\to N),\qquad d=\deg(N\to PC),\qquad z=z_N.
\]

**PROVED — a genuine rigid target has exactly one interior pole in its quotient disc.** The canonical quotient is seam-compatible. Every zero of \(N\) is fixed by its seam reflection, because all its preimages are zeros of \(Q\), hence lie on the source seam.

An off-seam pole has only regular preimages, each of local degree two. Thus \(\delta\) is even. A conjugate pair of such poles contributes \(\delta\) to ramification. Riemann–Hurwitz supplies only \(2\delta-2\), so there is at most one conjugate pair.

If there were no off-seam poles, the quotient disc would have no interior cone points. Since every \(y\)-point is a convex corner, permitted cell adjacencies preserve the opposite vertex. All cells consequently form one star, giving only a cell, domino, L-tromino, or \(2\times2\) square. These embedded targets cannot give Rig for an interior pair: allowable A images either coincide, or belong to the same live arc component. This includes the domino and square cases, without needing normalization.

Thus a genuine Rig target has exactly one interior \(\pi\)-cone, and \(\delta\) is even.

**PROVED — a target with \(z=1\) contributes no essential Rig.** Identity monodromy at \(y\) gives
\[
d=p_y\le p_N=z+4=5.
\]
A zero requires \(d\ge3\).

- For \(d=3\), the other profiles are \((3),(2,1),(2,1)\). If the certified class is the zero class, Rig already implies Par there. Otherwise the two possible A images are connected through the regular point of the other \((2,1)\) class, so Rig cannot separate them. This argument includes the non-planar adjacent-class target.
- For \(d=4\), the remaining profiles would be \((3,1),(2,2),(2,2)\). The product of two double transpositions lies in \(V_4\), so cannot cancel a 3-cycle.
- For \(d=5\), all five poles lie over \(y\). Each other odd-degree fibre would require an odd number of zeros; one zero cannot serve all three.

Hence essential Rig requires \(z\ge2\).

**PROVED — finish the area bound.** With at least three source corner classes, d36’s colour argument excludes a non-unit zero-free target. Also
\[
\delta z\le r,\qquad d\le z+4.
\]
Since \(\delta\) is even, \(z\ge2\), and \(r\le8\), only these cases remain:

- \(\delta=2\), \(z\le4\): \(n=\delta d\le16\).
- \(\delta=4\), \(z=2\), \(r=8\): \(d\le6\).

The exceptional \(d=6\) case is impossible. All six poles would lie over \(y\); the other profiles must be
\[
(3,3),\quad(2,2,2),\quad(2,2,2).
\]
This is the regular \(S_3\) cover. Its order-three deck subgroup fixes the two zeros and has two three-element orbits on the six poles.

Both zeros lie on the seam circle. Put them at \(0,\infty\); the order-three transformation becomes \(z\mapsto\omega z\), while the seam is a line through zero. At most one point from each three-element pole orbit lies on that line. At least four poles are therefore off the seam—two conjugate pairs—contradicting the ramification bound.

Thus \(d\le5\), and
\[
\boxed{\text{essential Rig at }r\le8\Longrightarrow n\le20.}
\]

**CITED — consequence for mixed triples.** The existing area-20 census reports no dark interior lattice pair at \(r\le8\). It was not rerun here. Combined with the proved bound and certificate soundness, it excludes a fully certified triple containing essential Rig, within the three-corner-class scope.

Therefore such a full triple reduces to **pure Par certificates**: Cut is redundant or impossible globally, and Rig is redundant or reduced to the already censused range.

This does **not** prove amalgamation. Three separate Par certificates are precisely the remaining per-class mechanism; d2 excludes only a common separating factor.

**4. PROVED — checks against the three named rooms.**

The completed check used these target degrees \(\deg(N\to PC)\):

| Presentation | \(N_b\) | \(N_c\) | \(N_d\) | \(N_*\) |
|---|---:|---:|---:|---:|
| 22-wall room | 5 | 15, discrete | 5 | 5 |
| P6 | 5 | 5 | 5 | 5 |
| Cross | 3 | 1 | 12, discrete | 1 |
| Same cross, even refinement | 2 | 2 | 2 | 1 |

For the 22-wall room,
\[
B_b=B_d=B_*,\qquad B_c=\mathrm{id}.
\]
For P6, all three class partitions equal \(B_*\). Their common target has profiles
\[
a:(2,2,1),\qquad b,c,d:(3,1,1),
\]
the staircase double. The covering degrees are respectively three and four. All four endpoint lift pairs separate, so both rooms retain their staircase darkness certificates.

For the original cross, every lift pair has:
\[
b:\text{lit},\qquad c:\mathrm{Cut},\qquad d:\mathrm{Par}.
\]
The original \(b\)-arc component contains all four endpoint lifts. Thus, with this fixed convention, \(d\) is dark rather than an alternative illuminating class. The cross has no full certificate triple.

The even refinement has 48 cells and all corners in A. Its three two-sheet pillowcase quotients identify the endpoint images; \(R_y=B_y\), so no ordinary Par or Rig separates them. Cut would require a degree-three target whose A pole fibre has degree \(48/3=16\), but the source A corners contribute
\[
8+3\cdot4=20
\]
prongs. Hence ordinary Cut is impossible too. Its \(c\)-darkness remains explained by relative Cut over the coarse pillowcase.

The check was the single completed process ending at approximately **0.0035 CPU seconds**, excluding imports. It was not repeated after the interruption. The refinements change the named cross’s lattice presentation, not its geometric shape.

**5. GUESSED — verdict and next step.**

The fixed-unit-pillow repaired target still needs correction: relative bases are indispensable outside normalized presentations. Within the three-corner-class scope, the new narrow result reduces fully certified mixed triples to the pure-Par amalgamation problem, using the cited census. Per-class certificate completeness remains open.

My probability that this certificate programme proves the full lattice minimum is **25%**.

**Next step:** independently verify the essential-Rig area-\(20\) lemma, especially the degree-six \(S_3\) seam argument, before using it to retire the mixed-Rig branch.