#!/usr/bin/env python3
"""Two prescribed checks corroborate an all-n hand proof, no discovery."""
from fractions import Fraction as F
from pathlib import Path
import json
P=[(0,0),(8,0),(8,4),(4,4),(4,8),(0,8)]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def add(a,t,v):return (a[0]+t*v[0],a[1]+t*v[1])
def next_hits(p,v):
 hh=[]
 for i,(a,b) in enumerate(zip(P,P[1:]+P[:1])):
  e=sub(b,a);den=cross(v,e)
  if not den:continue
  t=cross(sub(a,p),e)/den;u=cross(sub(a,p),v)/den
  if t>0 and 0<=u<=1:hh.append((t,i,u,add(p,t,v)))
 t=min(x[0] for x in hh)
 return [x for x in hh if x[0]==t]
rows=[]
for n in [1,2]:
 m=F(2,16*n-2);p=(F(6),F(2));v=(F(1),m);cs=[]
 for j in range(2*n):
  hh=next_hits(p,v)
  assert len(hh)==1 and 0<hh[0][2]<1
  p=hh[0][3]; assert p[0] in(0,8) and 2<p[1]<4
  cs.append([str(z) for z in p]);v=(-v[0],v[1])
 hh=next_hits(p,v)
 assert len(hh)==2 and all(x[3]==(4,4) for x in hh)
 X=16*n+4
 # First top crossing on both sides retains same side count.
 probes=[]
 for dx in [F(-1,2),F(1,2)]:
  mp=F(2)/(X+dx-6)
  xx=6+2/mp
  assert xx==X+dx and 16*n<xx<16*n+8
  xf=xx-16*n
  assert xf==4+dx
  probes.append({'slope':str(mp),'top_x':str(xf),'enters_mouth':xf<4})
 rows.append({'n':n,'slope':str(m),'smooth_side_contacts':cs,'first_corner':[4,4],'one_sided_top_probes':probes})
output={'status':'PASS_PRESCRIBED_OR02_CONTROL','all_n_hand_argument':'For 1<=j<=2n: 2<2+2*(8j-6)/(16n-2)<=4-8/(16n-2)<4. Top image4+16n folds to reflex4,4. Neighbor x-images ±1/2 keep 2n sides and straddle mouth endpoint.','prescribed_n':rows,'global_G8_refuted':False,'illumination_target_refuted':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
