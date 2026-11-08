"""Cross-check the exact decider on rooms with known verified rays.

For each room the decider returns a shear word. The word gives a direction v in X, and
some D4 image of v leaves the source mark in the room. Fold the straight line exactly
(Fractions), passing through regular vertices as X does, and check the folded path with
Claude's exact checker. A lit verdict counts only if a checked path exists.
Usage: claude_verify_lit.py rays.jsonl marks(x0,y0,x1,y1) [limit]
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
from claude_origami_dark import decide
from claude_unfold import G, app, refl
from claude_ray_guard_check import check_path

MAT = {'T': ((1, 1), (0, 1)), 't': ((1, -1), (0, 1)), 'S': ((1, 0), (1, 1)), 's': ((1, 0), (-1, 1))}


def direction(word):
    m = ((1, 0), (0, 1))
    for c in word:  # Y = M_k ... M_1 X
        a = MAT[c]
        m = tuple(tuple(sum(a[i][k]*m[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    (a, b), (c, d) = m  # det 1: inverse is ((d, -b), (-c, a)); v = M^-1 (1, 0)
    return (d, -c)


def inside(t, p):
    (x0, y0), (x1, y1), (x2, y2) = t
    s = lambda ax, ay, bx, by: (bx-ax)*(p[1]-ay)-(by-ay)*(p[0]-ax)
    d = [s(x0, y0, x1, y1), s(x1, y1, x2, y2), s(x2, y2, x0, y0)]
    return all(v >= 0 for v in d) or all(v <= 0 for v in d)


def fold(tiles, slits, src, tgt, d, max_steps=400):
    owners = {}
    for t in tiles:
        for e in [(t[0], t[1]), (t[0], t[2]), (t[1], t[2])]:
            owners.setdefault(tuple(sorted(e)), []).append(t)
    walls = {e for e, o in owners.items() if len(o) == 1 or e in slits}
    at = {}
    for t in tiles:
        for v in t:
            at.setdefault(v, []).append(t)
    P = tuple(map(F, src)); pts = [P]; d = tuple(map(F, d)); eps = F(1, 10**6)
    for _ in range(max_steps):
        ip = tuple(int(c) for c in P)
        # leave the vertex: pick a tile containing P + eps d; if none, reflect off the wall line
        for _ in range(2):
            q = (P[0]+eps*d[0], P[1]+eps*d[1])
            cand = [t for t in at[ip] if inside(t, q)]
            if cand:
                break
            wl = [e for e in walls if ip in e]
            lines = {(e[1][0]-e[0][0], e[1][1]-e[0][1]) for e in wl}
            lines = {(dx//max(abs(dx), abs(dy)), dy//max(abs(dx), abs(dy))) for dx, dy in lines}
            if len({tuple(sorted([v, (-v[0], -v[1])])) for v in lines}) != 1:
                return None  # a corner: blocked
            e = wl[0]; s = refl(e)
            d = (s[0][0]*d[0]+s[0][1]*d[1], s[1][0]*d[0]+s[1][1]*d[1])
            if pts[-1] != P:
                pts.append(P)
        else:
            return None
        t = cand[0]
        while True:  # walk inside tiles until the next integer point
            best = None
            for e in [(t[0], t[1]), (t[0], t[2]), (t[1], t[2])]:
                (ax, ay), (bx, by) = e
                den = d[0]*(by-ay)-d[1]*(bx-ax)
                if den == 0:
                    continue
                s_ = ((ax-P[0])*(by-ay)-(ay-P[1])*(bx-ax))/den
                if s_ > 0 and (best is None or s_ < best[0]):
                    best = (s_, e)
            s_, e = best
            E = (P[0]+s_*d[0], P[1]+s_*d[1])
            if E[0].denominator == 1 and E[1].denominator == 1:
                P = E; break
            e = tuple(sorted(e))
            if e in walls:
                s = refl(e); d = (s[0][0]*d[0]+s[0][1]*d[1], s[1][0]*d[0]+s[1][1]*d[1]); pts.append(E)
            else:
                t = next(x for x in owners[e] if x != t)
            P = E
        ip = tuple(int(c) for c in P)
        if ip == tuple(tgt):
            pts.append(P); return pts
        if ip == tuple(src):
            pass
        # integer point: blocked if a corner (not interior, not on one straight wall line)
        wl = [e for e in walls if ip in e]
        if wl:
            dirs = set()
            for a, b in wl:
                o = b if a == ip else a
                dirs.add((o[0]-ip[0], o[1]-ip[1]))
            if not (len(dirs) == 2 and sum(x for x, _ in dirs) == 0 and sum(y for _, y in dirs) == 0):
                return None
    return None


def main():
    src = sys.argv[1]; mk = list(map(int, sys.argv[2].split(','))); lim = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    marks = [(mk[0], mk[1]), (mk[2], mk[3])]
    stats = dict(rooms=0, decider_lit=0, folded_and_checked=0, decider_dark=0)
    for line in Path(src).read_text().splitlines()[:lim]:
        r = json.loads(line); room = r['room']
        res = decide(dict(triangles=room, marked=marks))
        stats['rooms'] += 1
        if res['status'] != 'lit':
            stats['decider_dark'] += 1; print('NOT LIT', res, flush=True); continue
        stats['decider_lit'] += 1
        v = direction(res['word']); tiles = [tuple(sorted(map(tuple, t))) for t in room]
        ok = False
        for g in G:
            pts = fold(tiles, set(), marks[0], marks[1], app(g, v))
            if pts:
                path = [[[c.numerator, c.denominator] for c in p] for p in pts]
                good, why, _ = check_path(frozenset(tiles), path, marks)
                if good:
                    ok = True; break
                print('checker rejected', why, flush=True)
        stats['folded_and_checked'] += ok
        print(res['word'], v, ok, flush=True)
    print(json.dumps(stats))


if __name__ == '__main__':
    main()
