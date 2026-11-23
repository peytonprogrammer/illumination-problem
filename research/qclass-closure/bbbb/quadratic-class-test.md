# Failure parity is not a quadratic refinement, even in BBBB

For fixed same-parity interior marks S,T let F(v)=1 exactly when no legal shot has primitive direction v modulo two. All slopes and all physical lift choices are included. A quadratic refinement of the specified symplectic form would satisfy

    F(1,0) + F(0,1) + F(1,1) = 1    in F₂.

This is necessary and sufficient on the three nonzero vectors, extending by F(0)=0. All three classes can be lit in a BBBB room. Thus the proposed odd-failure dichotomy is false, and any correction to this identity that vanishes on BBBB is impossible.

## Three short shots in a 12-wall room

Use the named DB55 room with left chamber [0,5]², connecting corridor [5,8]×[2,3], and right chamber [8,13]×[0,5]. It has four reflex corners, and d146 checked all four canonical equivalence relations are universal. Take S=(1,1), T=(3,1). Reflecting target coordinates in the bottom and left walls gives the following paths entirely in the left chamber. [DB55 factor check](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d146-review-exdescent/review.md)

| Developed target | Wall contacts in order | Primitive direction | Class |
|---|---|---|---|
| (3,1) | none | (1,0) | (1,0) |
| (3,−1) | (2,0) | (1,−1) | (1,1) |
| (−3,−1) | (0,1/2), (1,0) | (−2,−1) | (0,1) |

For the last path the developed segment is (1−4t,1−2t). Its two wall times are 1/4 and 1/2, so the shot misses the corner shared by the walls. The three paths settle F=(0,0,0) without any nonexistence check. Independently, all 574 same-parity pairs in the seven-unit cross have this same failure vector. [d147, checks 5–6](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d147-review-crossarcs/review.md)

## A defect determined by the corner-only site also fails within cov4181

If one defines the unique defect bit by δ=1+ΣF(v), DB55 above requires δ=1. There is also a stronger test of whether δ depends on corner data alone. Hold cov4181 and even the source S=(2,3) fixed. Both targets below are interior and have the same parity as S. The absolute clean site is (1,0), hence the relative diagonal class fails for both targets. D66's exact saved orbit log counts ten pairs in this room and exactly one additional room-pair/class failure at a B site. D144 independently identifies that unique failure. [d66 saved verdicts](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d66-pair-level/pair_level.log) · [d144 independent identification](../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d144-review-dyadic/review.md)

| Target | Failing primitive classes | δ |
|---|---|---:|
| (4,3) | (1,1), (0,1) | 1 |
| (4,1) | (1,1) only | 0 |

Thus the defect changes while the room, its corner-only site, the source, and both endpoint parities stay fixed. Writing an arbitrary pair-dependent bit always fits the three values and, without an independent geometric formula, has no predictive content. The calculation concerns the failure indicator after taking the union over legal shots. It leaves room for path-dependent dyadic invariants on individual shots.

## What remains of the intended implication

The weaker redundancy statement would permit **zero, one, or three** failed classes in BBBB. It excludes only the one-lit-class case. In algebraic terms let L be the set of realized primitive parities and let H be its linear span in F₂². Rank zero means total darkness, rank one means exactly one lit class, and rank two gives at least two lit classes. This formulation permits taking a linear span: rank two guarantees that two of the original witnesses were independent. It never requires their sum to be realized by a shot. Ruling out rank one and ruling out rank zero are separate claims.

D68 Lemma B gives the local criterion for a corner-only site. The equality n=fₓ+3rₓ counts its fiber once such a site is established. Neither result implies that absence of all legal shots forces such a site. The proposed dichotomy has failed its BBBB control, so it supplies no reduction of the triple-failure problem. [Fiber count and its direction of implication](clean-site-cost.md)

**Next discriminating question.** For a lit BBBB pair, can a nonzero linear functional annihilate the primitive parity of every legal shot? That is precisely the rank-one obstruction. A geometric way to attack it is to begin with a witnessed class and find a second legal chord on which its annihilator takes value one. The cylinder winding criterion already specifies when a single cylinder supplies that chord. [Winding criterion](cyclic-separation.md)
