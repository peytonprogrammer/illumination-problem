# COORD-COPRIME-01 independent review: ACCEPT

The terminal-pair lemma and whole-native-pair corollary are accepted at exactly the pinned candidate's scope. No correction is needed. All fourteen supplied source hashes match before and after the independent replay. The separate JSON receipt records them and the review evidence hashes. Nothing here closes all W10/r3, r<=8, arbitrary-real endpoint pairs or a novelty question.

## Accepted statement

Let a>0 be rational, N>=5 odd, l=(N-2)a, w=(N-1)a and A=Na. Let b,c,h,H be integers with 0<b<c<h<H and gcd(2(H-h),N)=1. Every rational source `(s,u)` with 0<s<a, b<u<=h and integral u connects to every rational lowest-chamber target `(t,v)` with l<t<A, 0<v<c, integral v and odd c-v, by a finite ordinary original-room specular path avoiding every true corner.

Consequently, for positive integral a, odd N>=5, integral 0<b<c<h with c odd and H=h+1, EVERY distinct actual interior even-even pair in the stated ten-wall room illuminates. There is no dimension, area, reflection or winding cutoff within this family.

## Claim-by-claim audit

### 1. Forbidden congruences and three-class covering: ACCEPT

At the grid slopes `(A+z-s+2aq)/D`, each bad phase condition is an affine congruence in the INTEGER q. Its constant need not be integral. If it is solvable at q0, subtracting that instance shows precisely `D divides t_i(q-q0)`, so its solution set is one class of period `D/gcd(t_i,D)`. If it is not solvable, the bad set is empty. All nonzero event times are distinct and strictly between 0 and D, so their periods are at least 2. At d0=0 the first event is impossible because 0<s<a; it is not a period-1 forbidden class.

An independent density/CRT proof of the covering restriction is as follows. Sort the three periods p<=q<=r. If p>=4, their total density is at most3/4. If p=3, density can reach 1 only at (3,3,3). If p=2 and q>=5, density is at most9/10. If p=2,q=4, density can reach 1 only at r=4. If p=2,q=3, the 2- and 3-classes overlap with density1/6, so their union has density2/3; adding a class with r>=4 gives at most11/12. At r=3, either the two 3-classes coincide or are distinct; in the latter case each adds only1/6 beyond the 2-class, giving at most5/6. The only remaining possibility has two periods2. Fewer classes do not enlarge the union. This proves the claimed NECESSARY list of possible coverings; it does not incorrectly assert that every choice of residues in a listed pattern covers.

Two period-2 event times would both have to equal D/2, contradicting distinctness. Three period-3 times cannot fit the only two positions D/3 and2D/3. With (2,4,4), the times must be the three sorted positions D/4,D/2,3D/4. Hence G=t2-t1=D/4=d2. But G=2(H-h) is even and d2 odd. This excludes the final possible covering. When d0=0 there are only two nonempty bad classes; neither two distinct period-2 times nor any larger-period pair can cover. Since every forbidden period divides D, testing q=0,...,D-1 finds a permissible q. The grid slope is positive because A+z-s>A-a>0.

### 2. Source invariance and strict coprime cap orbit: ACCEPT

The centered source residual is in (-a,a) after the first bad class is excluded. Under `tau -> tau+2aM`, the source center index increases by the INTEGER d0 M, leaving that residual exactly unchanged. Thus no source guard is lost while changing the cap phase.

Modulo 2A=2Na, the cap phase increments by 2aGM. Coprimality of G,N gives precisely N different points of one spacing-2a coset. Its target cap window is centered at odd multiples of A and has open length2a. Exclusion of the second bad phase means this coset misses BOTH endpoints of that window; therefore precisely one orbit point lies inside. This is a finite exact coset argument, not a density or asymptotic recurrence argument. The retained cap residual satisfies |z1|<a=R.

The right residual modulo2a equals `s+t3*tau-A`. Both source/right indices and the odd cap translation subtract multiples of2a because A=Na with N integral. Increasing tau by2aM changes this expression by an integer multiple of2a. The third exclusion therefore remains in force and gives |z2|<a. No independent source/right phase choice is assumed.

My selector uses the LAST permissible q, then solves M by a modular inverse rather than trying all cap periods. Because N is odd, if `r=X0/(2a)` and `k=(N-1)/2`, the forbidden-endpoint exclusion says r is nonintegral and the strict window requires `floor(r)+GM = k (mod N)`. Thus `M=G^{-1}(k-floor(r)) (mod N)` selects its unique point directly. This independently confirms the cap-orbit logic.

### 3. Final target parity: ACCEPT

