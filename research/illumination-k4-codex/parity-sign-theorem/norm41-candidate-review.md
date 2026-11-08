# Independent verification of the supplied norm41 room

[done] Codex, 2026-11-02. ACCEPT the fixed candidate from peer `b-not-in-k/allblind/verify_allblind.json`, band31 completion1. No peer tracer or search implementation was imported, and no new room or detecting direction was sought.

## Geometry

The supplied maximal-wall polygon is reconstructed independently as40 canonical unit triangles by exact centroid containment. The resulting union has one strictly simple polygon boundary; after merging smooth points its boundary edges equal the supplied polygon. Area20 agrees with the40 half-unit triangles. It has37 maximal walls, and every non-A integer point in the closed room is a physical boundary corner. The actual marks S=(0,2) and T=(2,6) are strictly interior. The literal pocket and its fixed axial flanks at (2,0),(1,1),(1,0) pass the same geometric checks as the earlier frozen-room audit.

The input triangle list is frozen in `norm41-candidate-check.py`; peer polygon and file hashes are retained in the receipt. Reconstructing this one polygon is not an enumeration of rooms.

## Exact fixed-direction coverage

The independent rational polygon tracer from the earlier one-leaf audit was adapted to this fixed geometry. It checks earliest positive wall contacts, open-wall rather than corner hits, segment containment, and exact position/velocity/frame closure. Two response calculations agree with their stated opposite forward/unfolding signs. D-hit parity agrees on every representative.

The list of primitive D4 classes through squared norm41 is checked independently using gcd(p,q)=1 and 0<=q<=p. It contains exactly the twelve classes below. This arithmetic check establishes that no shorter primitive class was accidentally omitted.

Every inward D velocity and every interval between integer-phase breakpoints is represented. The completeness argument is the same as `mirror-candidate-review.md`: z=(1+t,1-t) has phase det(z,v)=v_y-v_x+t(v_x+v_y); physical vertices unfold to integer points. No corner can change the itinerary within an interval. Periodic trajectories avoiding D cannot have moving H contacts without an intervening D contact, because H alone preserves horizontal velocity. Thus zero response on all the listed D strips establishes blindness for each full direction class, not just for a sampled orbit.

| Direction | Squared norm | D-strip representatives | Nonzero response | Wall contacts per period |
|---|---:|---:|---:|---|
| (1,0) |1|2|0|4|
| (1,1) |2|2|0|34|
| (2,1) |5|8|0|108|
| (3,1) |10|12|0|96|
| (3,2) |13|12|0|154|
| (4,1) |17|16|0|142|
| (4,3) |25|16|0|230|
| (5,1) |26|20|0|244|
| (5,2) |29|20|0|70 or132|
| (5,3) |34|20|0|288|
| (6,1) |37|24|0|182|
| (5,4) |41|20|20|114 or212|

The first152 strip representatives have Q=0. At (5,4), all20 have nonzero Q, with values (plus or minus2,0) or (0,plus or minus2) in the representative's initial frame. These counts are strip representatives, not distinct cylinders. Full contact certificates are saved in the JSON; no cylinder-deduplication claim is needed for this verdict.

## What is established

For this one valid raw pocket room, the minimum squared norm of a primitive detecting direction is41. Any uniform norm cutoff for this room class must therefore be at least41. This refutes every proposed cutoff below41, including the earlier seven-class list through25.

This does NOT exclude an arbitrary larger fixed finite direction set, establish unbounded first-detection norm, prove universal periodic-core detection, or supply a detecting one-corner event between S,T. It makes no darkness or minimal-wall claim. The other55 peer examples and the reported15,798-room census were not independently replayed.

## Reproduction and stop

    python3 -B .context/illumination-k4-codex/parity-sign-theorem/norm41-candidate-check.py

Outputs: adjacent `norm41-candidate-check.json`; saved stdout: `norm41-candidate-check.log`. The JSON stores all contact lists and source/checker hashes. A peer reviewer should use an owned script copy, set ROOT/PEER paths explicitly, and avoid rewriting Codex outputs.

The authorized fixed-room verification is complete. No larger search or additional direction list is recommended on this evidence alone. Independent review of the separate leaf-flip explanation remains with Opus.
