#!/usr/bin/env python3
"""Verify one predeclared hand-derived actual optical word. No search engine."""
from pathlib import Path
from fractions import Fraction as F
import json
P=[(4,4),(4,20),(20,20),(20,8),(12,8),(12,0),(28,0),(28,28),(0,28),(0,4)]
S=(2,6);T=(14,2)
expected=[(4,10),(0,18),(5,28),(9,20),(13,28),(17,20),(21,28),(28,14),(21,0),(17,8)]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def target_time(p,v):
 t=F(T[0]-p[0],v[0])
 return t if t>=0 and p[1]+t*v[1]==T[1] else None
p=tuple(map(F,S));v=(1,2);clock=F(0);rows=[];segments=[]
for wanted in expected:
 hits=[]
 for i,(a,b) in enumerate(zip(P,P[1:]+P[:1])):
  e=sub(b,a);q=sub(a,p);den=cross(v,e);assert den!=0
  t=F(cross(q,e),den);u=F(cross(q,v),den)
  if t>0 and 0<=u<=1:hits.append((t,i,u))
 t,i,u=min(hits);assert sum(h[0]==t for h in hits)==1
 assert 0<u<1, 'True corner contact'
 early=target_time(p,v);assert early is None or early>t
 segments.append((clock,p,v,t))
 contact=(p[0]+t*v[0],p[1]+t*v[1]);assert contact==wanted
 a=P[i];b=P[(i+1)%len(P)];e=sub(b,a);assert cross(e,v)<0
 incoming=v
 v=(-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1])
 assert cross(e,v)>0 and v[0]*v[0]+v[1]*v[1]==5
 clock+=t;rows.append({'contact':list(map(int,contact)),'time':int(clock),'actual_wall_index':i,'actual_wall':[a,b],'strict_wall_interior':True,'incoming_velocity':incoming,'outgoing_velocity':v})
 p=contact
final=target_time(p,v);assert final==3
hits=[]
for a,b in zip(P,P[1:]+P[:1]):
 e=sub(b,a);q=sub(a,p);den=cross(v,e);t=F(cross(q,e),den);u=F(cross(q,v),den)
 if t>0 and 0<=u<=1:hits.append(t)
assert min(hits)>final
segments.append((clock,p,v,final))
clock+=final;assert clock==48
# Portals crossed on specified open segments, with same velocity through each cut.
portals=[{'point':[1,20],'time':7,'guard':'0<x<4'}, {'point':[20,26],'time':26,'guard':'20<y<28'}, {'point':[25,8],'time':37,'guard':'20<x<28'}]
for portal in portals:
 matches=[(start,p0,direction,dt) for start,p0,direction,dt in segments if start<portal['time']<start+dt]
 assert len(matches)==1
 start,p0,direction,dt=matches[0];delta=portal['time']-start
 assert (p0[0]+delta*direction[0],p0[1]+delta*direction[1])==tuple(portal['point'])
out={'status':'PASS_EXACT_PRESCRIBED_OPTICAL_WITNESS','polygon':P,'actual_source':S,'actual_target':T,'initial_velocity':[1,2],'contacts':rows,'portal_crossings':portals,'first_actual_target_time':int(clock),'final_velocity':v,'true_corner_contacts':0,'artificial_reflections':0,'all_wall_contacts_strict':True,'method':'Hand-derived fixed word, independently check every finite wall intersection and specular velocity at each prescribed contact; no direction/word search.','coverage':'This one actual A-point pair in a uniformly scaled existing r3 spiral only.','whole_r3_theorem':False,'whole_goal_complete':False,'search_used':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'reflections':len(rows),'actual_target_time':int(clock),'forbidden_contacts':0,'search_used':False}))
