from pathlib import Path
from math import gcd
import os,subprocess,sys,tempfile
room=Path(sys.argv[1])
bound=int(sys.argv[2])
dirs=sorted(((p,q) for p in range(1,bound+1) for q in range(1,bound+1) if gcd(p,q)==1),key=lambda z:(sum(z),z))
with tempfile.NamedTemporaryFile(mode='w',delete=False) as f: name=f.name
def passes(ds):
    Path(name).write_text(''.join(f'{p} {q}\n' for p,q in ds))
    r=subprocess.run(['/tmp/og-choice',str(bound),'0','35000'],input=room.read_bytes(),capture_output=True,env={**os.environ,'CHOICE':name,'COVER_ALLDIRS':'1'})
    v=r.stdout.split()
    return r.returncode==0 and len(v)>13 and v[4]==b'DONE' and int(v[12])==0
assert passes(dirs)
for chunk in (12,4,1):
    i=len(dirs)
    while i>0:
        j=max(0,i-chunk)
        trial=dirs[:j]+dirs[i:]
        if trial and passes(trial):dirs=trial
        i=j
print(dirs)
room.with_suffix('.dirs').write_text(''.join(f'{p} {q}\n' for p,q in dirs))
os.unlink(name)
