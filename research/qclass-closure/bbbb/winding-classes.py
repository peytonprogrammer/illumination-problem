"""Read the saved d72 common cylinder and path per BBBB pair; no direction search."""
from collections import Counter
import json
from math import gcd
from pathlib import Path
import sys

archive = Path(__file__).resolve().parents[2] / 'illumination-generalization-2026-11-06/fable/directions-2026-11-09/d72-cylinder-test'
sys.path.insert(0, str(archive))
import cyl

def content2(n):
    return abs(n) & -abs(n)

def parity(x,y):
    g = gcd(x,y)
    return (x//g % 2, y//g % 2)

def winding_classes(origami, source, target, witness):
    v,sheet = witness
    basis = cyl.word(*v)
    r,u = cyl.act(origami.r,origami.u,basis)
    decomp = cyl.Decomp(origami,r,u)
    s = origami.lift(source,(1,1))
    t = origami.lift(target,tuple(sheet))
    assert decomp.cc(s,t)
    for step,sign in ((u,1),(cyl.inv(u),-1)):
        h,j = 0,s
        while decomp.reg[decomp.row[j]]:
            if decomp.row[j] == decomp.row[t]:
                offset,i = 0,j
                while i != t:
                    i,offset = r[i],offset+1
                C,i = 1,r[t]
                while i != t:
                    i,C = r[i],C+1
                assert not (offset%2 or C%2 or h%2)
                if h==0:
                    classes = {(1,0)}
                elif offset%content2(C) or h%content2(C):
                    classes = {parity(offset,h)}
                elif content2(C)==content2(h):
                    classes = {(0,1),(1,1)}
                else:
                    classes = {(1,0),(0,1),(1,1)}
                result=set()
                for x,y in classes:
                    for g,k in reversed(basis):
                        if g=='T':
                            x-=k*y
                        else:
                            y-=k*x
                    result.add((x%2,y%2))
                return result
            j,h = step[j],h+sign
            if j==s: break
    raise AssertionError('missing saved target row')

reports=json.loads((archive/'cyl_H40.json').read_text())
rooms=dict(cyl.rooms())
combined=Counter()
alone=Counter()
for name,report in reports.items():
    if report['group']!='BBBB': continue
    O=cyl.Origami(rooms[name])
    counts=Counter()
    for pair in report['pairs']:
        classes=winding_classes(O,tuple(pair['S']),tuple(pair['T']),pair['cc'])
        alone[len(classes)]+=1
        classes.add(parity(*pair['lit'][0]))
        counts[len(classes)]+=1
    combined.update(counts)
    print(name,sorted(counts.items()))
print('cylinder only',sorted(alone.items()),'plus saved straight witness',sorted(combined.items()))
assert sum(combined.values())==747
