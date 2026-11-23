"""Reconcile all 20-wall rooms, residual boxes and proofs by cell coordinates."""
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import gzip
from itertools import combinations_with_replacement
from pathlib import Path
import sys
from rational import point,tracer
from verify_boxes import verify_axis
base=Path(__file__).resolve().parent
root=Path(sys.argv[1])
def parse(line):
    h,c,pair=line.split('|');a=h.split()
    return a,c.strip(),pair.strip()
def check_hard(d,room):
    assert room==(d/'room').read_text().strip()
    flat=list(map(int,room.split()));n=flat[0];cells=list(zip(flat[2::2],flat[3::2]));C=set(cells)
    pairs=set();pts=set();boxes=set();ll=False
    rows=iter((d/'tiles').read_text().splitlines())
    buf=[]
    for l in rows:
        if l.startswith('BOX '):
            buf.append(tuple(map(int,l.split()[2:])));continue
        a,c,pt=parse(l);assert tuple(map(int,c.split()))==tuple(flat[2:])
        tag,r,i,j=next(rows).split();p=int(i),int(j)
        assert tag=='CELLPAIR' and r==a[1]=='1' and p not in pairs
        pairs.add(p)
        assert (a[4]=='RESID' and buf) or (a[4]=='DONE' and not buf)
        ll |= int(a[11])>0
        for b in buf:
            assert b[:2]==p and len(b)==5 and b not in boxes
            boxes.add(b)
        buf=[]
        assert len(pt.split())==int(a[12])
        pts.update(pt.split())
    assert not buf and pairs==set(combinations_with_replacement(range(n),2))
    for l in (d/'rational').read_text().splitlines():
        xy,v,x,y=l.split();pts.remove(xy);s,t=map(point,xy.split(';'))
        den,_,_,test=tracer(C,s,t);assert den==int(v) and test(int(x),int(y))
    assert not pts,(d,pts)
    nt=nl=0
    if (d/'pixel').is_dir():
        from pixel_finish import verify
        verify(d)
        regular=sum(all((x-j,y-k) in C for j in (0,1) for k in (0,1)) for x,y in C)
        return ll or regular>=2,len(pairs),len(boxes),0,0
    if boxes:
        skip=[set(),set()]
        for meta in d.glob('alternate/*/axis'):
            key=tuple(map(int,meta.parent.name.split('_')))
            assert key in boxes
            i,j,k,l,r=key
            chosen=int(meta.read_text());assert chosen in (0,1)
            for axis in (0,1):
                orient=lambda c:c[::-1] if axis else c
                oriented=set(map(orient,cells));marks=[];exposed=False
                for c,corner in ((i,k),(j,l)):
                    x,y=cells[c];center=orient((x+(corner&1),y+(corner>>1)))
                    a,b=orient((x,y));marks.extend((c,*center,a,b))
                    exposed|=(a,b+(1 if center[1]==b+1 else -1)) not in oriented
                skip[axis].add((tuple(marks),r))
                if axis==chosen:
                    assert exposed
                    pp=meta.parent/str(axis)
                    assert (pp/'room').read_bytes()==(d/'shears'/str(axis)/'room').read_bytes()
                    assert list(pp.glob('ends-*'))==[pp/f'ends-{r}']
                    assert list(map(int,(pp/f'ends-{r}').read_text().split()))==marks
                    t,lvs=verify_axis(pp,standalone=True);nt+=t;nl+=lvs
        for swap in (0,1):
            path=d/'shears'/str(swap)
            f=list(map(int,(path/'room').read_text().split()));assert f[:2]==flat[:2]
            assert list(zip(f[2::2],f[3::2]))==[c[::-1] if swap else c for c in cells]
            observed=set()
            for ends in path.glob('ends-*'):
                rad=int(ends.name.split('-')[1])
                for line in ends.read_text().splitlines():
                    vals=list(map(int,line.split()));ids=[];ks=[];centers=[]
                    for e in [0,5]:
                        i,x,y,a,b=vals[e:e+5]
                        if swap:x,y,a,b=y,x,b,a
                        assert cells[i]==(a,b);ids.append(i);ks.append((x-a)+2*(y-b));centers.append((x,y))
                    key=(*ids,*ks,rad);assert key not in observed;observed.add(key)
                    if centers[0]!=centers[1] and all(all((x-h,y-k) in C for h in [0,1] for k in [0,1]) for x,y in centers):ll=True
            assert observed==boxes
            t,l=verify_axis(path,skip[swap]);nt+=t;nl+=l
    return ll,len(pairs),len(boxes),nt,nl
if __name__=='__main__':
    count=Counter(); seen=set(); lattice=set(); hard=[]
    small='--lower' in sys.argv
    for k in range(2 if small else 10):
        initial=(root/f'i{k}').read_text().splitlines()
        for l in initial:
            assert l not in seen and (int(l.split()[1])<18 if small else int(l.split()[1])==20);seen.add(l)
        todo=initial
        for stage in 'abcd':
            left=[]
            with (root/f'{stage}{k}').open() as f:
                for idx,l in enumerate(todo):
                    a,c,_=parse(next(f))
                    assert int(a[1])==idx+1 and l==f'{a[2]} {a[3]} {c}'
                    if a[4]=='DONE' and a[12]=='0':
                        count[stage]+=1
                        if int(a[11]):lattice.add(c)
                    else:
                        left.append(l)
                        if stage=='d':hard.append((root/'hard'/f'{k}-{idx}',l))
                assert next(f,None) is None
            todo=left
    assert len(seen)==(26706 if small else 913622)
    with ProcessPoolExecutor(max_workers=5) as pool:
        results=list(pool.map(check_hard,[d for d,_ in hard],[r for _,r in hard]))
    for (d,room),(lat,p,b,t,l) in zip(hard,results):
        if lat:lattice.add(room.split(' ',2)[2])
        count['tilepairs']+=p;count['boxes']+=b;count['trees']+=t;count['leaves']+=l
    nlat=len(lattice)
    with gzip.open(base.parent/'witnesses.txt.gz','rt') as f:
        for line in f:
            if line.startswith('R '):
                a=line.split(maxsplit=5)
                if (int(a[3])<18 if small else a[3]=='20'):lattice.discard(a[5].strip())
    assert not lattice
    assert len(seen)==sum(count[k] for k in 'abcd')+len(hard)
    print(len(seen),'rooms. Accepted whole-room checks',dict(count),'; tile-by-tile rooms',len(hard))
    print(nlat,'rooms with lattice residuals matched the previous full lattice-path census.')
