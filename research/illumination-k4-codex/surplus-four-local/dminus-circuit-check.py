"""Fixed D-minus prefix identity, not a direction or word discovery scan."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'triangle-composition/inputs'))
from boundary_replay import replay,dot
from guard_checker import path_requirements
src=HERE/'single-e2-check.json';rooms=json.loads(src.read_text())['residues']
B=((1,-1),2);N=((1,1),2);L=((1,1),-2)
x=lambda a:((1,0),a)
y=lambda a:((0,1),a)
def construct(d,word,sign,terminal_x):
 p=(F(0),F(0));v=(d,F(sign));P=[p]
 for n,k in word:
  t=(k-dot(n,p))/dot(n,v);assert t>0
  p=tuple(p[j]+t*v[j] for j in (0,1));P.append(p)
  q=2*dot(n,v)/dot(n,n);v=tuple(v[j]-q*n[j] for j in (0,1))
 t=(terminal_x-p[0])/v[0];assert t>0
 P.append(tuple(p[j]+t*v[j] for j in (0,1)))
 return P,v
out={};d=F(153,1000)
for kind,lp in [('Louter4',[x(-3)]),('Louter3',[L,y(1),L])]:
 rr=rooms[kind+'_Nbplus_Dminus'];V=[tuple(map(F,q)) for q in rr['vertices']]
 tiles={tuple(sorted(map(tuple,t))) for t in rr['triangles']}
 down=[B,x(0),B,N,x(0),x(3),y(0)]+lp
 up=[N,x(0),N,B,x(0),x(3)]+lp
 row={}
 for name,word,sign in [('down',down,-1),('up',up,1)]:
  P,v=construct(d,word,sign,F(-1))
  assert P[-1]==(-1,17*d-2) and v==(1,d),(P[-1],v)
  U,Z=path_requirements(P)
  if name=='up':
   assert not U<=tiles
   row[name]={'status':'ALGEBRAIC_GATE_ONLY_PHYSICAL_PREFIX_INVALID_AT_CONTROL','reason':'L entry13*d-2 is negative; required L-minus triangle absent.','endpoint':list(map(str,P[-1])),'direction':list(map(str,v))}
   continue
  assert U<=tiles and not Z&tiles,(kind,name,U-tiles,Z&tiles)
  assert replay(V,(0,0),P[-1],P)==len(word)
  assert replay(V,P[-1],(0,0),P[::-1])==len(word)
  row[name]={'control_d':str(d),'reflections':len(word),'endpoint':list(map(str,P[-1])),'direction':list(map(str,v)),'actual_boundary_forward_reverse':'PASS','full_U_Z':'PASS','path':[[str(a) for a in pt] for pt in P]}
 # Fixed continuation: E3, four upper wall contacts, T one, D three.
 E=((1,-1),2);T=((1,-1),-2);D=((1,1),0)
 full=down+[E,y(2),E,x(1),x(3),x(1),x(3),T,D,x(2),D]
 # After D the terminal is prescribed by y=2; construct to a hand-derived x.
 endpoint_x=42*d-4
 P,v=construct(d,full,-1,endpoint_x)
 assert P[-1]==(endpoint_x,2) and v==(d,1)
 U,Z=path_requirements(P);assert U<=tiles and not Z&tiles
 assert replay(V,(0,0),P[-1],P)==len(full)
 assert replay(V,P[-1],(0,0),P[::-1])==len(full)
 row['continuation']={'status':'VALID_TRANSPORT_NOT_ACTUAL_T','control_d':str(d),'reflections':len(full),'endpoint':list(map(str,P[-1])),'target_equation':'42*d-4=2','required_target_d':'1/7','hand_branch':['5/33','2/13'],'actual_boundary_forward_reverse':'PASS','full_U_Z':'PASS','path':[[str(a) for a in pt] for pt in P]}
 out[kind]=row;print(kind,'new transport PASS; endpoint root outside hand branch')
(HERE/'dminus-circuit-check.json').write_text(json.dumps({'status':'NO_NEW_CLOSURE_VALID_TRANSPORT','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'scope':'Two prescribed downward prefixes and their hand-derived T/D continuations at d153/1000. Upward algebraic comparisons invalid at this control. Full interval is hand-derived only; no actual T certificate or discovery scan.','shared_gate':['-1','17*d-2'],'shared_direction':['1','d'],'retired_long_word':'Invalid at first L excursion: floor flips vertical component only. Claimed92d-12 endpoint is not established.','cases':out},indent=2)+'\n')
