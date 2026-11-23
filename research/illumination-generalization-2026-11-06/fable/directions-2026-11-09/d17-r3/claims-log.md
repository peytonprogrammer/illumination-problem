# Claims log for d17-r3

Each claim is written here before its test runs. Times are local.

## T1 (rational points, r = 3). Written 2026-11-10 before any d17 run.

Population F: every 10-wall room that is q times a base room, where the base
room has integer gaps with sum at most B on each axis, for (q, B) in
{(2, 6), (3, 5), (4, 4)}. Every order type with r = 3 (70 types). The lattice
points of the scaled room are the points of the base room with denominator q.
All rooms fit a 16 x 16 box.

Claim T1: in every room of population F, every pair of distinct interior
lattice points whose position types are in the open list of `cert_r3.json` is
lit. Decider: `d15-small-r/verify2` shooting, primitive directions with
|u| + |v| <= 40, then <= 400. This is a conjecture test, not a lemma test.
If a pair is undecided, the run stops and the pair goes to a second decider.
