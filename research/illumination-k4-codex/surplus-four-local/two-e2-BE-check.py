"""One hand-derived ten-hit path and four named B/E root controls; no discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as g
from boundary_replay import replay,dot,cross,sub
from guard_checker import path_requirements
tri=lambda t:tuple(sorted(map(tuple,t)))
D=g.DIRS
def fan(c,st,m):
 return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(st,st+m)}
H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
capsfile=ROOT/'triangle-composition/inputs/caps.json'
caps={n:tri(t) for n,t in json.loads(capsfile.read_text())['cap_options'].items()}
x=lambda a:((1,0),a)
y=lambda a:((0,1),a)
word=[x(-1),y(-2),x(4),y(3),x(-1),y(-2),y(3),x(4),y(-2),x(-1)]
d=F(12,13);p=(F(0),F(0));v=(-d,F(-1));P=[p]
for n,k in word:
 t=(k-dot(n,p))/dot(n,v);assert t>0
 p=tuple(p[j]+t*v[j] for j in (0,1));P.append(p)
 q=2*dot(n,v)/dot(n,n);v=tuple(v[j]-q*n[j] for j in (0,1))
t=(2-p[0])/v[0];assert t>0
P.append(tuple(p[j]+t*v[j] for j in (0,1)))
assert P[-1]==(2,2) and len(P)-2==10
U,Z=path_requirements(P)
Bmin=fan((0,-2),1,3);Emin=fan((4,2),2,3)
fixed=H|Bmin|Emin
# Full B/E rectangles plus the ENTIRE ordinary cap alphabet.
possible=H|fan((0,-2),0,4)|fan((4,2),2,4)|set(caps.values())
assert U<=fixed and not Z&possible,('missing',U-fixed,'conflicts',Z&possible)
sigma=lambda p:(2-p[1],2-p[0]);Ps=[sigma(p) for p in P][::-1]
Us,Zs=path_requirements(Ps)
transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
assert Us==transform(U) and Zs==transform(Z)
def polygon(ts):
 edges=set()
 for a,b,c in ts:
  if cross(sub(b,a),sub(c,a))<0:b,c=c,b
  for u,v in [(a,b),(b,c),(c,a)]:
   if (v,u) in edges:edges.remove((v,u))
   else:edges.add((u,v))
 nxt=dict(edges);assert len(nxt)==len(edges)==len(set(nxt.values()))
 start=min(nxt);q=start;cyc=[]
 while True:
  assert q not in cyc;cyc.append(q);q=nxt[q]
  if q==start:break
 assert len(cyc)==len(edges)
 return [q for i,q in enumerate(cyc) if cross(sub(q,cyc[i-1]),sub(cyc[(i+1)%len(cyc)],q))]
def ledger(ts):
 data=g.check({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 assert set(data['interior_A'])=={(0,0),(2,0),(2,2)}
 os=g.owners_of(list(ts));opens={e for e,ls in os.items() if len(ls)==2};Q=J=sN=0
 for q in set().union(*map(set,ts)):
  angles,full=g.check_fan_angles(list(ts),q,os,opens)
  if g.label(q)=='A':
   if not full:Q+=3 if angles==[4] else sum(angles)
  elif full:J+=1
  elif angles==[4]:sN+=1
 return {'W':data['walls'],'k':len(data['transparent_vertices']),'Q':Q,'J':J,'sN':sN,'Delta':Q+sN-8}
controls={}
for name,b,e in [('Bwest_Ewest',(1,3),(2,3)),('Brect_Ewest',(0,4),(2,3)),('Bwest_Erect',(1,3),(2,4)),('Brect_Erect',(0,4),(2,4))]:
 ts=H|fan((0,-2),*b)|fan((4,2),*e)|{caps[n] for n in ['L-','T+','D-','Nr-']}
 ll=ledger(ts);assert ll['W']==20 and ll['k']==6 and ll['Delta']==4,(name,ll)
 V=polygon(ts);assert replay(V,(0,0),(2,2),P)==10
 assert replay(V,(2,2),(0,0),P[::-1])==10
 assert replay([sigma(q) for q in V],(0,0),(2,2),Ps)==10
 controls[name]={'status':'PASS','ledger':ll,'actual_boundary_forward_reverse_sigma':'PASS','triangles':sorted(ts),'vertices':V}
 print(name,'TEN-HIT ACTUAL S/T PASS')
out={'status':'WHOLE_B_E_WEST_RECT_FAMILY_ILLUMINATED','reflections':10,'direction':[-12,-13],'parameter':'12/13','path':[[str(a) for a in q] for q in P],'required':sorted(U),'forbidden':sorted(Z),'fixed_minimum':sorted(fixed),'possible_envelope':sorted(possible),'whole_family_full_U_Z':'PASS','sigma_guard':'PASS','controls':controls,'scope':'Single predeclared path; all four B/E west/rectangle fan combinations and arbitrary valid ordinary caps in other slots. No W/k/b restriction needed for the optical implication; four prescribed budget controls only. No direction/word/room/cap-assignment scan.','caps_sha256':hashlib.sha256(capsfile.read_bytes()).hexdigest()}
(HERE/'two-e2-BE-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('Whole symbolic B/E envelope PASS')
