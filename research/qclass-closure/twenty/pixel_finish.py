"""Create and verify a reciprocal-bin certificate for one difficult room."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from math import lcm
import gzip,os,subprocess,sys
from box_room import generate
from verify_boxes import verify_axis
from verify_pixels import check as check_pixels
def verify(d):
    p=d/'pixel';grid=p/'grid';near=p/'near'
    def normal(file):
        return (l for l in file.open() if l.startswith(('ROOM ','CELLPAIR ')))
    assert list(normal(grid))==list(normal(d/'tiles'))
    pending=set();total=0
    for l in grid.open():
        if l.startswith('PIX '):
            _,a,b,i,j=l.split();v=tuple(map(int,(a,b,i,j)))
            assert 0<=v[2]<256 and 0<=v[3]<256 and v not in pending
            pending.add(v);total+=1
        elif l.startswith('CELLPAIR '):
            _,r,a,b=l.split();assert all(k[:2]==(int(a),int(b)) for k in pending);pending.clear()
    assert not pending
    flat=list(map(int,(d/'room').read_text().split()))
    cells=list(zip(flat[2::2],flat[3::2]));expected={tuple(map(int,l.split())) for l in (near/'boxes').read_text().splitlines()}
    for k in [0,1]:
        axis=near/'shears'/str(k)
        assert (axis/'room').read_bytes()==(d/'shears'/str(k)/'room').read_bytes()
        g=list(map(int,(axis/'room').read_text().split()))
        assert g[:2]==flat[:2] and list(zip(g[2::2],g[3::2]))==[c[::-1] if k else c for c in cells]
        got=set()
        for f in axis.glob('ends-*'):
            for l in f.open():
                v=list(map(int,l.split()));ids=[];corners=[]
                for e in (0,5):
                    i,x,y,a,b=v[e:e+5]
                    if k:a,b,x,y=b,a,y,x
                    assert cells[i]==(a,b) and x-a in (0,1) and y-b in (0,1)
                    ids.append(i);corners.append(x-a+2*(y-b))
                got.add((*ids,*corners,int(f.name.split('-')[1])))
        assert got==expected
        print('corner check',k,verify_axis(axis),flush=True)
    check_pixels(d/'shears',p,grid,near)
def solve(root,d):
    p=d/'pixel';p.mkdir(exist_ok=True);room=(d/'room').read_text()
    with (d/'room').open() as f,(p/'grid').open('w') as g:
        subprocess.run([root/'grid','18','1','6000'],stdin=f,stdout=g,env={**os.environ,'COVER_ALLDIRS':'1'},check=True)
    flags=[]
    for sw in (0,1):
        side=d/'shears'/str(sw);raw=list(map(int,(side/'room').read_text().split()))
        C=set(zip(raw[2::2],raw[3::2]));ws=[]
        for x,y in C:
            if (x-1,y) not in C:
                z=x+1
                while (z,y) in C:z+=1
                ws.append(2*(z-x))
        flags.append(str(lcm(*ws)))
    files=[(p/f'in{i}').open('w') for i in range(3)]
    for i,l in enumerate(l for l in (p/'grid').open() if l.startswith('PIX ')):files[i%3].write(l[4:])
    for f in files:f.close()
    def run(i):
        with (p/f'in{i}').open() as f,(p/f'receipts{i}.gz').open('wb') as g:
            gz=subprocess.Popen(['gzip','-1'],stdin=subprocess.PIPE,stdout=g)
            try:
                subprocess.run([root/'px-receipt',d/'room',d/'shears/0/labels',d/'shears/1/labels',*flags,'36'],stdin=f,stdout=gz.stdin,check=True,env={**os.environ,'LOCAL_PHASE':'1','RATIONAL_PHASE':'1'})
            finally:gz.stdin.close();assert gz.wait()==0
    with ThreadPoolExecutor(3) as ex:list(ex.map(run,range(3)))
    near=p/'near';near.mkdir(exist_ok=True)
    boxes=set()
    for f in p.glob('receipts?.gz'):
        for l in gzip.open(f,'rt'):
            assert not l.startswith('OPEN '),(d,l)
            if l.startswith('NEAR '):boxes.add((*map(int,l.split()[1:]),1024))
    (near/'boxes').write_text(''.join(' '.join(map(str,b))+'\n' for b in sorted(boxes)))
    generate(root,near/'shears',room,boxes)
    verify(d)
if __name__=='__main__':
    root=Path(sys.argv[1])
    for n in sys.argv[2:]:solve(root,root/'hard'/n)
