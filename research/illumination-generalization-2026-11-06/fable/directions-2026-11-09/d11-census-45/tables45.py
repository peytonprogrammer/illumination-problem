"""Per-(W, N) result tables from agg45 totals and decide45 verdicts.

usage: python3 -B tables45.py census/star-32 [census/cstar-24]
Writes D/table_WN.tsv (group AB or C, W, N, rooms with a pair of the group,
pairs, lit, dark, undecided, undecided with k = 0) and prints Markdown tables
per W and per N.  "dark" means a finished orbit45 orbit; "undecided" means
orbit45 hit its cap.  Rooms with both A and B pairs count once in AB.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path


def load(d):
    d = Path(d)
    tab = defaultdict(lambda: [0] * 6)
    for line in (d / 'totals.tsv').read_text().splitlines()[1:]:
        p = line.split('\t')
        g = 'C' if p[0] == 'C' else 'AB'
        key = (g, int(p[2]), int(p[1]))
        tab[key][1] += int(p[4])
        tab[key][2] += int(p[5])
    rooms = {}
    for line in (d / 'rooms.tsv').read_text().splitlines()[1:]:
        n, w, c = map(int, line.split('\t'))
        rooms[(w, n)] = c
    dec = d / 'decide45.json'
    for r in json.loads(dec.read_text()) if dec.exists() else []:
        g = 'C' if r['cls'] == 'C' else 'AB'
        v = r['orbit45']['verdict']
        t = tab[(g, r['W'], r['N'])]
        if v == 'DARK':
            t[3] += 1
        elif v == 'UNDECIDED_CAP':
            t[4] += 1
            t[5] += r['k'] == 0
        else:
            raise SystemExit('survivor decided LIT by orbit45: %r' % r)
    return d, tab, rooms


def main():
    for dd in sys.argv[1:]:
        d, tab, rooms = load(dd)
        group = 'C' if 'cstar' in d.name else 'AB'
        with open(d / 'table_WN.tsv', 'w') as f:
            f.write('group\tW\tN\trooms_with_pair\tpairs\tlit\tdark\tundecided\tundecided_k0\n')
            for (g, w, n), v in sorted(tab.items()):
                if g == group:
                    f.write('%s\t%d\t%d\t%d\t%s\n' % (g, w, n, rooms.get((w, n), 0), '\t'.join(map(str, v[1:]))))
        for by, name in ((1, 'W'), (2, 'N')):
            agg = defaultdict(lambda: [0] * 6)
            for (g, w, n), v in tab.items():
                if g != group:
                    continue
                k = (w, n)[by - 1]
                for a in range(1, 6):
                    agg[k][a] += v[a]
            for (w, n), c in rooms.items():
                agg[(w, n)[by - 1]][0] += c
            print('\n%s, %s: per %s\n' % (d, group, name))
            print('| %s | rooms with a pair | pairs | lit | dark | undecided (k = 0) |' % name)
            print('|---:|---:|---:|---:|---:|---:|')
            for k in sorted(agg):
                v = agg[k]
                print('| %d | %d | %d | %d | %d | %d (%d) |' % (k, v[0], v[1], v[2], v[3], v[4], v[5]))
            t = [sum(v[a] for v in agg.values()) for a in range(6)]
            print('| all | %d | %d | %d | %d | %d (%d) |' % tuple(t))


if __name__ == '__main__':
    main()
