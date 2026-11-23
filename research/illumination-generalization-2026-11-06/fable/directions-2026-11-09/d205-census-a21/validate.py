"""Check original D9 counts, all-class Part A controls, and the known DARK pair."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import subprocess
import orbit

here=Path(__file__).resolve().parent
d9=here.parent/'d9-census-w22'
val=here/'validation'

def counts(files):
    rooms=Counter()
    fixed=Counter()
    for file in files:
        lines=file.read_text().splitlines()
        assert lines[-1]=='# DONE',file
        for line in lines:
            v=line.split()
            if v[:2]==['#','count'] and int(v[5])<=20:
                rooms[int(v[3]),int(v[5])]+=int(v[7])
            if v[:2]==['#','fixed']:
                fixed[int(v[3])]+=int(v[4])
    return rooms,fixed

new=[val/f'{i}.counts' for i in range(28)]
assert all((val/f'{i}.done.json').exists() for i in range(28))
old=list((d9/'runs/a20').glob('job-*.counts'))
assert len(old)==26
rooms,nodes=counts(new)
stored,oldnodes=counts(old)
assert rooms=={key:value for key,value in stored.items() if key[0]==20}
assert nodes==oldnodes and sum(rooms.values())==247523973
small=val/'optimized.counts'
smallrooms,_=counts([small])
expected={}
for line in (d9/'partA-totals.md').read_text().splitlines():
    if not line.startswith('| '): continue
    f=[v.strip().replace(',','') for v in line.strip('|').split('|')]
    if len(f)!=19 or not f[0].isdigit(): continue
    w,a=map(int,f[:2])
    if w<=20 and a<=11:
        expected[a,w]=tuple(int(f[i]) for i in (2,9,10,11,12))
observed={key:(r,0,0,0,0) for key,r in smallrooms.items()}
for line in small.read_text().splitlines():
    if line.startswith('SHOT'):
        a,w,eligible,same,diff,sv=map(int,line.split()[1:])
        assert sv==0
        observed[a,w]=(smallrooms[a,w],same,same,diff,diff)
assert observed==expected and len(expected)>0
first=(here.parent/'d29-rigidity-test/control22.sv').read_text()
left,right=first.split('|')
head=list(map(int,left.split()))
cells=list(map(int,right.split()))
S=tuple(head[4:6]); T=tuple(head[6:8])
points=list(zip(cells[::2],cells[1::2]))
# Exercise the production shooter on the full room, then require that the
# sole survivor be the known pair, regardless of endpoint ordering.
xmax=max(x for x,y in points)+1;ymax=max(y for x,y in points)+1
rows=[sum(1<<x for x,y in points if y==r) for r in range(ymax)]
nmarks=sum((a&b&((a&b)<<1)).bit_count() for a,b in zip(rows,rows[1:]))
payload=' '.join(map(str,[head[1],head[2],xmax,ymax,nmarks,*rows]))
sv=subprocess.check_output([str(here/'control')],input=payload,text=True).strip()
assert len(sv.splitlines())==1
cellseq, markseq=sv.split('|')
marks=list(map(int,markseq.split()))
assert marks[0]==2 and {tuple(marks[1:3]),tuple(marks[3:5])}=={S,T}
c=subprocess.check_output([str(here/'orbitc'),'10000'],input=sv+'\n',text=True)
assert 'complete 1' in c and c.rstrip().endswith('DARK')
reach,ns,complete=orbit.decide(points,[S,T],{frozenset([S,T])},cap=10000)
assert complete and T not in reach[S]
summary={'binary':hashlib.sha256((here/'census').read_bytes()).hexdigest(),'orbit':hashlib.sha256((here/'orbitc').read_bytes()).hexdigest(),'area20_by_w':{str(w):n for (a,w),n in sorted(rooms.items())},'area20_rooms':sum(rooms.values()),'area20_fixed':nodes[20],'small_rows':len(observed),'small_rooms':sum(x[0] for x in expected.values()),'small_same':sum(x[1] for x in expected.values()),'small_diff':sum(x[3] for x in expected.values()),'control_problem':sv,'control_c':c,'control_python_complete':complete,'control_python_states':ns}
(val/'PASS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
