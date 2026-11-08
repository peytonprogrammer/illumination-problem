#!/usr/bin/env python3
"""Own exact prescribed OR01 controls, including a sole-root corner case."""
from fractions import Fraction as F
from pathlib import Path
import json

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def plus(a,t,v):return tuple(x+t*y for x,y in zip(a,v))
def fp(p):return tuple(F(x) for x in p)
def hit(p,v,poly):
 out=[]
 for i,(a,b) in enumerate(zip(poly,poly[1:]+poly[:1])):
  a,b=fp(a),fp(b); e=sub(b,a); den=cross(v,e)
  if not den:continue
  t=cross(sub(a,p),e)/den; u=cross(sub(a,p),v)/den
  if t>0 and 0<=u<=1:out.append((t,i,u,plus(p,t,v)))
 t=min(h[0] for h in out)
 return [h for h in out if h[0]==t]
def check_path(poly,points):
 points=[fp(p) for p in points]; ans=[]
 for j,(p,q) in enumerate(zip(points,points[1:])):
  v=sub(q,p); hh=hit(p,v,poly)
  if j==len(points)-2:
   assert hh[0][0]>1
  else:
   assert len(hh)==1 and hh[0][0]==1 and 0<hh[0][2]<1
   a,b=poly[hh[0][1]],poly[(hh[0][1]+1)%len(poly)]
   vv=(-v[0],v[1]) if a[0]==b[0] else (v[0],-v[1])
   out=sub(points[j+2],q)
   assert cross(vv,out)==0 and sum(x*y for x,y in zip(vv,out))>0
   ans.append({'point':[str(x) for x in q],'wall':hh[0][1]})
 return ans

def fold(u,w):
 k=u//w; r=u-k*w
 assert 0<r<w
 return (r,1) if k%2==0 else (w-r,-1)

def roots(w,h,a,b,alpha,beta,eps,J):
 K=a+b+2*h; lo,hi=J
 assert K*(hi-lo)>2*w
 L=(K*lo-eps*beta+alpha)/(2*w)
 U=(K*hi-eps*beta+alpha)/(2*w)
 # Exact finite list forced by this prescribed branch interval, no direction search.
 ns=range(L.numerator//L.denominator+1,-((-U.numerator)//U.denominator))
 rr=[((2*n*w+eps*beta-alpha)/K,n) for n in ns]
 assert rr and all(lo<m<hi for m,n in rr)
 return rr

# Smooth root in an actual rectangle, epsilon=+1 and -1.
rect=[(0,-8),(8,-8),(8,16),(0,16)]
smooth=[]
for eps in [1,-1]:
 rr=roots(F(8),F(16),F(4),F(4),F(2),F(6),eps,(F(-2,5),F(2,5)))
 for m,n in rr:
  xs=2+4*m; xt=6-eps*4*m
  endpoint,parity=fold(xs+32*m,F(8))
  assert endpoint==xt and parity==eps
  smooth.append({'epsilon':eps,'n':n,'m':str(m),'source_mouth':str(xs),'target_mouth':str(xt),'fold_parity':parity})
contacts=check_path(rect,[(2,-4),(4,16),(6,-4)])
# Physical low-reflex sole-root convex-corner control.
poly=[(-8,-24),(24,-24),(24,0),(16,0),(16,8),(0,8),(0,0),(-8,0)]
w,h,a,b,alpha,beta=map(F,[16,8,8,16,4,-2]); eps=-1; J=(F(1,5),F(11,10))
rr=roots(w,h,a,b,alpha,beta,eps,J)
assert rr==[(F(3,4),1)]
m,n=rr[0]
xs=alpha+a*m; xt=beta-eps*b*m
assert xs==xt==10
assert xs+h*m==16
# Whole J access guards are affine; their endpoint extrema suffice.
for intercept,slope in [(alpha,a),(beta,-eps*b)]:
 vals=[intercept+slope*t for t in J]
 assert 0<min(vals)<max(vals)<w
# Start positions and all endpoint-mouth line segments lie in lower rectangle.
S=fp((4,-8));T=fp((-2,-16))
assert -8<S[0]<24 and -24<S[1]<0 and -8<T[0]<24 and -24<T[1]<0
hh=hit(S,fp((m,1)),poly)
assert len(hh)==2 and all(v[3]==(16,8) for v in hh)
assert cross(sub(S,T),fp((m,1)))==0
check_path(poly,[S,T])
turns=[]
for j,p in enumerate(poly):
 z=cross(sub(p,poly[j-1]),sub(poly[(j+1)%len(poly)],p));turns.append(z)
assert sum(z<0 for z in turns)==2
out={'status':'PASS_PRESCRIBED_OR01_CONTROLS','method':'Own Fraction permutation-free optical intersections; whole interval guards checked as affine bounds','smooth_chart_roots':smooth,'actual_smooth_roof_path_contacts':contacts,'sole_root_corner':{'D':poly,'r':2,'S':[4,-8],'T':[-2,-16],'w':16,'h':8,'a':8,'b':16,'alpha':4,'beta':-2,'epsilon':-1,'J':['1/5','11/10'],'K_width':'36','two_w':'32','all_roots':[['3/4',1]],'source_and_target_mouth':['10','0'],'corner':['16','8'],'actual_direct_subpath_verified':True},'global_G8_proved':False,'whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
