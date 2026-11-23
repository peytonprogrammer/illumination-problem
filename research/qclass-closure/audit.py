"""Check room geometry, all endpoint pairs, retry coverage and small independent counts."""
import gzip
import itertools
from collections import Counter
from pathlib import Path

import sys
here=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
def records(name):
    cells=None
    with gzip.open(here/name,'rt') as data:
        for line in data:
            if line.startswith('R '):
                if cells is not None: yield cells,area,walls,rows
                fields=list(map(int,line.split()[1:]))
                _,area,walls=fields[:3]
                cells=tuple(zip(fields[4::2],fields[5::2]))
                rows=[]
            elif line.startswith('P '):
                row=line.split()
                assert 'VERIFYFAIL' not in row
                s,t=tuple(map(int,row[1:3])),tuple(map(int,row[3:5]))
                rows.append((tuple(sorted((s,t))),row[5]=='L'))
        if cells is not None:yield cells,area,walls,rows

def orbit_size(cells):
    shapes=set()
    for ex,ey in itertools.product((1,-1),repeat=2):
        xy=[(x*ex,y*ey) for x,y in cells]
        mx=min(x for x,y in xy);my=min(y for x,y in xy)
        norm=tuple(sorted((x-mx,y-my) for x,y in xy))
        shapes.add(norm);shapes.add(tuple(sorted((y,x) for x,y in norm)))
    return len(shapes)

retry={cells:{pair for pair,ok in rows if ok}
       for cells,_,_,rows in records('witnesses-retry.txt.gz')}
stats=Counter(); oriented=Counter(); byarea=Counter()
for cells,n,walls,rows in records('witnesses.txt.gz'):
    assert n==len(set(cells))
    degrees=Counter((x+i,y+j) for x,y in cells for i,j in ((0,0),(1,0),(0,1),(1,1)))
    assert sum(d in (1,3) for d in degrees.values())==walls<=20
    transparent={(x%2,y%2) for (x,y),d in degrees.items() if d in (2,4)}
    assert len(transparent)<4
    if n<=15:oriented[n]+=orbit_size(cells)
    marks=sorted(p for p,d in degrees.items() if d==4)
    assert len(rows)==len(marks)*(len(marks)-1)//2 and len(marks)>=2
    pairs=set(itertools.combinations(marks,2))
    other=retry.pop(cells,set())
    for pair,ok in rows:
        pairs.remove(pair)
        assert ok or pair in other
        same=all((x-y)%2==0 for x,y in zip(*pair))
        stats['same' if same else 'different']+=1
        stats['retry']+=not ok
    stats['rooms']+=1;byarea[n]+=1
assert not retry
for line in (here/'brute15.log').read_text().splitlines():
    fields=line.split()
    assert oriented[int(fields[1])]==int(fields[-1])
print(dict(stats))
print('area range',min(byarea),max(byarea),'rooms area >20',sum(v for n,v in byarea.items() if n>20))
print('independent fixed-room counts through area 15 match at each area')
