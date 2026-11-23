"""D103: rebuild every shear proof tree on D103's own root boxes and emit its leaves.

Usage: python3 -B shear_check.py HARDDIR LEAVES_OUT [--mutate]

For each tile-level room directory with saved boxes and no `pixel/` finish:
  * check `boxes` against the BOX lines of `tiles`;
  * decide per box which axes are needed (both, or one exposed axis when an
    `alternate/<box>/axis` proof exists) and derive the root boxes from the
    method (not from the author's verifier);
  * replay each tree's bisection, check E leaves, and write W leaves for leafchk;
  * list lattice center pairs (A = 0) that need a census path.
Pixel-finished rooms are reported and skipped. --mutate rewrites every witness
(j -> j+1) for the negative control.
"""
import sys
from math import lcm
from pathlib import Path

U = 65536
hard = Path(sys.argv[1]); out = open(sys.argv[2], 'w'); mutate = '--mutate' in sys.argv
stats = dict(rooms=0, boxes=0, trees=0, W=0, E=0, standalone_boxes=0, pixel_rooms=0, pixel_boxes=0)
lattice = []
rid = 0


def period(C):
    w = []
    for x, y in C:
        if (x - 1, y) not in C:
            z = x + 1
            while (z, y) in C:
                z += 1
            w.append(2 * (z - x))
    return lcm(*w)


def parse_trees(path):
    toks = path.read_text().splitlines()
    pos = 0
    trees = []
    while pos < len(toks):
        h = toks[pos].split(); pos += 1
        assert h[0] == 'R', h
        start = pos
        while not toks[pos].startswith('END '):
            pos += 1  # trees the author's search abandoned are incomplete; they are never used
        body = toks[start:pos]
        end = toks[pos].split(); pos += 1
        assert end[0] == 'END' and end[1:5] == h[1:5], (path, h, end)
        trees.append((tuple(map(int, h[1:])), body, int(end[5]), int(end[6])))
    return trees


def run_tree(rid, ends, fixed, main, box, body, tag):
    it = iter(body); nW = nE = 0

    def visit(z):
        nonlocal nW, nE
        t = next(it).split()
        if t[0] == 'S':
            i = int(t[1]); l, h = z[i]; m = (l + h) // 2
            assert l < m < h, (tag, z, i)
            visit(z[:i] + [(l, m)] + z[i + 1:]); visit(z[:i] + [(m, h)] + z[i + 1:])
            return
        if t[0] == 'E':
            assert not fixed and z[5 - main][0] > z[4 + main][1], ('bad E', tag)
            nE += 1
            return
        assert t[0] == 'W' and len(t) == 4, ('non-witness leaf', tag, t[0])
        j, p, q = map(int, t[1:])
        if mutate:
            j += 1
        nW += 1
        flat = ' '.join(f'{l} {h}' for l, h in z)
        e = ' '.join(map(str, ends))
        print(f'LEAF {rid} {int(fixed)} {e} {flat} {j} {p} {q} {tag}:{nW}', file=out)
    visit(list(box))
    assert next(it, None) is None
    return nW, nE


def regular(C, X, Y):
    return all((X - i, Y - j) in C for i in (0, 1) for j in (0, 1))


