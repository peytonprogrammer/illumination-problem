"""D103: classify every saved room by the stage that accepted it, then draw fixed-seed samples.

Usage: python3 -B sample.py WORKDIR NSHARDS LABEL N_WHOLE N_TILE OUT
Reads only the saved archives (i*, a*..d*, hard/*). Writes OUT with lines
  <class> <shard-index> <room line>
where class is a/b/c/d (whole-room stage) or hard:<dir>.
"""
import random, sys
from pathlib import Path
from collections import Counter
root = Path(sys.argv[1]); nsh = int(sys.argv[2]); label = sys.argv[3]
nwhole, ntile = int(sys.argv[4]), int(sys.argv[5]); out = Path(sys.argv[6])
whole = []; hard = []; cnt = Counter(); total = 0
for k in range(nsh):
    todo = [(i, l) for i, l in enumerate((root / f'i{k}').read_text().splitlines())]
    total += len(todo)
    for st in 'abcd':
        left = []
        with (root / f'{st}{k}').open() as f:
            for (idx, room), line in zip(todo, f, strict=True):
                head, cells, pts = line.split('|')
                a = head.split()
                assert f'{a[2]} {a[3]} {cells.strip()}' == room
                if a[4] == 'DONE' and a[12] == '0':
                    whole.append((st, f'{k}-{idx}', room, int(a[11]))); cnt[st] += 1
                else:
                    left.append((idx, room))
        if st == 'd':
            hard_here = [(pos, room) for pos, (idx, room) in enumerate(todo) if (idx, room) in set(left)]
        todo = left
    for idx, room in hard_here:
        d = root / 'hard' / f'{k}-{idx}'
        assert (d / 'room').read_text().strip() == room
        hard.append((f'hard', f'{k}-{idx}', room, -1))
print(label, 'rooms', total, 'stages', dict(cnt), 'tile-level', len(hard))
rng = random.Random(103)
pick = rng.sample(whole, min(nwhole, len(whole))) + rng.sample(hard, min(ntile, len(hard)))
with out.open('w') as f:
    for st, key, room, ll in pick:
        print(st, key, ll, room, file=f)
print(label, 'sampled', Counter(p[0] for p in pick))
