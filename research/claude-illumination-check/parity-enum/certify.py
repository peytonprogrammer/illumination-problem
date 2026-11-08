"""Dedupe enumerated parity rooms by symmetry and certify isolation for each pair of interior A points."""
import sys,json,subprocess,itertools,os
from fractions import Fraction
RIG=os.path.abspath('../rigidity')
def parse(line):
 f=line.split();W=int(f[0]);V=[tuple(map(int,p.split(','))) for p in f[2:]];return W,V
def interior_A(V):
 xs=[x for x,_ in V];ys=[y for _,y in V];out=[]
 n=len(V)
 def onb(x,y):
  for i in range(n):
   (ax,ay),(bx,by)=V[i],V[(i+1)%n]
   if (bx-ax)*(y-ay)-(by-ay)*(x-ax)==0 and min(ax,bx)<=x<=max(ax,bx) and min(ay,by)<=y<=max(ay,by):return True
  return False
 for y in range(min(ys)+1,max(ys)):
  for x in range(min(xs)+1,max(xs)):
   if x%2 or y%2 or onb(x,y):continue
   c=0
   for i in range(n):
    (ax,ay),(bx,by)=V[i],V[(i+1)%n]
    if (ay>y)!=(by>y) and ax+Fraction((y-ay)*(bx-ax),by-ay)>x:c^=1
   if c:out.append((x,y))
 return out
G=[lambda x,y:(x,y),lambda x,y:(-y,x),lambda x,y:(-x,-y),lambda x,y:(y,-x),lambda x,y:(-x,y),lambda x,y:(y,x),lambda x,y:(x,-y),lambda x,y:(-y,-x)]
def canon(V,marks):
 best=None
 for g in G:
  P=[g(*v) for v in V];M=[g(*m) for m in marks]
  mx=min(x for x,_ in P);my=min(y for _,y in P);mx-=mx%2;my-=my%2
  P=[(x-mx,y-my) for x,y in P];M=tuple(sorted((x-mx,y-my) for x,y in M))
  if sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P)))<0:P=P[::-1]
  i0=P.index(min(P));P=P[i0:]+P[:i0]
  k=(tuple(P),M)
  if best is None or k<best:best=k
 return best
rooms={}
for fn in sys.argv[1:]:
 for line in open(fn):
  if not line.strip():continue
  W,V=parse(line);IA=interior_A(V)
  for s,t in itertools.combinations(IA,2):
   k=canon(V,[s,t])
   if k not in rooms:rooms[k]=(W,V,s,t,len(IA))
print(len(rooms),'room-pair classes',file=sys.stderr)
os.makedirs('certs',exist_ok=True)
for i,(k,(W,V,s,t,nA)) in enumerate(sorted(rooms.items(),key=lambda kv:kv[1][0])):
 tag=f'parity-W{W}-{i}'
 json.dump(dict(vertices=[list(v) for v in V],marked=[list(s),list(t)],tag=tag,interior_A=nA),open(f'certs/{tag}.json','w'))
 res={}
 for R in (12,18):
  out=subprocess.run([f'{RIG}/venv/bin/python',f'{os.path.abspath(RIG)}/rigidity45.py',os.path.abspath(f'certs/{tag}.json'),str(R)],capture_output=True,text=True,cwd='certs')
  summ=json.loads(out.stdout.strip().splitlines()[-1]) if out.returncode==0 else {'error':out.stderr[-300:]}
  ps=subprocess.run([f'{RIG}/venv/bin/python',f'{os.path.abspath(RIG)}/posspan.py',f'funcs-{tag}-R{R}.json'],capture_output=True,text=True,cwd='certs') if 'error' not in summ else None
  rigid=bool(ps and 'RIGID' in ps.stdout)
  res=dict(W=W,interior_A=nA,R=R,events=summ.get('events'),lit=summ.get('lit_paths'),rank=summ.get('rank_on_closure'),target=summ.get('target'),rigid=rigid,error=summ.get('error'))
  if rigid or res['lit']:break
 print(json.dumps(dict(tag=tag,marks=[s,t],**res)),flush=True)
