"""Five analytically prescribed source/return compositions; no discovery."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,dot,cross,sub
from boundary_replay import replay
import illumination_geometry as g
D=g.DIRS;tri=lambda t:tuple(sorted(map(tuple,t)))
def fan(c,st,m):return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(st,st+m)}
H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options'].items()}
def polygon(ts):
 edges=set()
 for t in ts:
  a,b,c=t
  if cross(sub(b,a),sub(c,a))<0:b,c=c,b
  for u,v in [(a,b),(b,c),(c,a)]:
   if (v,u) in edges:edges.remove((v,u))
   else:edges.add((u,v))
 out={a:b for a,b in edges};assert len(out)==len(edges)
 start=min(out);p=start;cyc=[]
 while True:
  assert p not in cyc;cyc.append(p);p=out[p]
  if p==start:break
 assert len(cyc)==len(edges)
 return [p for i,p in enumerate(cyc) if cross(sub(p,cyc[i-1]),sub(cyc[(i+1)%len(cyc)],p))]

def prescribed(d,prefix,roof):
 p=(F(0),F(0));v=(F(-1),d);P=[p]
 E=[((1,-1),2),((0,1),2),((1,-1),2)]
 # E diagonal is y=x-2, equivalently x-y=2.
 N=[((1,1),2),((0,1),2),((1,1),2)] if roof else [((1,0),1)]
 for normal,offset in prefix+E+N:
  t=(offset-dot(normal,p))/dot(normal,v);assert t>0
  p=tuple(p[k]+t*v[k] for k in (0,1));P.append(p)
  q=2*dot(normal,v)/dot(normal,normal)
  v=tuple(v[k]-q*normal[k] for k in (0,1))
 t=(2-p[0])/v[0];assert t>0
 p=tuple(p[k]+t*v[k] for k in (0,1));assert p==(2,2);P.append(p)
 return P
source_specs={
 'short_square':([((1,0),-2)],7,3),
 'wide_rectangle':([((1,0),-3)],0,4),
 'trapezoid':([((1,1),-2),((0,1),1),((1,1),-2)],0,3),
}
specs=[('short_square_flat','short_square',False,F(1,6)),('wide_rectangle_Ncap','wide_rectangle',True,F(1,8)),('trapezoid_Ncap','trapezoid',True,F(1,8))]
results={}
for name,kind,N,d in specs:
 prefix,st,m=source_specs[kind];P=prescribed(d,prefix,N)
 U,Z=path_requirements(P)
 fixed=H|fan((-2,0),st,m)|{caps['E-']}|({caps['Nr-']} if N else set())
 assert U<=fixed and not Z&fixed,(name,'missing',U-fixed,'conflict',Z&fixed)
 absent=['L-','E+','Nb-','Nb+','Nr+'] if N else ['L-','E+','Nr-']
 # L is a prescribed positive cell, so possible must remove its ordinary
 # cap labels before re-adding the exact fan. L- is present in short_square.
 possible=H|fan((-2,0),st,m)|{t for n,t in caps.items() if not n.startswith('L') and n not in absent}
 assert not Z&possible,(name,'variable conflict',Z&possible)
 # Short-square and trapezoid prefixes tolerate the stated added lower mate.
 extensions=[]
 for est,em,label in ([(6,4,'Lrectangle')] if kind=='short_square' else [(7,4,'Lfullnorth')] if kind=='trapezoid' else []):
  root=fan((-2,0),est,em)
  assert U<=H|root|{caps['E-']}|({caps['Nr-']} if N else set())
  assert not Z&root
  extensions.append(label)
 labels=['B+','E-','T-','D-','R+']+(['Nr-'] if N else ['Nb+'])
 room=H|fan((-2,0),st,m)|{caps[n] for n in labels}
 gg=g.check({'triangles':sorted(room),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
 V=polygon(room);replay(V,(0,0),(2,2),P);replay(V,(2,2),(0,0),P[::-1])
 sigma=lambda p:(2-p[1],2-p[0])
 replay([sigma(p) for p in V],(0,0),(2,2),[sigma(p) for p in P][::-1])
 results[name]={'status':'PASS','parameter':str(d),'reflections':len(P)-2,'path':[[str(v) for v in p] for p in P],'required':sorted(U),'forbidden':sorted(Z),'cap_blockers':[n for n,t in caps.items() if t in Z],'added_fan_extensions':extensions,'fixture':{'W':gg['walls'],'k':len(gg['transparent_vertices']),'triangles':sorted(room),'vertices':V},'boundary_forward_reverse_sigma':'PASS'}
(HERE/'left-return-check.json').write_text(json.dumps({'status':'PASS','paths':results,'scope':'Three hand-derived prescribed paths; whole ordinary-cap implications and two extra-fan extensions; three prescribed controls and exact actual-boundary replay. No scan or archive.'},indent=2)+'\n')
print(json.dumps({n:{k:r[k] for k in ['reflections','parameter','cap_blockers','added_fan_extensions']} for n,r in results.items()},indent=2))
