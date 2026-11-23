"""Aggregate census chunks into tables and collect survivors.

usage: python3 -B agg45.py census/star-30 [census/cstar-24 ...]
Writes, per directory D: D/totals.tsv, D/khist.tsv, D/survivors.txt (rows of the
.sv files, each followed by its orbit45 problem line) and prints a summary.
Checks: every chunk finished ("# DONE"); enumerated room counts (.counts)
equal the rooms the shooter read (.out); verify_fail = 0.
"""
import sys
from collections import defaultdict
from pathlib import Path


def agg(d):
    d = Path(d)
    rooms_enum = defaultdict(int)
    rooms_shot = defaultdict(int)
    tab = defaultdict(lambda: [0] * 6)
    kh = defaultdict(lambda: [0] * 3)
    nodes = 0
    vf = 0
    maxm = 0
    chunks = 0
    sv_rows = []
    for c in sorted(d.glob('*.counts')):
        o = c.with_suffix('.out')
        ct, ot = c.read_text(), o.read_text()
        assert ct.rstrip().endswith('# DONE') and ot.rstrip().endswith('# DONE'), c
        chunks += 1
        for line in ct.splitlines():
            p = line.split()
            if p[0] == '#' and 'nodes' in p:
                nodes += int(p[p.index('nodes') + 1])
            elif p[0] == 'rooms':
                rooms_enum[(int(p[1]), int(p[2]))] += int(p[3])
        for line in ot.splitlines():
            p = line.split()
            if line.startswith('# ROOMS'):
                rooms_shot[(int(p[3]), int(p[5]))] += int(p[7])
            elif line.startswith('# T '):
                key = (p[2], int(p[4]), int(p[6]))
                for a, idx in enumerate((8, 10, 12, 14, 16, 18)):
                    tab[key][a] += int(p[idx])
            elif line.startswith('# K '):
                for a, idx in enumerate((5, 7, 9)):
                    kh[(p[2], int(p[3]))][a] += int(p[idx])
            elif line.startswith('# verify_fail'):
                vf += int(p[2])
            elif line.startswith('# max_steps'):
                maxm = max(maxm, int(p[2]))
        sv = c.with_suffix('.sv').read_text().splitlines()
        pr = c.with_suffix('.prob').read_text().splitlines()
        assert len(sv) == len(pr), c
        for a, b in zip(sv, pr):
            assert a.split()[1:2] == b.split('#')[1].split()[1:2]
            sv_rows.append((c.stem, a, b))
    assert dict(rooms_enum) == dict(rooms_shot), 'enumerated rooms != shot rooms'
    with open(d / 'totals.tsv', 'w') as f:
        f.write('class\tN\tW\teligible_rooms\tpairs\tlit\tunresolved\tlit_with_separating_Nmin\tunresolved_with_separating_Nmin\n')
        for (X, n, w), v in sorted(tab.items()):
            f.write('%s\t%d\t%d\t%s\n' % (X, n, w, '\t'.join(map(str, v))))
    with open(d / 'rooms.tsv', 'w') as f:
        f.write('N\tW\trooms\n')
        for (n, w), v in sorted(rooms_enum.items()):
            f.write('%d\t%d\t%d\n' % (n, w, v))
    with open(d / 'khist.tsv', 'w') as f:
        f.write('class\tk\tpairs\tlit\tunresolved\n')
        for (X, k), v in sorted(kh.items()):
            f.write('%s\t%d\t%s\n' % (X, k, '\t'.join(map(str, v))))
    with open(d / 'survivors.txt', 'w') as f:
        for stem, a, b in sv_rows:
            f.write('S %s %s\nQ %s\n' % (stem, a, b))
    print('%s: chunks %d nodes %d rooms %d verify_fail %d max_steps %d survivors %d' % (
        d, chunks, nodes, sum(rooms_enum.values()), vf, maxm, len(sv_rows)))
    for X in 'ABC':
        s = [sum(v[a] for (x, n, w), v in tab.items() if x == X) for a in range(6)]
        s22 = [sum(v[a] for (x, n, w), v in tab.items() if x == X and w <= 22) for a in range(6)]
        print('  class %s: eligible_rooms %d pairs %d lit %d unresolved %d | W<=22: eligible_rooms %d pairs %d lit %d unresolved %d'
              % (X, s[0], s[1], s[2], s[3], s22[0], s22[1], s22[2], s22[3]))


if __name__ == '__main__':
    for d in sys.argv[1:]:
        agg(d)
