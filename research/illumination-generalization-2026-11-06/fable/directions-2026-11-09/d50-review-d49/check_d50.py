"""d50 read-only check on named rooms only (12-wall cross, 22-wall room). No search.

Reuses the d49 report() machinery (check_even.py, executed up to its room list only).
1. Per-target counterexample of d49 section 4: cross, S=(1,2), T=(2,2) (T_x - S_x odd),
   base (1/2)Z x Z. Expect Par at the V target d for all four lift pairs, nothing at b, c.
2. Same for the 22-wall room with S=(0,0), T=(1,2) if both are interior (checked).
"""
import sys, time
sys.dont_write_bytecode = True
from pathlib import Path
HERE = Path(__file__).resolve().parent
src = (HERE.parent / 'd49-even-index' / 'check_even.py').read_text()
src = src.split('\nR22 = ')[0].replace('Path(__file__).resolve().parent', 'Path(%r)' % str(HERE.parent / 'd49-even-index'))
g = {'__name__': 'ce'}
exec(compile(src, 'check_even_head', 'exec'), g)
report, status, cells_from_vertices = g['report'], g['status'], g['cells_from_vertices']
CROSS = {(i, j) for i in range(4) for j in range(1, 3)} | {(i, j) for i in range(1, 3) for j in range(4)}
R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
C22 = cells_from_vertices(R22)
print('cross (1,2),(2,2):', status(CROSS, (1, 2)), status(CROSS, (2, 2)))
for ab in ((2, 1), (1, 2)):
    report('12-wall cross, S=(1,2), T=(2,2)', CROSS, (1, 2), (2, 2), *ab)
for T in ((1, 2), (2, 0), (2, 1)):
    print('22-wall (0,0),%s:' % (T,), status(C22, (0, 0)), status(C22, T))
    if status(C22, T) == 'interior':
        for ab in ((2, 1), (1, 2)):
            report('22-wall room, S=(0,0), T=%s' % (T,), C22, (0, 0), T, *ab)
print('total CPU', round(time.process_time(), 3))
