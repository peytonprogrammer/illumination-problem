"""Search mirror-band completions for a room blind in all seven short directions (Daniel approved 2026-11-02).

Fixed in advance. Bands: the 25 R=4 bands that band_space_R4.json marks open (escaped, or at least two
full-fan slots), plus R=3 band 0 (Section 33's band). Completions: the SAT model of mirror_complete.py with a triangle cap rising
from 20 to 40 in steps of 4, every completion enumerated once, at most 3000 per band, 20 minutes per
band. Each completion runs the seven D4 classes with |theta|^2 <= 25, each core checked by the second
tracer of mirror_complete.py, and stops at the first loaded class.
A room blind in all seven then runs every primitive class (p,q), 0 <= q <= p, with p^2+q^2 <= 100.
"""
import json
import math
import sys
import time
from fractions import Fraction as F

from pysat.card import CardEnc, EncType

R, BAND = int(sys.argv[1]), int(sys.argv[2])
CAPS, MAXC, TLIM = range(20, 41, 4), 3000, 1200
SHORT = [(1, 1), (2, 1), (3, 2), (4, 3), (3, 1), (4, 1), (1, 0)]
LONG = sorted({(p, q) for p in range(1, 11) for q in range(0, p + 1)
               if math.gcd(p, q) == 1 and p * p + q * q <= 100}, key=lambda t: (t[0] ** 2 + t[1] ** 2, t))
sys.argv = ["x", str(R), "1"]
exec(open("mirror_complete.py").read().split("if __name__")[0])


def loads(room, dirs, stop_at_load):
    tris = [mb.verts(k) for k in sorted(room)]
    cl.TRIANGLES = tris
    cl.ROOM = set(room)
    cnt = Counter(tuple(sorted((t[a], t[(a + 1) % 3]))) for t in tris for a in range(3))
    walls = [e for e, n in cnt.items() if n == 1]
    out = {}
    for th in dirs:
        d = cl.run_direction(th)
        assert d["strip_weighted_sum"] == [0, 0]
        for c in d["cores"]:
            x0 = F(c["start_x_on_D"])
            got = second_tracer(room, walls, (x0, 2 - x0), tuple(c["start_velocity"]), th)
            assert got == (c["wall_hits"], c["D_hits"], c["H_hits"], c["Q"]), "tracers disagree"
        out[str(th)] = [c["Q"] for c in d["cores"]]
        if stop_at_load and any(q != [0, 0] for q in out[str(th)]):
            break
    return out


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
    tested, first_loaded, allblind, t0, stop = 0, {}, [], time.time(), ""
    for N in CAPS:
        sel = pool.id(("cap", N))
        for c in CardEnc.atmost(lits=[x[k] for k in BOX], bound=N, vpool=pool, encoding=EncType.seqcounter).clauses:
            s.add_clause(c + [-sel])
        while s.solve(assumptions=[sel]):
            if tested >= MAXC or time.time() - t0 > TLIM:
                stop = "limit"
                break
            m = set(l for l in s.get_model() if l > 0)
            room = {k for k in BOX if x[k] in m}
            cs = cuts(room, x)
            if cs:
                for c in cs:
                    s.add_clause(c)
                continue
            ok, info = independent_check(room)
            assert ok, info
            tested += 1
            short = loads(room, SHORT, True)
            assert all(q == [0, 0] for q in short["(1, 1)"]), "band is not a mirror"
            hit = next((k for k, qs in short.items() if any(q != [0, 0] for q in qs)), None)
            first_loaded[hit] = first_loaded.get(hit, 0) + 1
            if hit is None:
                allblind.append({"n_tri": len(room), "tris": [mb.verts(k) for k in sorted(room)],
                                 "long": loads(room, LONG, False)})
                print("ALL SEVEN BLIND", len(room), flush=True)
            s.add_clause([-x[k] for k in room] + [x[k] for k in BOX if k not in room])
        if stop:
            break
    res = {"R": R, "band": BAND, "tested": tested, "last_cap": N, "stop": stop or "caps done",
           "seconds": round(time.time() - t0), "first_loaded": first_loaded, "allblind": allblind}
    json.dump(res, open(f"allblind/R{R}_b{BAND}.json", "w"))
    print(f"R={R} band={BAND} tested={tested} cap={N} stop={res['stop']} first_loaded={first_loaded} "
          f"allblind={len(allblind)}", flush=True)


if __name__ == "__main__":
    main()
