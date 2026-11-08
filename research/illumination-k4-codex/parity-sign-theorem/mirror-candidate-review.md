# Independent verification: supplied leaf-flip counterexample

[done] Codex, 2026-11-02. ACCEPT the single supplied counterexample to the two-direction conjecture. The all-direction pocket-detection claim remains open.

## Frozen input and independent method

The input is the Section33 room with its leaf at A=(-4,-2) changed from the triangle toward (-5,-1) to the triangle toward (-3,-1). The other27 triangles are unchanged. The checker independently transcribes the room; it imports no peer tracer or geometry code. It compares its reconstructed maximal-wall polygon with room0 of peer `b-not-in-k/verify_min_blind_R3_b0.json`. Peer optical conclusions are not inputs to the trace.

Geometry checks pass:28 distinct unit canonical triangles, area14, one strictly simple boundary,25 maximal walls, no non-A integer points except physical boundary corners, S=(-4,0) and T=(0,0) strictly interior, and the specified literal pocket at (2,0),(1,1),(1,0) with fixed axial flanks. Its reconstructed polygon agrees with the supplied polygon.

## Complete coverage of the specified directions

The exact tracer intersects polygon walls with rational arithmetic, always takes the earliest positive intersection, rejects corner hits, checks segment containment, and requires exact return of position, velocity and unfolding frame. A finite safety cap causes rejection, never acceptance.

For each of the three supplied direction classes (1,1),(2,1),(3,2), include every D4 velocity pointing inward through D. Write z=(1+t,1-t) on D. For integer velocity v, det(z,v)=v_y-v_x+t(v_x+v_y). Since all unfolded physical vertices have integer coordinates, a corner event can occur only at t=j/|v_x+v_y|. The open intervals between these values have a common itinerary: no physical corner or wall endpoint can cross the unfolded strip. The checker traces one midpoint of EVERY such interval, not one arbitrary orbit. It records full contact lists in its JSON.

These intervals cover every nonsingular D-contact cylinder in the prescribed direction class. A cylinder avoiding D cannot have a moving H contact either: within a pocket excursion, H preserves horizontal velocity, so a trajectory cannot enter and leave through the same vertical portal using only H reflections. Every complete excursion with a moving-wall contact therefore hits D. Thus no loaded cylinder is omitted by the D-based coverage.

At every moving hit, the checker accumulates unfolding Q. It separately differentiates the forward affine reflection composition. At frame closure the two quantities are negatives of one another, as follows because each reflection reverses its normal displacement. They agree in this convention on every tested period; D-count parity also agrees. The checker initially compared these opposite conventions without the minus sign; that assertion was corrected before acceptance. A syntax error was also corrected; neither correction changes the frozen geometry or any traced path.

| Direction | D-strip representatives | Nonzero response | Periods in wall contacts |
|---|---:|---:|---|
| (1,1) |2|0|14 each|
| (2,1) |8|0|78 each|
| (3,2) |12|12|8 or104|

Representatives are not counts of distinct cylinders: several sample points can lie on the same cylinder, and initial-frame changes rotate response vectors. No independent claim about the peer's cylinder deduplication is needed here. Zero versus nonzero response is invariant under these frame changes.

## Consequence and scope

The one fixed room is blind to the pocket slide in BOTH (1,1) and (2,1), so the universal two-direction conjecture is false. It has nonzero response at (3,2), so it is not a counterexample to target1 (existence of some loaded periodic core). This supplies no actual S/T one-corner detecting event and makes no darkness or wall-minimality claim.

The further75 rooms, the31-triangle examples loading only at (4,3), the full enumeration, and the alternate-local-shape assertion were not independently audited here. They remain peer findings. Do not replace the refuted conjecture with a larger finite-direction conjecture on this verification's authority.

## Reproduction and independent handoff

Run:

    python3 -B .context/illumination-k4-codex/parity-sign-theorem/mirror-candidate-check.py

The script writes adjacent `mirror-candidate-check.json`; the saved stdout is `mirror-candidate-check.log`. JSON records source/checker hashes, all fixed-strip contact lists and responses. To preserve file ownership, a reviewer should copy the script to an owned directory and adjust ROOT and PEER paths explicitly before execution, or hand-audit the recorded certificates. No peer code imports, new rooms, direction discovery, or enumeration rerun is involved.
