"""One nice supervisor plus at most seven single-process census workers."""
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
stage = sys.argv[1]
assert stage in ('validation','a21')
area = 20 if stage=='validation' else 21
folder = Path(stage)
folder.mkdir(exist_ok=True)
shards = 28 if area==20 else 84
live = {}
def write(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data,indent=2)+'\n')
    temp.replace(path)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def stop(*_):
    for pid in live:
        try: os.kill(pid,signal.SIGTERM)
        except ProcessLookupError: pass
    raise SystemExit(2)

signal.signal(signal.SIGTERM,stop)
assert stage=='a21'
original=Path('../d205-census-a21')
assert sha('enum_rooms.c')==sha(original/'enum_rooms.c')
assert sha('orbitc')==json.loads((original/'validation/PASS.json').read_text())['orbit']
manifest={'area':area,'walls':20,'shards':shards,'binary':sha('census'),'stage':stage,'nice':os.getpriority(os.PRIO_PROCESS,0),'sources':{f:sha(f) for f in ['enum_rooms.c','shoot.c','verify_plane.c','orbitc.c','orbit.py']}}
assert manifest['nice']>=10
mfile=folder/'manifest.json'
if mfile.exists(): assert json.loads(mfile.read_text())==manifest
else: write(mfile,manifest)
todo=[i for i in range(shards) if not (folder/f'{i}.done.json').exists()]
def launch(i):
    base=folder/str(i)
    args=['./census',str(area),'20',str(shards),str(i),str(area),str(base)+'.counts']
    if stage=='a21': args.append('shoot')
    with open(str(base)+'.sv','wb') as sv,open(str(base)+'.err','wb') as err:
        proc=subprocess.Popen(args,stdout=sv,stderr=err,env={**os.environ,"PAIR_FILE":str(base)+".bin"})
    live[proc.pid]=(i,proc,time.monotonic())
def survivor(line):
    # Pause worker scheduling before consuming the one extra orbit process slot.
    orbit_out=None
    for limit in (100000,1000000,5000000):
        res=subprocess.run(['./orbitc',str(limit)],input=line+'\n',capture_output=True,text=True)
        if res.returncode==3: continue
        res.check_returncode()
        orbit_out=res.stdout
        break
    if orbit_out is None: raise RuntimeError('orbit cap reached: unresolved '+line)
    with (folder/'orbits.log').open('a') as f: f.write(line+'\n'+orbit_out)
    if 'DARK' in orbit_out:
        assert 'complete 1' in orbit_out
        import orbit
        cells,marks=line.split('|')
        xy=list(map(int,cells.split()[1:])); st=list(map(int,marks.split()[1:]))
        s,t=tuple(st[:2]),tuple(st[2:])
        reach,states,complete=orbit.decide(list(zip(xy[::2],xy[1::2])),[s,t],{frozenset([s,t])})
        if not complete or t in reach[s]: raise RuntimeError('orbit disagreement')
        write(folder/'DARK.json',{'problem':line,'C':orbit_out,'python_states':states})
        stop()
    assert 'LIT' in orbit_out
def stats(path):
    lines=path.read_text().splitlines()
    assert lines[-1]=='# DONE'
    r=e=k=diff=sv=0
    want={}; got={}; eligible={}; observed={}
    for line in lines:
        v=line.split()
        if v[:2]==['#','count']:
            r+=int(v[7]); e+=int(v[9]); eligible[v[5]]=int(v[9])
        if v[0]=='EXPECT': want[v[2]]=int(v[3])
        if v[0]=='SHOT':
            observed[v[2]]=int(v[3]); k+=int(v[4]); diff+=int(v[5]); sv+=int(v[6])
            got[v[2]]=int(v[4])+int(v[5])
    if stage=='a21':
        assert want==got and {w:n for w,n in eligible.items() if n}==observed
    return dict(rooms=r,eligible=e,same_pairs=k,different_pairs=diff,survivors=sv)
try:
    while todo or live:
        while todo and len(live)<7:
            launch(todo.pop(0))
        pid,status,usage=os.wait4(-1,0)
        i,proc,start=live.pop(pid)
        proc.returncode=os.waitstatus_to_exitcode(status)
        if proc.returncode: raise RuntimeError(f'shard {i} exit {proc.returncode}')
        base=folder/str(i)
        data=stats(Path(str(base)+'.counts'))
        old=(original/'a21'/f'{i}.counts').read_text().splitlines()
        lines=Path(str(base)+'.counts').read_text().splitlines()
        assert [s for s in lines if not s.startswith(('TOP ','HIST '))]==old
        assert sum(int(s.split()[3]) for s in lines if s.startswith('HIST '))==data['same_pairs']+data['different_pairs']
        records=Path(str(base)+'.sv').read_text().splitlines()
        assert len(records)==data['survivors']
        orbit_cpu=0
        orbit_rss=0
        if records:
            before=resource.getrusage(resource.RUSAGE_CHILDREN)
            own=time.process_time()
            for line in records: survivor(line)
            after=resource.getrusage(resource.RUSAGE_CHILDREN)
            orbit_cpu=time.process_time()-own + after.ru_utime+after.ru_stime-before.ru_utime-before.ru_stime
            orbit_rss=max(after.ru_maxrss,resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        data['orbit_cpu_s']=orbit_cpu
        data['orbit_peak_rss_upper_bytes']=orbit_rss
        data.update(shard=i,wall_s=time.monotonic()-start,cpu_s=usage.ru_utime+usage.ru_stime+orbit_cpu,peak_rss_bytes=max(usage.ru_maxrss,orbit_rss),counts_sha256=sha(str(base)+'.counts'))
        write(Path(str(base)+'.done.json'),data)
        print(stage,i,data,flush=True)
finally:
    for pid in live:
        try: os.kill(pid,signal.SIGTERM)
        except ProcessLookupError: pass
