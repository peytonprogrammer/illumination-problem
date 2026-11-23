"""Staircase 4991 (`#.../##../###./####`), pair types (1, 7) and (7, 1).
Rooms with gaps (3, a, 6 - a, 3) x (3, c, 6 - c, 3): 25 rooms, 16 pairs each.
V1 = (3, 9), V3 = (9, 3), V2 = (3 + a, 3 + c). Checks the window family of
Lemma C+ with and without the condition on K."""
from rooms import Room, shoot
import newlemmas as nl
from newlemmas import Geo
nl.CHECK_K = False
tot = nbelow = bad = 0; hard = None
for a in range(1, 6):
    for c in range(1, 6):
        R = Room(4, 4, 4991, [3, a, 6 - a, 3], [3, c, 6 - c, 3]); g = Geo(R.cells, R.W, R.H)
        o = g.tr((0, 1, 0))
        for S in [(x, y) for x in (1, 2) for y in (10, 11)]:
            for T in [(x, y) for x in (10, 11) for y in (1, 2)]:
                A, B = g.tp((0, 1, 0), T), g.tp((0, 1, 0), S)
                cf = list(nl.Cperp_configs(o, A, B))
                assert cf
                below = a + c < 6
                sols = [nl.Cperp_solve(o, x, A, B, K=60) for x in cf]
                tot += 1; nbelow += below
                if not below: assert any(all(x) for x in sols)
                elif not any(any(x) for x in sols):
                    bad += 1
                    sh = shoot(R, S, T, 60)
                    if hard is None or len(sh[3]) > hard[4]: hard = (R.gx, R.gy, S, T, len(sh[3]), sh[:3])
print("instances", tot, "V2 strictly below the chord", nbelow, "of these, no valid window candidate for any sign pair", bad)
print("example with the most reflections in its shortest lighting direction:", hard)
