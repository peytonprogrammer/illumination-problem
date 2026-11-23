"""Tests of Claim H and Claim C+ on population G. Usage:
  test_lemmas.py gen            -> runs/g_rooms.txt
  test_lemmas.py run W limit r  -> runs/g_out{W}_{r}.json (worker W of 3, first `limit` rooms with r reflex corners)"""
import sys, json, random, time
from rooms import Room, shoot
from newlemmas import *
SEED, BOX = 20261110, 16
NUM = {1: 200, 2: 800, 3: 3000, 4: 3000}
D15 = "../d15-small-r/"


def gen():
    rng = random.Random(SEED)
    def gaps(n):
        c = [0] + sorted(rng.sample(range(1, BOX + 1), n))
        return [c[i + 1] - c[i] for i in range(n)]
    with open("runs/g_rooms.txt", "w") as f:
        for r in (1, 2, 3, 4):
            types = [tuple(map(int, l.split())) for l in open(f"{D15}types_r{r}.txt")]
            for _ in range(NUM[r]):
                nx, ny, W, mask = rng.choice(types)
                f.write(f"{r} {nx} {ny} {mask} {' '.join(map(str, gaps(nx)))} | {' '.join(map(str, gaps(ny)))}\n")


def open_lists():
    out = {}
    for r in (3, 4):
        for row in json.load(open(f"{D15}cert_r{r}.json")):
            out[(row["nx"], row["ny"], row["mask"])] = {frozenset((tuple(a), tuple(b))) for a, b in row["uncovered"]}
    return out


def run(w, limit, only=0):
    opens = open_lists()
    st = dict(rooms=0, pairs=0, H_cfg=0, H_sign_sol=0, H_trace_ok=0, H_cfg_nosol_res=0,
              Cperp_cfg=0, Cperp_new=0, Cpar_cfg=0, Cpar_new=0, C_sign_ok=0,
              open3=0, open3_H=0, open3_C=0, open3_any=0, open4=0, open4_H=0, open4_C=0, open4_any=0,
              maxlen=0, fail=[])
    t0 = time.time()
    bytype = {}
    lines = [l for l in open("runs/g_rooms.txt")]
    for idx, l in enumerate(lines):
        a, b = l.split("|")
        r, nx, ny, mask, *gx = map(int, a.split())
        if idx % 3 != w or (only and r != only): continue
        if limit and st["rooms"] >= limit: break
        gy = list(map(int, b.split()))
        R = Room(nx, ny, mask, gx, gy)
        g = Geo(R.cells, R.W, R.H)
        pts = R.interior_points()
        op = opens.get((nx, ny, mask), set())
        st["rooms"] += 1
        st["pairs"] += len(pts) * (len(pts) - 1) // 2
        covH, covC = set(), set()
        for sym in SYMS:
            o = g.tr(sym)
            tp = [g.tp(sym, P) for P in pts]
            for i, A in enumerate(tp):
                for j, B in enumerate(tp):
                    if i == j or A[0] > B[0]: continue    # all three canonical frames need this
                    key = (min(i, j), max(i, j))
                    for cfg in H_configs(o, A, B):
                        st["H_cfg"] += 1
                        sol = H_solve(cfg, A, B)
                        good = [x for x in sol if x]
                        if not good:
                            if H_resonant(cfg, A, B): st["H_cfg_nosol_res"] += 1
                            else: st["fail"].append(("H-consequence", l.strip(), sym, A, B, cfg))
                            continue
                        covH.add(key)
                        for (e1, e2, dx, dy) in good:
                            st["H_sign_sol"] += 1
                            st["maxlen"] = max(st["maxlen"], abs(dx) + dy)
                            if trace(o, A, B, dx, dy): st["H_trace_ok"] += 1
                            else: st["fail"].append(("H-trace", l.strip(), sym, A, B, cfg, (e1, e2, dx, dy)))
                    for name, confs, solve in (("Cperp", Cperp_configs, Cperp_solve), ("Cpar", Cpar_configs, Cpar_solve)):
                        for cfg in confs(o, A, B):
                            st[name + "_cfg"] += 1
                            if cfg[-1]: continue          # G in P: this is Lemma C of d15
                            st[name + "_new"] += 1
                            sol = solve(o, cfg, A, B)
                            if all(sol):
                                st["C_sign_ok"] += 4; covC.add(key)
                            else: st["fail"].append((name + "-undecided", l.strip(), sym, A, B, cfg, sol))
            if st["fail"]: break
        if st["fail"]: break
        if r in (3, 4):
            for i in range(len(pts)):
                for j in range(i + 1, len(pts)):
                    ty = sorted((R.ptype(pts[i]), R.ptype(pts[j])))
                    if frozenset(ty) not in op: continue
                    h, c = (i, j) in covH, (i, j) in covC
                    st[f"open{r}"] += 1
                    st[f"open{r}_H"] += h; st[f"open{r}_C"] += c; st[f"open{r}_any"] += h or c
                    e = bytype.setdefault(f"{r} {nx} {ny} {mask} {ty}", [0, 0, 0, 0])
                    e[0] += 1; e[1] += h; e[2] += c; e[3] += h or c
    st["seconds"] = round(time.time() - t0, 1)
    json.dump(bytype, open(f"runs/g_types{w}_{only}.json", "w"))
    json.dump(st, open(f"runs/g_out{w}_{only}.json", "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in st.items() if k != "fail"}), "fails", len(st["fail"]))
    for f in st["fail"][:3]: print("FAIL", f)


if __name__ == "__main__":
    if sys.argv[1] == "gen": gen()
    else: run(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