for d in sorted(hard.glob('*-*')):
    if not (d / 'boxes').exists():
        continue
    raw = list(map(int, (d / 'room').read_text().split()))
    cells = list(zip(raw[2::2], raw[3::2])); C = set(cells)
    boxes = [tuple(map(int, l.split())) for l in (d / 'boxes').read_text().splitlines()]
    tiles_boxes = [tuple(map(int, l.split()[2:])) for l in (d / 'tiles').read_text().splitlines() if l.startswith('BOX ')]
    assert sorted(boxes) == sorted(tiles_boxes) and len(set(boxes)) == len(boxes), d
    if (d / 'pixel').exists():
        stats['pixel_rooms'] += 1; stats['pixel_boxes'] += len(boxes)
        print('pixel-finished room (not checked here):', d.name, len(boxes), 'boxes', file=sys.stderr)
        continue
    stats['rooms'] += 1
    # oriented geometry and own period per axis
    geo = {}
    for ax in (0, 1):
        o = (lambda c: (c[1], c[0])) if ax else (lambda c: c)
        oc = [o(c) for c in cells]; L = period(set(oc))
        rid += 1
        print(f'ROOM {rid} {L} {len(oc)} ' + ' '.join(f'{x} {y}' for x, y in oc), file=out)
        geo[ax] = (rid, o, set(oc), L)
    # index the author's trees by (axis, ends line, main, mode); ends identify the box
    avail = {}

    def load(dirpath, ax, key_filter=None):
        for f in sorted(dirpath.glob('ends-*')):
            r = int(f.name.split('-')[1])
            lines = [tuple(map(int, l.split())) for l in f.read_text().splitlines()]
            trees = parse_trees(dirpath / f'cert-{r}')
            ti = 0
            for m in lines:
                while ti < len(trees) and trees[ti][0][0] == m[0] and trees[ti][0][1] == m[5] and trees[ti][0][4] == r:
                    hdr, body, ok, n = trees[ti]
                    # the next ends line may share c0,c1: stop when (main,mode) repeats
                    k = (dirpath, ax, m, r, hdr[2], hdr[3])
                    if k in avail:
                        break
                    avail[k] = (body, ok); ti += 1
            assert ti == len(trees), (dirpath, ti, len(trees))

    for ax in (0, 1):
        load(d / 'shears' / str(ax), ax)
    alt = {}
    for meta in d.glob('alternate/*/axis'):
        key = tuple(map(int, meta.parent.name.split('_')))
        ax = int(meta.read_text())
        alt[key] = ax
        load(meta.parent / str(ax), ax)
    for box in boxes:
        stats['boxes'] += 1
        i, jj, k, l, r = box
        centers = []
        for c, corner in ((i, k), (jj, l)):
            a, b = cells[c]; centers.append((a + (corner & 1), b + (corner >> 1)))
        # A = 0: both endpoints at their centers
        if centers[0] != centers[1] and all(regular(C, *z) for z in centers):
            lattice.append((d.name, centers))
        if box in alt:
            axes = [alt[box]]; standalone = True; stats['standalone_boxes'] += 1
        else:
            axes = [0, 1]; standalone = False
        for ax in axes:
            rid_, o, OC, L = geo[ax]
            ends = []
            for c, z in zip((i, jj), centers):
                ends += [c, *o(z), *o(cells[c])]
            ends = tuple(ends)
            if standalone:
                # A_t > 0 needs a tile side through a center, perpendicular to the transverse axis, to be a wall
                exposed = False
                for e in (0, 1):
                    c, X, Y, a, b = ends[5 * e:5 * e + 5]
                    exposed |= (a, b + (1 if Y == b + 1 else -1)) not in OC
                assert exposed, (d, box)
                base_dir = d / 'alternate' / '_'.join(map(str, box)) / str(ax)
            else:
                base_dir = d / 'shears' / str(ax)
            cap = -(-(U // 8) // L)
            for main in (0, 1):
                modes = [0] + ([1] if r >= cap else [])
                for fixed in modes:
                    k_ = (base_dir, ax, ends, r, main, fixed)
                    assert k_ in avail, ('missing tree', d.name, box, ax, main, fixed)
                    body, ok = avail[k_]
                    if fixed:
                        z = [(0, r)] * 4 + [(0, 0)] * 2
                        z[2 * main + 1] = ((U // 8) // L, r)
                    else:
                        rr = min(r, cap); top = max(U // 4, L * rr)
                        z = [(0, rr)] * 4 + [(0, top)] * 2
                        if standalone:
                            z[0] = z[2] = (0, r)
                        z[4 + main] = (U // 8, top)
                    tag = f'{d.name}/{"_".join(map(str, box))}/ax{ax}/m{main}/f{fixed}'
                    nW, nE = run_tree(rid_, ends, fixed, main, z, body, tag)
                    stats['trees'] += 1; stats['W'] += nW; stats['E'] += nE
print('shear-trees', stats, file=sys.stderr)
print('lattice center pairs', len(lattice), file=sys.stderr)
with open(sys.argv[2] + '.lattice', 'w') as f:
    for name, cs in lattice:
        print(name, *[f'{x},{y}' for x, y in cs], file=f)
