"""d69: exact pair verdicts (d66 pair_level.test_room, pure-braid orbit model) on the hand-built
rooms of decomp.py: types of the four classes, R* membership, and the pair-level verdict.
Usage: python3 -B verdicts.py ROOM [ROOM ...] [--states N]
"""
import resource
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE.parent
sys.path.insert(0, str(D / 'd66-pair-level'))
import pair_level as PL  # noqa: E402  (path setup; CPU cap 560 s)
import decomp  # noqa: E402

resource.setrlimit(resource.RLIMIT_CPU, (300, 300))

if __name__ == '__main__':
    args = sys.argv[1:]
    states = 20000
    if '--states' in args:
        i = args.index('--states')
        states = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    hb = decomp.handbuilt()
    for name in args:
        t0 = time.process_time()
        rows = []
        R = PL.test_room(name, hb[name], states, rows)
        lit = {}
        for r in rows:
            lit.setdefault((tuple(r['S']), tuple(r['T'])), (r['pair_lit'], r['lit_targets']))
        print(name, 'n', R['n'], 'r', R['r'], 'W', R['W'], 'norm', R['normalized'], 'types', R['types'],
              'R*', R['Rstar'], R['counts'], 'CPU %.1f s' % (time.process_time() - t0), flush=True)
        for k, v in sorted(lit.items()):
            print('   x-dark row pair', k, 'pair lit', v[0], 'lit targets', v[1])
