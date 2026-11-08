import sys,importlib.util,hashlib
E='../../illumination-k4-codex/k5-proof-pilot/inputs/'; sys.path.insert(0,E)
spec=importlib.util.spec_from_file_location('enc',E+'encode.py'); enc=importlib.util.module_from_spec(spec); spec.loader.exec_module(enc)
from pysat.solvers import Solver
shapes={'O':[(0,0),(1,0),(0,1),(1,1)],'T':[(0,1),(1,0),(1,1),(2,1)],'S':[(0,0),(1,0),(1,1),(2,1)]}
for name,cells in shapes.items():
    case={'full':cells,'allowed':[(a+dx,b+dy) for a,b in cells for dx in range(-15,16) for dy in range(-15,16)]}
    row=[]
    for k in (6,7):
        cnf,pool,x,ts=enc.geometry(case,wmax=21,kmax=k)
        with Solver(name='glucose4',bootstrap_with=cnf.clauses,with_proof=True) as s:
            r=s.solve(); row.append((k,r))
            if not r and k==6:
                cnf.to_file(f'{name}.cnf'); open(f'{name}.drat','w').write('\n'.join(s.get_proof())+'\n')
    mw=None
    for w in range(21,40):
        cnf,pool,x,ts=enc.geometry(dict(case),wmax=w,kmax=6)
        with Solver(name='glucose4',bootstrap_with=cnf.clauses) as s:
            if s.solve(): mw=w; break
    print(name,'W<=21:',row,'| min W at k=6:',mw,'| universe tiles',len(ts) if False else '',flush=True)
