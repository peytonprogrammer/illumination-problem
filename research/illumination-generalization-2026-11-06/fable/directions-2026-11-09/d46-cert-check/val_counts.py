"""d46 requirement 1: room counts from F*-off campaigns against the d9 census (free rooms per
(W, area), area <= 20, W <= 22) and against d44's exact fixed counts (cnt_14_25.log, W <= 14,
area <= 25).  usage: val_counts.py CAMPAIGN_DIR [CAMPAIGN_DIR ...]
Every census cell inside a campaign's (W, area) range must be present and equal.
"""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from aggregate import load  # noqa: E402

census = {tuple(map(int, k.split(','))): v['rooms']
          for k, v in json.load(open(HERE.parent / 'd9-census-w22' / 'census_totals.json'))['per_W_area'].items()}
d44 = {}
for ln in open(HERE.parent / 'd44-cert-check-sizing' / 'cnt_14_25.log'):
    m = re.match(r'\s+W (\d+) area (\d+) fixed (\d+)', ln)
    if m:
        W, a, fx = map(int, m.groups()); d44[(W, a)] = fx

for cdir in sys.argv[1:]:
    cfg, cells, shapes, tot, jobs, pos = load(cdir)
    wmin, wmax, amin, amax, cap5r, fstar, scope3, check = cfg['args']
    assert fstar == 0 and scope3 == 0, 'count validation needs F* and the scope filter off'
    assert len(jobs) == cfg['nj'], 'campaign incomplete'
    def inrange(W, a):
        return wmin <= W <= wmax and amin <= a <= min(amax, 5 * (W - 4) // 2 if cap5r else amax)
    ok = bad = 0
    for (W, a), v in sorted(census.items()):
        if not inrange(W, a):
            continue
        mine = cells.get((W, a), [0] * 6)[0]
        if mine == v:
            ok += 1
        else:
            bad += 1; print('  CENSUS MISMATCH W %d area %d census %d mine %d' % (W, a, v, mine))
    extra = [(W, a) for (W, a), v in cells.items() if v[0] and (W, a) not in census and a <= 20]
    ok2 = bad2 = 0
    for (W, a), v in sorted(d44.items()):
        if not inrange(W, a) or v == 0:
            continue
        mine = cells.get((W, a), [0] * 6)[1]
        if mine == v:
            ok2 += 1
        else:
            bad2 += 1; print('  D44 MISMATCH W %d area %d d44 fixed %d mine %d' % (W, a, v, mine))
    print('%s: census free counts: %d cells compared, %d match, %d mismatch; cells with rooms missing from census: %d; '
          'd44 fixed counts: %d cells compared, %d match, %d mismatch; free rooms total %d'
          % (cdir, ok + bad, ok, bad, len(extra), ok2 + bad2, ok2, bad2, sum(v[0] for v in cells.values())))
