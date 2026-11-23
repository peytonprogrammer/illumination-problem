# Resonant cov279 stretches

**Partial theorem.** For every q≥6 divisible by three, every same-parity interior lattice pair is lit except possibly pairs at heights 1 and 5. In particular the narrow first opening, where the old two-band gcd equals its full width, can be crossed for every pair at heights 1 and 3. The proof changes the number of bottom-chamber traversals.

Set U=2q, L=U−3 and V=U+3. The bottom and next bands have widths U and V. The mouth at y=2 is (L,U). Write X,Y for the abscissas at heights 1,3. On the simple upward route the possible positive-sheet crossing positions form (X+Y)/2+3ℤ. If this misses the open mouth, flip either endpoint image. Every run origin here is divisible by three, so the flip changes the translate modulo three by the corresponding abscissa up to sign. Hence only X,Y both divisible by three need repair. Since they have the same parity they are both zero or both three modulo six.

Use a virtual terminal abscissa B and a small signed developed horizontal travel s per unit of vertical travel. Unfold only the vertical side walls for the following description.

- If X,Y are even, start at X, set B=U and s=3/2. Take D=(B−X)/s, a positive multiple of four.
- If X,Y are odd, start at the reflected image 2U−X, set B=L and s=−3/2. Now D=(B−(2U−X))/s is again a positive multiple of four.

Launch downward in physical y. In the bottom band of height two the visits to y=2 are at times 3,7,…,D−1. The last visit is at U−3/2 in both cases. Earlier visits are spaced by six in developed x. In the even case they lie below L and above zero. In the odd case they lie above U+3 and below 2U, so their folded positions are below L. They reflect from solid ceiling. In the odd case the crossing of x=U occurs two time units before the virtual target, at physical height one. All bottom-wall contacts are smooth: the even leg stays between 0 and U; on the odd leg the only interior vertical mirror line crossed is U and the crossing has just been checked. The final mouth is on the positive folding sheet in both cases.

Replace s by s+2Uk. Every integer-time event in the bottom band keeps its position and sheet. Extra side reflections between events are smooth. The last unit of vertical travel in the second band now ends at developed B+2Uk modulo 2V. Choose k solving B+2Uk≡Y modulo 2V. It exists because gcd(2U,2V)=6 and B≡Y modulo six. This proves the repair even when the mark starts immediately below a lip.

For (2,4) the two-band gcd divides nine and the overlap width 2q exceeds nine. For (3,5) the signed two-band proof and its exceptional cap reflection in thin-room.md require no coprimality. Equal-height pairs have direct chords.

**Four-band obstruction.** Every physical vertical wall now has abscissa divisible by three. All unfolded source and target abscissas are consequently ±X and ±Y modulo six. On the reviewed bottom-cap route the total vertical travel is six and the first mouth is reached halfway, after three. If X,Y are both divisible by three and of the same parity, both signed endpoint images have the same residue modulo six. Their average is divisible by three. Folding preserves divisibility by three, but the open interval (2q−3,2q) contains no multiple of three. This rules out the entire route on all sheets, for every possible slope and choice of absorbing band. It does not rule out a different route. A repair must change the halfway encounter or the order of mouth visits. The two-band repair above controls a variable first-hit time; it does not place the two subsequent upper crossings for height five.

Exact arithmetic replay at q=6 and 30 checked all 5 and 181 same-parity (1,3) placements, respectively, with both abscissas divisible by three. It checked every prescribed floor and ceiling contact, the first open mouth, and the final congruence.
