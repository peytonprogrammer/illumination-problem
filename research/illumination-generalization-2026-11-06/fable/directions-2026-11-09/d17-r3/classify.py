"""Sort the open position-type pairs of cert_r{r}.json by kind and by the
metric-free part of the new lemmas. door2 counts chain pairs where one point is
in a maximal corridor whose mouth has two reflex ends. Usage: classify.py r [table]
Kinds: 1 collinear (one grid line, common rectangle), 2 half-period door (one
point in a maximal corridor whose door has two reflex ends, the other sees the
whole door), 3 chain (the rest).
H = a Lemma H configuration exists; C = a Lemma C+ configuration exists whose
rectangle G isn't in P (so only the metric condition on K is missing)."""
import sys, json
from collections import Counter
from rooms import Room
import newlemmas as nl
from newlemmas import Geo, SYMS

r = int(sys.argv[1])
nl.CHECK_K = False
tot, per = Counter(), []
for row in json.load(open(f"../d15-small-r/cert_r{r}.json")):
    if not row["uncovered"]: continue
    R = Room(row["nx"], row["ny"], row["mask"], [2] * row["nx"], [2] * row["ny"])
    g = Geo(R.cells, R.W, R.H)
    frames = [(g.tr(sym), sym) for sym in SYMS]
    c = Counter()
    for S, T in row["uncovered"]:
        S, T = tuple(S), tuple(T)
        kind, H, C, DA = 3, False, False, False
        if (S[0] == T[0] and S[0] % 2 == 0) or (S[1] == T[1] and S[1] % 2 == 0):
            x0, x1 = sorted((S[0], T[0])); y0, y1 = sorted((S[1], T[1]))
            xo = [(x0, x1)] if x0 < x1 else [(x0 - 2 + (x0 % 2), x0 + (x0 % 2)), (x0 - (x0 % 2), x0 + 2 - (x0 % 2))]
            yo = [(y0, y1)] if y0 < y1 else [(y0 - 2 + (y0 % 2), y0 + (y0 % 2)), (y0 - (y0 % 2), y0 + 2 - (y0 % 2))]
            if any(all((x, y) in R.cells for x in range(a, b) for y in range(e, f)) for a, b in xo for e, f in yo): kind = 1
        for o, sym in frames:
            for A, B in ((S, T), (T, S)):
                a, b = g.tp(sym, A), g.tp(sym, B)
                if any(True for _ in nl.H_configs(o, a, b)): H = True
                if any(not cfg[-1] for cfg in nl.Cperp_configs(o, a, b)): C = True
                if any(not cfg[-1] for cfg in nl.Cpar_configs(o, a, b)): C = True
                p, q, d = nl.corridor_up(o, b)
                if o.npt(p, d) == 3 and o.npt(q, d) == 3 and o.npt(a[0], a[1]) == 4: DA = True
                if kind == 3 and a[1] < b[1]:
                    if a[1] < d and o.npt(p, d) == 3 and o.npt(q, d) == 3 and \
                       all((x, y) in o.cells for x in range(min(a[0], p), max(a[0], q)) for y in range(a[1], d)):
                        kind = 2
        c[f"kind{kind}"] += 1; c["door2"] += (kind == 3 and DA); c["H"] += H; c["C"] += C; c["H or C"] += H or C; c[f"kind{kind} H or C"] += H or C
    tot += c; tot["types"] += 1
    per.append((row["nx"], row["ny"], row["mask"], row["shape"], len(row["uncovered"]), c))
keys = ["kind1", "kind2", "kind3", "door2", "H", "C", "H or C"]
print("r", r, "types with open pairs", tot["types"], "open", sum(tot[k] for k in keys[:3]), {k: tot[k] for k in keys},
      {f"kind{k} H or C": tot[f"kind{k} H or C"] for k in (1, 2, 3)})
if len(sys.argv) > 2:
    print("| nx x ny | mask | shape | open | collinear | door | chain | H | C+ |\n|---|---|---|---|---|---|---|---|---|")
    for nx, ny, mask, shape, n, c in per:
        print(f"| {nx} x {ny} | {mask} | `{shape}` | {n} | {c['kind1']} | {c['kind2']} | {c['kind3']} | {c['H']} | {c['C']} |")
