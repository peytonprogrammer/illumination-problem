# Recovered stronger optical foundation: regular corners can be removed on the full fibers

This is an existing accepted argument, recovered from parity-sign-theorem/pocket-detection.md section20 and independently checked here. It is not a new theorem or an off-orbit wall bound.

Let P be a canonical45 room and S,T distinct interior points. Let M be its unfolding, Z its genuine cone singularities, and Sigma the full actual-corner lift set, including regular lifts. Then

    physical S,T illuminate
    iff some geodesic between their full actual lift fibers avoids Sigma
    iff some geodesic between their full actual lift fibers avoids Z only.

The last equivalence is stronger than an assertion about one prescribed ordered lift pair. A zero-only connection can change endpoint sheet labels when regular-corner excursions are removed.

## Exact retracing argument

A regular corner lift corresponds to a physical angle pi/4 or pi/2 in this class. Straight continuation across that lift folds to reversal and retracing of the physical incoming path. Given a finite zero-avoiding segment between the actual fibers, fold it and let a>0 be the time of its first regular corner, L its total length. The path before a is an ordinary corner-free billiard path. Ordinary flow uniqueness gives gamma(a+u)=gamma(a-u) until time min(2a,L).

If a<L<2a, the physical target already occurs at time 2a-L<a, giving a legal connection. Equality L=2a would make T=S and is excluded. If L>2a, the path returns to the actual physical S at time2a. Discard that excursion and restart with the remaining segment from its then-current lift of S. It still has the same actual physical target and has fewer regular-corner contacts. There are finitely many such contacts on a finite zero-avoiding segment: the finite set of regular points has positive pairwise distances and flat neighborhoods, so distinct visits have a positive minimum travel separation. Iteration ends in a fully corner-avoiding physical connection, or finds an earlier target as above.

Consequently physical darkness requires ALL pairs of the two distinct actual fibers to be dark EVEN IN THE UNMARKED translation surface with only genuine zeros forbidden.

## Consequence for new strategies

The universal canonical-half-turn graph established with every corner in Sigma forbidden is a correct control in that marked model. It does not refute a degree or optical theorem stated with only genuine cone singularities forbidden: regular fixed midpoints may be allowed in that different model. Conversely, any use of a cone-only theorem on our physical problem must retain the FULL actual endpoint fibers; an arbitrary selected lift pair cannot have its label silently changed.

For orthogonal rooms, there are r genuine order2 zeros but r+4 regular convex corner lifts. In particular the six-wall L control has one cone zero and five regular fixed points. Its marked-surface reversal obstruction is not automatically an unmarked-surface zero-blocking obstruction. No claim is made here that these particular unmarked lift pairs always connect, only that the marked proof does not establish their failure.

This gives a useful admissible simplification for a genuine off-orbit optical proof: work with zero-only surface geodesics and preserve every actual lift orbit. It supplies no lower bound of nine reflex corners or22walls on its own.

Primary comparison: Wolecki v3 Remark2.2 records the same physical distinction for removable corner continuation. The source section's arbitrary-lift retracing proof is explicit for the present even-denominator angles. [Primary remark](https://arxiv.org/html/1905.09358v3).
