"""Fixed-room seed check (Daniel approved 2026-11-01). Rooms: raw (kmax=0) models of Codex's frozen encoder,
re-verified raw and simple here. Seed test: SL2(Z) orbit of the unit-square origami based at the S square;
hit = label T at r^2(s) or r u r u^-1 (s), direction not wall-parallel. Every hit is re-verified by an exact
physical walk of both halves to the same corner at parameter 1, plus a pi-sweep fold check at that corner."""
import sys,json,os,math,time,importlib.util
from fractions import Fraction as F
from collections import deque
H=os.path.dirname(os.path.abspath(__file__)); B=H+'/..'; X=B+'/../illumination-k4-codex/'
E=X+'k5-proof-pilot/inputs/'; sys.path[:0]=[E]
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
enc=load('enc',E+'encode.py'); o=load('of',E+'origami_frame.py')
from pysat.solvers import Solver
g={}; src=open(B+'/k6-i4/i4.py').read(); exec('from collections import defaultdict',g)
exec(src[src.index('def polygon'):src.index('shapes={')],g); polygon=g['polygon']

def ccw(V):
    n=len(V); return V if sum(V[i][0]*V[(i+1)%n][1]-V[(i+1)%n][0]*V[i][1] for i in range(n))>0 else V[::-1]
def inside_closed(V,x,y):
    n=len(V)
    for i in range(n):
        (ax,ay),(bx,by)=V[i],V[(i+1)%n]
        if (bx-ax)*(y-ay)-(by-ay)*(x-ax)==0 and min(ax,bx)<=x<=max(ax,bx) and min(ay,by)<=y<=max(ay,by): return 'edge'
    c=False
    for i in range(n):
        (ax,ay),(bx,by)=V[i],V[(i+1)%n]
        if (ay>y)!=(by>y) and x<ax+F(y-ay)*(bx-ax)/(by-ay): c=not c
    return 'in' if c else 'out'
def raw_ok(V,marks):
    Vs=set(V); xs=[p[0] for p in V]; ys=[p[1] for p in V]
    for x in range(min(xs),max(xs)+1):
        for y in range(min(ys),max(ys)+1):
            r=inside_closed(V,x,y)
            if r=='out' or (x%2==0 and y%2==0): continue
            if (x,y) not in Vs: return False
    return all(inside_closed(V,*m)=='in' for m in marks)

def walk(V,a,d,maxhits=100000):
    """Ray from lattice point a in direction d; return (corner, parameter, final direction) at first vertex."""
    n=len(V); Vs={(F(v[0]),F(v[1])) for v in V}; x,y=F(a[0]),F(a[1]); dx,dy=F(d[0]),F(d[1]); T=F(0); last=-1
    for _ in range(maxhits):
        best=None
        for i in range(n):
            if i==last: continue
            ex,ey=V[(i+1)%n][0]-V[i][0],V[(i+1)%n][1]-V[i][1]; den=dx*ey-dy*ex
            if den==0: continue
            t=((V[i][0]-x)*ey-(V[i][1]-y)*ex)/den; s=((V[i][0]-x)*dy-(V[i][1]-y)*dx)/den
            if t>0 and 0<=s<=1 and (best is None or t<best[0]): best=(t,i)
        if best is None: return None
        t,bi=best; hx,hy=x+t*dx,y+t*dy; T+=t
        if (hx,hy) in Vs: return (hx,hy),T,(dx,dy)
        ex,ey=V[(bi+1)%n][0]-V[bi][0],V[(bi+1)%n][1]-V[bi][1]
        dd=(dx*ex+dy*ey)/(ex*ex+ey*ey); dx,dy=2*dd*ex-dx,2*dd*ey-dy; x,y=hx,hy; last=bi
    return None
