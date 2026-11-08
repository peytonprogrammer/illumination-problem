"""Structure study of seeds on varied raw rooms (approved fixed-room checks)."""
import sys,json,random,os
from collections import defaultdict,deque
from fractions import Fraction as F
CFG=json.loads(sys.argv[1]); sys.argv=['x']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'seedenum.py')).read().replace("sys.argv,ARGS=['x'],sys.argv[1:]","").replace("os.path.dirname(os.path.abspath(__file__))","'"+os.path.dirname(os.path.abspath(__file__))+"'"))
def tris_of(V):
    xs=[p[0] for p in V]; ys=[p[1] for p in V]; out=[]
    for x in range(min(xs),max(xs)):
        for y in range(min(ys),max(ys)):
            c=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
            k=[i for i in range(4) if (c[i][0]%2==0 and c[i][1]%2==0) or (c[i][0]%2 and c[i][1]%2)]
            # A corner of the unit square is the even-even one; B is opposite
            a=[p for p in c if p[0]%2==0 and p[1]%2==0][0]; b=[p for p in c if p[0]%2 and p[1]%2][0]
            for o in [p for p in c if p not in (a,b)]:
                cx,cy=F(a[0]+b[0]+o[0],3),F(a[1]+b[1]+o[1],3)
                if inside_closed(V,cx,cy)=='in': out.append((a,b,o))
    return out
def fan_tree(V):
    T=tris_of(V); edge=defaultdict(list)
    for t in T:
        for e in ((t[1],t[2]),):  # BC edge only can be a portal between fans
            edge[frozenset(e)].append(t[0])
    adj=defaultdict(set)
    for e,owners in edge.items():
        if len(owners)==2 and owners[0]!=owners[1]: adj[owners[0]].add(owners[1]); adj[owners[1]].add(owners[0])
    return T,adj
def path(adj,S,T):
    prev={S:None}; Q=deque([S])
    while Q:
        u=Q.popleft()
        for v in adj[u]:
            if v not in prev: prev[v]=u; Q.append(v)
    p=[T]
    while p[-1]!=S: p.append(prev[p[-1]])
    return p[::-1]
def gen(cells,wmax,count,seed):
    random.seed(seed)
    case={'full':cells,'allowed':[(a+dx,b+dy) for a,b in cells for dx in range(-30,31) for dy in range(-30,31) if abs(dx)+abs(dy)<=30]}
    cnf,pool,x,ts=enc.geometry(case,wmax=wmax,kmax=0); out=[]; tries=0
    with Solver(name='glucose4',bootstrap_with=cnf.clauses) as so:
        while len(out)<count and tries<200:
            tries+=1; so.set_phases([v if random.random()<CFG.get('p',0.3) else -v for v in x.values()])
            if not so.solve(): break
            m={l for l in so.get_model() if l>0}; room=[t for t,v in x.items() if v in m]
            so.add_clause([-x[t] for t in room]); V=polygon(room)
            if V is not None:
                V=[tuple(map(int,v)) for v in V]
                if raw_ok(V,[(2*a,2*b) for a,b in cells]): out.append(V)
    return out
for V in gen(CFG['cells'],CFG['wmax'],CFG.get('count',4),CFG.get('seed',1)):
    marks=[(2*a,2*b) for a,b in CFG['cells']]; S,T=marks[0],marks[-1]
    Tr,adj=fan_tree(V); P=path(adj,S,T); Pset=set(P)
    sd=seeds_all(V,S,T,CFG.get('R',13))
    near=Pset|{v for u in P for v in adj[u]}
    rec=dict(W=len(V),S=S,T=T,nfans=len(adj),pathlen=len(P),path=P,nseeds=len(sd),
        minw=min((s['w'][0]**2+s['w'][1]**2 for s in sd),default=None),
        in_path=sum(set(map(tuple,s['fansS']))|set(map(tuple,s['fansT']))<=Pset for s in sd),
        in_near=sum(set(map(tuple,s['fansS']))|set(map(tuple,s['fansT']))<=near for s in sd),
        corners=[s['c'] for s in sorted(sd,key=lambda s:s['w'][0]**2+s['w'][1]**2)][:6],
        ws=[s['w'] for s in sorted(sd,key=lambda s:s['w'][0]**2+s['w'][1]**2)][:6],V=V)
    print(json.dumps(rec,default=str),flush=True)
