"""Fold test on census job lines. A disc is a list of cells (x, y, east, north, west, south) with neighbour ids, -1 for a wall.
Usage: foldtest.py jobs.txt skip out.tsv    (skip = number of leading fields before the cell records)"""
import sys, multiprocessing as mp
from collections import Counter

CCW = {0: 4, 1: 5, 2: 2, 3: 3}   # quadrant NE,NW,SW,SE -> link index to step counterclockwise (west, south, east, north)
CW = {0: 5, 1: 2, 2: 3, 3: 4}    # clockwise: south, east, north, west
CORNER = {0: (0, 0), 1: (1, 0), 2: (1, 1), 3: (0, 1)}   # the cell sits in quadrant q of its corner at (x, y) + CORNER[q]

def perms(cells):
    n = len(cells); g = {(0, 0): list(range(n)), (1, 0): list(range(n)), (1, 1): list(range(n)), (0, 1): list(range(n))}
    marks = 0; kinds = Counter()
    for i, c in enumerate(cells):
        front = (c[0] + c[1]) % 2 == 0
        for q in range(4):
            arc = [(i, q)]; j, r = i, q; full = False
            while True:
                k = cells[j][CCW[r]]
                if k < 0: break
                j, r = k, (r + 1) % 4
                if j == i: full = True; break
                arc.append((j, r))
            if not full:
                j, r = i, q
                while True:
                    k = cells[j][CW[r]]
                    if k < 0: break
                    j, r = k, (r - 1) % 4
                    arc.insert(0, (j, r))
            m = len(arc)
            px, py = c[0] + CORNER[q][0], c[1] + CORNER[q][1]
            if full:
                assert m == 4
                t = arc[2][0]; marks += 1
            else:
                seq = [('F', a) for a in arc] + [('B', a) for a in reversed(arc)]
                pos = seq.index(('F' if front else 'B', (i, q)))
                t = seq[(pos + 2) % (2 * m)][1][0]
            g[(px % 2, py % 2)][i] = t
    return list(g.values()), marks // 4

def blocks(gens, n):
    """Smallest block count over the nontrivial invariant partitions, or n when the group is primitive."""
    best = n
    for x in range(1, n):
        par = list(range(n))
        def f(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        stack = [(0, x)]
        while stack:
            a, b = stack.pop(); a, b = f(a), f(b)
            if a == b: continue
            par[a] = b
            for p in gens: stack.append((p[a], p[b]))
        cnt = len({f(i) for i in range(n)})
        if 1 < cnt < best: best = cnt
    return best

def work(args):
    line, skip = args
    f = line.split(); v = list(map(int, f[skip:])); cells = [v[k:k + 6] for k in range(0, len(v), 6)]
    gens, marks = perms(cells); n = len(cells)
    for p in gens: assert sorted(p) == list(range(n))
    b = blocks(gens, n)
    walls = sum(1 for c in cells for k in c[2:] if k < 0)
    return (' '.join(f[:skip]), n, marks, b, line if b < n else None)

if __name__ == '__main__':
    path, skip, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    tally = Counter(); folds = []
    with mp.Pool(12) as pool, open(path) as fh:
        for head, n, marks, b, line in pool.imap_unordered(work, ((l, skip) for l in fh if l.strip()), chunksize=2000):
            tally[(head, 'folds' if b < n else 'primitive')] += 1
            if line: folds.append('%d\t%s' % (b, line.strip()))
    with open(out, 'w') as o: o.write('\n'.join(folds) + '\n')
    tot = sum(tally.values()); nf = sum(v for k, v in tally.items() if k[1] == 'folds')
    print('discs', tot, 'fold', nf, 'share %.4f%%' % (100 * nf / tot))
    agg = Counter()
    for (head, kind), v in tally.items(): agg[(head.split()[1:] and ' '.join(head.split()[1:]) or 'all', kind)] += v
    for k in sorted(agg): print('  ', k[0], k[1], agg[k])
