"""Five prescribed C2 geometry controls. Deterministic band hull, no census/search.
Universal assertions require the separate hand proof, not these controls.
"""
from pathlib import Path
from fractions import Fraction as F
import ast,json,hashlib
R=Path(__file__).resolve().parent;A=R.parent/'construction'
requests=[json.loads((A/f'geometric-reduction-review-request-0{i}.json').read_text()) for i in (1,2)]
def pins():
 d={}
 for req in requests:
  for n,h in req['files_sha256'].items():
   assert hashlib.sha256((A/n).read_bytes()).hexdigest()==h,n
   d[n]=h
 return d
before=pins()
src=R/'geometric-reduction-ear-monotonicity-check.py';ns={'F':F}
mod=ast.parse(src.read_text());exec(compile(ast.Module(body=[n for n in mod.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),str(src),'exec'),ns)
cr=ns['cross'];edges=ns['edges'];intersect=ns['intersects'];classify=ns['classify']
def area2(p):return sum(a[0]*b[1]-a[1]*b[0] for a,b in edges(p))
def positive(p):return p if area2(p)>0 else p[::-1]
def kinds(p):return [cr(p[i-1],p[i],p[(i+1)%len(p)])<0 for i in range(len(p))]
def validate(p):
 assert area2(p)>0 and len(set(p))==len(p)
 for i,(a,b) in enumerate(edges(p)):
  assert a!=b and (a[0]==b[0] or a[1]==b[1]) and cr(p[i-1],a,b)!=0
  for j,(c,d) in enumerate(edges(p)):
   if j<=i or j in ((i+1)%len(p),(i-1)%len(p)):continue
   assert not intersect(a,b,c,d),(i,j)
 return sum(kinds(p))
def simplify(p):
 q=[]
 for x in p:
  if not q or q[-1]!=x:q.append(x)
 if q[0]==q[-1]:q.pop()
 while True:
  drop=next((i for i in range(len(q)) if cr(q[i-1],q[i],q[(i+1)%len(q)])==0),None)
  if drop is None:break
  q.pop(drop)
 return positive(q)
def canonical(p):return min(tuple(p[i:]+p[:i]) for i in range(len(p)))
def hull(p):
 ys=sorted({y for x,y in p});bands=[]
 for low,high in zip(ys,ys[1:]):
  y=F(low+high,2)
  xs=sorted(a[0] for a,b in edges(p) if a[0]==b[0] and min(a[1],b[1])<y<max(a[1],b[1]))
  assert xs and len(xs)%2==0
  bands.append((low,high,xs[0],xs[-1]))
 for a,b in zip(bands,bands[1:]):assert max(a[2],b[2])<min(a[3],b[3])
 left=[(bands[0][2],bands[0][0])];right=[(bands[0][3],bands[0][0])]
 for i,(low,high,l,r) in enumerate(bands):
  left.append((l,high));right.append((r,high))
  if i+1<len(bands):
   left.append((bands[i+1][2],high));right.append((bands[i+1][3],high))
 q=simplify([left[0]]+right+list(reversed(left)))
 return q,bands
D=[(-1,-1),(0,-1),(0,-2),(1,-2),(1,-3),(2,-3),(2,-1),(1,-1),(1,1),(3,1),(3,0),(5,0),(5,1),(4,1),(4,2),(3,2),(3,3),(1,3),(1,2),(0,2),(0,1),(-1,1)]
spiral=[(2,2),(2,10),(10,10),(10,4),(6,4),(6,0),(14,0),(14,14),(0,14),(0,2)]
avail=json.loads((A/'geometric-reduction-check-01.json').read_text())['availability_control']
controls=[('known22',D,(0,0),(2,2)),('reviewer_r3_spiral',spiral,(2,12),(12,2)),('author_r4_noCRC',list(map(tuple,avail['polygon'])),(2,10),(18,10)),('reviewer_L',[(0,0),(8,0),(8,4),(4,4),(4,8),(0,8)],(6,2),(2,6)),('prescribed_square',[(0,0),(24,0),(24,24),(0,24)],(12,12),(16,18))]
rows=[]
for name,p,S,T in controls:
 p=positive(p);r=validate(p)
 for axis in ['horizontal','vertical']:
  w=p if axis=='horizontal' else positive([(y,x) for x,y in p]);marks=[S,T] if axis=='horizontal' else [(y,x) for x,y in (S,T)]
  types=kinds(w);walls=[];C=M=RR=0
  for i,(a,b) in enumerate(edges(w)):
   if a[1]!=b[1]:continue
   refs=types[i]+types[(i+1)%len(w)]
   if refs==0:C+=1
   elif refs==1:M+=1
   else:RR+=1
   walls.append((a,b,refs,i))
  assert C==RR+2 and r==M+2*RR
  q,bands=hull(w);rq=validate(q)
  assert rq<=M+RR and all(classify(q,mark)=='interior' for mark in marks)
  assert canonical(hull(q)[0])==canonical(q)
  changed=canonical(w)!=canonical(q)
  assert not changed or (RR>0 and rq<r)
  # Independent injection: every output horizontal wall contains one WHOLE old nonRR wall.
  matching=[];used=set()
  for a,b in edges(q):
   if a[1]!=b[1]:continue
   candidates=[idx for c,d,refs,idx in walls if refs<2 and c[1]==a[1] and min(a[0],b[0])<=min(c[0],d[0])<max(c[0],d[0])<=max(a[0],b[0])]
   assert candidates
   chosen=next(idx for idx in candidates if idx not in used);used.add(chosen);matching.append(dict(output_wall=[a,b],input_wall_index=chosen))
  rows.append(dict(name=name,axis=axis,input_reflex=r,C=C,M=M,R=RR,output_reflex=rq,changed=changed,output_polygon=q,band_rectangles=bands,whole_old_wall_injection=matching))
after=pins();assert before==after
out={'status':'PASS_TEN_PRESCRIBED_HULL_CONTROLS','source_pins_before':before,'source_pins_after':after,'reviewer_geometry_helpers_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'prescribed_input_polygons':5,'axis_controls':10,'rows':rows,'author_checker_executed':False,'new_search_or_census':False,'universal_lemma_proved_by_controls':False,'whole_goal_complete':False}
(R/'geometric-reduction-hull-independent-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['name','axis','input_reflex','R','output_reflex','changed']} for r in rows],indent=2))
