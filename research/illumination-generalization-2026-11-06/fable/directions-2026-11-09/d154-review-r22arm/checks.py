"""d154 referee checks for r22-arm-descent.md (snapshot 2026-11-22 03:35).

Named rooms only; no room, direction or witness search. Integer arithmetic.
Lattice illumination verdicts use d8's SL(2,Z)-orbit decider (imported
unchanged); every returned witness is re-traced with d8's Fraction tracer.
Run: python3 -B checks.py > checks.log
"""
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path

T0 = time.process_time()
HERE = Path(__file__).resolve().parent
ARCH = HERE.parent
sys.path.insert(0, str(ARCH / "d8-perturbation-test"))
import room as RM                                  # noqa: E402
from decider import decide, regular_points         # noqa: E402
from tracer import certify                         # noqa: E402

ROOMS = {r["id"]: {tuple(c) for c in r["cells"]} for r in
         json.load(open(ARCH / "d8-perturbation-test" / "rooms.json"))}
R22 = ROOMS["R22-base"]
CLASSES = [(0, 0), (1, 0), (0, 1), (1, 1)]


def hdr(s):
    print("\n== " + s)


def lines(cells):
    """Distinct supporting-line coordinates of vertical and horizontal walls."""
    vs = RM.vertex_cycle(cells)
    xs, ys = set(), set()
    for k in range(len(vs)):
        a, b = vs[k], vs[(k + 1) % len(vs)]
        if a[0] == b[0]:
            xs.add(a[0])
        else:
            ys.add(a[1])
    return sorted(xs), sorted(ys)


def gaps(cells):
    xs, ys = lines(cells)
    return [b - a for a, b in zip(xs, xs[1:])], [b - a for a, b in zip(ys, ys[1:])]


def parity(cells):
    """Per class: (regular count, corner count) over lattice points of the closure."""
    reg, cor = Counter(), Counter()
    for p in RM.lattice_points(cells):
        c = (p[0] % 2, p[1] % 2)
        st = RM.status(cells, p)
        if st in ("interior", "smooth"):
            reg[c] += 1
        elif st in ("convex", "reflex"):
            cor[c] += 1
        else:
            raise ValueError(st)
    return {c: (reg[c], cor[c]) for c in CLASSES}


def geom(cells):
    s = RM.summary(cells)
    vs = RM.vertex_cycle(cells)
    hl = [abs(vs[k][0] - vs[(k + 1) % len(vs)][0]) for k in range(len(vs))]
    vl = [abs(vs[k][1] - vs[(k + 1) % len(vs)][1]) for k in range(len(vs))]
    return dict(W=s["W"], r=s["r"], n=len(cells), simple=RM.is_strictly_simple(cells),
                hgcd=math.gcd(*[x for x in hl if x]), vgcd=math.gcd(*[y for y in vl if y]))


