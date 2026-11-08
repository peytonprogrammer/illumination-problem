"""Fixed36residue candidate cover for the A1 below-upper-mark region."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import json,signal,math,hashlib
R=Path(__file__).resolve().parent
E=json.loads((R/'c2-A1-below-effort.json').read_text());end=datetime.fromisoformat(E['deadline'])
remaining=(end-datetime.now(timezone.utc)).total_seconds();assert remaining>0
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original aggregate deadline')))
signal.setitimer(signal.ITIMER_REAL,remaining)
def deadline():
    if datetime.now(timezone.utc)>=end:raise TimeoutError('original aggregate deadline')
def geometry(h,d):
    G=2*h+d+4
    rects=[(0,2,0,G),(2,3,1,3),(2,3,2*h+1,2*h+3),(-1,0,h,h+2),(-1,0,h+d+2,h+d+4)]
    cells={(x,y) for a,b,c,e in rects for x in range(a,b) for y in range(c,e)}
    boundary=set()
    for x,y in cells:
        v=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        for a,b in zip(v,v[1:]+v[:1]):
            if (b,a) in boundary:boundary.remove((b,a))
            else:boundary.add((a,b))
    nxt={}
    for a,b in boundary:assert a not in nxt;nxt[a]=b
    start=min(nxt);cycle=[];i=start
    while i not in cycle:cycle.append(i);i=nxt[i]
    assert i==start and len(cycle)==len(boundary)
    V=[cycle[i] for i in range(len(cycle)) if det(sub(cycle[i],cycle[i-1]),sub(cycle[(i+1)%len(cycle)],cycle[i]))]
    assert len(V)==20 and len(cells)==2*G+8
    S,T=(2,2),(2,2*h+2)
    for x,y in(S,T):assert all((x+i,y+j) in cells for i in(-1,0) for j in(-1,0))
    return V,S,T

def sub(a,b):return(a[0]-b[0],a[1]-b[1])

def det(a,b):return a[0]*b[1]-a[1]*b[0]

def dot(a,b):return a[0]*b[0]+a[1]*b[1]

def trace(vel):
    p=tuple(map(Q,S));v=vel;path=[p];walls=[];seen=set();guards=0
    for _ in range(4000):
        deadline();state=(p,v)
        if state in seen:return None
        seen.add(state);events=[]
        for k,(a,b) in enumerate(edges):
            guards+=1;e=sub(b,a);den=det(v,e)
            if not den:continue
            t=Q(det(sub(a,p),e),den);z=Q(det(sub(a,p),v),den)
            if t>0 and 0<=z<=1:events.append((t,k,z))
        assert events
        first=min(a[0] for a in events)
        dt=Q(T[0]-p[0],v[0]) if v[0] else Q(T[1]-p[1],v[1])
        if 0<dt<first and tuple(p[k]+dt*v[k] for k in(0,1))==T:
            path.append(tuple(map(Q,T)));return {'direction':vel,'path':path,'walls':walls,'reflections':len(walls),'all_wall_leg_guards':guards}
        collisions=[e for e in events if e[0]==first]
        if len(collisions)!=1 or not 0<collisions[0][2]<1:return None
        _,wall,_=collisions[0];p=tuple(p[k]+first*v[k] for k in(0,1));path.append(p);walls.append(wall)
        a,b=edges[wall]
        v=(-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1])
    return None

rows=[];failure=None
try:
    for d in range(2,14,2):
        for rr in range(6):
            deadline();h=d+4+2*rr;V,S,T=geometry(h,d);edges=list(zip(V,V[1:]+V[:1]));answer=None;trials=0
            directions=[(-7,-3)]
            for q in(1,3):
                for pp in range(1,36):
                    if math.gcd(pp,q)!=1:continue
                    for sx in(-1,1):
                        for sy in(-1,1):
                            v=(sx*pp,sy*q)
                            if v not in directions:directions.append(v)
            for v in directions:
                trials+=1;actual=trace(v)
                if actual:
                    answer={'h':h,'d':d,'r':rr,'status':'FIRST_ACTUAL_PATH_VERIFIED','polygon':V,'S':S,'T':T,'actual':actual,'trials':trials};break
            if answer is None:
                failure={'h':h,'d':d,'r':rr,'status':'FINITE_PACK_UNRESOLVED','trials':trials};print(json.dumps(failure),flush=True);break
            rows.append(answer);print(json.dumps({'h':h,'d':d,'r':rr,'direction':actual['direction'],'reflections':actual['reflections'],'guards':actual['all_wall_leg_guards'],'trials':trials}),flush=True)
        if failure:break
    status='ALL36_FIXED_RESIDUES_ACTUALLY_VERIFIED' if len(rows)==36 and failure is None else 'FIXED_PACK_FAILED_NO_DARKNESS_CLAIM'
except TimeoutError:
    status='UNDECIDED_ORIGINAL_DEADLINE'
finally:
    signal.setitimer(signal.ITIMER_REAL,0)
    out={'status':status,'rows':rows,'first_uncovered_residue':failure,'original_deadline':E['deadline'],'finished_utc':datetime.now(timezone.utc).isoformat(),'discovery':True,'whole_goal_complete':False,'no_darkness_claim':True,'source_sha256':{'c2-critical-family-check.py':hashlib.sha256((R/'c2-critical-family-check.py').read_bytes()).hexdigest()}}
    (R/'c2-A1-below-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(status,flush=True)
