"""d52: count admissible quotients modulo the V<->H mirror (the only square symmetry fixing x)."""
import json
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fold import canon  # noqa
for f in sys.argv[1:]:
    recs = json.load(open(f))
    keys = {tuple(tuple(r) for r in k['canon']): k for k in recs}
    orb = set()
    by = Counter()
    for kc, k in keys.items():
        m = canon([list(kc[2]), list(kc[3]), list(kc[0]), list(kc[1])])
        rep = min(kc, m)
        if rep not in orb:
            orb.add(rep)
            by[(k['d'], k['z'], k['cone'])] += 1
    print(f, 'shapes:', len(recs), 'modulo V<->H mirror:', len(orb))
    print('  by (d, z, cone):', dict(sorted(by.items())))
