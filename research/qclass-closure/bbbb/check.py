"""Arithmetic checks on DB55 and existing records. No candidate directions enumerated."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,product
from math import gcd, lcm
from pathlib import Path
import json
import sys
base=Path(__file__).resolve().parents[2]
src=next(base.glob('illumination-generalization*/fable/directions*/d72-cylinder-test')).parent
sys.path.insert(0,str(src/'d69-bbbb'))
from decomp import handbuilt,trace
data=json.loads((src/'d72-cylinder-test/cyl_H40.json').read_text())
chamber=set(product(range(1,5),repeat=2))
points=chamber|{(x+8,y) for x,y in chamber}
pairs={(s,t) for s,t in combinations(sorted(points),2) if all((a-b)%2==0 for a,b in zip(s,t))}
records=data['DB55']['pairs']
assert pairs=={(tuple(r['S']),tuple(r['T'])) for r in records}
periods=Counter()
for row in records:
    s,t=tuple(row['S']),tuple(row['T'])
    if s in chamber and t not in chamber:
        (p,q),_=row['lit']
        assert p and q
        # D72's lit predicate tests both senses on the saved direction line.
        assert any(trace(handbuilt()['DB55'],s,t,abs(p),abs(q),sense*(1 if p>0 else -1),sense*(1 if q>0 else -1),8*53+8,set()) for sense in (1,-1))
        periods[2*abs(p)//gcd(2*abs(p),abs(q))]+=1
assert len(pairs)==112 and sum(periods.values())==64 and lcm(2,*periods)==6
print('DB55 saved directions replayed for 64 cross-chamber pairs. Insertion periods:',dict(periods))
# Formula for both identical end chambers. d is the distance to the portal wall.
def entry(d,y):
    for j in range(5):
        run=d+10*j
        h=(F(y)+F(run,10))%10
        if 2<h<3 or 7<h<8:return run
    raise AssertionError((d,y))
legs=[entry(d,y) for d,y in chamber]
assert max(legs)<=44
assert F(44,450)<F(1,10)
print('DB55 endpoint access: 16 of 16 per chamber. Maximum horizontal travel at slope 1/10:',max(legs))
for row in data['cov2929']['pairs']:
    if (row['S'],row['T']) in [([3,1],[5,3]),([3,3],[5,5])]:
        print('cov2929 turning pair:',row)
for m,phases in [(1,[F(190,100),F(175,100)]),(3,[F(170,100),F(125,100)])]:
    # Bad arc from D58: [1+beta+kappa,2-beta].
    assert all(1+F(1,20)+F(m,16)<=v<=2-F(1,20) for v in phases)
print('D58: all four stored H/E phases stay inside their respective bad arcs.')
