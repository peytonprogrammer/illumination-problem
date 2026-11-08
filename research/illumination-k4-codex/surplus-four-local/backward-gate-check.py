"""Four hand-derived upward-launch paths, no direction or word search."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,dot,cross,sub
from boundary_replay import replay
import illumination_geometry as g
SOURCE=HERE/'single-e2-check.json'
rooms=json.loads(SOURCE.read_text())['residues']
Ndiag=((1,1),2);Bdiag=((1,-1),2);Rdiag=((1,-1),4)
Ediag=((1,-1),2);Tdiag=((1,-1),-2);Ldiag=((1,1),-2)
base=[Ndiag,((1,0),0),Ndiag,Bdiag,((1,0),0)]
# Each mirror sequence is fixed by the preceding hand derivation.
Dtail=[Ediag,((0,1),2),Ediag,
       ((1,0),1),((1,0),3),((1,0),1),((1,0),3),
       ((0,1),3),((1,0),1),((1,0),3),((1,0),1)]
Rtail=[((1,0),3),((1,0),-1),Rdiag,
       ((0,1),3),((0,1),-1),Tdiag,
       ((1,0),3),((1,0),1),((1,0),3)]
Dleft={'Louter4':[((1,0),-3)],'Louter3':[Ldiag,((0,1),1),Ldiag]}
Rleft={'Louter4':[((1,0),-3),((0,1),1)],'Louter3':[Ldiag,((0,1),1),Ldiag,((0,1),1)]}

def prescribed(d,word):
 p=(F(0),F(0));v=(d,F(1));P=[p]
 for normal,k in word:
  t=(k-dot(normal,p))/dot(normal,v)
  assert t>0,('nonpositive flight',p,v,normal,k,t)
  p=tuple(p[i]+t*v[i] for i in (0,1));P.append(p)
  scale=2*dot(normal,v)/dot(normal,normal)
  v=tuple(v[i]-scale*normal[i] for i in (0,1))
 t=(2-p[0])/v[0];assert t>0
 p=tuple(p[i]+t*v[i] for i in (0,1));assert p==(2,2),('missed actual target',p)
 P.append(p);return P

results={}
for kind in ['Louter3','Louter4']:
 for variant,d,word in [
  ('Dminus',F(3,19),base+[((1,0),3)]+Dleft[kind]+Dtail),
  ('Rminus',F(4,25),base+[Rdiag,((0,1),0),Rdiag]+Rleft[kind]+Rtail)]:
  if variant=='Dminus':continue
  name=kind+'_Nbplus_'+variant;rr=rooms[name]
  V=[tuple(map(F,p)) for p in rr['vertices']]
  ts={tuple(sorted(map(tuple,t))) for t in rr['triangles']}
  P=prescribed(d,word)
  
  U,Z=path_requirements(P)
  assert U<=ts and not Z&ts,(name,'missing',U-ts,'conflict',Z&ts)
  assert replay(V,(0,0),(2,2),P)==len(word)
  assert replay(V,(2,2),(0,0),P[::-1])==len(word)
  sigma=lambda p:(2-p[1],2-p[0])
  Ps=[sigma(p) for p in P][::-1]
  assert replay([sigma(p) for p in V],(0,0),(2,2),Ps)==len(word)
  Us,Zs=path_requirements(Ps)
  transform=lambda a:{tuple(sorted(sigma(p) for p in t)) for t in a}
  assert Us==transform(U) and Zs==transform(Z)
  gg=g.check({'triangles':sorted(ts),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
  assert gg['walls']==20 and len(gg['transparent_vertices'])==6 and set(gg['interior_A'])=={(0,0),(2,0),(2,2)}
  results[name]={'status':'ACTUAL_S_T_PASS','direction':[d.numerator,d.denominator],'initial_direction_convention':'(numerator,denominator), both positive','parameter':str(d),'reflections':len(word),'path':[[str(x) for x in p] for p in P],'required_triangles':sorted(U),'forbidden_triangles':sorted(Z),'mirrors':[{'normal':n,'offset':k} for n,k in word],'actual_boundary_forward_reverse_sigma':'PASS','ledger':rr['ledger']}
  print(name,len(word),'PASS')
out={'status':'TWO_R_MINUS_RESIDUES_ILLUMINATED','rejected_D_candidate':{'parameter':'3/19','reason':'The earlier ascent reaches true315-degree corner (1,1); omitted elbow inequality requires d<3/19.'},'scope':'Two successful predeclared R-variant words and directions; D-variant endpoint rejected. No direction/word/room scan or archive. Physical actual-boundary forward/reverse/sigma plus full tile guards.','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'paths':results}
(HERE/'backward-gate-check.json').write_text(json.dumps(out,indent=2)+'\n')
