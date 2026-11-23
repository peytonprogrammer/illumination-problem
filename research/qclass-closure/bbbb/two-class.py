"""Compare midpoint candidates to saved D72 witnesses without enumerating directions."""
import json
import sys
from collections import Counter
from pathlib import Path

base = next(Path(__file__).resolve().parents[2].glob('illumination-generalization*/fable/directions*'))
sys.path.insert(0, str(base / 'd72-cylinder-test'))
import cyl

labels = {(0, 0): 'a', (1, 0): 'b', (1, 1): 'c', (0, 1): 'd'}


def candidate_table(cells, origin):
    room, perms = cyl.PL.room_tuple(cells, origin)
    n = len(perms[0])
    orbit = {}
    classes = {}
    for i in range(n):
        for j in range(n):
            key = i, j
            if i == j or key in orbit:
                continue
            todo = [key]
            orbit[key] = key
            while todo:
                u, v = todo.pop()
                for p in perms:
                    z = p[u], p[v]
                    if z not in orbit:
                        orbit[z] = key
                        todo.append(z)
            classes[key] = set()
    for lab, p in zip('abcd', perms):
        for i, j in enumerate(p):
            if i != j and p[j] == i:
                classes[orbit[i, j]].add(lab)

    def lifts(point):
        return [k for cycle in room.points_at(tuple(p-o for p, o in zip(point, origin)))[1] for k in cycle]

    def candidates(S, T):
        return set.union(*(classes[orbit[i, j]] for i in lifts(S) for j in lifts(T)))
    return candidates


def witness_midpoints(O, S, T, witness):
    v, sheet = witness
    r, _ = cyl.act(O.r, O.u, cyl.word(*v))
    s, t = O.lift(S, (1, 1)), O.lift(T, tuple(sheet))
    mids = set()
    for step in (r, cyl.inv(r)):
        j, k, hits = s, 0, []
        while True:
            j, k = step[j], k + 1
            if O.marked[j] or j == s:
                break
            if j == t:
                hits.append(k)
        for h in hits:
            lengths = [h]
            if j == s:
                lengths.append(h+k)  # a second lap exhausts midpoint parities
            for length in lengths:
                assert length % 2 == 0
                mids.add(labels[tuple((length//2 * x) % 2 for x in v)])
    assert mids
    return mids


def cylinder_midpoint(O, S, T, witness):
    """Use a single saved open cylinder and test its displacement coset mod 4."""
    v, sheet = witness
    r, u = cyl.act(O.r, O.u, cyl.word(*v))
    d = cyl.Decomp(O, r, u)
    s, t = O.lift(S, (1, 1)), O.lift(T, tuple(sheet))
    assert d.cc(s, t)
    for vertical, sign in ((u, 1), (cyl.inv(u), -1)):
        j, h = s, 0
        while d.reg[d.row[j]]:
            if d.row[j] == d.row[t]:
                offset, i = 0, j
                while i != t:
                    i, offset = r[i], offset + 1
                period, i = 1, r[t]
                while i != t:
                    i, period = r[i], period + 1
                assert offset % 2 == h % 2 == period % 2 == 0
                mids = set()
                for winding in (0, 1):
                    x, y = (offset + winding*period)//2, h//2
                    for g, k in reversed(cyl.word(*v)):
                        if g == 'T':
                            x -= k*y
                        else:
                            y -= k*x
                    mids.add(labels[x%2, y%2])
                return mids
            j, h = vertical[j], h + sign
            if j == s:
                break
    raise AssertionError('target row missing from cylinder')


data = json.loads((base / 'd72-cylinder-test/cyl_H40.json').read_text())
rooms = dict(cyl.rooms())
total = Counter()
coverage = Counter()
for name, report in data.items():
    if report['group'] != 'BBBB':
        continue
    cells = rooms[name]
    O = cyl.Origami(cells)
    tables, counts = {}, Counter()
    first_miss = None
    for pair in report['pairs']:
        S, T = tuple(pair['S']), tuple(pair['T'])
        parity = tuple(x%2 for x in S)
        if parity not in tables:
            tables[parity] = candidate_table(cells, S)
        candidates = tables[parity](S, T)
        mids = witness_midpoints(O, S, T, pair['lit'])
        assert mids <= candidates
        cm = cylinder_midpoint(O, S, T, pair['cc'])
        assert cm <= candidates
        coverage[len((cm | mids) - {'a'})] += 1
        cc = bool(cm - {'a'})
        if not cc and mids == {'a'} and first_miss is None:
            first_miss = (S, T, pair['cc'], pair['lit'])
        counts[len(candidates - {'a'}), bool(mids - {'a'}), cc] += 1
    total.update(counts)
    print(name, sorted(counts.items()), first_miss)
print('total', sorted(total.items()))
print('distinct non-source classes certified', sorted(coverage.items()))
