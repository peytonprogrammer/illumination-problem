"""Compare skel.c enumeration with enum_K.c output re-canonicalized by skel.c.
Usage: python3 -B cmp.py MINE.txt RECANON.txt Z DMAX"""
import sys
from collections import Counter
mine_f, ref_f, z, dmax = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])

def load(path):
    out = {}
    for line in open(path):
        head, form = line.split('|')
        d, zz, cone, sing = map(int, head.split())
        if zz == z and d <= dmax:
            out[form.strip()] = (d, cone, sing)
    return out

mine, ref = load(mine_f), load(ref_f)
print('z', z, 'dmax', dmax, 'mine', len(mine), 'enum_K', len(ref),
      'missing from enum_K', len(set(mine) - set(ref)), 'extra in enum_K', len(set(ref) - set(mine)))
for f in sorted(set(mine) ^ set(ref))[:10]:
    print('DIFF', 'mine' if f in mine else 'enum_K', (mine.get(f) or ref.get(f)), f)
by = lambda S: Counter(v[0] for v in S.values())
adm = lambda S: Counter(v[0] for v in S.values() if v[2] >= 3)
bm, br, am, ar = by(mine), by(ref), adm(mine), adm(ref)
print('d  genus0(mine) genus0(enum_K)  admissible(mine) admissible(enum_K)')
for d in sorted(set(bm) | set(br)):
    print(d, bm[d], br[d], am[d], ar[d], '' if (bm[d], am[d]) == (br[d], ar[d]) else 'MISMATCH')
print('totals', sum(bm.values()), sum(br.values()), sum(am.values()), sum(ar.values()))
