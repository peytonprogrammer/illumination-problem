"""Canonical class types of family members via d66 pair_level.test_room (as d69 verdicts.py)."""
import sys, time
from pathlib import Path
D = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(D / 'd66-pair-level')); sys.path.insert(0, str(D / 'd69-bbbb'))
import pair_level as PL
import decomp
from room import cells
hb = decomp.handbuilt()
assert hb['DBas'] == cells(4), "DBas cells differ from d69"
print("DBas cells identical to d69 decomp.py: True")
for l in map(int, sys.argv[1:]):
    t0 = time.process_time(); rows = []
    R = PL.test_room(f"fam{l}", cells(l), 2000, rows)
    print(f"l={l} n={R['n']} r={R['r']} W={R['W']} norm={R['normalized']} types={R['types']} "
          f"counts={R['counts']} CPU {time.process_time()-t0:.1f}s", flush=True)
