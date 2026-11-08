"""Extend Section 12 to rooms of 41-60 triangles (Daniel approved 2026-11-02: "ok go").

Fixed in advance. Bands: the same 26 as allblind_search.py. Size windows 41-44, 45-48, 49-52, 53-56,
57-60, each enumerated separately with at most 500 completions and 4 minutes, so the per-band limit is
2,500 completions and 20 minutes. Tests as in allblind_search.py: the seven short classes, stopping at
the first loaded class, then the 25 classes with |theta|^2 <= 100 for a room blind in all seven.
A room blind in all 25 is recorded only; running further classes on it needs Daniel's approval.
"""
exec(open("allblind_search.py").read().split("def main")[0])

WINDOWS, MAXW, TLIMW = [(n - 3, n) for n in range(44, 61, 4)], 500, 240


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
    lits = [x[k] for k in BOX]
    windows, first_loaded, allblind, t_all = {}, {}, [], time.time()
    for lo, hi in WINDOWS:
        sel = pool.id(("win", hi))
        for enc in (CardEnc.atmost(lits=lits, bound=hi, vpool=pool, encoding=EncType.seqcounter),
                    CardEnc.atleast(lits=lits, bound=lo, vpool=pool, encoding=EncType.seqcounter)):
            for c in enc.clauses:
                s.add_clause(c + [-sel])
        tested, t0, stop = 0, time.time(), "exhausted"
        while s.solve(assumptions=[sel]):
            if tested >= MAXW or time.time() - t0 > TLIMW:
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
            assert lo <= len(room) <= hi
            tested += 1
            short = loads(room, SHORT, True)
            assert all(q == [0, 0] for q in short["(1, 1)"]), "band is not a mirror"
            hit = next((k for k, qs in short.items() if any(q != [0, 0] for q in qs)), None)
            first_loaded[str(hit)] = first_loaded.get(str(hit), 0) + 1
            if hit is None:
                long = loads(room, LONG, False)
                first = next((k for k in map(str, LONG) if any(q != [0, 0] for q in long[k])), None)
                allblind.append({"n_tri": len(room), "first_long": first,
                                 "tris": [mb.verts(k) for k in sorted(room)], "long": long})
                print("ALL SEVEN BLIND", len(room), "first long load", first, flush=True)
                if first is None:
                    print("BLIND THROUGH |theta|^2 <= 100", flush=True)
            s.add_clause([-x[k] for k in room] + [x[k] for k in BOX if k not in room])
        windows[f"{lo}-{hi}"] = {"tested": tested, "stop": stop, "seconds": round(time.time() - t0)}
        print(f"window {lo}-{hi}: {windows[f'{lo}-{hi}']}", flush=True)
    res = {"R": R, "band": BAND, "windows": windows, "seconds": round(time.time() - t_all),
           "first_loaded": first_loaded, "allblind": allblind}
    json.dump(res, open(f"allblind60/R{R}_b{BAND}.json", "w"))
    print(f"R={R} band={BAND} tested={sum(w['tested'] for w in windows.values())} "
          f"first_loaded={first_loaded} allblind={len(allblind)} "
          f"blind_through_100={sum(a['first_long'] is None for a in allblind)}", flush=True)


if __name__ == "__main__":
    main()
