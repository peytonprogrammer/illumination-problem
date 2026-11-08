import sys, random
sys.path.insert(0,'../folded')
from origami_dark import decide
from exact import run
random.seed(1)
rows=[]
for f in ['../folded/dark-k1.txt','../folded/dark-k2.txt','../folded/dark-k3.txt','../folded/dark-k4.txt']:
    for line in open(f):
        h,v=line.split('|');t=h.split()
        rows.append(([tuple(map(int,s.split(','))) for s in v.split()],tuple(map(int,t[2][2:].split(','))),tuple(map(int,t[3][2:].split(',')))))
rows=random.sample(rows,150)
for V,a,b in rows:
    d,n=decide(V,a,b,limit=200000)
    if d!='LIT': print('DARKSIDE',d,n,a,b,V,flush=True); continue
    if run(V,a,b,R=15)[0]: continue
    r=run(V,a,b,R=40,B=3000)
    print('R15none',a,b,V,'R40:',r,flush=True)
