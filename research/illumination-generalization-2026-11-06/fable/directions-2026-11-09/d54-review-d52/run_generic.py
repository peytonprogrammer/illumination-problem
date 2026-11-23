"""d54: finish d52's model-free cross-check (validate_generic.generic_covers vs enum_P.covers) on
named (K, delta) cases. Usage: python3 -B run_generic.py CPU_CAP K:delta [K:delta ...]
The CPU cap (seconds, whole process) is enforced by RLIMIT_CPU; each case prints when done."""
import json
import resource
import sys
import time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fold import *  # noqa
import enum_P  # noqa
from validate_generic import generic_covers  # noqa

if __name__ == '__main__':
    cap = int(sys.argv[1])
    resource.setrlimit(resource.RLIMIT_CPU, (cap, resource.getrlimit(resource.RLIMIT_CPU)[1]))
    adm = json.load(open(HERE / 'data/K_adm_r8.json'))
    for arg in sys.argv[2:]:
        ki, dl = map(int, arg.split(':'))
        k = adm[ki]
        K = [list(r) for r in k['canon']]
        t1 = time.process_time()
        gen = set(generic_covers(K, dl, 8))
        t2 = time.process_time()
        coll = set()
        res, stats, st = enum_P.covers(K, k['z'], dl, 8, collect=coll)
        npos = sum(1 for c in gen if positives([list(r) for r in c])[0])
        print('K%d d=%d z=%d cone=%d delta=%d: generic %d, arc model %d, missing %d, extra %d, '
              'generic positives %d, generic CPU %.1f s%s' % (
                  ki, k['d'], k['z'], k['cone'], dl, len(gen), len(coll), len(gen - coll),
                  len(coll - gen), npos, t2 - t1, '' if gen == coll else '  <-- MISMATCH'), flush=True)
