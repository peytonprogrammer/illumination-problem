# CE08 independent final review

Decision: ACCEPT all six pinned claims at their stated sufficient scope. All56 source pins and the request hash match before/after independent replay. Read the complete candidate, hand proof, arithmetic checker and evidence; author code was not executed. No unresolved mathematical corrections.

## Claim-by-claim decisions

1. **ACCEPT — target-compatible lattice in one strict cap window.** For h<=u<H, no source fold occurs. At fixed integer m the exact q interval has length KD/C. Its target-compatible lattice is Nm+gZ, where Lambda=lcm(N,K), g=gcd(Lambda*d2,L). An open interval longer than2g contains two consecutive points of this lattice, including integral endpoint cases. Taking m large ensures nonnegative q and positive slopes. K is the integer right width in units e; the physical window has width2Ke. The author's control D uses (38,42) for the physical X window, not the q interval; direct substitution confirms its selected q41,42 are inside the correct pullback.

2. **ACCEPT — actual right-corner exclusion.** At fixed m the Y phase increases per q by2e(C+g1)/D. The corner event modulo2Ke is empty or one residue class of exact period KD/gcd(C+g1,KD)>K. Since g|K, the two indices separated by g cannot both be corners. This proof uses actual period2Ke and is stronger than the unit-period surrogate in the reviewer's earlier prerequisite. Both signs of centered residuals, including zero, are handled; zero is a smooth outer-wall reflection.

3. **ACCEPT — full actual target congruence.** The exact unfolded J is q-Nm-Kk. Selecting q=Nm modg and g|K implies J divisibleg for either surviving k. The reduced congruence has coefficient Lambda*d2/g invertible modulo L/g. The shift2eLambda*p preserves literal signed cap/right residuals with integral changes of m,k. There is no source band to preserve, so Lambda need not include P. The resulting phase is z modulo2Le, which folds to actual t, not merely a projected residue. The prescribed g2 control has initialJ=-4 and finalJ128; the competing q1 has strict portals but oddJ1 and cannot be corrected on this period orbit.

4. **ACCEPT — original physical ray, seam, roof and first target.** Independent position/derivative checks agree with the accepted CE04 upper-cap charts. Every open-band mirror is an original wall, both reflex portals have strict signed residuals, and all true corners are excluded. At u=h the actual source lies on a regular passage; no source-band condition is introduced. A roof endpoint would force coincident ascending/descending h mouths, impossible since s<a<w. For u>h a singular final roof gives the exact same-S downward suffix using triangular-wave symmetry. One final direction governs all retained legs. Its target height is reached on descent only at the final time, so it reaches first actual T. Independent replay checks the original polygon's earliest contacts and specular velocities.

5. **ACCEPT — whole cap-only native family.** With even b,c=b+1,h=b+2 every native terminal source has even u>b and hence u>=h. Odd N, K<L=2^j and odd d2 give g=2^v2(K). The odd part of K>=3 makes K>=3g and KD/C>K>2g. Source P may have either parity, and H is arbitrary. All stated pairs satisfy the new lemma; the already accepted TR01/TR05 exact placement join and reversal cover the complement. No cap-gcd, prime-N or depth condition is inherited unnecessarily.

6. **ACCEPT — second family with lower sources.** Odd P,K,N,c, K>=3, L a power of two and gcd(2P*epsilon,N)<K give CE04 for every below-h native source. At/above-h sources use CE08 with g1 and KD/C>K>=3. Every target d2 is odd. TR01/TR05 complete the join. Composite N and arbitrary epsilon are permitted subject only to the stated lower-source gcd.

## Independent reproducible evidence and limits

Run `python3 .context/illumination-generalization-2026-11-06/review/three-reflex-coprime-upper-window-final-check.py`.

Own7 prescribed actual rays pass: 718 reflections and7250 finite-wall/leg guards. All four author hand slopes/J values are independently reproduced. Added controls cover an exactly integral open interval endpoint, first q bad/next q good, and the exact singular-roof same-S suffix. The discarded q42 in author D independently hits true corner(w,c)=(6,3); the wrong-J control independently shows why strict portals alone are insufficient. These are prescribed checks, not discovery, an exhaustive room census or evidence for quantifiers by sampling.

The earlier review prerequisite and four-ray check remain preserved as a narrower sufficient result before the author packet existed. This final receipt supersedes its pending-packet flag without changing those historical files.

The theorem remains a restricted ordered-spiral family. General lower-source cap/target selection, arbitrary target arithmetic, other W10 forms/types and r4..8 remain open. The full native goal is active and incomplete. No dark counterexample or new wall bound is claimed.

Next substantive extension: reviewer-originated LC01 first-crossing proof in `three-reflex-coprime-forward-crossing-proof.md`, disjoint from CE08. It claims all lower sources with K>=4 and the existing target gcd, and awaits independent author review. CE08 plus LC01 would remove every cap-depth/cap-gcd restriction for odd P,N,K>=5, L a power of two and c odd; this combined corollary is not yet reciprocally accepted.
