"""Compare the two tracers of rv.py (Fraction-based wall-by-wall tracer and
the division-free integer tracer) on every candidate path of random pairs,
including invalid ones. Usage: python3 -B tracer_compare.py rooms seed"""
import sys, random, time
sys.dont_write_bytecode = True
import attack, rv
from collections import Counter
types = attack.load_types()
rng = random.Random(int(sys.argv[2]))
agree = Counter(); dis = []
log = []
def both(room, S, D, T, maxref=None):
    a = rv.trace(room, S, D, T, 300)
    b = rv.trace_fast(room, S, D, T, 300)
    agree[a[0]] += 1
    if a != b: dis.append((a, b, S, D, T))
    return a
rv.TRACER[0] = both
t0 = time.time()
for rno in range(int(sys.argv[1])):
    ot = rng.choice(types)
    R, Q, style, D = attack.make_room(ot, rng)
    for (label, S, T) in attack.gen_pairs(R, Q, rng, 30):
        for inst in rv.all_instances(R, S, T, rng):
            rv.evaluate(R, inst, rng)
        # also random shots that mostly miss or hit vertices
        V = R.vertices()
        v = rng.choice(V)
        both(R, S, (v[0] - S[0] + (v[0] - S[0]), v[1] - S[1] + (v[1] - S[1])), T)
        both(R, S, ((T[0] - S[0]) * 3, (T[1] - S[1]) * 5), T)
print("statuses", dict(agree), "disagreements", len(dis), f"{time.time()-t0:.0f}s")
for d in dis[:5]: print(d)
