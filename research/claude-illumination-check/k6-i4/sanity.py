import sys,importlib.util
E='../../illumination-k4-codex/k5-proof-pilot/inputs/'; sys.path.insert(0,E)
spec=importlib.util.spec_from_file_location('enc',E+'encode.py'); enc=importlib.util.module_from_spec(spec); spec.loader.exec_module(enc)
from pysat.solvers import Solver
from illumination_geometry import label
shapes={'O':[(0,0),(1,0),(0,1),(1,1)],'T':[(0,1),(1,0),(1,1),(2,1)],'S':[(0,0),(1,0),(1,1),(2,1)]}
for name,cells in shapes.items():
    # forced interior non-A points: lattice points strictly inside the union of the 4 full patches
    pts=set()
    for a,b in cells:
        for X in range(2*a-1,2*a+2):
            for Y in range(2*b-1,2*b+2):
                # strictly interior to union: all 4 unit quadrants around (X,Y) inside some full patch
                if all(any(2*c-1<X+dx<2*c+1 and 2*d-1<Y+dy<2*d+1 for c,d in cells) for dx in (-0.5,0.5) for dy in (-0.5,0.5)):
                    if label((X,Y))!='A': pts.add((X,Y))
    case={'full':cells,'allowed':[(a+dx,b+dy) for a,b in cells for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1))]}
    res=[]
    for w,k in ((21,6),(21,8),(21,12),(26,10),(30,12)):
        case2=dict(case,allowed=[(a+dx,b+dy) for a,b in cells for dx in range(-15,16) for dy in range(-15,16)])
        cnf,pool,x,ts=enc.geometry(case2,wmax=w,kmax=k)
        with Solver(name='glucose4',bootstrap_with=cnf.clauses) as s: res.append(((w,k),s.solve()))
    print(name,'forced interior non-A points:',len(pts),sorted(pts),res)
