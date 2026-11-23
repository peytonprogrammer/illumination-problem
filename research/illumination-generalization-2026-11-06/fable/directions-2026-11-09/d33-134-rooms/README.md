# d33: capped search for dark (1,3,4) rooms with at most 21 walls

Date: 2026-11-12. Approved by Daniel on 2026-11-12. Compute used: about 18 CPU minutes, under 200 KB of disk.

## Result

No dark room found. Every strictly simple room with two full stars, at most 8 extra tiles, and `W <= 21` is lit by an exact path for every interior A pair. That's 3,734 rooms, with no candidates. The checkpoint (clean-room) criterion never applied, because no room is clean.

## Method

- `scan.py` reuses `../d7-review/enum_rooms.py` (exhaustive Redelmeier enumeration) and `../d7-review/shoot.py` (exact tracer).
- It drops every T whose star shares a C-tip with St(S) (`T = 2c`). Proposition R2.1 lights those rooms. Only one T is dropped, but it carries about 99.9% of the rooms.
- For every interior A pair, the scan runs a plain image search at depth 0 to 4, then a midpoint search at depth 1 to 4.
- `fastshoot.py` prefilters candidates in floats. Every accepted path is rebuilt from its reflection word and confirmed by the exact `Tracer.trace`.

## Validation against d7-review (k <= 6)

- No-shared-tip rooms: 915, with the same W histogram as d7-review (17:2, 18:4, 19:6, 20:137, 21:54, 22:48, 23:664).
- On the 251 rooms with `W <= 22`, the exact-only run (`k6-exact.log`, 276 s) and the prefiltered run (`k6-fast.log`, 28 s) give identical depth tables. The 38-tile, 20-wall room again needs a midpoint path with 12 reflections.

## Counts, no shared C-tip (all W; searched rooms have W <= 21)

| k (max extra tiles) | Rooms | W = 17 | 18 | 19 | 20 | 21 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| <= 6 | 915 | 2 | 4 | 6 | 137 | 54 |
| <= 7 | 9,535 | 2 | 8 | 126 | 137 | 306 |
| <= 8 | 76,862 | 8 | 41 | 134 | 445 | 3,106 |

## Hardest lit rooms

- Five 40-tile, 21-wall rooms with k = 8 need midpoint-targeted paths with 13 or 14 reflections (`scan-k8-W21-21.json`, `hardest`).
- In total, 20 rooms with W = 21 need the midpoint search; none goes past midpoint depth 3.

## Astra's 17-wall test room

`astra_room.py` builds the room from `../d32-fold-minimum/astra-r2.md`. It's valid, strictly simple, and has 40 tiles and W = 17 (`astra_room.log`). The pair (S, T) is lit by an exact path with 2 reflections. Four enumerated k = 8 rooms match its corner sequence, and all four are lit.

## Not covered

- Rooms with more than 8 extra tiles.
- Triangles other than (1,3,4) and (1,4,5).

## Follow-up: (1,4,5) pi/10 triangle (n, b = 10, 4)

Requested by the coordinator after the first run. Astra's bound for this triangle is `W >= 21`, so only `W = 21` matters. Run: `python3 scan.py k 21 4 4 0 10 4`. Compute: about 11 CPU minutes, so about 29 minutes for d33 in total.

**Result.** No dark room exists with at most 10 extra tiles and `W <= 21`. Through k = 10, exactly two rooms have 21 walls, and none has fewer. Both have 46 tiles and k = 6. Both are lit by exact 3-reflection paths found at image depth 3. Neither room is clean, so the checkpoint criterion doesn't apply.

**Validation.**

- k <= 2 (`--nofilter`, all T kept): 551 rooms, W 18 to 22. Every star pair shares a C-tip, and every room is lit by a direct segment, as R2.1 predicts. The exact-only and prefiltered runs agree (`v2-10-4-*.log`).
- k <= 6, W <= 23, rooms with no shared C-tip: 12 rooms. The exact-only and prefiltered runs give identical depth tables (`v6-10-4-*.log`).

**Counts, no shared C-tip.**

| k (max extra tiles) | Rooms | W = 21 | W = 22 | W = 23 | Enumeration time |
| --- | ---: | ---: | ---: | ---: | ---: |
| <= 4 | 2 | 0 | 0 | 2 | < 1 s |
| <= 6 | 986 | 2 | 4 | 6 | < 1 s |
| <= 7 | 10,692 | 2 | 8 | 126 | 2 s |
| <= 9 | 604,630 | 2 | 42 | 244 | 85 s |
| <= 10 | 3,513,725 | 2 | 54 | 566 | 515 s |

Logs: `k9-10-4.log`, `k10-10-4.log`. Rooms: `scan-10-4-k10-W0-21.json`.

For k <= 7, the three smallest wall counts match the (1,3,4) counts shifted by 4 walls (2, 4 or 8, 6 or 126). Larger wall counts differ.

**Not covered.** k >= 11 would take an estimated 70 CPU minutes or more, which exceeds the cap.
