"""One frozen c2 room: exact geometry, first origami candidate, actual ray check."""
from pathlib import Path
from fractions import Fraction as Q
from collections import deque
from datetime import datetime,timezone
import importlib.util,sys,json,hashlib,signal,time,math
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
E=json.loads((R/'tooth-return-grid-effort.json').read_text());end=datetime.fromisoformat(E['deadline'])
remaining=(end-datetime.now(timezone.utc)).total_seconds()
assert remaining>0
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('original aggregate deadline')))
signal.setitimer(signal.ITIMER_REAL,remaining)
def deadline():
    if datetime.now(timezone.utc)>=end:raise TimeoutError('original aggregate deadline')
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
UNIT="cells={(x,y) for a,b,c,d in rectangles for x in range(a,b) for y in range(c,d)}\nassert len(cells)==G+4*(D+1)+2*(aa+bb)\nboundary=set()\nfor x,y in cells:\n    vertices=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]\n    for a,b in zip(vertices,vertices[1:]+vertices[:1]):\n        if (b,a) in boundary:boundary.remove((b,a))\n        else:boundary.add((a,b))\nnexts={}\nfor a,b in boundary:assert a not in nexts;nexts[a]=b\nstart=min(nexts);cycle=[];at=start\nwhile at not in cycle:cycle.append(at);at=nexts[at]\nassert at==start and len(cycle)==len(boundary)\nV=[cycle[i] for i in range(len(cycle)) if det(sub(cycle[i],cycle[i-1]),sub(cycle[(i+1)%len(cycle)],cycle[i]))]\nassert len(V)==expected_W\nS=(1+D,2);T=(1+D,2*h+2)\nfor x,y in (S,T):assert all((x+i,y+j) in cells for i in(-1,0) for j in(-1,0))\nedges=list(zip(V,V[1:]+V[:1]))\noldfile=R.parents[1]/'illumination-k4-codex/origami-decider-review/inputs/origami_dark.py'\nsp=importlib.util.spec_from_file_location('frozen',oldfile);old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)\nr,u,labels,root=old.build(V,S,T);labels=[{'.':0,'S':1,'T':2,'block':3}[z] for z in labels]\ndef canon(r,u,l,root=0):\n    order=[root];index={root:0}\n    for i in order:\n        for j in(r[i],u[i]):\n            if j not in index:index[j]=len(order);order.append(j)\n    return tuple(index[r[i]] for i in order),tuple(index[u[i]] for i in order),tuple(l[i] for i in order)\ndef inv(p):\n    a=[0]*len(p)\n    for i,j in enumerate(p):a[j]=i\n    return a\ndef trans(st,k):\n    r,u,l=st\n    if k==0:\n        ri=inv(r);return canon(r,[u[ri[i]] for i in range(len(r))],l)\n    ui=inv(u);return canon([r[ui[i]] for i in range(len(r))],u,l)\ndef hit(st):\n    r,_,l=st;i=r[0];length=1\n    while i:\n        if l[i]==3:return None\n        if l[i]==2:return length\n        i=r[i];length+=1\n    return None\ndef multiply(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in(0,1)) for j in(0,1)) for i in(0,1))\ndef trace(vel):\n    p=tuple(map(Q,S));v=vel;path=[p];walls=[];seen=set();guards=0\n    for _ in range(4000):\n        deadline();state=(p,v)\n        if state in seen:return None\n        seen.add(state);events=[]\n        for k,(a,b) in enumerate(edges):\n            guards+=1;e=sub(b,a);den=det(v,e)\n            if not den:continue\n            t=Q(det(sub(a,p),e),den);z=Q(det(sub(a,p),v),den)\n            if t>0 and 0<=z<=1:events.append((t,k,z))\n        assert events\n        first=min(a[0] for a in events)\n        dt=Q(T[0]-p[0],v[0]) if v[0] else Q(T[1]-p[1],v[1])\n        if 0<dt<first and tuple(p[k]+dt*v[k] for k in(0,1))==T:\n            path.append(tuple(map(Q,T)));return {'direction':vel,'path':path,'walls':walls,'reflections':len(walls),'all_wall_leg_guards':guards}\n        collisions=[e for e in events if e[0]==first]\n        if len(collisions)!=1 or not 0<collisions[0][2]<1:return None\n        _,wall,_=collisions[0];p=tuple(p[k]+first*v[k] for k in(0,1));path.append(p);walls.append(wall)\n        a,b=edges[wall]\n        v=(-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1])\n    return None\ninitial=canon(r,u,labels,root);assert len(initial[0])<2000\nqueue=deque([(initial,((1,0),(0,1)),())]);seen={initial};candidates=0;tried=0;answer=None\nwhile queue and len(seen)<=1500:\n    deadline();st,A,word=queue.popleft();length=hit(st)\n    if length:\n        candidates+=1;chart=(A[1][1],-A[1][0]);directions=set()\n        for p,q in (chart,chart[::-1]):\n            for sx in(-1,1):\n                for sy in(-1,1):directions.add((sx*p,sy*q))\n        for vel in sorted(directions):\n            tried+=1;actual=trace(vel)\n            if actual:\n                answer={'status':'FIRST_ACTUAL_PATH_VERIFIED','word':''.join('TU'[k] for k in word),'matrix':A,'chart_direction':chart,'horizontal_length':length,'actual':actual};break\n        if answer:break\n    for k,M in enumerate((((1,1),(0,1)),((1,0),(1,1)))):\n        nxt=trans(st,k)\n        if nxt not in seen:seen.add(nxt);queue.append((nxt,multiply(M,A),word+(k,)))\nif answer is None:answer={'status':'UNDECIDED','reason':'finite_state_cap_or_completed_no_positive_path','darkness_claimed':False}\n"
rows=[];h=4;d=2;D=1;G=16;expected_W=20
try:
 for aa in (2,3,4,8):
  for bb in (2,3,4,8):
   deadline();rectangles=[(0,1,0,G),(1,D+2,1,3),(1,D+2,2*h+1,2*h+3),(-aa,0,h,h+2),(-bb,0,h+d+2,h+d+4)]
   exec(UNIT,globals())
   answer.update({"h":h,"d":d,"D":D,"a":aa,"b":bb,"polygon":V,"S":S,"T":T,"walls":len(V),"area":len(cells),"orbit_states_seen":len(seen)})
   rows.append(answer);print(json.dumps({k:v for k,v in answer.items() if k not in("polygon","actual")}),flush=True)
   if answer["status"]!="FIRST_ACTUAL_PATH_VERIFIED":raise RuntimeError("first isolated room undecided; stop prescribed effort")
except (TimeoutError,RuntimeError) as ex:rows.append({"status":"INCOMPLETE","reason":str(ex)})
finally:
 signal.setitimer(signal.ITIMER_REAL,0)
 out={"status":"ALL_SIXTEEN_PRESCRIBED_ISOLATED_PATHS_PASS" if len(rows)==16 and all(z["status"]=="FIRST_ACTUAL_PATH_VERIFIED" for z in rows) else"INCOMPLETE_NO_DARKNESS","rows":rows,"original_deadline":E["deadline"],"finished_utc":datetime.now(timezone.utc).isoformat(),"discovery":True,"whole_goal_complete":False}
 (R/"tooth-return-grid-seeds.json").write_text(json.dumps(out,indent=2,default=str)+"\n");print(out["status"],flush=True)
