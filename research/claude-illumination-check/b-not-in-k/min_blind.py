"""Smallest (1,1)+(2,1)-blind completion of one closed mirror band (same approved enumeration, stage B).

Same SAT model as mirror_complete.py, plus a cap of N triangles. For N = N0, N0+STEP, ..., enumerate
every completion with at most N triangles (blocking each one), run (1,1) and (2,1) with the second
tracer, and stop at the first N that has a (2,1)-blind completion. Completions found at earlier caps
are blocked, so every completion is tested once.
"""
import json
import sys
import time
from fractions import Fraction as F

from pysat.card import CardEnc, EncType

R, BAND, N0, STEP, NMAX = (int(a) for a in sys.argv[1:6])
sys.argv = ["x", str(R), "1"]
exec(open("mirror_complete.py").read().split("if __name__")[0])


def main():
    b = json.load(open(f"mirror_bands_R{R}.json"))["bands"][BAND]
    pool = IDPool()
    x, cls = base_cnf(pool)
    s = Solver(name="cd15", bootstrap_with=cls)
    cen = lambda t: mb.key(F(sum(p[0] for p in t), 3), F(sum(p[1] for p in t), 3))
    for t in b["tris_in"]:
        s.add_clause([x[cen([tuple(q) for q in t])]])
    for t in b["tris_out"]:
        k = cen([tuple(q) for q in t])
        if k in BOXSET:
            s.add_clause([-x[k]])
    s.set_phases([-x[k] for k in BOX])
    tested, found, t0 = 0, [], time.time()
    for N in range(N0, NMAX + 1, STEP):
        sel = pool.id(("cap", N))
        for c in CardEnc.atmost(lits=[x[k] for k in BOX], bound=N, vpool=pool, encoding=EncType.seqcounter).clauses:
            s.add_clause(c + [-sel])
        while s.solve(assumptions=[sel]):
            m = set(l for l in s.get_model() if l > 0)
            room = {k for k in BOX if x[k] in m}
            cs = cuts(room, x)
            if cs:
                for c in cs:
                    s.add_clause(c)
                continue
            ok, info = independent_check(room)
            assert ok, info
            res, mism = run_room(room)
            assert mism == 0
            tested += 1
            if all(q == [0, 0] for q in res["(2, 1)"]):
                assert all(q == [0, 0] for q in res["(1, 1)"])
                found.append({"n_tri": len(room), "Q21": res["(2, 1)"], "Q11": res["(1, 1)"],
                              "tris": [mb.verts(k) for k in sorted(room)]})
            s.add_clause([-x[k] for k in room] + [x[k] for k in BOX if k not in room])
        print(f"cap N={N}: tested so far {tested}, blind found {len(found)}, {time.time() - t0:.0f}s", flush=True)
        if found:
            break
    json.dump({"R": R, "band": BAND, "tested": tested, "cap": N, "blind": found},
              open(f"min_blind_R{R}_b{BAND}.json", "w"))
    print("smallest blind sizes", sorted(f["n_tri"] for f in found))


if __name__ == "__main__":
    main()
