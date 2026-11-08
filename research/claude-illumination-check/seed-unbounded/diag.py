import json,sys,random
from collections import Counter
__file__='<SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded/study.py'
sys.argv=['x','{"cells":[[0,0],[2,0],[4,0]],"wmax":44,"count":0}']
exec(open('study.py').read().split('for V in gen(')[0])
cells=[[0,0],[2,0],[4,0]]
case={'full':cells,'allowed':[(a+dx,b+dy) for a,b in cells for dx in range(-30,31) for dy in range(-30,31) if abs(dx)+abs(dy)<=30]}
cnf,pool,x,ts=enc.geometry(case,wmax=44,kmax=0); print(len(ts))
C=Counter()
with Solver(name='glucose4',bootstrap_with=cnf.clauses) as so:
  for i in range(30):
    asm=[x[t] for t in random.sample(ts,2)]
    if not so.solve(assumptions=asm): C['unsat']+=1; continue
    m={l for l in so.get_model() if l>0}; room=[t for t,v in x.items() if v in m]; V=polygon(room)
    if V is None: C['nonsimple']+=1; continue
    V=[tuple(map(int,v)) for v in V]; C['raw' if raw_ok(V,[(2*a,2*b) for a,b in cells]) else 'notraw']+=1
print(C)
