"""Certificate test: for each census disc, find same-class mark pairs with a folded-parity certificate.
Usage: fp.py jobs.txt skip"""
import sys, multiprocessing as mp
from itertools import combinations
import foldtest as F

CLS = [(0, 0), (1, 0), (1, 1), (0, 1)]

def marks_of(cells):
    """interior lattice points as (class index, frozenset of 4 cells)."""
    out = set()
    for i, c in enumerate(cells):
        j, r, ring = i, 0, [i]
        for _ in range(3):
            j = cells[j][F.CCW[r]]
            if j < 0: break
            r = (r + 1) % 4; ring.append(j)
        else:
            if cells[j][F.CCW[r]] == i:
                p = ((c[0] + 0) % 2, (c[1] + 0) % 2)   # cell i sits in quadrant NE of its corner (x, y)
                out.add((CLS.index(p), frozenset(ring)))
    return sorted(out, key=lambda m: (m[0], sorted(m[1])))

def partition_from(gens, n, pairs):
    par = list(range(n))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    stack = list(pairs)
    while stack:
        a, b = stack.pop(); a, b = f(a), f(b)
        if a == b: continue
        par[a] = b
        for p in gens: stack.append((p[a], p[b]))
    return tuple(f(i) for i in range(n))

def canon(part):
    seen = {}; return tuple(seen.setdefault(x, len(seen)) for x in part)

def all_partitions(gens, n):
    base = {canon(partition_from(gens, n, [(0, x)])) for x in range(1, n)}
    parts = set(base) | {tuple(range(n))}
    grew = True
    while grew:
        grew = False
        for p, q in list(combinations(parts, 2)):
            pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if p[i] == p[j] or q[i] == q[j]]
            r = canon(partition_from(gens, n, pairs))
            if r not in parts: parts.add(r); grew = True
    return [p for p in parts if len(set(p)) > 1]

def has2(perm, part):
    """does the quotient of perm on the blocks of part have a 2-cycle?"""
    q = {}
    for i, t in enumerate(perm): q[part[i]] = part[t]
    return any(q[b] != b and q[q[b]] == b for b in q)

def work(args):
    line, skip = args
    f = line.split(); v = list(map(int, f[skip:])); cells = [v[k:k + 6] for k in range(0, len(v), 6)]
    gens, _ = F.perms(cells); n = len(cells); ms = marks_of(cells)
    same = [(s, t) for s, t in combinations(ms, 2) if s[0] == t[0]]
    if not same: return (0, 0, None)
    hits = []
    parts = None
    for s, t in same:
        others = [gens[c] for c in range(4) if c != s[0]]
        single = tuple(range(n))
        if not any(has2(p, single) for p in others):
            hits.append(('cells', s, t)); continue
        if parts is None: parts = all_partitions(gens, n)
        for part in parts:
            if len(set(part)) == n: continue
            if any(has2(p, part) for p in others): continue
            if {part[i] for i in s[1]} != {part[i] for i in t[1]}:
                hits.append((len(set(part)), s, t)); break
    return (len(same), len(hits), (line.strip(), [(h[0], sorted(h[1][1]), sorted(h[2][1])) for h in hits]) if hits else None)

if __name__ == '__main__':
    path, skip = sys.argv[1], int(sys.argv[2])
    tot = cert = 0; found = []
    with mp.Pool(12) as pool, open(path) as fh:
        for a, b, rec in pool.imap_unordered(work, ((l, skip) for l in fh if l.strip()), chunksize=2000):
            tot += a; cert += b
            if rec: found.append(rec)
    print(path.split('/')[1], 'same-class pairs', tot, 'with certificate', cert)
    for line, hits in found: print('  ', ' '.join(line.split()[:3]), hits)
