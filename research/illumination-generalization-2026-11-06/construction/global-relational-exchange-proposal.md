# B06: one relational feature and a falsifiable exchange lemma

Original allowance 2026-11-07 16:21:00–16:35:00 UTC, including setup and all restarts. No new orbit/room/ray census, coefficient fitting or workers. Universal goal and accounting unchanged.

## Domain and retained data

Take a connected full labelled four-copy orthogonal unfolding. Every genuine zero has its complete length-three cycle in C=v h v^-1 h^-1. S and T each retain all four actual regular cover points. Regular corner labels remain recorded but transparent. All N square slots remain; we never suppress degree or regular components. Distinct actual endpoints are required.

T:(h,v,L)->(h,v h^-1,L) and U:(h,v,L)->(h v^-1,v,L). C stays exactly fixed before common relabelling. A named-zero incidence array can be stored on the raw finite slot-labelled states without choosing a spanning-tree gauge: h,v are permutations of the same N slots, so at most (N!)^2 raw triples exist for fixed labels. This is a finiteness argument, NOT a degree bound, census, or physical realization theorem. All sectors used below are explicitly indexed by slots of the appropriate C cycle. No full transported real reflection is used or claimed to descend. The physical origin is required of the initial orbit only; no claim that all its shears are orthogonal rooms is used by the algebraic lemma.

## ONE feature: shared-zero incidence of the two endpoint colors

For a directional permutation p, EACH color A in {S,T}, and EACH sign e in {+,-}, trace p^e from each of its four marked points until the first genuine zero, opposite-color mark, or return to the starting actual point. Other same-color marks are allowed in between. Retain the complete endpoint order, terminal type and terminal slot. A regular periodic return is recorded explicitly and contributes zero to shared-zero incidence, not a fictitious corner hit.

Let n_(A,e,z) count marks of color A first stopping at slot z. Define

    F_p = sum_(e=+,-) sum_(zero cycles Z)
             sum_(z,z' in Z, z != z') n_(S,e,z) n_(T,e,z').

Thus F counts ordered pairs of actual S/T lifts incident on the SAME genuine zero through DIFFERENT incoming slots, separately for each orientation. This is relational: total corner counts, return counts and stopping lengths do not specify whether two colors reach the same zero or different zeros. The full incidence tensor is the retained evidence; F is its fixed, unweighted aggregate. Zero names and sector slots are carried explicitly; simultaneous relabelling leaves F unchanged.

Checkable lemma: same-slot cross-color first-zero incidence is impossible with the opposite-color stopping convention. If both rays first reached z without crossing an opposite mark or zero, their starts would lie in the same oriented zero-free predecessor interval of p. One start lies before the other, forcing its trace to hit the opposite mark first. Hence the omitted z=z' terms are identically zero. This is an ordered-mark argument, not an illumination assumption.

## Proposed exchange claim, fixed before testing

Use Phi=F_v and Psi=F_h. Put d=h v^-1. Since F_p includes both orientations, F_(p^-1)=F_p by a literal exchange of the + and - incidence records. Therefore the intended exact identities are

    F_v(Ts)=F_(v h^-1)(s)=F_(d^-1)(s)=F_d(s),
    F_h(Us)=F_d(s),
    D_F(s)=Delta_T Phi+Delta_U Psi=2F_d-F_h-F_v.

Candidate pointwise inequality on the refined orbit, for 1<=r<=9:

    H_pm(s) >= (9-r) * F_h(s)/(16N) + D_F(s),

where H_pm counts actual source starts reaching a target in either horizontal orientation before a genuine zero. The factor16N merely normalizes the incidence weight; it supplies no positive density or degree cutoff. No coefficient will be fitted. The r=9 boundary is deliberately included for calibration on known22. A positive theorem would additionally require a PROOF that sum_orbit F_h>0 for every dark qualifying physical orbit with 1<=r<=8. That positivity is NOT assumed proved. The r=0 case has no zero incidences at all and must be treated separately; the prescribed lit square tests this lack of force explicitly.

Success criterion: symbolic transition proof plus the proposed inequality AND nonzero orbit weight justified for all required low-reflex physical orbits. Failure criterion: one prescribed fixed control violates the candidate inequality, or a structural obstruction makes its claimed positive force unavailable. A failed candidate retires only this named feature/weight/potential combination, not all relational exchange methods.
