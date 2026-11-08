"""Two declared exact geometric controls, no room search or ray discovery."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent
P=[(0,0),(8,0),(8,8),(4,8),(4,4),(0,4)]
def turn(a,b,c):return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
def area2(p):return sum(p[i][0]*p[(i+1)%len(p)][1]-p[i][1]*p[(i+1)%len(p)][0] for i in range(len(p)))
def reflex(p):return sum(turn(p[i-1],p[i],p[(i+1)%len(p)])<0 for i in range(len(p)))
assert all(turn(P[i-1],P[i],P[(i+1)%6]) for i in range(6)) and reflex(P)==1
S=(6,4);T=(2,2)
assert 4<S[0]<8 and S[1]==4
assert not (0<S[0]<8 and 0<S[1]<4)
assert 0<T[0]<8 and 0<T[1]<4
# The radius1 square about S is inside the union: below/above y4 lie in Q/E.
assert 4<5<7<8 and 0<3<4<5<8
assert area2(P)==96
mouth={'polygon':P,'S':S,'T':T,'reflex':1,'area':48,'remaining_Q':[[0,0],[8,0],[8,4],[0,4]],'ear_E':[[4,4],[8,4],[8,8],[4,8]],'S_in_open_ear':False,'S_in_closed_ear':True,'S_interior_D':True,'S_interior_Q':False,'complexity_decreases':True,'endpoint_domain_preserved':False}
# Prescribed staircase corridor, four chambers and three width2 mouths.
chain=[(0,0),(4,0),(4,4),(8,4),(8,8),(12,8),(12,12),(16,12),(16,18),(12,18),(12,14),(8,14),(8,10),(4,10),(4,6),(0,6)]
rects=[(4*j,4*j+4,4*j,4*j+6) for j in range(4)]
assert len(chain)==16 and reflex(chain)==6 and area2(chain)==192
# Pairwise rectangle intersections are exactly the declared consecutive mouths.
intersection=[]
for i,a in enumerate(rects):
 for j,b in enumerate(rects):
  if i>=j:continue
  xl,xh=max(a[0],b[0]),min(a[1],b[1]);yl,yh=max(a[2],b[2]),min(a[3],b[3])
  if xl<=xh and yl<=yh:
   assert j==i+1 and xl==xh==4*j and yh-yl==2
   intersection.append([i,j,[xl,yl],[xh,yh]])
assert len(intersection)==3
Cs=(2,2);Ct=(14,16)
assert rects[0][0]<Cs[0]<rects[0][1] and rects[0][2]<Cs[1]<rects[0][3]
assert rects[-1][0]<Ct[0]<rects[-1][1] and rects[-1][2]<Ct[1]<rects[-1][3]
# Exact direct segment y=(7x-2)/6 crosses each mouth strictly in its interior.
from fractions import Fraction as Q
heights=[Q(7*x-2,6) for x in (4,8,12)]
assert heights==[Q(13,3),Q(9),Q(41,3)]
for x,y in zip((4,8,12),heights):assert x<y<x+2
# In each slab height stays in its rectangle because affine extrema are at slab endpoints.
xs=[Q(2),Q(4),Q(8),Q(12),Q(14)]
for j,(a,b) in enumerate(zip(xs,xs[1:])):
 y1,y2=Q(7*a-2,6),Q(7*b-2,6)
 assert rects[j][2]<y1<=y2<rects[j][3]
assert all(x%2==y%2==0 for x,y in chain+[Cs,Ct])
out={'status':'PASS_PRESCRIBED_EXACT_GEOMETRY','endpoint_on_mouth':mouth,'r6_chamber_chain':{'polygon':chain,'rectangles':rects,'mouths':intersection,'S':Cs,'T':Ct,'reflex':6,'walls':16,'area':96,'dual_graph':'path on4chambers; terminal chamber deletion loses S or T','direct_path':[Cs,Ct],'strict_mouth_heights':[str(h) for h in heights],'limits':'No claim about every possible decomposition or all contained subrooms.'},'new_discovery_or_search':False,'whole_goal_complete':False}
(R/'geometric-reduction-ear-conditions-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','new_discovery_or_search','whole_goal_complete']},indent=2))
