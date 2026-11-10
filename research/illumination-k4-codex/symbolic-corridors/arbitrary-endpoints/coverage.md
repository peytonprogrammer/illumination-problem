# Endpoint-extension coverage

6 November 2026. All new mathematical statements are parent proofs pending
independent review. Previous symmetric proof packet is unchanged.

- [done] Exact sufficient two-portal criterion retains actual endpoints,
  first passage through both open portals, matching velocity, finite smooth
  vertical contacts, and unrestricted positive dimensions.
- [done] Finite Fourier argument proves that failure of vertical-wall-only
  illumination forces one of finitely many depth relations with |m|,|n|≤32
  and |r|≤64. It does not identify every failed criterion with darkness.
- [done] Same construction gives sufficient one-portal criteria for outer/
  middle and portal/nonadjacent-outer placements. Same-band and adjacent-
  portal pairs connect directly.
- [done] A complementary chart proves all equal-depth, equal-horizontal-
  coordinate outer pairs illuminate; rational depths use modular arithmetic,
  irrational depths use an elementary rotation-density proof. One exceptional
  placement uses the previous three-contact middle path.
- [done] Exact fixed check verifies the binomial/threshold inequality and
  rational enclosures for one prescribed noncommensurable connection. Its
  two strict portal intervals certify 24 smooth vertical contacts by the
  folding theorem, without a trajectory search.
- [done] Prescribed modular formulas tested on 70 rational equal-coordinate
  instances, 336 actual wall contacts, at most 19 per tested connection.
  Their parameters are fixed q∈{3,4,5,7,8,11}, all reduced p/q in (0,1/2),
  and s/d∈{1/100,1/2,1,3/2,199/100}; the code chooses M by the theorem's
  rounding/inverse formula, never by testing candidate directions.
- [done] These rational controls check both portal derivatives, actual target,
  first actual boundary contacts, wall interiors, forward specular law,
  containment and interior marks. They use our prior packet's pure geometry
  helpers and are not an independent implementation or review.
- [waiting on Codex01a1a00f / Opus] Independent hand review requested on the
  shared board. No running worker or completed peer review is asserted.
- [in progress] General exceptional outer pairs, equal-depth pairs with
  independently varying horizontal coordinates, and one-portal resonances
  remain open. The arbitrary-endpoint theorem has NOT been completed.
- [in progress] Universal wall minimality remains unresolved. No numerical
  wall bound, generic-illumination theorem
  claim follows from this packet.
- [done] No discovery search, external message, worker, branch change,
  commit or frozen-input modification was performed.

Run parent arithmetic controls:
`python3 .context/illumination-k4-codex/symbolic-corridors/arbitrary-endpoints/check.py`.
This writes only this directory's check.json.

Next mathematical target: equal depths a=b but s≠t. Its orbit has a fixed
phase sum; the positive diagonal subcase is closed, but a complete covering
argument for independently varying s,t is not yet supplied. This is a
specific arithmetic/optical implication, not a request for more examples.
