"""Class-level darkness per corner (saved data only).

For a Nielsen class (ordered cycle types) and a corner x, say the class is x-empty when no
tuple of the class, in any pure-braid orbit, has two distinct regular points over a joined
by a chain at x.  This is a property of cycle types alone.  The script lists x-empty
classes in which g_x has a 2-cycle and g_a has two 2-cycles, and compares with the
certificates Par / Rig / Cut over B.
"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
for n in [int(a) for a in sys.argv[1:]]:
    d = json.loads((HERE / f'mine_n{n}.json').read_text())
    cls = defaultdict(list)
    for o in d['orbits']:
        cls[json.dumps(o['cts'])].append(o)
    S = Counter()
    for key, orbs in cls.items():
        cts = json.loads(key)
        for xi in range(3):
            if 2 not in cts[xi + 1]:
                continue
            S['class-corners with a 2-cycle at x'] += 1
            anylit = any(p['lit_x'][xi] for o in orbs for p in o['pairs'])
            if anylit:
                continue
            S['x-empty class-corners'] += 1
            allcert = all(p['cert_x'][xi] for o in orbs for p in o['pairs'])
            S['x-empty, every pair certified over B' if allcert else 'x-empty, some pair NOT certified over B'] += 1
            if not allcert:
                print('  ', n, 'x-empty without certificate:', cts, 'x=' + 'bcd'[xi],
                      [(o['order'], o['primitive'], o['plain'], sum(1 for p in o['pairs'] if not p['cert_x'][xi]), len(o['pairs'])) for o in orbs])
    # exceptions that are not class-level
    for o in d['orbits']:
        for xi in range(3):
            exc = [p for p in o['pairs'] if not p['lit_x'][xi] and not p['cert_x'][xi]]
            if exc:
                orbs = cls[json.dumps(o['cts'])]
                if any(p['lit_x'][xi] for oo in orbs for p in oo['pairs']):
                    S['uncertified x-dark pair-corners in a class that is not x-empty'] += len(exc)
                else:
                    S['uncertified x-dark pair-corners in an x-empty class'] += len(exc)
    print(n, dict(S))
