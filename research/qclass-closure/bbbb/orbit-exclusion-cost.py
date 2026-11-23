"""Aggregate a corner-incidence statistic on d144's fixed cov4181 permutation orbit."""
from collections import Counter, deque
from pathlib import Path
import runpy

review = Path(__file__).resolve().parents[2] / 'illumination-generalization-2026-11-06/fable/directions-2026-11-09/d144-review-dyadic/checks.py'
d = runpy.run_path(str(review))
cols = [range(6), (2,3), (2,3), range(6), range(6), (2,3), (2,), range(3)]
room = {(x,y) for x, col in enumerate(cols) for y in col}
o = d['build_origami'](room, (2,3), (4,3))
canon, inv, compose = (d[k] for k in ('canon','inv','compose'))


def incidence(h, v, labels):
    """Read the S/T labels of cut-cycle intervals incident to a reflex."""
    comm = compose(v, compose(h, compose(inv(v), inv(h))))
    assert sum(i != j for i,j in enumerate(comm)) == 24
    assert all(labels[i] == 'X' for i,j in enumerate(comm) if i != j)
    visited = set()
    incident = set()
    target_lengths = []
    for i in range(len(v)):
        if i in visited:
            continue
        cycle = []
        j = i
        while j not in visited:
            visited.add(j)
            cycle.append(j)
            j = v[j]
        if any(labels[k]=='T' for k in cycle):
            assert all(comm[k]==k and labels[k]!='S' for k in cycle)
            target_lengths.append(len(cycle))
        cuts = [k for k,j in enumerate(cycle) if labels[j]=='X']
        if not cuts:
            assert not {'S','T'} <= {labels[j] for j in cycle}
            continue
        for a,b in zip(cuts, cuts[1:] + [cuts[0]+len(cycle)]):
            ends = cycle[a], cycle[b % len(cycle)]
            marks = {labels[cycle[k % len(cycle)]] for k in range(a+1,b)} & {'S','T'}
            assert len(marks) < 2
            if any(comm[end] != end for end in ends):
                incident.update(marks)
    return (''.join(sorted(incident)) or 'neither'), target_lengths


initial = canon(o['h'],o['v'],[a[0] for a in o['corner']]), ((1,0),(0,1))
seen = {initial}
queue = deque([initial])
hist = Counter()
periods = Counter()
while queue:
    (h,v,labels), mod = queue.popleft()
    (a,b),(c,e) = mod
    if (b,a)==(0,1):
        who, lengths = incidence(h,v,labels)
        hist[who] += 1
        periods.update(lengths)
    # Identical two d144 transitions, retaining only the six mod-2 matrices.
    for h2,v2,m2 in [(h,compose(v,inv(h)),((a^c,b^e),(c,e))),
                      (compose(h,inv(v)),v,((a,b),(c^a,e^b)))]:
        key = canon(h2,v2,labels),m2
        if key not in seen:
            seen.add(key)
            assert len(seen) <= 3888
            queue.append(key)
assert len(seen)==3888 and sum(hist.values())==1296
print('reviewed states:',len(seen),'class states:',sum(hist.values()))
print({k:hist[k] for k in ('neither','S','T','ST')})
print('uncut target-cycle lengths and multiplicities:',dict(sorted(periods.items())))
