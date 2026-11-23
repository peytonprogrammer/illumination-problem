"""Check the chain from the 18-wall input list to the open tile pairs."""
from collections import defaultdict
import gzip
from itertools import combinations_with_replacement
from pathlib import Path
base=Path(__file__).resolve().parent
def lines(name):
    return gzip.open(base/"results"/(name+".gz"),"rt")
def row(line):
    a,c,*_=line.split("|")
    h=a.split()
    return c.strip(),h[4]=="DONE" and h[12]=="0",int(h[11])
with lines("og18rooms") as f:
    need={" ".join(x.split()[2:]) for x in f}
print("initial",len(need))
lat=set()
for name in ("og18pass1","og18pass2","og18pass3","og-skipped"):
    seen=set()
    failed=set()
    for line in lines(name):
        c,ok,res=row(line)
        if name=="og-skipped" and c not in need:continue
        assert c not in seen
        seen.add(c)
        if not ok:failed.add(c)
        elif res:lat.add(c)
    assert seen==need
    need=failed
    print(name,len(need),"left")
pairs=defaultdict(set)
failed=defaultdict(list)
with lines("eighteen-pairs") as f:
    for line in f:
        c,ok,res=row(line)
        t,r,a,b=next(f).split()
        assert t=="CELLPAIR" and line.split()[1]==r
        p=(int(a),int(b))
        assert p not in pairs[c]
        pairs[c].add(p)
        if not ok:failed[c].append(p)
        elif res:lat.add(c)
assert set(pairs)==need and all(p==set(combinations_with_replacement(range(len(c.split())//2),2)) for c,p in pairs.items())
with gzip.open(base.parent/"witnesses.txt.gz","rt") as f:
    for line in f:
        if line.startswith("R "):
            a=line.split(maxsplit=5)
            if a[3]=="18":lat.discard(a[5].strip())
assert not lat
print(len(failed),"rooms remain")
for c,p in failed.items(): print("cells",c,"open tile pairs",p)
