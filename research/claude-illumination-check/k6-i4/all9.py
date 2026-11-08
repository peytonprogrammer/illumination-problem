import sys,importlib.util
E='../../illumination-k4-codex/k5-proof-pilot/inputs/'; sys.path.insert(0,E)
spec=importlib.util.spec_from_file_location('enc',E+'encode.py'); enc=importlib.util.module_from_spec(spec); spec.loader.exec_module(enc)
from pysat.solvers import Solver
from itertools import combinations
pts=[(x,y) for x in range(0,4) for y in range(0,4)]
N=lambda p:{(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)}
seen=set(); res=[]
for S in combinations(pts,4):
    s=set(S)
    if len(set().union(*(N(p) for p in s))-s)!=8: continue
    n=tuple(sorted((x-min(a for a,b in S),y-min(b for a,b in S)) for x,y in S))
    if n in seen: continue
    seen.add(n); case={'full':list(n),'allowed':[(a+dx,b+dy) for a,b in n for dx in range(-3,4) for dy in range(-3,4)]}
    cnf,pool,x,ts=enc.geometry(case,wmax=21,kmax=6)
    with Solver(name='glucose4',bootstrap_with=cnf.clauses) as so: res.append((n,so.solve()))
print(len(res),'normalized equality sets;', 'all UNSAT' if not any(r for _,r in res) else res)
