"""Check of Astra's canonical partition: Pi = least invariant partition merging the two cells of every off-class 2-cycle.
Claim: a same-class pair has an FP certificate (fp.py) exactly when its two marks have disjoint block sets on Pi."""
import sys, multiprocessing as mp
from itertools import combinations
import foldtest as F, fp

def work(args):
    line, skip = args
    f = line.split(); v = list(map(int, f[skip:])); cells = [v[k:k + 6] for k in range(0, len(v), 6)]
    gens, _ = F.perms(cells); n = len(cells); ms = fp.marks_of(cells)
    same = [(s, t) for s, t in combinations(ms, 2) if s[0] == t[0]]
    if not same: return (0, 0, 0, 0)
    a = fp.work((line, skip))[1]; hits = unequal_only = 0; cache = {}
    for s, t in same:
        c = s[0]
        if c not in cache:
            pairs = [(i, p[i]) for x in range(4) if x != c for p in [gens[x]] for i in range(n) if p[i] != i and p[p[i]] == i]
            cache[c] = fp.partition_from(gens, n, pairs) if pairs else tuple(range(n))
        part = cache[c]; bs, bt = {part[i] for i in s[1]}, {part[i] for i in t[1]}
        if not (bs & bt): hits += 1
        elif bs != bt: unequal_only += 1
    return (len(same), a, hits, unequal_only)

if __name__ == '__main__':
    for path, skip in (('../d237-dark-examples-w22-26/astra/production/jobs.txt', 3), ('../d236-immersed-disc-control/astra/production/jobs.txt', 1)):
        tot = [0, 0, 0, 0]
        with mp.Pool(12) as pool, open(path) as fh:
            for r in pool.imap_unordered(work, ((l, skip) for l in fh if l.strip()), chunksize=2000):
                for i in range(4): tot[i] += r[i]
        print(path.split('/')[1], 'same-class pairs', tot[0], '| FP by any partition', tot[1], '| disjoint on Pi', tot[2], '| unequal but overlapping on Pi', tot[3])
