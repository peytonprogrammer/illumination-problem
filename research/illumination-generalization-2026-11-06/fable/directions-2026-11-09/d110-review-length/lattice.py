"""D110 claim 1, w=1 corollary: all 180 cross-chamber interior lattice pairs of DBas at L=K,
by the note's construction, each traced exactly. Also lists interior lattice sites by region."""
from fractions import Fraction as F
from geom import room
from tail import constants, run

R0 = room('DBas', 1); c = constants(R0); K = c[3]; R = room('DBas', K)
left = [(F(x), F(y)) for x in range(1, 5) for y in range(1, 4)]
right = [(F(x), F(y)) for x in range(K + 6, K + 9) for y in range(0, 5)]
# no lattice site in the open corridor or open mouths: y in (1,2) has no integer
print(f"DBas L=K={K}: interior lattice sites left={len(left)} right={len(right)} corridor/mouths=0 (open y-range (1,2))")
n = 0
for S in left:
    for T in right:
        r = run('DBas', K, S, T, c)
        assert 'traced OK' in r
        n += 1
print(f"cross-chamber lattice pairs lit by the construction: {n}/180; same-chamber pairs: direct segments in convex rectangles")
