"""Audit the exact residual geometry and produce the shear inputs."""
from ast import literal_eval
from fractions import Fraction
from pathlib import Path
import sys
base=Path(__file__).resolve().parent
out=Path(sys.argv[1])
rooms=[]
expected=set()
for line in (base.parent/'offgrid/results/eighteen-audit.txt').read_text().splitlines():
    if not line.startswith('cells '): continue
    coords,pairs=line[6:].split(' open tile pairs ')
    xy=list(map(int,coords.split()))
    r=len(rooms)
    rooms.append(list(zip(xy[::2],xy[1::2])))
    expected.update((r,i,j) for i,j in literal_eval(pairs))
centers={}
finished=set()
radius=Fraction(0)
regions=0
for line in (out/'regions.txt').open():
    if line.startswith('CELLPAIR'):
        _,r,i,j=line.split()
        token=(int(r)-1,int(i),int(j))
        assert token not in finished
        finished.add(token)
    if not line.startswith('REG '):continue
    h,u,v=line.split('|')
    r,i,j,source=map(int,h.split()[1:]);r-=1
    assert source in (i,j)
    ends=[]
    for poly in ([u,v] if source==i else [v,u]):
        pts=list(map(int,poly.split()))
        assert pts and len(pts)%3==0
        x0,y0,d0=pts[:3]
        cx,cy=round(Fraction(x0,d0)),round(Fraction(y0,d0))
        for x,y,d in zip(pts[::3],pts[1::3],pts[2::3]):
            deviation=max(abs(x-cx*d),abs(y-cy*d))
            assert 17*deviation<=d
            radius=max(radius,Fraction(deviation,d))
        ends.append((cx,cy))
    key=(r,i,j)
    assert centers.setdefault(key,ends)==ends
    regions+=1
assert set(centers)==finished==expected
for r,cells in enumerate(rooms):
    for swap in [0,1]:
        def pos(v):return v[::-1] if swap else v
        with (out/f'room{r}{swap}').open('w') as f:
            print(18,18,*(z for c in cells for z in pos(c)),file=f)
        with (out/f'ends{r}{swap}').open('w') as f:
            for (s,i,j),(a,b) in sorted(centers.items()):
                if r!=s:continue
                for cell,p in ((i,a),(j,b)):
                    assert sum((p[0]-u,p[1]-v) in cells for u in (0,1) for v in (0,1))<4
                    print(cell,*pos(p),*pos(cells[cell]),end=' ',file=f)
                print(file=f)
print(regions,'residual polygon products;',len(expected),'tile pairs; maximum coordinate displacement',radius)