def row_witness(cells, axis_lines, vertical=True):
    """Lemma A construction: for each gap >= 3 between consecutive vertical
    (resp. horizontal) lines, find an occupied full row and check that its
    two ends at intermediate abscissas are regular and cover all 4 classes."""
    out = []
    for a, b in zip(axis_lines, axis_lines[1:]):
        if b - a < 3:
            continue
        if vertical:
            rows = sorted({j for (i, j) in cells if a <= i < b
                           and all((t, j) in cells for t in range(a, b))})
            pts = lambda j: [(c, j + e) for c in range(a + 1, b) for e in (0, 1)]
        else:
            rows = sorted({i for (i, j) in cells if a <= j < b
                           and all((i, t) in cells for t in range(a, b))})
            pts = lambda i: [(i + e, c) for c in range(a + 1, b) for e in (0, 1)]
        # cross-section constancy: every cell column in the slab has the same occupancy
        if vertical:
            prof = {i: frozenset(j for (ii, j) in cells if ii == i) for i in range(a, b)}
        else:
            prof = {j: frozenset(i for (i, jj) in cells if jj == j) for j in range(a, b)}
        const = len(set(prof.values())) == 1
        ok = bool(rows)
        cls_cnt = Counter()
        if rows:
            P = pts(rows[0])
            ok = all(RM.status(cells, p) in ("interior", "smooth") for p in P)
            cls_cnt = Counter((p[0] % 2, p[1] % 2) for p in P)
        G = b - a
        out.append(dict(gap=(a, b), G=G, const_section=const, rows=len(rows), regular=ok,
                        all4=len(cls_cnt) == 4,
                        min_per_class=min(cls_cnt.get(c, 0) for c in CLASSES),
                        floor=(G - 1) // 2))
    return out


def lemma_a_report(name, cells):
    g = geom(cells)
    xs, ys = lines(cells)
    gx, gy = gaps(cells)
    par = parity(cells)
    clean = [c for c in CLASSES if par[c][0] == 0]
    G = max(gx + gy)
    print(f"  {name}: {g}")
    print(f"    x-lines {xs} gaps {gx}; y-lines {ys} gaps {gy}; max gap {G}")
    print(f"    (regular, corner) per class {par}; corner-only classes {clean}")
    w = row_witness(cells, xs, True) + row_witness(cells, ys, False)
    for d in w:
        print(f"    gap {d['gap']} G={d['G']}: constant section {d['const_section']}, full rows {d['rows']}, "
              f"row ends regular {d['regular']}, all 4 classes {d['all4']}, "
              f"min per class {d['min_per_class']} >= floor((G-1)/2)={d['floor']}: {d['min_per_class'] >= d['floor']}")
        assert d["const_section"] and d["rows"] and d["regular"] and d["all4"]
        assert d["min_per_class"] >= d["floor"]
    # global per-class lower bound floor((G-1)/2)
    assert all(par[c][0] >= (G - 1) // 2 for c in CLASSES)
    if clean:
        assert G <= 2, "Lemma A violated"
    print(f"    Lemma A consistent: clean class present -> G<=2 ({'n/a' if not clean else G <= 2}); "
          f"every class has >= floor((G-1)/2)={(G - 1) // 2} regular points: True")
    return G, clean, par


def cov4181():
    cov = set()
    for x, ys in enumerate([range(6), (2, 3), (2, 3), range(6), range(6), (2, 3), (2,), range(3)]):
        for y in ys:
            cov.add((x, y))
    return cov


def arm(L, which):
    """R22 with one terminal arm of length L (L=1 is R22)."""
    c = set(R22)
    if which == "bottom":
        c |= {(1, -3 - j) for j in range(L)}
    elif which == "right":
        c |= {(4 + j, 0) for j in range(L)}
    else:
        c |= {(1, 2 + j) for j in range(L)} | {(2, 2 + j) for j in range(L)}
    return c


# ------------------------------------------------------------------ 1. Lemma A
hdr("1. Gap lemma A on named rooms")
three = set()
for i in range(3):
    for j in range(3):
        three.add((i, j))
X = Y = 4
for t in range(X):
    three.add((3 + t, 1))
for i in range(3):
    for j in range(3):
        three.add((3 + X + i, j))
for t in range(Y):
    three.add((6 + X + t, 1))
for i in range(3):
    for j in range(3):
        three.add((6 + X + Y + i, j))
named = [("R22-base", R22), ("cov4181 (d66/d144 cells)", cov4181()),
         ("L-room (3 cells, d145)", {(0, 0), (1, 0), (0, 1)}),
         ("R22-L1-027 junction J (d152)", ROOMS["R22-L1-027"]),
         ("three-chamber X=Y=4 (d152)", three)]
for nm, c in named:
    lemma_a_report(nm, c)

# ------------------------------------------------------------------ 2. Lemma B
hdr("2. Gap lemma B arithmetic")
for k in range(1, 9):
    for J in (1, 2, 3, 4):
        gmax = max(G for G in range(1, 200) if J * ((G - 1) // 2) <= 2 * k - 2)
        assert gmax == 2 * ((2 * k - 2) // J) + 2, (k, J)
print("  max G with |J| floor((G-1)/2) <= 2k-2 equals 2 floor((2k-2)/|J|)+2 for k<=8, |J|<=4: True")
print("  |J|=1, k=r=8: G <= ", 2 * (2 * 8 - 2) + 2, "(= 4r-2 =", 4 * 8 - 2, ")")
# R22 staircase: Q->N inner degree k=3 (three copies of a 5-cell staircase); J = three off-source classes
par = parity(R22)
q = {c: par[c][0] for c in CLASSES}
print(f"  R22 physical regular counts per class {q} (axial q on the double = 2 each, smooth wall points)")
k, J = 3, [(1, 0), (0, 1), (1, 1)]
print(f"  R22 staircase k=3, J=3 off-source classes: sum q = {sum(q[c] for c in J)} <= 2k-2 = 4;"
      f" gap bound 2 floor(4/3)+2 = {2 * (4 // 3) + 2}; actual max gap {max(sum(gaps(R22), []))}")
cv = cov4181()
gx, gy = gaps(cv)
print(f"  cov4181 four-sheet quotient: n=28=4k so k=7 <= r={geom(cv)['r']}; J={{c}} gives G <= {2 * (12 // 1) + 2};"
      f" actual gaps x {gx} y {gy}")
# Lemma B needs a downstairs zero for k <= r. N = B (k = n) is clean at every site but is not proper.
print("  N = B (k = n) is clean at all four sites; the bound would read G <= 4n-2, so 'proper' is load-bearing.")

# ------------------------------------------------------------------ 3. R22 arms
hdr("3. R22 arm slices: old cap vertex and parity cleanliness, L = 1..10")
spec = {"bottom": ("R22-L1-007", (1, -3)), "right": ("R22-L1-025", (5, 1)), "top": ("R22-L1-012", (1, 3))}
for which, (nm, v) in spec.items():
    assert arm(1, which) == R22
    assert arm(2, which) == ROOMS[nm], which
    print(f"  {which} arm, L=2 equals d8 {nm}: True; note's vertex {v}")
    for L in range(1, 11):
        c = arm(L, which)
        g = geom(c)
        par = parity(c)
        clean = [cl for cl in CLASSES if par[cl][0] == 0]
        oo_reg = sorted(p for p in RM.lattice_points(c) if p[0] % 2 and p[1] % 2
                        and RM.status(c, p) in ("interior", "smooth"))
        n_inc = len(RM.around(c, v))
        G = max(sum(gaps(c), []))
        print(f"    L={L:2d} W={g['W']} r={g['r']} n={g['n']} simple={g['simple']} gcd=({g['hgcd']},{g['vgcd']}) "
              f"maxgap={G} vertex {v}: {RM.status(c, v)} ({n_inc} cells); clean classes {clean}; "
              f"odd-odd regular pts {oo_reg[:6]}{'...' if len(oo_reg) > 6 else ''}")
        if L >= 2:
            assert RM.status(c, v) == "smooth" and n_inc == 2 and not clean
        assert g["W"] == 22 and g["r"] == 9 and g["simple"]

# ------------------------------------------------------------------ 4. Length-2 illumination
hdr("4. Length-2 arm rooms: every regular lattice pair lit (d8 orbit decider, early stop)")
for which, (nm, v) in spec.items():
    c = ROOMS[nm]
    regs = regular_points(c)
    want = [(p, q) for i, p in enumerate(regs) for q in regs[i + 1:]]
    t = time.process_time()
    res = decide(c, regs, wanted=want, cap=4_000_000)
    lit_un = {tuple(sorted(pq)) for pq in res["lit"]}
    unlit = [pq for pq in want if tuple(sorted(pq)) not in lit_un]
    # re-trace one witness per unordered pair with d8's Fraction tracer
    bad, graze = 0, []
    for (p, q) in want:
        ok = False
        for S, T in ((p, q), (q, p)):
            D = res["witness"].get((S, T))
            if D is not None and certify(c, S, T, D) is not None:
                ok = True
                break
        if not ok:
            # d8's tracer rejects a start running along a wall; such a decider
            # witness is a wall-grazing segment. Report it and test one named
            # non-grazing alternative: the single bounce off the opposite wall.
            alt = (1, 2) if p[1] == q[1] else (2, 1)
            Ds = certify(c, p, q, alt)
            graze.append((p, q, res["witness"].get((p, q)), alt, Ds))
            if Ds is None:
                bad += 1
    print(f"  {nm} ({which}): regular pts {len(regs)}, unordered pairs {len(want)}, status {res['status']}, "
          f"states {res['states']}, unlit {len(unlit)}, wall-grazing witnesses {len(graze)}, "
          f"pairs without a re-traced legal witness {bad}")
    for g in graze:
        print(f"    grazing witness {g[0]}-{g[1]} D={g[2]} rejected by tracer; alternative {g[3]} re-traces as {g[4]}")
    assert res["status"] in ("EARLY", "DONE") and not unlit and bad == 0
# base R22 control: complete scan
regs = regular_points(R22)
res = decide(R22, regs, cap=4_000_000)
dark = sorted({tuple(sorted((p, q))) for p in regs for q in regs if p != q and (p, q) not in res["lit"]})
print(f"  control R22-base: status {res['status']}, states {res['states']}, dark pairs {dark}")

# ------------------------------------------------------------------ 5. 45-degree control
hdr("5. Mixed-wall control: d141/d143 V-notch B (0,0),(4,0),(4,4),(2,2),(0,4)")
# Points of the closed polygon: interior lattice points and points on edges.
verts = [(0, 0), (4, 0), (4, 4), (2, 2), (0, 4)]
def on_seg(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    return (x2 - x1) * (y - y1) == (y2 - y1) * (x - x1) and min(x1, x2) <= x <= max(x1, x2) \
        and min(y1, y2) <= y <= max(y1, y2)
def inside(p):
    # V-notch: square [0,4]^2 minus the open triangle above |x-2| + 2 < y
    x, y = p
    return 0 <= x <= 4 and 0 <= y <= 4 and y <= 2 + abs(x - 2)
pts = [(x, y) for x in range(5) for y in range(5) if inside((x, y))]
reg, cor = Counter(), Counter()
for p in pts:
    c = (p[0] % 2, p[1] % 2)
    (cor if p in verts else reg)[c] += 1
print("  axis-parallel supporting lines: vertical x in {0,4} (gap 4); horizontal y = 0 only; the two top walls are diagonal")
print(f"  physical (regular, corner) per class: {{{', '.join(f'{c}: ({reg[c]},{cor[c]})' for c in CLASSES)}}}")
print("  r = 1, so the orthogonal Lemma B budget 4r-2 = 2 < 4; d145 records four clean sites on the")
print("  degree-3 torus quotient X/C3. The orthogonal gap lemmas do not transfer verbatim to 45-degree rooms.")

print(f"\nTotal CPU: this process {time.process_time() - T0:.1f}s")
import resource  # noqa: E402
ch = resource.getrusage(resource.RUSAGE_CHILDREN)
print(f"children {ch.ru_utime + ch.ru_stime:.1f}s")
