# A47: darkness forces a near-end endpoint or a close pair in thin combs

Status: author hand proof pending independent review. No discovery or computation. Original deadline2026-11-07T06:36:56.768851Z.

Let P be any finite integer two-sided rectangular-spine comb with core width c>=1, each tooth of width1 and height2, positive same-side gaps, and opposite overlaps allowed. Let the actual core floor be y0, roof y0+G. For a distinct actual interior A pair on the same seam write its ordered RELATIVE heights s<t. Put h=(t-s)/2 and q=min(s,G-t). If q>=3 and h>=3, this actual pair illuminates whenever W<=23 (hence whenever W<=21).

Normalization y0 to0 need not preserve the named even-even sublattice; this is only a Euclidean coordinate change preserving the ACTUAL endpoints. Since their original ordinates are even, t-s is even and h is an integer regardless of y0 parity. s,t,G are integers. No assertion that s,t,G or mu are even is used. Other A placements are already connected by the accepted strict-core/seam placement lemma; this statement only addresses the genuinely remaining same-seam pair.

## Optical prerequisite retained with its actual hypotheses

Assume for contradiction actual darkness. Let mu=(s+t)/2. The independently accepted A38 four-level theorem, using actual end-fold charts, actual seam far returns and no fictitious seam mirror, forces every number in

L={h,mu,G-mu,G-h}

to be a mouth ENDPOINT of an opposite-side tooth. If one is a smooth wall level, its actual folded core path connects the marks. If one is a tooth midpoint, the actual far-wall midpoint return connects them. These are the only alternatives because the levels are integers and every opposite tooth has integer band edges and height2. This necessary implication is used with ALL its actual-endpoint/corner guards; no Euclidean deformation transfer or finite search assumption is substituted for it.

## Charge proof without parity or a size bound

Write v=G-t, d=|s-v|>=0, q=min(s,v). Then G=2h+2q+d and the sorted list of levels, with possible repetition, is

h, h+q, h+q+d, h+2q+d.

All these levels lie in[3,G-3], since h>=3 and mu,G-mu are between h and G-h. A floor-flush height2 opposite tooth has only endpoints0,2, and a roof-flush one only G-2,G. Thus neither can block ANY listed level. Every blocker actually contributing is NONFLUSH.

If d=0 there are three distinct levels h,h+q,h+2q. Each pair differs at least q>=3. A height2 tooth therefore supplies at most one. At least THREE nonflush opposite teeth are necessary.

If d>0 there are four distinct levels. Every distance except possibly the central gap d is at least q>=3: distances involving nonadjacent levels are larger still. A height2 tooth can supply two distinct levels only if their distance is EXACTLY2. Hence at most the central pair can share a blocker, and only when d=2. The two outer levels cannot share that blocker or each other. At least THREE nonflush opposite teeth are again necessary. If d!=2, all four need distinct blockers.

The selected same-side teeth are themselves nonflush: their centers s>=q>=3 and t<=G-q<=G-3 put both height2 bands strictly between floor and roof. They are distinct and cannot be opposite blockers. Consequently N_nonflush>=2+3=5.

The exact maximal-wall identity is W=4+4N_nonflush+2N_flush; additional unused attachments only increase this charge. Hence actual darkness would force W>=24, contradicting W<=23. For d>0,d!=2 the same argument even gives W>=28, but no universal wall lower bound follows from this restricted geometry.

This proof does not delete teeth or infer monotonic illumination under attachment. It counts the entire physical room after the actual optical necessary conditions. Same-side positive gaps, source/target interiority and opposite overlaps all retain their original hypotheses.

## Residual cases and main-goal alignment

In the integer unitwidth/height2 comb model, a pair of distinct selected teeth has h>=2: h1 would make their height2 bands touch, which violates the positive-gap hypothesis. Every relative endpoint height is positive, so q>=1. Therefore any remaining actual dark same-seam pair at W<=21 must satisfy

q in{1,2}, OR h=2.

For core widths c>=3 the stronger accepted A39 already closes the entire class. For c2 the accepted five-family reduction plus pending optical joins is stronger. A47 supplies new uncapped positive coverage principally for c1, and narrows its unclassified geometry to actual endpoints within two units of a global end, or actual endpoint separation4. The q1/2,h2 classes are NOT asserted illuminated by A47. General taller/deeper teeth, diagonal walls and arbitrary canonical45 rooms remain open; the main objective is unfinished.
