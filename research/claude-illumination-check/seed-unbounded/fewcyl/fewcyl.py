"""Check (b), approved by Daniel 2026-11-02: cylinder data of existing fixed rooms in every strip direction
w with |w| <= L. For each w, the state with M e1 = w gives the cylinders (R-cycles; findings Section 7.6),
and the seed endpoints of the whole strip family w' = m w + v are E_w(s) = {u r^m u r^m s, u r^(m+1) u r^(m-1) s}.
Every endpoint class mod lcm holds infinitely many m, so the at most 4 wall-parallel w' never matter.
Records: cylinder count, type I count, s's half-circumference q, whether T is in E_w(s), and whether
the coprime criterion holds. Validates the formula against exact physical walks on a sample.
Run: python3 -B fewcyl.py ROOMFILE START END L [validate]"""
import sys,json,time,types
from math import gcd
ARGS=sys.argv[1:]; sys.argv=['x']
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
def pw(P,k):
    if k<0: P=o.inv(P); k=-k
    out=list(range(len(P)))
    for _ in range(k): out=[P[x] for x in out]
    return out
def mm(A,C): return tuple(tuple(sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def word_for(w):
    """Moves (gen, k) whose product, applied in order from I, is M with M e1 = w (gen 1: N1^k, gen 2: N2^k)."""
    a,c=w
    def eg(x,y):
        if y==0: return (x,1,0)
        g,s,t=eg(y,x%y); return (g,t,s-(x//y)*t)
    g,x,y=eg(a,c)                      # a x + c y = g = +-1
    x,y=x*g,y*g                        # a x + c y = 1
    A=[[a,-y],[c,x]]                   # det = a x + c y = 1
    ops=[]
    def T(k):   # A <- A T^k: col2 += k col1
        A[0][1]+=k*A[0][0]; A[1][1]+=k*A[1][0]; ops.append((1,k))
    def L(k):   # A <- A L^k: col1 += k col2
        A[0][0]+=k*A[0][1]; A[1][0]+=k*A[1][1]; ops.append((2,k))
    for _ in range(200):
        a0,b0=A[0]
        if b0==0: break
        if a0==0: L(b0); continue
        if abs(b0)>=abs(a0): T(-(b0//a0) if b0%a0==0 else -int(b0/a0))
        else: L(-(a0//b0) if a0%b0==0 else -int(a0/b0))
    if A[0][0]==-1: T(1);L(-1);T(1);T(1);L(-1);T(1)   # S^2 = -I
    L(-A[1][0]*A[0][0])
    assert A==[[1,0],[0,1]],A
    return ops[::-1]                   # M = product of inverses in reverse order
def state(r,u,w):
    R,U=list(r),list(u); M=((1,0),(0,1))
    N={1:((1,-1),(0,1)),2:((1,0),(-1,1))}
    for gnr,k in word_for(w):
        if k==0: continue
        if gnr==1: U=o.comp(U,pw(R,-k))
        else: R=o.comp(R,pw(U,-k))
        Nk=((1,0),(0,1))
        for _ in range(abs(k)): Nk=mm(Nk,N[gnr] if k>0 else tuple(tuple(-x if i!=j else x for j,x in enumerate(row)) for i,row in enumerate(N[gnr])))
        M=mm(M,Nk)
    assert (M[0][0],M[1][0])==tuple(w),(M,w)
    return R,U,(M[0][1],M[1][1])
def cyc(R):
    n=len(R); cid=[-1]*n; pos=[0]*n; L=[]
    for a in range(n):
        if cid[a]>=0: continue
        x=a; i=0
        while cid[x]<0: cid[x]=len(L); pos[x]=i; i+=1; x=R[x]
        L.append(i)
    return cid,pos,L
def analyse(r,u,lab,cls4,s,Tl,w):
    R,U,v=state(r,u,w); cid,pos,L=cyc(R); n=len(R)
    h=(w[0]%2,w[1]%2); typeI={0,{(1,0):1,(0,1):2,(1,1):3}[h]}  # class ids: 0=O; 1,2,3 as cls4 below
    nI=len({cid[x] for x in range(n) if cls4[x] in typeI})
    Cs=cid[s]; q2=L[Cs]; Ends=set(); cop=False
    for side in (0,1):
        for j in range(q2):            # residue of the first exponent mod 2q
            first=pw_apply(R,s,j-side)  # side 0: r^m u r^m; side 1: r^(m+1) u r^(m-1), m = j
            x=U[first]; Dd=cid[x]; qD2=L[Dd]; g2_=gcd(q2,qD2)
            for t in range(qD2//g2_):
                m=j+q2*t
                y=U[pw_apply(R,x,m+side)]; Ends.add(y)
            if g2_==2 and any(lab[U[z]] in Tl for z in range(n) if cid[z]==Dd): cop=True
    hit=any(lab[e] in Tl for e in Ends)
    return dict(w=w,v=v,ncyl=len(L),nI=nI,q=q2//2,hit=hit,cop=cop,nE=len({lab[e] for e in Ends if isinstance(lab[e],tuple)}))
def pw_apply(R,x,k):
    if k>=0:
        for _ in range(k): x=R[x]
    else:
        Ri=o.inv(R)
        for _ in range(-k): x=Ri[x]
    return x
def classes(r,u,s):
    """4-class id per square: developed lower-left corner mod 2, relative to s (0 = O)."""
    n=len(r); c=[None]*n; c[s]=(0,0); st=[s]; ri,ui=o.inv(r),o.inv(u)
    while st:
        x=st.pop()
        for y,d in ((r[x],(1,0)),(u[x],(0,1)),(ri[x],(1,0)),(ui[x],(0,1))):
            z=((c[x][0]+d[0])%2,(c[x][1]+d[1])%2)
            if c[y] is None: c[y]=z; st.append(y)
            else: assert c[y]==z
    m={(0,0):0,(1,0):1,(0,1):2,(1,1):3}
    return [m[x] for x in c]
rows=[json.loads(l) for l in open(ARGS[0])]; Lmax=int(ARGS[3]); VAL=len(ARGS)>4
ws=[(a,b) for a in range(-Lmax,Lmax+1) for b in range(-Lmax,Lmax+1) if gcd(a,b)==1 and a*a+b*b<=Lmax*Lmax]
ws.sort(key=lambda w:(w[0]**2+w[1]**2,w))
for k in range(int(ARGS[1]),int(ARGS[2])):
    rm=rows[k]; V=[tuple(x) for x in rm['V']]; S=tuple(rm['S']); T=tuple(rm['T']); t0=time.time()
    r,u,lab,s0,fr=build2(V,S,S); r,u,lab=o.canon(r,u,lab,s0); r,u,lab=list(r),list(u),list(lab)
    ft=tuple(zip(*fr)); ph=lambda w:[ft[0][0]*w[0]+ft[0][1]*w[1],ft[1][0]*w[0]+ft[1][1]*w[1]]  # copy frame -> room frame
    cls4=classes(r,u,0)
    # lab holds physical A points; T's lifts are squares labelled T
    res=[analyse(r,u,lab,cls4,0,{T},w) for w in ws]
    val=None
    if VAL:
        bad=0; tot=0
        for d in res[:40]:
            Rr,Uu,v=state(r,u,d['w']); Ui=o.inv(Uu)
            for m in range(-3,4):
                wp=(m*d['w'][0]+v[0],m*d['w'][1]+v[1])
                if (abs(wp[0]),abs(wp[1])) in {(1,0),(0,1),(1,1)}: continue
                # formula endpoints for this m, in the base state
                e1=Uu[pw_apply(Rr,Uu[pw_apply(Rr,0,m)],m)]; e2=Uu[pw_apply(Rr,Uu[pw_apply(Rr,0,m-1)],m+1)]
                pred=T in (lab[e1],lab[e2]); phys=verify(V,S,T,tuple(ph(wp))) is not None
                tot+=1; bad+=pred!=phys
        val=[bad,tot]
    hits=[d for d in res if d['hit']]
    mc=min(d['ncyl'] for d in res); mI=min(d['nI'] for d in res)
    print(json.dumps(dict(room=k,W=len(V),S=S,T=T,N=len(r),ndirs=len(res),min_cyl=mc,min_cyl_dirs=[ph(d['w']) for d in res if d['ncyl']==mc][:6],
        min_cyl_hit=any(d['hit'] for d in res if d['ncyl']==mc),min_nI=mI,nI_dist={i:sum(d['nI']==i for d in res) for i in sorted({d['nI'] for d in res})},
        oneI_hit=sum(d['hit'] for d in res if d['nI']==1),hit_dirs=len(hits),first_hit=ph(hits[0]['w']) if hits else None,wall_hits=[ph(d['w']) for d in hits if (abs(d['w'][0]),abs(d['w'][1])) in {(1,0),(0,1),(1,1)}],
        cop_dirs=sum(d['cop'] for d in res),first_cop=next((ph(d['w']) for d in res if d['cop']),None),
        q_s_min=min(d['q'] for d in res),q1_dirs=sum(d['q']==1 for d in res),q1_cop=sum(d['q']==1 and d['cop'] for d in res),first_q1_cop=next((ph(d['w']) for d in res if d['q']==1 and d['cop']),None),validate=val,secs=round(time.time()-t0,1))),flush=True)
