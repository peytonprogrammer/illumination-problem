"""Which A points are one-corner seed endpoints from S (approved fixed-room check). Orbit BFS with physical
A labels; a state contributes lab[r^2 b] and lab[r u r u^-1 b] when the state's direction is not wall-parallel."""
import sys,json,time
ARGS=sys.argv[1:]; sys.argv=['x']
__file__='<SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded/seedcheck.py'
exec(open(__file__).read().split("if __name__")[0])
src=open(E+'origami_frame.py').read()
src=src.replace("lab[s]='block' if v in corners else ('T' if v==T else ('S' if v==S else '.'))",
                "lab[s]='block' if v in corners else (v if cls(v)==0 else 'bc')")
g2={}; exec(src,g2); build2=g2['build']
def reach(V,S,limit):
    mul=lambda A,C:tuple(tuple(sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    r,u,lab,s0,fr=build2(list(V),S,S); st=o.canon(r,u,lab,s0); seen={st}; Q=deque([(st,((1,0),(0,1)))]); hit={}
    Aall={x for x in lab if isinstance(x,tuple)}
    while Q:
        (R,U,lab),M=Q.popleft(); dev=(M[0][0],M[1][0])
        Ri,Ui=o.inv(R),o.inv(U)
        if dev not in WALL:
            for sq in (R[R[0]],R[U[R[Ui[0]]]]):
                if isinstance(lab[sq],tuple) and lab[sq] not in hit: hit[lab[sq]]=dev
        for a,b,N in ((R,tuple(o.comp(U,Ri)),((1,-1),(0,1))),(tuple(o.comp(R,Ui)),U,((1,0),(-1,1)))):
            nn=o.canon(a,b,lab,0)
            if nn not in seen: seen.add(nn); Q.append((nn,mul(M,N)))
        if len(seen)>limit or len(hit)==len(Aall): break
    return Aall,hit,len(seen)
rows=[json.loads(l) for l in open(ARGS[0])]
for r in rows[int(ARGS[1]):int(ARGS[2])]:
    t0=time.time(); V=[tuple(v) for v in r['V']]
    Aall,_,_=reach(V,tuple(r['S']),0); out=[]
    for a in sorted(Aall):
        _,hit,n=reach(V,a,int(ARGS[3])); out.append([a,sorted(Aall-set(hit)),n])
    print(json.dumps(dict(W=len(V),S=r['S'],T=r['T'],nA=len(Aall),allpairs=all(not m for _,m,_ in out),
                          gaps=[x for x in out if x[1]],maxstates=max(x[2] for x in out),secs=round(time.time()-t0))),flush=True)
