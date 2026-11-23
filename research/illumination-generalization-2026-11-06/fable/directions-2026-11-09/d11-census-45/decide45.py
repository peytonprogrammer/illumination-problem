"""Decide every census survivor and describe it.

usage: python3 -B decide45.py CAP WD6 census/star-30/survivors.txt [more survivors.txt ...] > decide.log
  CAP  orbit45 state cap per pair
  WD6  run d6's Hurwitz decider and d4's block analysis on survivors with W <= WD6

For each survivor pair: orbit45 verdict and state count; an independent
re-check of strict simplicity and W by rooms45.boundary (Python boundary walk,
not the C vertex-run test); k and N_min separation from shoot45; equivalence to
a known dark room (up to integer translations and the 8 lattice symmetries,
marks included); for W <= WD6 also d6's decider and d4's block systems.
Both need the marks on A points: B pairs are translated by (1,1), a tiling
symmetry; C rooms are scaled by 2 (each scaled tile is 4 tiles, and C points
land on A points), which gives a similar room with the same pair.
Writes decide45.json next to the first survivors file.
"""
import json
import subprocess
import sys
from pathlib import Path

import rooms45 as R

D4MAPS = [(1, 0, 0, 1), (0, -1, 1, 0), (-1, 0, 0, -1), (0, 1, -1, 0), (1, 0, 0, -1), (-1, 0, 0, 1), (0, 1, 1, 0), (0, -1, -1, 0)]


def key(tiles, marks):
    """Canonical form under integer translations and D4 (tiles as vertex triples)."""
    best = None
    tris = [R.tile_verts(*t) for t in tiles]
    for a, b, c, d in D4MAPS:
        f = lambda p: (a * p[0] + b * p[1], c * p[0] + d * p[1])  # noqa
        tt = [[f(p) for p in t] for t in tris]
        mm = [f(p) for p in marks]
        mx = min(p[0] for t in tt for p in t)
        my = min(p[1] for t in tt for p in t)
        s = lambda p: (p[0] - mx, p[1] - my)  # noqa
        k = (tuple(sorted(tuple(sorted(s(p) for p in t)) for t in tt)), tuple(sorted(s(p) for p in mm)))
        if best is None or k < best:
            best = k
    return best


def known_rooms():
    k = R.worksheet_constants()
    out = {}
    for name, poly, marks in (('castro24', k['CASTRO24'], k['PUBLISHED_ST']), ('tokarsky26', k['TOKARSKY26'], k['PUBLISHED_ST']),
                              ('room22', k['ROOM22'], [(0, 0), (2, 2)])):
        t = R.tiles_from_polygon(poly)
        out[key(t, [tuple(m) for m in marks])] = name
        out.setdefault(('room', key(t, [])[0]), name)
    for f in sorted((R.D4 / 'inputs' / 'census').glob('parity-W*.json')):
        d = json.loads(f.read_text())
        poly = [tuple(p) for p in (json.loads(d['vertices']) if isinstance(d['vertices'], str) else d['vertices'])]
        marks = json.loads(d['marked']) if isinstance(d['marked'], str) else d['marked']
        t = R.tiles_from_polygon(poly)
        out.setdefault(key(t, [tuple(m) for m in marks]), d['tag'])
        out.setdefault(('room', key(t, [])[0]), d['tag'])
    return out


