"""Exact replay of three prescribed analytic continuations; no optical search."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
from guard_checker import path_requirements,dot,cross,sub
from boundary_replay import replay
import illumination_geometry as g
source=json.loads((HERE/'single-e2-check.json').read_text())['residues']
# Mirrors were derived by local return maps, before these replays.
prefixes={
 'Louter4':[((1,0),-3)],
 'Louter3':[((1,1),-2),((0,1),1),((1,1),-2)]}
Ndiag=((1,1),2);Bdiag=((1,-1),2)
words={
 'N_B_roundtrip':[Ndiag,Bdiag,((1,0),0),Bdiag,((1,0),0),Ndiag,((1,0),0),Ndiag,Bdiag,((1,0),0),Bdiag,((1,-1),-2),((1,0),2),((1,-1),-2)],
 'D_turn':[((0,1),1),((1,0),3),((1,0),-1),((1,0),2),((1,1),0)],
 'R_turn':[((0,1),1),((1,0),3),((1,0),-1),((1,-1),4)]}

def prescribed(d,word,terminal):
 p=(F(0),F(0));v=(F(-1),d);P=[p]
 for normal,k in word:
  t=(k-dot(normal,p))/dot(normal,v);assert t>0
  p=tuple(p[i]+t*v[i] for i in (0,1));P.append(p)
  scale=2*dot(normal,v)/dot(normal,normal)
  v=tuple(v[i]-scale*normal[i] for i in (0,1))
 axis,k=terminal;t=(k-p[axis])/v[axis];assert t>0
 p=tuple(p[i]+t*v[i] for i in (0,1));P.append(p)
 return P,v
results={}
for kind,prefix in prefixes.items():
 for attempt,cap,control,terminal in [('N_B_roundtrip','Dminus',F(3,20),(1,F(2))),('N_B_roundtrip','Rminus',F(3,20),(1,F(2))),('D_turn','Dminus',F(7,36),(1,F(2))),('R_turn','Rminus',F(6,35),(0,F(3)))]:
  name=kind+'_'+cap+'_'+attempt
  record=source[kind+'_Nbplus_'+cap]
  V=[tuple(map(F,p)) for p in record['vertices']]
  room={tuple(sorted(map(tuple,t))) for t in record['triangles']}
  P,v=prescribed(control,prefix+words[attempt],terminal)
  q=P[-1]
  if attempt=='N_B_roundtrip':assert q==(26*control-2,2)
  elif attempt=='D_turn':assert q==(20*control-2,2) and v==(control,1)
  else:assert q==(3,3/control-18) and v==(-control,1)
  u,z=path_requirements(P);assert u<=room and not z&room
  replay(V,(0,0),q,P);replay(V,q,(0,0),P[::-1])
  os=g.owners_of(list(room));opens={e for e,ls in os.items() if len(ls)==2}
  vertices={}
  for point in [(0,1),(-1,1),(1,-1)]:
   angles,full=g.check_fan_angles(list(room),point,os,opens)
   vertices[str(point)]={'angles_degrees':[45*x for x in angles],'full':full}
  assert vertices['(-1, 1)']['angles_degrees']==[180]
  assert vertices['(0, 1)']['angles_degrees']==[270]
  assert vertices['(1, -1)']['angles_degrees']==([270] if cap=='Dminus' else [225])
  results[name]={'status':'PREFIX_PASS_NOT_ILLUMINATION','control_parameter':str(control),'reflections':len(P)-2,'path':[[str(x) for x in p] for p in P],'terminal':[str(x) for x in q],'terminal_velocity':[str(x) for x in v],'required':sorted(u),'forbidden':sorted(z),'corner_checks':vertices,'boundary_forward_reverse':'PASS'}
(HERE/'four-left-check.json').write_text(json.dumps({'status':'EXACT_PREFIX_CHECKS_PASS_NO_ROOM_CLOSED','scope':'Three analytically prescribed continuations, eight named room/control applications. No initial directions or reflection words scanned. Endpoint equations and interval limitations are in four-left.txt.','controls':results},indent=2)+'\n')
print(json.dumps({'status':'PREFIX_CHECKS_PASS_NO_ROOM_CLOSED','prescribed_control_applications':len(results),'reflections':{n:r['reflections'] for n,r in results.items()}}))
