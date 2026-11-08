"""Independent soundness check of Codex's ray cuts. Uses no Codex code.

For each saved guard (room, path, tile_facts) this script:
1. Rebuilds the complete triangle support from the analytic reduction and checks
   it matches the indexed support Codex used (via the recorded SHA-256).
2. Verifies with exact rational arithmetic that the path is a legal billiard path
   from one mark to the other: open segments stay in the room interior, every
   bounce is on a wall or smooth boundary point with the reflection law, and no
   path point is a nonsmooth corner.
3. Computes every tile whose closure meets the path and checks that tile_facts
   fixes each one to its state in the room. Then any room satisfying the facts
   contains the same path, so the cut removes only illuminated rooms.
"""
import hashlib
import json
import sys
from fractions import Fraction as F
from math import floor
from pathlib import Path

BASE = Path(__file__).parent
NB = ((1, 0), (-1, 0), (0, 1), (0, -1))


def label(p):
    x, y = p
    return 'A' if x % 2 == 0 and y % 2 == 0 else 'B' if x % 2 and y % 2 else 'C'


def square_tiles(i, j):
    """Two canonical triangles of unit square [i,i+1]x[j,j+1], split on the A-B diagonal."""
    c = [(i, j), (i+1, j), (i+1, j+1), (i, j+1)]
    if (i - j) % 2 == 0:  # (i,j) and (i+1,j+1) share parity -> A/B diagonal
        ts = [(c[0], c[1], c[2]), (c[0], c[2], c[3])]
    else:
        ts = [(c[1], c[2], c[3]), (c[1], c[3], c[0])]
    return [tuple(sorted(t)) for t in ts]


def cell_tiles(cx, cy):
    """The eight triangles whose A vertex is (2cx, 2cy)."""
    a = (2*cx, 2*cy)
    out = set()
    for i in (a[0]-1, a[0]):
        for j in (a[1]-1, a[1]):
            out |= {t for t in square_tiles(i, j) if a in t}
    assert len(out) == 8
    return out


def support(target):
    full = {(0, 0), tuple(target)}
    mandatory = full | {(x+dx, y+dy) for x, y in full for dx, dy in NB}
    b = len(mandatory - full)
    r = 9 - b
    assert r >= 0
    allowed = {(x, y) for x in range(-12, 17) for y in range(-12, 17)
               if min(abs(x-u)+abs(y-v) for u, v in mandatory) <= r}
    return full, mandatory, allowed


def in_closed_triangle(p, t):
    (ax, ay), (bx, by), (cx, cy) = t
    def cross(ox, oy, qx, qy):
        return (qx-ox)*(p[1]-oy) - (qy-oy)*(p[0]-ox)
    d1 = cross(ax, ay, bx, by); d2 = cross(bx, by, cx, cy); d3 = cross(cx, cy, ax, ay)
    return not ((min(d1, d2, d3) < 0) and (max(d1, d2, d3) > 0))


def tiles_at(p):
    """All canonical tiles whose closure contains p."""
    out = set()
    for i in (floor(p[0])-1, floor(p[0])):
        for j in (floor(p[1])-1, floor(p[1])):
            for t in square_tiles(i, j):
                if in_closed_triangle(p, t):
                    out.add(t)
    return out


def interior(p, room):
    return all(t in room for t in tiles_at(p))


def crossings(p, q):
    """Parameters in (0,1) where segment pq meets a tile-edge line."""
    ts = set()
    dx, dy = q[0]-p[0], q[1]-p[1]
    def add(c0, dc, lo_hi):
        if dc == 0:
            return
        a, b = sorted(lo_hi)
        for k in range(floor(a)-1, floor(b)+2):
            s = (k - c0) / dc
            if 0 < s < 1:
                ts.add(s)
    add(p[0], dx, (p[0], q[0]))
    add(p[1], dy, (p[1], q[1]))
    for sgn in (1, -1):  # x + sgn*y = even
        c0, dc = p[0]+sgn*p[1], dx+sgn*dy
        if dc:
            a, b = sorted((c0, c0+dc))
            for k in range(floor(a)-2, floor(b)+3):
                if k % 2 == 0:
                    s = (k - c0) / dc
                    if 0 < s < 1:
                        ts.add(s)
    return sorted(ts)


def boundary_line(p, room):
    """Direction of the straight wall through boundary point p, or None if p is a corner."""
    inc = tiles_at(p)
    present = [t for t in inc if t in room]
    if not present or len(present) == len(inc):
        return None
    # p is a smooth boundary point iff the present tiles exactly fill a half-plane
    # through p. Test candidate lines through p in the four tiling directions.
    for d in ((1, 0), (0, 1), (1, 1), (1, -1)):
        n = (-d[1], d[0])
        for side in (1, -1):
            ok = True
            for t in inc:
                # Present tiles lie weakly on the + side, absent tiles weakly on
                # the - side; a tile cut by the line rejects this candidate.
                ss = [side*((v[0]-p[0])*n[0] + (v[1]-p[1])*n[1]) for v in t]
                want = 1 if t in room else -1
                if any(s*want < 0 for s in ss) or all(s == 0 for s in ss):
                    ok = False; break
            if ok:
                return d
    return None


def reflect(v, d):
    dd = d[0]*d[0] + d[1]*d[1]
    k = 2*(v[0]*d[0] + v[1]*d[1]) / F(dd)
    return (k*d[0] - v[0], k*d[1] - v[1])


