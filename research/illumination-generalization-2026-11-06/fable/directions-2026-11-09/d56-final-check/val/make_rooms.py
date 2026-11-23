"""Validation room lists (seeded): random strictly simple W = 20, area-20 rooms (Set A shape), and
class (iii) rooms in the Set E range taken from Part A's C3 lists (area <= 12)."""
import sys, random, glob
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'd10-mechanisms'))
from roomtools import is_strictly_simple, ledger  # noqa
random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
want = int(sys.argv[1])
out = []
while len(out) < want:
    cells = {(0, 0)}
    while len(cells) < 20:
        i, j = random.choice(sorted(cells))
        cells.add(random.choice([(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]))
    if not is_strictly_simple(cells):
        continue
    if ledger(cells)['W'] != 20:
        continue
    mx = min(c[0] for c in cells); my = min(c[1] for c in cells)
    out.append('20 20 ' + ' '.join('%d %d' % (x - mx, y - my) for x, y in sorted(cells)))
with open(HERE / 'roomsA.txt', 'w') as f:
    f.write('\n'.join(out) + '\n')
e = []
for fn in sorted(glob.glob(str(HERE.parent.parent / 'd9-census-w22/runs/partA/a16/job-*.rf'))):
    for line in open(fn):
        v = line.split()
        if v[0] == 'C3' and 12 <= int(v[2]) <= 20 and int(v[1]) <= int(v[2]) - 4:
            e.append(' '.join(v[1:]))
random.shuffle(e)
with open(HERE / 'roomsE.txt', 'w') as f:
    f.write('\n'.join(e[:want]) + '\n')
print(len(out), 'A rooms;', len(e), 'C3 rooms in E range with area <= 12, wrote', min(want, len(e)))
