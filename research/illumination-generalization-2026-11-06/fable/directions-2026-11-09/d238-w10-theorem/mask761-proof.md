Advances: T10, pyramid — computer-assisted proof for the remaining position type of mask 761, submitted for independent review.

**Claim.** With the strict placement and positive dimensions of onepass.py, at least one axis has a one-pass chord. The construction needs only the actual terminal image on each axis. It applies in particular to all lattice realizations. The d169 position-type coverage and d172 review identify this as the only remaining pair type in mask 761. The other pyramid masks are outside this claim.

**Gate coordinates.** Use local widths w,u, local longitudinal travels a,d,b, and L=d+b, D=a+L. Start in the image s=σx+2kw, aim at z+2ui, and subtract 2ui after the second gate. Linear interpolation gives
```
DE = Ls + a(z+2ui)
DF = bs + (a+d)z − 2bui.
```
For the vertical sweep, |E|<w and |F|<u suffice. For the horizontal sweep substitute (w,u,x,z,a,d,b)=(h,U,h−b,U+a,z−u,u−w,w−x), with U=h+d in original coordinates. Require |E|<h and 0<F<U. The actual target image requires no assumption on the exterior floor or roof. These are the t10-pyramid-2 folding rules. Equality at a singular endpoint is never used to certify a hit.

**Four necessary inequalities for simultaneous failure.** Write R=(dz−2ubi)/L. Then F=R+bE/L. For fixed i,σ the source windings space E by 2wL/D. Varying i spaces R by 2ub/L. These statements already hold with the actual terminal image.

1. Necessarily wb>ud. Otherwise choose R nearest zero, then E nearest zero. We have |R|≤ub/L, |E|≤wL/D<w and |F|≤ub/L+bw/D<u.
2. Necessarily a<L. Again choose |R|≤ub/L. The allowed E interval is the intersection of (−w,w) with the interval of radius uL/b centered at −RL/b. Its length is at least min(2w,2uL/b,w+ud/b)>w. If a≥L the spacing is at most w.
3. Put L′=u−x, b′=w−x, d′=u−w, D′=z−x. Necessarily D′≤2L′. In the horizontal sweep choose R′ in [0,U]. If d′≥b′ the row spacing is at most U. Otherwise i=0 works because a<L<h+d=U and d′<b′. The allowable E′ interval then has length at least h: the second gate pulls back to an interval of length UL′/b′>h whose closure contains zero. Clipping to (−h,h) retains at least h. If D′>2L′ the source spacing is strictly below h.
4. Necessarily d′≤3b′. Otherwise b′/L′<1/4. Choose R′ nearest U/2, then E′ nearest zero. The deviation from the center is ≤Ub′/L′+hb′/D′<(U+h)/4<U/2. Also |E′|≤hL′/D′<h.

**Finite contradiction.** Under these four necessary inequalities, eight vertical witnesses suffice. In (i,k,σ) notation use (0,k,+1) for k=−5,−4,−3,−2, and (i,k,−1) for i=0,1 and k=−1,0. The linear certificate proves that at least one passes strictly.

Use X=(x,w−x,u−w,z−u) and Y=(a,d,b,h−b). Every gate margin and every assumption below is bilinear. Replace each product XᵢYⱼ by an independent positive real pᵢⱼ. Impose (1) as written, (2) multiplied by u, (4) multiplied by b, and (3) multiplied separately by each positive Yⱼ. The last four constraints are (X₁+X₂−X₃)Yⱼ≥0, indexing from zero. Every actual room gives a feasible product table for these assumptions if both lists miss. Dropping the product identities enlarges the feasible set.

For each witness assert that at least one of wD±DE, uD±DF is nonpositive. The resulting rational linear-real formula is unsatisfiable. Thus no actual room can satisfy all eight misses and the necessary inequalities. This is a proof by finite arithmetic, with no sampled rooms or algebraic-number approximation.

**Reproduction.** From this directory run `python verify_761.py` with cvc5 1.4.2, then `z3 mask761.smt2` (tested with Z3 5.4.1). Both return `unsat`. The script constructs coefficients by evaluating each bilinear margin on pairs of coordinate unit vectors. It enables cvc5 proof checking and requests the proof. The SMT-LIB file can also be checked on its own. The final certificate does not depend on the discovery calculation, solver timeouts, or completeness of a bounded winding search.