def fold_ok(V,c,v1,u2):
    """Corner c, arrival direction v1 (from S), departure u2 (toward T). Pi sweep CCW or CW from the S germ."""
    V=ccw(V); i=V.index((int(c[0]),int(c[1]))); n=len(V); nx,pv=V[(i+1)%n],V[i-1]
    a0=math.atan2(nx[1]-c[1],nx[0]-c[0]); a1=math.atan2(pv[1]-c[1],pv[0]-c[0]); th=(a1-a0)%(2*math.pi)
    def rel(v): return (math.atan2(float(v[1]),float(v[0]))-a0)%(2*math.pi)
    gS=rel((-v1[0],-v1[1])); gT=rel(u2)
    for sgn in (1,-1):
        z=(gS+sgn*math.pi)%(2*th); f=z if z<=th else 2*th-z
        if abs(f-gT)<1e-9: return True
    return False

D4=[((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)),((1,0),(0,-1)),((-1,0),(0,1)),((0,1),(1,0)),((0,-1),(-1,0))]
def verify(V,S,T,w):
    r=walk(V,S,w)
    if not r or r[1]!=1: return None
    c,_,v1=r
    for m in D4:
        w2=(m[0][0]*w[0]+m[0][1]*w[1],m[1][0]*w[0]+m[1][1]*w[1]); q=walk(V,T,w2)
        if q and q[1]==1 and q[0]==c and fold_ok(V,c,v1,(-q[2][0],-q[2][1])): return (int(c[0]),int(c[1])),w2
    return None

WALL={(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)}
def seeds(V,S,T,limit=3_000_000,want=3):
    mul=lambda A,C:tuple(tuple(sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    r,u,lab,s0,fr=o.build(list(V),S,T); st=o.canon(r,u,lab,s0); seen={st}; Q=deque([(st,((1,0),(0,1)))]); hits=[]
    ft=tuple(zip(*fr))
    while Q:
        (R,U,lab),M=Q.popleft(); dev=(M[0][0],M[1][0])
        if dev not in WALL:
            Ui=o.inv(U)
            for word,sq in (('up',R[R[0]]),('down',R[U[R[Ui[0]]]])):
                if lab[sq]=='T':
                    w=(ft[0][0]*dev[0]+ft[0][1]*dev[1],ft[1][0]*dev[0]+ft[1][1]*dev[1])
                    hits.append(dict(w=w,word=word,verified=verify(V,S,T,w)))
                    if len(hits)>=want: return hits,len(seen),'HIT'
        Ri,Ui=o.inv(R),o.inv(U)
        for a,b,N in ((R,tuple(o.comp(U,Ri)),((1,-1),(0,1))),(tuple(o.comp(R,Ui)),U,((1,0),(-1,1)))):
            nn=o.canon(a,b,lab,0)
            if nn not in seen: seen.add(nn); Q.append((nn,mul(M,N)))
        if len(seen)>limit: return hits,len(seen),'CAP'
    return hits,len(seen),('HIT' if hits else 'ORBIT_COMPLETE_NO_SEED')

def rooms(cells,wmax,count):
    case={'full':cells,'allowed':[(a+dx,b+dy) for a,b in cells for dx in range(-30,31) for dy in range(-30,31) if abs(dx)+abs(dy)<=30]}
    cnf,pool,x,ts=enc.geometry(case,wmax=wmax,kmax=0); out=[]
    with Solver(name='glucose4',bootstrap_with=cnf.clauses) as so:
        while len(out)<count and so.solve():
            m={l for l in so.get_model() if l>0}; room=[t for t,v in x.items() if v in m]
            so.add_clause([-x[t] for t in room]); V=polygon(room)
            if V is not None: out.append([tuple(map(int,v)) for v in V])
    return out
if __name__=='__main__':
    cfg=json.loads(sys.argv[1])
    for V in rooms(cfg['cells'],cfg['wmax'],cfg.get('count',3)):
        marks=[(2*a,2*b) for a,b in cfg['cells']]; S,T=marks[0],marks[-1]
        rec=dict(cells=cfg['cells'],W=len(V),V=V,S=S,T=T,raw=raw_ok(V,marks))
        if rec['raw']:
            t0=time.time(); h,n,st=seeds(V,S,T); rec.update(status=st,orbit_states=n,hits=h,secs=round(time.time()-t0,1))
        print(json.dumps(rec,default=str),flush=True)
