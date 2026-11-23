"""d46: cross-check sampled rooms (lines "n x0 y0 ...") between cert_check (C, stdin mode) and
verify_room.py methods I and II.  Compares r, corner classes, rho, F* verdict (C fstar_pass vs
d44 filter_rate.passes), pair count, positive pairs, and every B_x block count C computed (C stops
at the first one-block partition of each mark class).
usage: val_sample.py ROOMFILE [ROOMFILE ...]
"""
import re, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_room import verify  # noqa: E402

lines = []
for f in sys.argv[1:]:
    lines += [ln for ln in open(f).read().splitlines() if ln.strip() and ln[0].isdigit()]
out = subprocess.run([str(HERE / 'cert_check'), 'stdin', 'v'], input='\n'.join(lines) + '\n',
                     capture_output=True, text=True, check=True).stdout
crow = []
for ln in out.splitlines():
    if ln.startswith('room'):
        crow.append({'line': ln, 'pos': 0})
    elif 'POSITIVE' in ln:
        crow[-1]['pos'] += 1
assert len(crow) == len(lines)
stats = dict(rooms=0, mismatch=0, fstar_pass=0, positives=0, block_compared=0, scope3=0)
for ln, c in zip(lines, crow):
    v = list(map(int, ln.split())); cells = set(zip(v[1::2], v[2::2]))
    p = verify(cells)
    m = re.match(r'room \d+ n (\d+) r (\d+) corner_classes (\d+) rho (\d+) (\d+) (\d+) (\d+) pairs (\d+) positives (\d+) fstar (\d+)', c['line'])
    n, r, ncls, r0, r1, r2, r3, pairs, pos, fs = map(int, m.groups())
    bad = []
    if (n, r, ncls, [r0, r1, r2, r3], pairs) != (p['n'], p['r'], p['ncls'], p['rho'], p['pairs']):
        bad.append('geometry')
    if bool(fs) != p['fstar']:
        bad.append('fstar')
    if not (pos == len(p['posI']) == len(p['posII'])):
        bad.append('positives')
    if p['blocksI'] != p['blocksII']:
        bad.append('blocks I vs II')
    for o, a, b, cc, dd in re.findall(r'o\((\d),(\d)\) marks \d+ bcd (\d+) (\d+) (\d+)', c['line']):
        key = (int(o), int(a)); cb = [int(b), int(cc), int(dd)]
        for k in range(3):
            if cb[k] == 0:
                break
            stats['block_compared'] += 1
            if cb[k] != p['blocksI'][key][k]:
                bad.append('block count'); break
            if cb[k] == 1:
                break
    stats['rooms'] += 1; stats['fstar_pass'] += p['fstar']; stats['positives'] += len(p['posI'])
    stats['scope3'] += p['ncls'] >= 3
    if bad:
        stats['mismatch'] += 1
        print('MISMATCH', bad, ln[:200])
print('sample cross-check:', ' '.join('%s %d' % kv for kv in stats.items()))
