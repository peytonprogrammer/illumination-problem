"""Check (a), approved by Daniel 2026-11-02: monodromy group of each existing room's unfolding.
K = ker(F2 -> (Z/2)^2) has 4 orbits (the fibers over the 4 unit squares of T2). For each orbit, test
whether K acts primitively and whether it contains the alternating group (Jordan's theorem with a
prime cycle p, n/2 < p <= n-3). Pure group computation on fixed rooms, no search. Run: python3 -B mono.py"""
import sys,json,random,types
sys.argv=['x']
class _Stub(types.ModuleType):
    __path__=[]
    def __getattr__(self,k): return object
for n in ('pysat','pysat.formula','pysat.solvers','pysat.card','pysat.pb'): sys.modules[n]=_Stub(n)
D='<SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded/'
__file__=D+'seedcheck.py'
exec(open(__file__).read().split("if __name__")[0])
src=open(E+'origami_frame.py').read()
src=src.replace("lab[s]='block' if v in corners else ('T' if v==T else ('S' if v==S else '.'))",
                "lab[s]='block' if v in corners else (v if cls(v)==0 else 'bc')")
g2={}; exec(src,g2); build2=g2['build']
exec(open(D+'generation.py').read().split("assert fold")[0])
P=lambda w,r,u:[ {'r':r,'R':o.inv(r),'u':u,'U':o.inv(u)}[c] for c in w]
def word(w,r,u):
    ps=P(w,r,u); out=list(range(len(r)))
    for p in reversed(ps): out=[p[x] for x in out]   # leftmost letter acts last
    return out
KW=['rr','uu','ruRU','ruuR','urrU']
assert fold([list(w) for w in KW])==(4,True)          # these five words generate K
def orbits(gens,n):
    seen=[-1]*n; out=[]
    for a in range(n):
        if seen[a]>=0: continue
        k=len(out); seen[a]=k; st=[a]; orb=[a]
        while st:
            x=st.pop()
            for g in gens:
                y=g[x]
                if seen[y]<0: seen[y]=k; st.append(y); orb.append(y)
        out.append(orb)
    return out
def primitive(gens,n):
    for b in range(1,n):
        par=list(range(n))
        def f(x):
            while par[x]!=x: par[x]=par[par[x]]; x=par[x]
            return x
        par[f(b)]=f(0); todo=[(0,b)]
        while todo:
            x,y=todo.pop()
            for g in gens:
                a,c=f(g[x]),f(g[y])
                if a!=c: par[max(a,c)]=min(a,c); todo.append((g[x],g[y]))
        size=sum(1 for x in range(n) if f(x)==f(0))
        if size<n: return False,size
    return True,n
def isprime(p): return p>1 and all(p%d for d in range(2,int(p**.5)+1))
def cycles(g):
    n=len(g); seen=[0]*n; out=[]
    for a in range(n):
        if not seen[a]:
            L=0; x=a
            while not seen[x]: seen[x]=1; x=g[x]; L+=1
            out.append(L)
    return out
def jordan(gens,n,tries=4000,seed=1):
    rnd=random.Random(seed); X=[list(g) for g in gens]*3; acc=list(range(n))
    for _ in range(tries):
        i,j=rnd.sample(range(len(X)),2)
        X[i]=[X[i][X[j][x]] for x in range(n)] if rnd.random()<.5 else [X[j][X[i][x]] for x in range(n)]
        acc=[X[i][acc[x]] for x in range(n)]
        cs=cycles(acc)
        for p in set(cs):
            if isprime(p) and n/2<p<=n-3 and cs.count(p)==1: return p
    return None
def even(g): return sum(L-1 for L in cycles(g))%2==0
rooms=[json.loads(l) for l in open(D+'study.jsonl')]+[json.loads(l) for l in open(D+'res_rooms.jsonl')]
for k,rm in enumerate(rooms):
    V=[tuple(v) for v in rm['V']]; S=tuple(rm['S']); T=tuple(rm['T'])
    r,u,lab,s0,_=build2(V,S,S); n=len(r)
    Kg=[word(w,r,u) for w in KW]; obs=orbits(Kg,n)
    res=[]
    for ob in obs:
        idx={x:i for i,x in enumerate(ob)}; gens=[[idx[g[x]] for x in ob] for g in Kg]
        kind='A' if s0 in idx else ('A*' if isinstance(lab[ob[0]],tuple) or any(isinstance(lab[x],tuple) for x in ob) else 'BC')
        prim,bs=primitive(gens,len(ob)); p=jordan(gens,len(ob)) if prim else None
        res.append(dict(kind=kind,n=len(ob),prim=prim,block=bs,jordan_p=p,all_even=all(even(g) for g in gens)))
    print(json.dumps(dict(room=k,W=len(V),S=S,T=T,N=n,G_even=even(r) and even(u),orbits=res)),flush=True)