def parallel_same(u, v):
    return u[0]*v[1] - u[1]*v[0] == 0 and u[0]*v[0] + u[1]*v[1] > 0


def check_path(room, path, marks):
    """Return (ok, reason, touched_tiles)."""
    pts = [tuple(F(*c) for c in pt) for pt in path]
    touched = set()
    ends = {pts[0], pts[-1]}
    if ends != {tuple(map(F, m)) for m in marks} or pts[0] == pts[-1]:
        return False, 'endpoints are not the two marks', touched
    for e in (pts[0], pts[-1]):
        touched |= tiles_at(e)
        if label(tuple(int(c) for c in e)) != 'A' or not interior(e, room):
            return False, 'mark not an interior A', touched
    for a, b in zip(pts, pts[1:]):
        if a == b:
            return False, 'zero-length segment', touched
        cuts = [F(0)] + crossings(a, b) + [F(1)]
        for s in cuts[1:-1]:
            m = (a[0]+s*(b[0]-a[0]), a[1]+s*(b[1]-a[1]))
            touched |= tiles_at(m)
            if not interior(m, room):
                return False, f'crossing point {m} not interior', touched
        for s0, s1 in zip(cuts, cuts[1:]):
            s = (s0+s1)/2
            m = (a[0]+s*(b[0]-a[0]), a[1]+s*(b[1]-a[1]))
            touched |= tiles_at(m)
            if not interior(m, room):
                return False, f'segment midpoint {m} not interior', touched
    for prev, p, nxt in zip(pts, pts[1:], pts[2:]):
        touched |= tiles_at(p)
        d = boundary_line(p, room)
        if d is None:
            return False, f'bounce at {p} is not on a straight wall', touched
        vin = (p[0]-prev[0], p[1]-prev[1]); vout = (nxt[0]-p[0], nxt[1]-p[1])
        if not parallel_same(reflect(vin, d), vout):
            return False, f'reflection law fails at {p}', touched
    return True, 'ok', touched


def guard_sources():
    for name in ['two-global-1-1', 'two-global-2-0', 'two-global-2-1', 'two-global-2-2',
                 'two-pair-search-1-1', 'two-pair-search-2-0', 'two-pair-search-2-1']:
        data = json.loads((BASE/f'{name}.json').read_text())
        tgt = tuple(int(v) for v in name.split('-')[-2:])
        yield name, tgt, data


def main():
    report = dict(files={}, failures=[])
    total = 0
    for name, tgt, data in guard_sources():
        full, mandatory, allowed = support(tgt)
        ts = sorted({t for c in allowed for t in cell_tiles(*c)})
        ts_json = [[list(v) for v in t] for t in ts]
        digest = hashlib.sha256(json.dumps(ts_json).encode()).hexdigest()
        prov = data['summary'].get('provenance', {})
        want_digest = prov.get('triangle_index_sha256')
        if want_digest is not None and want_digest != digest:
            report['failures'].append(dict(file=name, error='support digest mismatch'))
        if 'complete_support_triangles' in data['summary'] and data['summary']['complete_support_triangles'] != len(ts):
            report['failures'].append(dict(file=name, error='support size mismatch'))
        marks = [(0, 0), (2*tgt[0], 2*tgt[1])]
        n = 0
        cut_keys = set()
        for ri, rec in enumerate(data['records']):
            for gi, g in enumerate(rec['derived_guards']):
                n += 1
                room = {tuple(sorted(tuple(v) for v in t)) for t in g['room']['triangles']}
                facts = {i: v for i, v in g['tile_facts']}
                cut_keys.add(tuple(sorted(facts.items())))
                where = dict(file=name, record=ri, guard=gi)
                if not room <= set(ts):
                    report['failures'].append(dict(**where, error='room outside support')); continue
                if sorted(map(tuple, g['room']['marked'])) != sorted(marks):
                    report['failures'].append(dict(**where, error=f"marks {g['room']['marked']}")); continue
                ok, why, touched = check_path(room, g['witness']['path'], marks)
                if not ok:
                    report['failures'].append(dict(**where, error=why)); continue
                index = {t: i for i, t in enumerate(ts)}
                for t in touched:
                    if t not in index:
                        if t in room:
                            report['failures'].append(dict(**where, error=f'touched tile {t} outside support but present'))
                        continue  # tiles outside the support are absent in every model room
                    i = index[t]
                    if i not in facts or facts[i] != int(t in room):
                        report['failures'].append(dict(**where, error=f'touched tile {t} not fixed by guard'))
                        break
                for i, v in facts.items():
                    if v != int(ts[i] in room):
                        report['failures'].append(dict(**where, error=f'fact {i} disagrees with room'))
                        break
        report['files'][name] = dict(target=tgt, support_triangles=len(ts), digest_match=want_digest == digest if want_digest else None,
                                     guards=n, distinct_cuts=len(cut_keys))
        total += n
        print(json.dumps(dict(file=name, guards=n, failures=len(report['failures']))), flush=True)
    report['total_guards'] = total
    report['status'] = 'PASS' if not report['failures'] else 'FAIL'
    (BASE/'claude-ray-guard-check.json').write_text(json.dumps(report, indent=2, default=list)+'\n')
    print(json.dumps(dict(status=report['status'], total_guards=total, failures=report['failures'][:10]), default=list))


if __name__ == '__main__':
    main()