Expanding the glued phase gives `E=z+2aJ` with integral J. This is initially only a congruence modulo2a; it is not yet the required bottom folding period4a. The correction `tau -> tau+2aN` preserves all three residuals: source n grows by Nd0, cap m by G, and right k by Ng1. Meanwhile E grows by2aNd2. Since both N and d2 are odd, J changes parity. At most one correction gives `E=z (mod4a)`. With `0<z<2a`, folding in the actual bottom width2a returns exactly z and hence the original abscissa t. This checks the potentially missing factor of two rather than assuming endpoint projection suffices.

### 4. Actual walls, signed directions, roof corners and u=h: ACCEPT

The four bands use source width a, cap width A, right width a and bottom width2a. At the source seam both local expressions are the same absolute value. At the descending cap seam, subtraction of `(2m+1)A` uses the exact identity `F_A((2m+1)A+x)=A-|x|` for |x|<a<A. At the right/bottom seam, subtraction of 2ka gives the same local `A-|x|` expression on both sides. These neighborhood identities preserve the SIGNED horizontal velocity. Vertical velocity agrees at each seam and reverses only at H. A zero residual is a single ordinary contact with the smooth outer x=0 or x=A wall, never an artificial reflection.

Strict residual bounds avoid the genuine reflex corners and ledges. Each open-band vertical contact is on the original finite wall interval: x=0,a between b and h; x=0,A above h; x=w,A between c and h; x=l,A below c. All widths, flight times and the selected slope are finite, giving a finite trajectory without imposing a uniform reflection bound.

If the cap midpoint at H were a fold cusp, triangular-wave symmetry about that cusp would equate the two h-level cap mouth coordinates. Their disjoint ranges `[0,a)` and `(w,A]` contradict this. Thus its one roof hit is strictly inside the actual roof. When u=h, the empty source band contributes z0=s and matches the source velocity directly; the same disjoint-range roof argument applies. No limiting seam argument is used.

The actual target height v occurs on ascent only in the source arm, where x<a<t because l>=3a, or does not occur on ascent. Cap heights exceed v. On descent height reaches v only at the final time. The selected ray therefore reaches actual T first at its nominated end, with no sheet or endpoint substitution.

### 5. Whole native family and inherited coverage: ACCEPT

For H=h+1 and integral coordinates, no actual native mark has h<y<H. A native source in the left terminal therefore has integral u<=h, including u=h when available. Every lowest-chamber mark has even v, so odd c gives odd d2. G=2 is coprime to odd N. All residual native terminal pairs meet the lemma.

The original strict order a<l<w<A and b<c<h<H holds for this family. The pinned TR01 protected U/L theorem applies to every same-region actual pair, with its artificial-wall and added-corner guards intact. With no native marks in the open cap, its uncovered unordered pairs are exactly left terminal versus lowest chamber. The new lemma covers these; reversal handles either label order. Empty terminal mark sets for very small a do not create an exceptional case. This proves the quantified family corollary, rather than extrapolating it from the one-room check.

## Independent reproducible evidence

Run `python3 -B .context/illumination-generalization-2026-11-06/review/three-reflex-coprime-independent-check.py`.

The code executes no coordinator or author functions. It selects different slopes (last permissible q and direct modular inverse), then replays that ONE prescribed ray using earliest intersections with the ORIGINAL finite walls, rejecting true vertices and checking exact target arrival before the next wall. It separately checks every resulting leg and specular contact with reviewer-owned geometric predicates. It does not derive the path by copying the coordinator's folded event list.

All nine prescribed terminal inputs pass: 1016 actual reflections and10250 wall/leg guards, including rational horizontal marks, composite N, a two-unit cap, long arms and u=h. Counts differ from the coordinator's because the selectors deliberately choose different valid slopes. In the one prescribed room `(4,12,16,20;1,5,7,8)`, all ten actual native marks and all45 pairs pass,18 via the new terminal method, with1494 reflections and15470 guards. This room fails both former sufficient thresholds H>=505 and A>=644. These finite checks corroborate the construction; the arbitrary-size quantifiers follow from the hand argument above.

## Concrete next optical extension

The final parity correction is a target-residue correction modulo a bottom-width multiplier. For B=K a one can seek `J=0 (mod K)` by shifts of tau by2aN; their step on J is Nd2. The natural precise extension requires `gcd(Nd2,K)=1` and retains the three strict portal guards. The existing improvement author has already claimed the broader construction, so this reviewer does not duplicate that proof packet. A useful all-native corollary to challenge is K=2^r, N odd>K+1, c odd, H=h+1: all native d2 are odd and therefore coprime to K. This remains a proposed next scope until the author's generalized packet is independently reviewed. Removing the coprime or arithmetic-height hypotheses is separate and currently unproved.
