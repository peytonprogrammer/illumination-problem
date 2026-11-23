"""Reconcile the two complete room lists, all successive passes and lattice witnesses."""
from collections import Counter, defaultdict
import gzip
from itertools import combinations_with_replacement
from pathlib import Path

base = Path(__file__).resolve().parent
def lines(name):
    return gzip.open(base / "results" / (name + ".gz"), "rt")
def canon(raw):
    # Width and height are at most 15. Pack a normalized (x,y) in one byte.
    xy = list(zip(raw[::2], raw[1::2]))
    w = max(x for x,y in xy)
    h = max(y for x,y in xy)
    options = [[] for _ in range(8)]
    for x,y in xy:
        for i,(a,b) in enumerate(((x,y),(w-x,y),(x,h-y),(w-x,h-y))):
            options[i].append(16*a+b)
            options[i+4].append(16*b+a)
    return min(bytes(sorted(v)) for v in options)
def census(name):
    rows = {}
    for line in lines(name):
        n,w,*xy = map(int,line.split())
        assert n==15 and len(xy)==30
        key=canon(xy)
        assert key not in rows
        rows[key]=w
    return rows
rooms=census("og15rooms")
assert rooms == census("og-brute15rooms")
print("Independent census agrees by shape and wall count:",sorted(Counter(rooms.values()).items()))
def row(line):
    header,cells,*_=line.split('|')
    a=header.split()
    return tuple(map(int,cells.split())), a[4]=="DONE" and int(a[12])==0, int(a[11]), int(a[3])
pending=None
lattice=set()
for name in ("og15pass1","og15pass2","og-skipped"):
    seen=set()
    failed=set()
    for line in lines(name):
        cells,ok,res,w=row(line)
        if name=="og-skipped" and cells not in pending: continue
        assert cells not in seen
        seen.add(cells)
        if pending is None: assert rooms[canon(cells)]==w
        if not ok: failed.add(cells)
        elif res: lattice.add(cells)
    if pending is None: assert len(seen)==len(rooms)==len({canon(c) for c in seen})
    else: assert pending==seen
    pending=failed
    print(name,len(seen),"rooms;",len(pending),"remain")
checked=defaultdict(set)
with lines("final-pairs") as inp:
    for line in inp:
        cells,ok,res,w=row(line)
        t,r,a,b=next(inp).split()
        assert t=="CELLPAIR" and line.split()[1]==r and ok and cells in pending
        pair=(int(a),int(b))
        assert pair not in checked[cells]
        checked[cells].add(pair)
        if res: lattice.add(cells)
assert set(checked)==pending
assert all(p==set(combinations_with_replacement(range(15),2)) for p in checked.values())
print("Final tile pairs:",sum(map(len,checked.values())),"of",len(pending)*120)
need=lattice.copy()
with gzip.open(base.parent/"witnesses.txt.gz","rt") as inp:
    for line in inp:
        if line.startswith("R "):
            a=line.split()
            if a[2]=="15": need.discard(tuple(map(int,a[5:])))
assert not need
print("All",len(lattice),"rooms with accepted lattice residuals found in previously replayed lattice census.")
