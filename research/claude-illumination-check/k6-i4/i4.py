"""k=6, I=4 equality branch: T and S diagonal pairs. Codex's frozen encoder for necessary geometry
(read-only import); my own polygon extraction, exact tracer, guard derivation and guard check."""
import sys,json,importlib.util,time
from fractions import Fraction as F
from collections import defaultdict
E='../../illumination-k4-codex/k5-proof-pilot/inputs/'; sys.path.insert(0,E)
sys.path.insert(0,'../folded'); from exact import run
spec=importlib.util.spec_from_file_location('enc',E+'encode.py'); enc=importlib.util.module_from_spec(spec); spec.loader.exec_module(enc)
from pysat.solvers import Solver
sys.argv=[sys.argv[0],'0','0']+sys.argv[1:]
exec(open('../k5-residual/guard_audit.py').read().split('idx=random')[0].split('L=[json.loads')[0]+open('../k5-residual/guard_audit.py').read().split('idx=random')[0].split("open('../../illumination-k4-codex/k5-proof-continuation/learned.jsonl')]")[1])
def polygon(tiles):
    cnt=defaultdict(int)
    for t in tiles:
        t=tuple(t)
        for i in range(3): cnt[frozenset((t[i],t[(i+1)%3]))]+=1
    bd=[tuple(e) for e,c in cnt.items() if c==1]; adj=defaultdict(list)
    for a,b in bd: adj[a].append(b); adj[b].append(a)
    if any(len(v)!=2 for v in adj.values()): return None
    start=min(adj); cyc=[start]; prev=None; cur=start
    while True:
        nxt=[v for v in adj[cur] if v!=prev][0] if prev is not None else adj[cur][0]
        if nxt==start: break
        cyc.append(nxt); prev,cur=cur,nxt
    if len(cyc)!=len(adj): return None
    V=[cyc[i] for i in range(len(cyc)) if (cyc[i][0]-cyc[i-1][0])*(cyc[(i+1)%len(cyc)][1]-cyc[i][1])-(cyc[i][1]-cyc[i-1][1])*(cyc[(i+1)%len(cyc)][0]-cyc[i][0])!=0]
    return V
def guard_from(path,room):
    room={frozenset(t) for t in room}; P=[(F(x),F(y)) for x,y in path]; U=set(); Z=set()
    for a,b in zip(P,P[1:]):
        ts={F(0),F(1)}
        for T in room:
            T=tuple(T)
            for i in range(3):
                p,q=T[i],T[(i+1)%3]; d=(b[0]-a[0],b[1]-a[1]); e=(q[0]-p[0],q[1]-p[1]); den=d[0]*e[1]-d[1]*e[0]
                if den: 
                    t=F((p[0]-a[0])*e[1]-(p[1]-a[1])*e[0])/den
                    if 0<t<1: ts.add(t)
        ts=sorted(ts); pts=[(a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])) for t in ts]
        for m in [((p[0]+q[0])/2,(p[1]+q[1])/2) for p,q in zip(pts,pts[1:])]+pts[1:-1]: U|=tiles_at(m)
    for p in P[1:-1]:
        for t in tiles_at(p): (U if t in room else Z).add(t)
    return U,Z
shapes={'T':([(0,1),(1,0),(1,1),(2,1)],[(0,1),(1,0)]),'S':([(0,0),(1,0),(1,1),(2,1)],[(0,0),(1,1)])}
out={}
for name,(cells,pair) in shapes.items():
    case={'full':cells,'allowed':[(a+dx,b+dy) for a,b in cells for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1))]}
    cnf,pool,x,ts=enc.geometry(case,wmax=21,kmax=6)
    S,T=[(2*a,2*b) for a,b in pair]; inv={v:t for t,v in x.items()}; lit=dark=0; rounds=0; darkrooms=[]
    with Solver(name='glucose4',bootstrap_with=cnf.clauses) as sol:
        while sol.solve():
            rounds+=1; m=set(l for l in sol.get_model() if l>0); room=[t for t,v in x.items() if v in m]
            V=polygon(room)
            if V is None: print(name,'non-simple model?'); sol.add_clause([-x[t] for t in room]+[x[t] for t in x if x[t] not in m]); continue
            r=run(V,S,T,R=12,B=2000)
            if r[0] is None:
                darkrooms.append(V); sol.add_clause([-x[t] for t in room]+[x[t] for t in x if x[t] not in m]); dark+=1; continue
            path=r[1]; U,Z=guard_from(path,room)
            g={'U':[list(t) for t in U],'Z':[list(t) for t in Z],'q':[T[0]-S[0],T[1]-S[1]],'path':[[[p[0].numerator,p[0].denominator],[p[1].numerator,p[1].denominator]] for p in [(F(a)-S[0],F(b)-S[1]) for a,b in path]]}
            # check in source-at-origin coordinates
            sh=lambda t:[[v[0]-S[0],v[1]-S[1]] for v in t]
            g0=dict(g,U=[sh(t) for t in U],Z=[sh(t) for t in Z]); res=check(g0)
            assert res=='ok',res
            sol.add_clause([-x[t] for t in U]+[x[t] for t in Z if t in x]); lit+=1
    out[name]=dict(models=rounds,lit_guards=lit,unresolved=dark,unresolved_rooms=[[list(map(int,v)) for v in V] for V in darkrooms])
    print(name,'UNSAT after',rounds,'models;',lit,'guards;',dark,'unresolved (R=12)',flush=True)
json.dump(out,open('i4.json','w'),indent=1)