def main():
    cap, wd6 = int(sys.argv[1]), int(sys.argv[2])
    rows = []
    for fn in sys.argv[3:]:
        lines = Path(fn).read_text().splitlines()
        for a in range(0, len(lines), 2):
            s, q = lines[a], lines[a + 1]
            assert s.startswith('S ') and q.startswith('Q ')
            head, tl = s[2:].split('|')
            h = head.split()
            v = list(map(int, tl.split()))
            tiles = [tuple(v[3 * i:3 * i + 3]) for i in range(len(v) // 3)]
            rows.append(dict(src=fn, chunk=h[0], rid=int(h[1]), cls=h[2], N=int(h[3]), W=int(h[4]),
                             S=(int(h[5]), int(h[6])), T=(int(h[7]), int(h[8])), k=int(h[10]), nb=int(h[12]),
                             sep=int(h[14]), tiles=tiles, prob=q[2:]))
    print('survivor pairs', len(rows), flush=True)
    inp = ''.join(r['prob'] + '\n' for r in rows)
    out = subprocess.run([str(R.HERE / 'orbit45'), str(cap)], input=inp, capture_output=True, text=True, check=True).stdout.splitlines()
    assert len(out) == len(rows)
    known = known_rooms()
    for r, o in zip(rows, out):
        p = o.split()
        r['orbit45'] = dict(states=int(p[1]), verdict=p[2])
        b = R.boundary(r['tiles'])
        r['py_simple'], r['py_W'] = b['simple'], b['W_cycle']
        kk = key(r['tiles'], [r['S'], r['T']])
        r['equivalent_pair'] = known.get(kk)
        r['equivalent_room'] = known.get(('room', kk[0]))
        if r['W'] <= wd6:
            tris, marks = to_A_marks(r['tiles'], r['cls'], [r['S'], r['T']])
            r['d6'] = d6_on_tris(tris, marks)
            try:
                r['d4_blocks'] = d4_on_tris(tris, marks)
            except Exception as e:  # noqa
                r['d4_blocks'] = dict(error=repr(e))
        print('%s %s N %d W %d S %s T %s k %d sep %d | orbit45 %s %d | py_simple %s py_W %d | equiv pair %s room %s | d6 %s' % (
            r['chunk'], r['cls'], r['N'], r['W'], r['S'], r['T'], r['k'], r['sep'], r['orbit45']['verdict'],
            r['orbit45']['states'], r['py_simple'], r['py_W'], r['equivalent_pair'], r['equivalent_room'],
            r.get('d6', {}).get('verdict')), flush=True)
    res = [dict((k, v) for k, v in r.items() if k != 'prob') for r in rows]
    Path(sys.argv[3]).with_name('decide45.json').write_text(json.dumps(res, default=str) + '\n')
    tally = {}
    for r in rows:
        t = (r['cls'], r['W'] <= 22, r['orbit45']['verdict'], r['sep'], r['k'] == 0)
        tally[t] = tally.get(t, 0) + 1
    print('tally (class, W<=22, orbit45, sep, k==0): count')
    for t, c in sorted(tally.items()):
        print('  ', t, c)


def to_A_marks(tiles, cls, marks):
    """Same polygon up to similarity, with both marks on A points of the tiling.
    A: unchanged.  B: translate by (1,1) (a tiling symmetry).  C: scale by 2
    (every scaled tile is a union of 4 tiles; C and B points go to A points)."""
    if cls == 'A':
        return [R.tile_verts(*t) for t in tiles], [tuple(m) for m in marks]
    if cls == 'B':
        return [[(x + 1, y + 1) for (x, y) in R.tile_verts(*t)] for t in tiles], [(m[0] + 1, m[1] + 1) for m in marks]
    out = []
    for t in tiles:
        for u in R.tiles_from_polygon([(2 * x, 2 * y) for (x, y) in R.tile_verts(*t)]):
            out.append(R.tile_verts(*u))
    assert len(out) == 4 * len(tiles)
    return out, [(2 * m[0], 2 * m[1]) for m in marks]


def d6_on_tris(tris, marks):
    sys.path.insert(0, str(R.D6))
    import d4_monodromy as d4
    import validate_rooms as vr
    room = d4.Room('r', 'tri', [tuple(map(tuple, t)) for t in tris], [tuple(m) for m in marks])
    r = vr.decide_room(room, vr.tri_tuple(room), max_states=200000)
    return dict(verdict=r['verdict'], basis=r['verdict_basis'], states=[c['orbit_states'] for c in r['components']],
                complete=[c['complete'] for c in r['components']], k=[c['k_transparent'] for c in r['components']])


def d4_on_tris(tris, marks):
    sys.path.insert(0, str(R.D4))
    import monodromy as m4
    room = m4.Room('r', 'tri', [tuple(map(tuple, t)) for t in tris], [tuple(m) for m in marks])
    out = m4.analyse_room(room, full_group=True)
    return dict(order=out.get('order'), primitive=out['primitive'], degree=out['degree'],
                block_systems=[dict(size=b['block_size'], parity=b['parity_property'], sep=b['phiS_disjoint_phiT'])
                               for b in out['block_systems']])


if __name__ == '__main__':
    main()
