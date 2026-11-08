"""R57 protected-word discovery and exact critical-parameter partition."""
from fractions import Fraction as Q
from pathlib import Path
import ast,json,time,importlib.util
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
DEADLINE=1794039360 # 2026-11-07 08:16 UTC

def contour(D):
 return [tuple(map(Q,z)) for z in [(0,0),(1,0),(1,1),(Q(4,3),1),(Q(4,3),3),(1,3),(1,5),(D+2,5),(D+2,7),(1,7),(1,9),(0,9),(0,7),(-1,7),(-1,5),(0,5),(0,4),(-1,4),(-1,2),(0,2)]]
def trace(D,v,limit=70):
 V=contour(D);S=(Q(1),Q(2));T=(1+D,Q(6));z=S;word=[];path=[S]
 for step in range(limit+1):
  if time.time()>DEADLINE:raise TimeoutError
  cc=[]
  for i,(a,b) in enumerate(g.edges(V)):
   e=g.vec(a,b);den=g.det(v,e)
   if not den:continue
   tt=g.det(g.vec(z,a),e)/den;rr=g.det(g.vec(z,a),v)/den
   if tt>0 and 0<=rr<=1:cc.append((tt,i,rr))
  if not cc:return None
  tm=min(x[0] for x in cc);dt=g.vec(z,T)
  if g.det(v,dt)==0 and g.dot(v,dt)>0:
   tt=dt[0]/v[0] if v[0] else dt[1]/v[1]
   if tt<tm:return word,path+[T]
  hits=[(i,r) for t,i,r in cc if t==tm]
  if len(hits)!=1 or not 0<hits[0][1]<1:return None
  i=hits[0][0]
  if i in [8,12,13,14,16,17,18]:return None
  z=(z[0]+tm*v[0],z[1]+tm*v[1]);path.append(z)
  # target tooth excursion cannot go beyond actual target abscissa
  if z[0]>1+D and 5<=z[1]<=7:return None
  word.append(i);a,b=g.edges(V)[i];v=(-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1])
 return None

def image(word,p):
 # compose actual wall reflections on the right of current copy map
 sx=sy=Q(1);tx=ty=Q(0);V=contour(Q(0))
 for i in word:
  a,b=g.edges(V)[i]
  if a[0]==b[0]:tx+=2*sx*a[0];sx=-sx
  else:ty+=2*sy*a[1];sy=-sy
 return sx*p[0]+tx,sy*p[1]+ty

def direction(word,D):
 x,y=image(word,(1+D,Q(6)));return x-1,y-2

def root(f):
 a=f(Q(0));b=f(Q(1))-a
 return [-a/b] if b and 0<=-a/b<=2 else []

def cuts(word):
 out={Q(0),Q(2)};out.update(root(lambda D:direction(word,D)[0]))
 for j in range(len(word)+1):
  prefix=word[:j]
  # all transformed corners: candidate next-wall/corner events
  for k in range(20):
   def detcorner(D):
    x,y=image(prefix,contour(D)[k]);dx,dy=direction(word,D);return (x-1)*dy-(y-2)*dx
   out.update(root(detcorner))
  # actual target in every earlier physical copy: early-arrival events
  def early(D):
   x,y=image(prefix,(1+D,Q(6)));dx,dy=direction(word,D);return (x-1)*dy-(y-2)*dx
  out.update(root(early))
  # protection boundary x=1+D in target band: all horizontal hit levels
  for yy in [Q(5),Q(7)]:
   def boundary(D):
    x,y=image(prefix,(1+D,yy));dx,dy=direction(word,D);return (x-1)*dy-(y-2)*dx
   out.update(root(boundary))
 return sorted(out)

def discover(D):
 # Exact group-derived target images. Bounded failure is undecided.
 for N in range(1,25):
  for r in range(-N,N+1):
   if not r:continue
   for k in range(-N,N+1):
    if max(abs(r),abs(k))!=N:continue
    for sig in [1,-1]:
     v=(sig*D+sig-1+Q(2*k,3),Q(2*r))
     if v==(0,0):continue
     ans=trace(D,v)
     if ans:return ans[0]
 return None

def certify(word):
 cs=cuts(word);ints=[];pts=[]
 for D in cs:
  a=trace(D,direction(word,D))
  if a and a[0]==word:pts.append(D)
 for a,b in zip(cs,cs[1:]):
  ans=trace((a+b)/2,direction(word,(a+b)/2))
  if ans and ans[0]==word:ints.append((a,b))
 return ints,pts

def enc(x):return str(x)
if __name__=='__main__':
 words=[[19,0,3,15]];rows=[];allints=[];allpts=set();tested=[]
 try:
  for attempt in range(25):
   w=words[-1];ii,pp=certify(w);rows.append({'word':w,'intervals':[[str(a),str(b)] for a,b in ii],'points':list(map(str,pp))});allints+=ii;allpts.update(pp)
   endpoints=sorted({Q(0),Q(2)}|{x for ab in allints for x in ab}|allpts)
   todo=[x for x in endpoints if x not in allpts and not any(a<x<b for a,b in allints)]
   todo += [(a+b)/2 for a,b in zip(endpoints,endpoints[1:]) if not any(c<(a+b)/2<d for c,d in allints)]
   if not todo:break
   D=next((x for x in todo if x not in tested),None)
   if D is None:break
   tested.append(D);w=discover(D)
   print('point',D,'word',w,flush=True)
   if w is None:break
   if w in words:break
   words.append(w)
  status='CANDIDATE_FULL_COVER' if not todo else 'INCOMPLETE'
 except TimeoutError:status='DEADLINE';todo=['not fully computed']
 out={'status':status,'whole_goal_complete':False,'original_deadline_utc':'2026-11-07T08:16:00Z','rows':rows,'uncovered_probes':list(map(str,todo)),'tested':list(map(str,tested)),'warning':'Interval argument requires independent proof audit; no darkness inference.'}
 (R/'h2-depth-prefix-check.json').write_text(json.dumps(out,indent=2)+'\n');print(status,flush=True)
