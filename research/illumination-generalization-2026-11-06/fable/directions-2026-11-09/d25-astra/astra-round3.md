**[Proved] The band lemma works within its stated scope. A uniform bound on the crossing numerators does not—even for rectangles. This does not refute periodicity of lit/dark status.**

**1. Band lemma.**

**[Proved]** Develop each chord of width \(w\) as the folded quotient of a horizontal line with period \(2w\). A crossing with primitive direction \((q,p)\) gains horizontal displacement
\[
\frac{Dq}{|p|}.
\]
For the proposed \(D\), this is divisible by \(2w\). Consequently, both the exit position and horizontal direction agree with the original crossing. The vertical direction also agrees. Repeating this replacement at every crossing reconstructs the original trajectory outside the band, with its upper portions translated.

**[Proved]** A crossing at a chord endpoint requires comparing unfolded directional germs. The inserted traversal returns to the same phase modulo \(2w\), so the original vertical-wall reflection is preserved. The seam points are flat wall points: the hypothesis excluding vertices on \(y=c\) ensures that the extended walls remain straight there.

**[Proved]** Intermediate lattice points in the inserted band cause no obstruction. None is a room vertex; boundary hits there are ordinary reflections.

**[Proved]** The statement excludes \(S\) or \(T\) on the line, so their placement is not a gap in its proof. An extension works if points on the cut remain on the lower seam: insert a full traversal at an endpoint whenever its original path enters or leaves the translated upper portion.

**[Proved]** In an orthogonal room, all segments have the same absolute primitive components \((|q|,|p|)\). Thus \(\operatorname{lcm}(|p_j|)=|p|\); different crossing numerators are unnecessary.

**2. Unbounded necessary numerators.**

**[Proved]** Consider the fixed skeleton
\[
P_D=[0,6]\times[0,3D],\qquad
S_D=(2,D),\quad T_D=(4,2D),
\]
with \(D=2^j,\ j\ge2\). Its horizontal gaps are \(2,2,2\); its vertical gaps are \(D,D,D\). Both endpoints belong to class A.

Every billiard path unfolds to a segment whose displacement is
\[
(a,b)=\bigl(\pm4-2+12m,\;D(\pm2-1+6n)\bigr).
\]
Here \(v_2(a)=1\) and \(v_2(b)=j\). Writing \((a,b)=g(q,p)\) primitively therefore gives
\[
2^{j-1}\mid p,\qquad |p|\ge D/2.
\]
Every path crosses any horizontal line strictly between the endpoint rows. Thus its crossing numerator is necessarily unbounded.

**[Proved]** The direct segment has primitive direction \((1,D/2)\), so the bound is attained. Every room-pair is lit.

**[Proved]** This disproves a skeleton-uniform numerator bound, even with fixed chord width. It also prevents obtaining one fixed period \(Q\) solely by selecting band-compatible witnesses: compatibility requires \(p\mid Q\), impossible eventually here.

**[Proved]** Three gaps vary together in this example. It does not disprove a numerator bound depending on the other fixed gaps, nor eventual periodicity itself.

**3. A restricted stabilization theorem.**

**[Proved, using d17’s unfolding construction]** For Lemma H’s channel-and-door configuration, fix \(L,w,h>0\) and vary the channel distance \(D\). Every pair is lit once
\[
D>Lh/w.
\]

Indeed, write \(Lh/(wD)=m/n\) in lowest terms. Above that threshold, \(n\ge2\). The candidate door-crossing numerators form a coset with spacing
\[
2wD/n\le wD,
\]
while the valid open window has length \(w(D+h)>wD\). Therefore a candidate lies strictly inside the door. This gives explicit eventual constancy with
\[
G=\lfloor Lh/w\rfloor+1,\qquad Q=2
\]
when preserving parity.

**[Proved]** This threshold depends on other metric parameters. It supplies no skeleton-uniform \(G\) when those parameters also vary.

**[Proved]** The band propagation property alone cannot imply eventual periodicity. Abstractly, let “lit” mean “composite”: each lit integer \(n\) remains lit along \(n+kn\). Nevertheless, this status is not eventually periodic. For any proposed period \(Q\), choose a sufficiently large prime \(p\); then \(p\) and \(p(1+Q)\) have different status and the same residue modulo \(Q\). This is a logical counterexample, not a geometric one.

**4. Weakest useful replacement.**

**[Guessed]** Seek an explicit bound \(B\) such that every minimal-area dark room-pair with \(W\le20\) has every skeleton gap at most \(B\). This requires neither periodicity nor bounded witness slopes. A sufficient compression theorem would turn any larger-gap dark counterexample into a smaller-area dark counterexample.

**[Proved]** Gap bounds are still area bounds. For \(r\le8\), adding endpoint rows and columns leaves at most \(r+3\le11\) gaps per axis. Hence a bound \(B\) gives area at most \(121B^2\). Changing the size parameter does not remove the original finiteness obstacle.

**[Guessed] Probability that a stabilization-type reduction is provable for \(W\le20\): 5%.**