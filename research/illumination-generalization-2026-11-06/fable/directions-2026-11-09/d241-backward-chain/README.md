# d241: backward chain from the goal (2026-11-28 00:13 HST)

Advances: L1 (scoping only). No lemma is claimed. Daniel asked: think of new ideas, work backward, state what must be true and what happens if not.

## The chain

1. With A′ reviewed (d240), a counterexample to the W ≤ 20 goal is a dark same-class interior pair with **no** fold-parity certificate. So the goal equals "no certificate-free dark pair at W ≤ 20".
2. **Must be true if certificates are the only mechanism:** a dark room has normalized area ≤ W − 4. My extension of the cert-a count to every r (unreviewed): k = 1 gives 3n ≤ (r + 4) + 3r; k, m ≥ 2 gives kz ≤ r and m ≤ 4(z + 1)/3, so km ≤ 2r. By Pick's formula the room then has at most r − 1 interior lattice points: reflex corners outnumber interior points.
3. **If not:** some dark room has area above W − 4. That is a second mechanism of darkness. Existing data show none: W ≤ 20 at areas 17–21 (d9, d205, d206), W = 22 at areas 19–20 (d9), slit and pinched rooms (d55), W = 22–26 immersed discs to area 16 (d237, inside the bound, so no test).
4. **Must be true of any proof:** it contains an 8-versus-9 step (PROGRAM.md, 2026-11-23 tally). The only known one is the count on a fold. So a proof needs "dark implies certificate" (B′).
5. **Calibration (from memory, a guess until checked):** B′ asks that every SL(2,Z) orbit of a marked pillowcase cover without a certificate contains a connected configuration. Orbit classification for square-tiled surfaces is solved only in the smallest genus-2 stratum. A room with r reflex corners lives in a stratum of dimension 2r + 2.

## Ideas generated and where they already live

| Idea | Earlier note | State there |
|---|---|---|
| Two marks in one closed cylinder are lit; use it as the unit of proof | d87 every-direction | 12-wall crosses fail the cylinder tests in every rational direction |
| Unbounded dark rooms force a continuous dark family (EMM isolation), then Apisa–Wright | d59, d115, d116, d117 | Sound, non-effective; "effective bounds restate the target"; crux was a wholly dark component |
| Harvest dark rooms at higher W and test for certificates | d55, d237 | Done to area 16; one strictly simple dark pair |
| Braid orbit equals the whole marked Nielsen class when the group is primitive | d220 | Needs the pure-braid realization lemma (same gap) |
| Short lattice walks | bbbb/cert-b-short-steps.md | Refuted at six walls |

All five map to closed routes. I checked RESULTS.md by concept before writing this, per the d239 lesson.

## What is left

- The area law in step 2 as a stated corollary (Astra to confirm; her note).
- The provenance gap d240 found: d9's room list is independently checked only through area 12. A recount of areas 13–16 needs Daniel's approval (census).
- No route to B′ with named leverage.
