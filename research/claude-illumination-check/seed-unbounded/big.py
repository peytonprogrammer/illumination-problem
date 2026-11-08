"""Generate larger raw test rooms (approved fixed-room checks) and write V,S,T lines for reach.py."""
import sys,json,random,os
CFG=json.loads(sys.argv[1]); sys.argv=['x']
__file__='<SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded/seedcheck.py'
exec(open(__file__).read().split("if __name__")[0])
def gen(cells,wmax,count,seed,p):
    random.seed(seed)
    case={'full':cells,'allowed':[(a+dx,b+dy) for a,b in cells for dx in range(-30,31) for dy in range(-30,31) if abs(dx)+abs(dy)<=30]}
    cnf,pool,x,ts=enc.geometry(case,wmax=wmax,kmax=0); out=[]; tries=0
    with Solver(name='glucose4',bootstrap_with=cnf.clauses) as so:
        while len(out)<count and tries<100:
            tries+=1; so.set_phases([v if random.random()<p else -v for v in x.values()])
            if not so.solve(): break
            m={l for l in so.get_model() if l>0}; room=[t for t,v in x.items() if v in m]
            so.add_clause([-x[t] for t in room]); V=polygon(room)
            if V is not None:
                V=[tuple(map(int,v)) for v in V]
                if raw_ok(V,[(2*a,2*b) for a,b in cells]): out.append(V)
    return out
for V in gen(CFG['cells'],CFG['wmax'],CFG.get('count',3),CFG.get('seed',1),CFG.get('p',0.3)):
    marks=[(2*a,2*b) for a,b in CFG['cells']]
    print(json.dumps(dict(V=V,S=marks[0],T=marks[-1],cells=CFG['cells'],W=len(V))),flush=True)
