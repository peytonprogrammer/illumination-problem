"""One frozen c2 room: exact geometry, first origami candidate, actual ray check."""
from pathlib import Path
from fractions import Fraction as Q
from collections import deque
from datetime import datetime,timezone
import importlib.util,sys,json,hashlib,signal,time,math
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
E=json.loads((R/'c2-four-corner-effort.json').read_text());end=datetime.fromisoformat(E['deadline'])
remaining=(end-datetime.now(timezone.utc)).total_seconds()
assert remaining>0
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original aggregate deadline')))
signal.setitimer(signal.ITIMER_REAL,remaining)
def deadline():
    if datetime.now(timezone.utc)>=end:raise TimeoutError('original aggregate deadline')
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
rectangles=[(0,2,0,16),(2,3,1,3),(2,3,13,15),(-1,0,6,8),(-1,0,10,12)]
cells={(x,y) for a,b,c,d in rectangles for x in range(a,b) for y in range(c,d)}
assert len(cells)==40
boundary=set()
for x,y in cells:
    vertices=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
        if (b,a) in boundary:boundary.remove((b,a))
        else:boundary.add((a,b))
nexts={}
for a,b in boundary:assert a not in nexts;nexts[a]=b
start=min(nexts);cycle=[];at=start
while at not in cycle:cycle.append(at);at=nexts[at]
assert at==start and len(cycle)==len(boundary)
V=[cycle[i] for i in range(len(cycle)) if det(sub(cycle[i],cycle[i-1]),sub(cycle[(i+1)%len(cycle)],cycle[i]))]
assert len(V)==20
S=(2,2);T=(2,14)
for x,y in (S,T):assert all((x+i,y+j) in cells for i in(-1,0) for j in(-1,0))
edges=list(zip(V,V[1:]+V[:1]))
oldfile=R.parents[1]/'illumination-k4-codex/origami-decider-review/inputs/origami_dark.py'
sp=importlib.util.spec_from_file_location('frozen',oldfile);old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
r,u,labels,root=old.build(V,S,T);labels=[{'.':0,'S':1,'T':2,'block':3}[z] for z in labels]
def canon(r,u,l,root=0):
    order=[root];index={root:0}
    for i in order:
        for j in(r[i],u[i]):
            if j not in index:index[j]=len(order);order.append(j)
    return bytes(index[r[i]] for i in order),bytes(index[u[i]] for i in order),bytes(l[i] for i in order)
def inv(p):
    a=[0]*len(p)
    for i,j in enumerate(p):a[j]=i
    return a
def trans(st,k):
    r,u,l=st
    if k==0:
        ri=inv(r);return canon(r,[u[ri[i]] for i in range(len(r))],l)
    ui=inv(u);return canon([r[ui[i]] for i in range(len(r))],u,l)
def hit(st):
    r,_,l=st;i=r[0];length=1
    while i:
        if l[i]==3:return None
        if l[i]==2:return length
        i=r[i];length+=1
    return None
def multiply(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in(0,1)) for j in(0,1)) for i in(0,1))
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
initial=canon(r,u,labels,root);assert len(initial[0])<256
queue=deque([(initial,((1,0),(0,1)),())]);seen={initial};candidates=0;tried=0;answer=None
try:
    while queue and len(seen)<=25000:
        deadline();st,A,word=queue.popleft();length=hit(st)
        if length:
            candidates+=1;chart=(A[1][1],-A[1][0]);directions=set()
            for p,q in (chart,chart[::-1]):
                for sx in(-1,1):
                    for sy in(-1,1):directions.add((sx*p,sy*q))
            for vel in sorted(directions):
                tried+=1;actual=trace(vel)
                if actual:
                    answer={'status':'FIRST_ACTUAL_PATH_VERIFIED','word':''.join('TU'[k] for k in word),'matrix':A,'chart_direction':chart,'horizontal_length':length,'actual':actual};break
            if answer:break
        for k,M in enumerate((((1,1),(0,1)),((1,0),(1,1)))):
            nxt=trans(st,k)
            if nxt not in seen:seen.add(nxt);queue.append((nxt,multiply(M,A),word+(k,)))
    if answer is None:answer={'status':'UNDECIDED','reason':'finite_state_cap_or_completed_no_positive_path','darkness_claimed':False}
except TimeoutError:
    answer={'status':'UNDECIDED','reason':'original_aggregate_deadline','darkness_claimed':False}
finally:
    signal.setitimer(signal.ITIMER_REAL,0)
    answer.update({'polygon':V,'S':S,'T':T,'walls':len(V),'area':len(cells),'origami_component_squares':len(initial[0]),'orbit_states_seen':len(seen),'horizontal_candidates_tested':candidates,'actual_direction_trials':tried,'finished_utc':datetime.now(timezone.utc).isoformat(),'original_deadline':E['deadline'],'discovery':True,'whole_goal_complete':False,'source_sha256':{'frozen_origami_builder':hashlib.sha256(oldfile.read_bytes()).hexdigest()}})
    (R/'c2-four-corner-check.json').write_text(json.dumps(answer,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in answer.items() if k not in ('polygon','actual','source_sha256')}))
    if 'actual' in answer:print(json.dumps({k:v for k,v in answer['actual'].items() if k!='path'}))
