"""d52 step 2: filter and tabulate the enumerated quotients K (x = (0, 0)).

Admissible as N_x of a positive room with r <= RMAX (memo section 1):
  K1 genus 0, x has no regular point                    (enforced in enum_K)
  K2 singular points (cvx, rfx, cone) in >= 3 classes   (P has corners in >= 3 classes; Fact L)
  K3 1 <= z and some delta >= 3 with delta * z <= RMAX (delta even if K has a cone)
  K4 some class a != x has >= 2 non-rfx orbits (two distinct images for S, T)
Also reports d36.4's bound d <= 4z + 1 (4z if d even) on the survivors.
Usage: python3 -B analyze_K.py K.json RMAX [zmax]
"""
import json
import sys
from collections import Counter


def deltas(k, rmax):
    return [dl for dl in range(3, rmax + 1) if dl * k['z'] <= rmax and (k['cone'] == 0 or dl % 2 == 0)]


def admissible(k, rmax):
    reasons = []
    if len(k['sing']) < 3:
        reasons.append('K2')
    if k['z'] < 1 or not deltas(k, rmax):
        reasons.append('K3')
    if not any(sum(1 for t in k['types'][a] if t != 'rfx') >= 2 for a in ('10', '01', '11')):
        reasons.append('K4')
    return reasons


if __name__ == '__main__':
    recs = json.load(open(sys.argv[1]))
    rmax = int(sys.argv[2])
    zmax = int(sys.argv[3]) if len(sys.argv) > 3 else 99
    recs = [k for k in recs if k['z'] <= zmax]
    print('K enumerated:', len(recs), ' by (z, cone):', sorted(Counter((k['z'], k['cone']) for k in recs).items()))
    rej = Counter()
    keep = []
    for k in recs:
        rs = admissible(k, rmax)
        if rs:
            rej[tuple(rs)] += 1
        else:
            keep.append(k)
    print('rejected by filter:', dict(rej))
    print('admissible:', len(keep))
    bad = [k for k in keep if k['d'] > (4 * k['z'] + 1 if k['d'] % 2 else 4 * k['z'])]
    print('admissible K violating d36.4 bound:', len(bad))
    print('max d among all enumerated with >= 3 singular classes:',
          max([k['d'] for k in recs if len(k['sing']) >= 3] or [0]))
    print('\n| # | d | z | cone | deltas | types x=00 | 10 | 01 | 11 |')
    print('|---|---|---|---|---|---|---|---|---|')
    for i, k in enumerate(keep):
        T = k['types']
        f = lambda ts: ','.join('%s%d' % (t, ts.count(t)) for t in ('cvx', 'smooth', 'rfx', 'cone', 'int') if ts.count(t))
        print('| %d | %d | %d | %d | %s | %s | %s | %s | %s |' % (i, k['d'], k['z'], k['cone'],
              ','.join(map(str, deltas(k, rmax))), f(T['00']), f(T['10']), f(T['01']), f(T['11'])))
    if len(sys.argv) > 4:
        json.dump(keep, open(sys.argv[4], 'w'))
