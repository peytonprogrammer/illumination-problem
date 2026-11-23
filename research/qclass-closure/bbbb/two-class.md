# Can two candidate midpoint classes both fail?

The nine true BBBB rooms in D72 contain 747 distinct same-parity interior lattice pairs. All 747 have regular algebraic candidates in **all three** non-source classes. None tests the case of exactly two populated classes. D66 (dumb12) and D69 (the other eight) certify every pair in every primitive direction parity class, but that labels the direction, not necessarily the midpoint. For a displacement of m primitive steps, m is even; the midpoint has source parity when 4 divides m.

## An exact winding test

Fix two lifts of the endpoints in one open cylinder of primitive lattice direction v. Apply an integral unimodular change of coordinates taking v to a horizontal unit vector. In the cylinder strip take the displacement between the lifts to be (u,h), modulo the horizontal circumference C. The winding displacements are precisely (u+kC,h) for integers k. Every such segment is legal because its transverse coordinate stays between the endpoint heights in the open strip. The quantities u,h are even for same-parity endpoints, and C is even because a circuit returns to the same lift and therefore the same base parity. A unimodular change preserves both the even lattice and the lattice of multiples of four.

Consequently this cylinder and these lifts realize a non-source midpoint **if and only if at least one of u,h,C is nonzero modulo four**. Its complete set of midpoint classes is obtained from k=0,1 by halving the displacement and transforming back, modulo two. This is independent of the initial choice of longitudinal representative. In particular even arbitrarily many windings cannot repair a failure of this test in that cylinder.

## Audit of existing evidence

The checker computes ordered-sheet orbits once per source parity and checks the actual regular candidates incident to the marked pair. It then reads one saved D72 straight-path witness and one saved common-cylinder witness per pair. It checks both orientations of the saved straight leaf up to a forbidden corner or a full lap, allowing a further lap on a closed regular leaf. For the cylinder it reads transverse row distance, longitudinal offset and circumference from the saved direction's square permutations. It generates no new directions. The source lift and target sheet are fixed to those of each saved witness.

| Witnesses used | Pairs certified with a non-source midpoint |
| --- | ---: |
| Saved straight leaf | 569 |
| Saved common cylinder | 664 |
| Either | 687 |
| Neither | 60 |

Of the 747 pairs, 538 have one certified non-source class and 149 have two. For the latter 149, **every choice of two candidate classes contains a realized one**, by intersection of two two-element subsets of three classes. For the weaker claim that some candidate succeeds, 687 are certified. All 60 remaining pairs are already known to be lit.

For example DBw2, (1,1) to (13,3), has candidates in b,c,d. D72 stored the direction (2,11) for lighting and (6,13) for the common cylinder. In both saved configurations every midpoint has source parity. This rules out a proof that uses arbitrary witnesses of these two types. It leaves open what another choice of lifts or cylinder realizes. The room has four reflex corners.

**Proof gap.** The coincidence budget only counts which poles meet a marked component. It supplies no congruence condition on a realizing cylinder. The precise additional statement sufficient for the weak claim would be existence of some open common cylinder and compatible endpoint lifts for which the displacement coset is not contained in the lattice of multiples of four. Other legal paths could also establish the claim. Neither the universal implication nor a counterexample follows from the saved verdicts.

[Exact checker](two-class.py) · [per-room counts and first unresolved witnesses](two-class.txt) · [D72 cylinder data](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d72-cylinder-test/README.md)
