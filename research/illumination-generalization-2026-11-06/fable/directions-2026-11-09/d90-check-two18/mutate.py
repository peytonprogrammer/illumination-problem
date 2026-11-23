"""Mutation test: perturb each saved witness and count how many the leaf check rejects.

Usage: python3 -B mutate.py REGIONS_TXT
"""
import sys
sys.argv = [sys.argv[0], sys.argv[1], '0', '0']
src = open(__file__.replace('mutate.py', 'check.py')).read().split('tot = [0, 0, 0]')[0]
exec(src)
for tag in ('00', '01', '10', '11'):
    check_tag(tag)
n = rej = 0
for (tag, c0, c1, main), leaves in TREES.items():
    r, swap = int(tag[0]), int(tag[1])
    d = centers[(r, c0, c1)]
    ends = [(c, tr(d[c], swap), tr(ROOMS[r][c], swap)) for c in (c0, c1)]
    for z, kind, w in leaves:
        if kind != 'W':
            continue
        j, p, q = w
        for jj, pp, qq in ((j + 1, p, q), (-j, p, q), (j, q, p)):
            if (pp, qq) == (p, q) and jj == j:
                continue
            n += 1
            rej += not witness_ok(ROOMOBJ[tag], ends, z, jj, pp, qq)
print(f'mutations: {n} perturbed witnesses, {rej} rejected')
