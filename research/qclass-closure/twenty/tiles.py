"""Run each hard room and retain the terminal proof inputs, including isolated pairs."""
import os,sys,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations_with_replacement
from box_room import generate
from rational import point,find
root=Path(sys.argv[1]);out=root/'hard';out.mkdir(exist_ok=True)
def task(arg):
    name,room=arg;d=out/name;d.mkdir(exist_ok=True)
    (d/'room').write_text(room+'\n')
    flat=list(map(int,room.split()));n=flat[0];cells=set(zip(flat[2::2],flat[3::2]))
    with (d/'room').open() as inp,(d/'tiles').open('w') as f:
        subprocess.run([root/'tile','18','1','6000'],stdin=inp,stdout=f,check=True,env={**os.environ,'COVER_ALLDIRS':'1'})
    boxes=[];coords=set();failed=set();seen=set();pending=[];ll=0
    for l in (d/'tiles').read_text().splitlines():
        if l.startswith('BOX '):
            pending.append(tuple(map(int,l.split()[2:])));continue
        if l.startswith('ROOM '):
            h,c,t=l.split('|');a=h.split()
            assert tuple(map(int,c.split()))==tuple(flat[2:]) and a[4] in ('DONE','RESID')
            if a[4]=='RESID':assert pending
            if a[4]=='DONE':assert not pending
            ll+=int(a[11])
            pts=t.split();assert len(pts)==int(a[12])
            for pair in pts:coords.add(pair)
            continue
        tag,r,i,j=l.split();assert tag=='CELLPAIR' and r=='1'
        pair=int(i),int(j);assert pair not in seen
        seen.add(pair)
        assert all(t[:2]==pair for t in pending)
        boxes.extend(pending);pending=[]
    assert not pending and seen==set(combinations_with_replacement(range(n),2))
    with (d/'rational').open('w') as f:
        for xy in sorted(coords):
            s,t=map(point,xy.split(';'));v=find(cells,s,t)
            if v:print(xy,*v,file=f)
            else:failed.add(xy)
    if boxes:
        (d/'boxes').write_text(''.join(' '.join(map(str,b))+'\n' for b in boxes))
        generate(root,d/'shears',room,boxes)
    bad=0;trees=0
    for f in d.glob('shears/*/cert-*'):
        for l in f.open():
            if l.startswith('END '):
                trees+=1
                if l.split()[5]!='1':bad+=1
    msg=f'{n} cells {len(seen)} tilepairs {len(boxes)} boxes {trees} trees {bad} failed trees {len(coords)} isolated {len(failed)} failed isolated {ll} lattice'
    (d/'status').write_text(msg+'\n')
def shards(k):
    for idx,l in enumerate((root/f'd{k}').open()):
        h,c,_=l.split('|');a=h.split()
        if a[4]!='DONE' or a[12]!='0':yield f'{k}-{idx}',f'{a[2]} {a[3]} {c.strip()}'
if __name__=='__main__':
    import time,shutil
    from collections import deque
    from concurrent.futures import wait,FIRST_COMPLETED
    seen=set();todo=deque();running=set()
    # Reuse verified pilot outputs for the same exact room when they exist.
    cached={(p.parent/'room').read_text().strip():p.parent for p in out.glob('p*/status')}
    shards_count=len(list(root.glob('i[0-9]')))
    with ThreadPoolExecutor(10) as pool:
        while True:
            finished=True
            for k in range(shards_count):
                p=root/f'd{k}';q=root/f'd-in{k}'
                if not p.exists():finished=False;continue
                data=p.read_text().splitlines(keepends=True)
                expected=sum(1 for _ in q.open())
                done=sum(l.endswith('\n') for l in data)
                assert done<=expected
                if done<expected:finished=False
                for idx,l in enumerate(data[:done]):
                    key=f'{k}-{idx}'
                    if key in seen:continue
                    seen.add(key);h,c,_=l.split('|');a=h.split()
                    if a[4]!='DONE' or a[12]!='0':
                        room=f'{a[2]} {a[3]} {c.strip()}'
                        if room in cached:
                            shutil.copytree(cached[room],out/key,dirs_exist_ok=True)
                        elif not (out/key/'status').exists():todo.append((key,room))
            capacity=10 if finished else 3
            while todo and len(running)<capacity:running.add(pool.submit(task,todo.popleft()))
            if finished and not todo and not running:break
            if running:
                settled,running=wait(running,timeout=6,return_when=FIRST_COMPLETED)
                for f in settled:f.result()
            else:time.sleep(5)
