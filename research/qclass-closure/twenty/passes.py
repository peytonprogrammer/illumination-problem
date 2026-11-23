"""Run successive whole-room checks on exactly the failures of the preceding pass."""
import os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
root=Path(sys.argv[1])
def stage(k):
    prev=root/f'a{k}'
    # Read each shard only after all its rows have been flushed.
    with (root/f'i{k}').open('rb') as f: expected=sum(1 for _ in f)
    while True:
        with prev.open('rb') as f: emitted=sum(1 for _ in f)
        if emitted==expected:break
        assert emitted<expected
        time.sleep(8)
    for tag,prog,args in [('b',root/'order',(9,0,18000)),('c',root/'cover',(14,0,50000)),('d',root/'skip',(18,1,7000))]:
        inputpath=root/f'{tag}-in{k}'
        with inputpath.open('w') as out, prev.open() as src:
            for l in src:
                h,c,*_=l.split('|')
                a=h.split()
                if a[4]!='DONE' or a[12]!='0':print(a[2],a[3],c.strip(),file=out)
        prev=root/f'{tag}{k}'
        with inputpath.open() as inp, prev.open('w') as out:
            subprocess.run([prog,*map(str,args)],stdin=inp,stdout=out,env={**os.environ,'COVER_ALLDIRS':'1'},check=True)
with ThreadPoolExecutor(max_workers=10) as pool:list(pool.map(stage,range(len(list(root.glob("i[0-9]"))))))
