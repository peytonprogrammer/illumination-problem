"""Reconcile counts, reproduce the FULL survivors, and identify the d205 control."""
from collections import Counter
import csv
import json
from pathlib import Path
import shutil
import sys

here=Path(__file__).resolve().parent
sys.path.insert(0,str(here.parent/'validator'))
import validate_w26 as validator

def rows(path):
    with path.open() as f:
        return list(csv.DictReader(f,delimiter='\t'))

def fingerprint(cells,marks):
    # Center and vertex coordinates on the doubled lattice share a translation.
    c=[(2*x+1,2*y+1) for x,y in cells]
    t=[(2*x,2*y) for x,y in marks]
    variants=[]
    for flip in (False,True):
        for sx in (-1,1):
            for sy in (-1,1):
                points=[(sx*y,sy*x) if flip else (sx*x,sy*y) for x,y in c+t]
                dx=min(x for x,y in points)
                dy=min(y for x,y in points)
                pts=[(x-dx,y-dy) for x,y in points]
                variants.append((sorted(pts[:len(c)]),sorted(pts[len(c):])))
    return min(variants)

def main():
    prod=here/'production'
    counts=rows(prod/'raw-counts.tsv')
    for folder,maxarea in [('gate11',11),('pilot',13)]:
        assert [r for r in counts if int(r['area'])<=maxarea]==rows(here/folder/'raw-counts.tsv')
    reference=[r for r in rows(here.parent/'validator/counts.tsv') if int(r['W']) in (22,24,26) and int(r['area'])<=11]
    assert reference==rows(here/'gate11/raw-counts.tsv')
    print('G2 matched',len(reference),'rows')
    key=lambda r:(int(r['area']),int(r['W']),r['bucket'])
    expected={key(r):int(r['pairs']) for r in counts}
    actual=Counter()
    totals=Counter()
    for r in rows(prod/'lighting.tsv'):
        n=int(r['pairs'])
        actual[key(r)]+=n
        totals[r['result']]+=n
    assert all(actual[k]==expected.get(k,0) for k in actual.keys()|expected.keys())
    dark=rows(prod/'dark.tsv')
    assert len(dark)==totals['FULL']
    assert len(rows(prod/'undecided.tsv'))==totals['CAP']+totals['CRASH']
    control=json.loads((here.parent.parent/'d205-census-a21/validation/PASS.json').read_text())['control_problem']
    left,right=[list(map(int,s.split()))[1:] for s in control.split('|')]
    ref=fingerprint(list(zip(left[::2],left[1::2])),list(zip(right[::2],right[1::2])))
    matched=[]
    for r in dark:
        cells=json.loads(r['complex'])
        adj=[c[2:] for c in cells]
        comp,info=validator.links(adj)
        marks=[json.loads(r[k]) for k in ('mark_a','mark_b')]
        qmap=[2,3,1,0]  # SW,SE,NW,NE to validator corner order
        ids=[comp[4*cell+qmap[q]] for (cell,q),point in marks]
        assert ids[0]!=ids[1] and all(info[i]==(4,True) for i in ids)
        (lit,states,full),src=validator.light(adj,comp,info)
        pair=tuple(sorted(src.index(i) for i in ids))
        assert full and pair not in lit
        print('independent FULL',key(r),'states',states,'production',r['states'],'marks',marks)
        if r['bucket']=='EMBEDDED' and int(r['W'])<=24:
            matched.append(key(r)==(15,22,'EMBEDDED') and fingerprint([c[:2] for c in cells],[p for root,p in marks])==ref and int(r['states'])==2592)
    assert matched==[True],matched
    print('G1 matched d205 control including marked coordinates up to D4 and translation')
    for source,target in [('raw-counts.tsv','counts.tsv'),('lighting.tsv','lighting.tsv'),('dark.tsv','dark.tsv'),('undecided.tsv','undecided.tsv')]:
        shutil.copyfile(prod/source,here/target)
    print('discs',sum(int(r['discs']) for r in counts),'pairs',sum(expected.values()),'dispositions',dict(totals))
    for bucket in ('EMBEDDED','TOUCHING','OVERLAP'):
        sub=[r for r in counts if r['bucket']==bucket]
        print(bucket,sum(int(r['discs']) for r in sub),sum(int(r['pairs']) for r in sub),sum(r['bucket']==bucket for r in dark))
if __name__=='__main__':main()
