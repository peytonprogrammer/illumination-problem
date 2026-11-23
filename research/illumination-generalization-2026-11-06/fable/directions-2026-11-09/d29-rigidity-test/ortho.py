#!/usr/bin/env python3
"""ortho.py SVFILE... -- decide shooting survivors with orbitc, then for every dark pair report
W, area, box, pair, run lines, and darkness after stretching each run (g = 2..5).
A run line is a lattice line y = c (or x = c) strictly inside the room, not the row (column) of S
or T, with no corner on it (no lattice point with 1 or 3 cells).  Then cell rows c-1 and c are
identical.  Stretching gives cell row c height g (rows above shift by g-1); S, T move with it."""
import subprocess, sys
ORBITC = sys.path[0] + "/../d9-census-w22/orbitc"
CAP = 20_000_000

def orbitc(cells, srcs):
    line = f"{len(cells)} " + " ".join(f"{x} {y}" for x, y in sorted(cells)) + f" | {len(srcs)} " + " ".join(f"{x} {y}" for x, y in srcs)
    out = subprocess.run([ORBITC, str(CAP)], input=line + "\n", capture_output=True, text=True, check=True).stdout.split("\n")
    st = out[0].split()
    v = [ln.split()[4] for ln in out[1:] if len(ln.split()) == 5]
    return int(st[1]), st[3] == "1", v[0] if v else "?"

def nc(C, x, y): return sum((x - a, y - b) in C for a in (0, 1) for b in (0, 1))

def run_lines(cells, S, T):
    C = set(cells); res = {}
    for ax in (0, 1):
        o = 1 - ax
        lo, hi = min(c[o] for c in cells), max(c[o] for c in cells) + 1
        al, ah = min(c[ax] for c in cells), max(c[ax] for c in cells) + 1
        L = []
        for c in range(lo + 1, hi):
            if c in (S[o], T[o]): continue
            pts = [(a, c) if ax == 0 else (c, a) for a in range(al, ah + 1)]
            if not any(nc(C, *p) in (1, 3) for p in pts): L.append(c)
        res["rows" if ax == 0 else "cols"] = L
    return res

def stretch(cells, S, T, ax, c, g):
    """give the cell row (ax=0) / column (ax=1) with index c height g"""
    out = []
    for x, y in cells:
        k = y if ax == 0 else x
        if k < c: out.append((x, y))
        elif k > c: out.append((x, y + g - 1) if ax == 0 else (x + g - 1, y))
        else: out += [(x, y + j) if ax == 0 else (x + j, y) for j in range(g)]
    mv = lambda p: ((p[0], p[1] + g - 1) if ax == 0 else (p[0] + g - 1, p[1])) if p[1 - ax] > c else p
    return out, mv(S), mv(T)

def main():
    for fn in sys.argv[1:]:
        for ln in open(fn):
            if not ln.strip(): continue
            head, cs = ln.split("|")
            h = list(map(int, head.split())); v = list(map(int, cs.split()))
            area, W = h[1], h[2]; S, T = (h[4], h[5]), (h[6], h[7]); sep, k = h[8], h[9]
            cells = [(v[2 * i], v[2 * i + 1]) for i in range(len(v) // 2)]
            st, comp, verdict = orbitc(cells, [S, T])
            xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
            print(f"PAIR W {W} area {area} box {max(xs)-min(xs)+1}x{max(ys)-min(ys)+1} S {S} T {T} k {k} sep {sep} "
                  f"orbitc {verdict} states {st} complete {int(comp)}")
            print("  cells", " ".join(f"{x},{y}" for x, y in sorted(cells)))
            if verdict != "DARK": continue
            rl = run_lines(cells, S, T)
            print(f"  runs rows {rl['rows']} cols {rl['cols']} -> {'RUN' if rl['rows'] or rl['cols'] else 'NO RUN'}")
            for ax, key in ((0, "rows"), (1, "cols")):
                for c in rl[key]:
                    for g in (2, 3, 4, 5):
                        oc, S2, T2 = stretch(cells, S, T, ax, c, g)
                        same = (S2[0] - T2[0]) % 2 == 0 and (S2[1] - T2[1]) % 2 == 0
                        st2, comp2, v2 = orbitc(oc, [S2, T2])
                        print(f"  stretch {key[:-1]} {c} g {g}: S {S2} T {T2} same_class {int(same)} orbitc {v2} states {st2} complete {int(comp2)}")
if __name__ == "__main__":
    main()
