import sys, random, glob, json
sys.path.insert(0,'../folded')
from origami_dark import decide
from exact import run
random.seed(1)
rows=[]
for f in ['../folded/dark-k1.txt','../folded/dark-k2.txt','../folded/dark-k3.txt','../folded/dark-k4.txt']:
    for line in open(f):
        h,v=line.split('|');t=h.split()
        rows.append(([tuple(map(int,s.split(','))) for s in v.split()],tuple(map(int,t[2][2:].split(','))),tuple(map(int,t[3][2:].split(','))),'tracer-dark'))
rows=random.sample(rows,150)
for line in random.sample(open('../folded/lit-rel.txt').read().splitlines(),150):
    h,v=line.split('|');_,a,b,d=h.split()
    rows.append(([tuple(map(int,s.split(','))) for s in v.split()],tuple(map(int,a.split(','))),tuple(map(int,b.split(','))),'tracer-lit'))
for c in [c for c in glob.glob('../parity-enum/certs/parity-W2*.json') if 'R1' not in c][:60]:
    j=json.load(open(c)); rows.append(([tuple(p) for p in j['vertices']],tuple(j['marked'][0]),tuple(j['marked'][1]),'parity-room'))
from collections import Counter
C=Counter(); bad=[]
for V,a,b,tag in rows:
    d,n=decide(V,a,b,limit=200000); print(tag,d,n,flush=True)
    C[(tag,d)]+=1
    if (tag=='tracer-lit' and d!='LIT') or (tag=='parity-room' and d!='DARK'): bad.append((tag,d,V,a,b))
    if tag=='tracer-dark' and d=='LIT':
        dd,_=run(V,a,b,R=15); C[('tracer-dark->LIT','R15 '+('found' if dd else 'none'))]+=1
print(sorted(C.items())); print('contradictions',len(bad)); [print(x) for x in bad[:5]]
