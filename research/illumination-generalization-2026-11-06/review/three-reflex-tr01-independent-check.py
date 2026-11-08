#!/usr/bin/env python3
"""Independent prescribed U/L formula replay in ORIGINAL TR01 rooms; no search."""
from fractions import Fraction as F
from pathlib import Path
import ast,json,hashlib
HERE=Path(__file__).parent;BASE=HERE.parent
request=json.loads((BASE/'construction/three-reflex-review-request-01.json').read_text())
pins=[]
for item in request['source_pins']:
 actual=hashlib.sha256(Path(item['path']).read_bytes()).hexdigest();assert actual==item['sha256'];pins.append({**item,'actual':actual,'pass':True})
# Reuse only reviewer-owned pure guard functions, with no top-level execution/writes.
old=ast.parse((HERE/'resumed-exact-check.py').read_text())
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
ns={'Q':F}
exec(compile(ast.Module(body=[n for n in old.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'<reviewer-pure-guards>','exec'),ns)
fold=ns['fold'];path_check=ns['path_check'];simple=ns['simple'];location=ns['location']
def point(p):return tuple(map(F,p))
def L_vertical(A,a,c,C,S,T):
 S=point(S);T=point(T)
 if (S[1]<=c and T[1]<=c) or (S[0]<=a and T[0]<=a):return [S,T]
 if not(S[0]>a and S[1]<c):return list(reversed(L_vertical(A,a,c,C,T,S)))
 sx,sy=S;tx,ty=T;r=(ty-c)/(c-sy);h=-r*sx
 candidates=[]
 for sign in [-1,1]:
  k=(h-sign*tx)//(2*a)
  for j in [k-1,k,k+1]:
   image=sign*tx+2*a*j
   if image!=h:candidates.append(image)
 image=min(candidates,key=lambda x:(abs(x-h),x));assert 0<abs(image-h)<=a
 Xs,Xt=(sx,image) if image>h else (-sx,-image)
 slope=(Xt-Xs)/(ty-sy);assert slope!=0
 portal=(r*Xs+Xt)/(1+r);assert 0<portal<a
 levels={sy,c,ty}
 yz=sy-Xs/slope
 if sy<yz<c:levels.add(yz)
 lo,hi=sorted([portal,Xt])
 for j in range(int(lo//a)-1,int(hi//a)+2):
  y=sy+(j*a-Xs)/slope
  if c<y<ty:levels.add(y)
 path=[]
 for y in sorted(levels):
  X=Xs+slope*(y-sy)
  path.append((abs(X) if y<=c else fold(X,a),y))
 assert path[0]==S and path[-1]==T
 return path

def L_horizontal(A,a,c,C,S,T):
 # Transpose the standard L, then map back.
 p=L_vertical(C,c,a,A,(S[1],S[0]),(T[1],T[0]))
 return [(y,x) for x,y in p]

def U_opposite(a,w,A,d,HL,HR,S,T):
 if S[0]>w:return list(reversed(U_opposite(a,w,A,d,HL,HR,T,S)))
 sx,sy=S;tx_global,ty=T;b=A-w;tx=tx_global-w;M=w-a
 tau0=2*max(a,b)/d+1;k=max(0,int((2*d*tau0-M)//(2*A))+1);B=M+2*k*A
 assert B>2*d*tau0
 tau=tau0;iterations=0
 while True:
  n=max(0,int(((sy-d)*tau-(a-sx))//(2*a))+1)
  m=max(0,int(((ty-d)*tau-tx)//(2*b))+1)
  L=a-sx+2*n*a;R=tx+2*m*b
  new=(L+R+B)/(sy+ty);iterations+=1
  if new==tau:break
  assert new>tau;tau=new
  assert iterations<10000,'Prescribed verification runtime guard, not universal bound'
 es=L-(sy-d)*tau;et=R-(ty-d)*tau;assert 0<es<2*a and 0<et<2*b
 u=sy-L/tau;v=ty-R/tau;assert 0<u<d and 0<v<d and u+v==B/tau
 distances={F(0),L}
 for j in range(0,int((sx+L)//a)+2):
  dx=j*a-sx
  if 0<dx<L:distances.add(dx)
 left=[(fold(sx+dx,a),sy-dx/tau) for dx in sorted(distances)]
 distances={F(0),B,u*tau}
 for j in range(0,int((a+B)//A)+2):
  dx=j*A-a
  if 0<dx<B:distances.add(dx)
 middle=[(fold(a+dx,A),abs(u-dx/tau)) for dx in sorted(distances)]
 distances={F(0),R}
 for j in range(int((tx-R)//b)-1,int(tx//b)+2):
  dx=tx-j*b
  if 0<dx<R:distances.add(dx)
 backward=[(w+fold(tx-dx,b),ty-dx/tau) for dx in sorted(distances)]
 assert left[-1]==middle[0] and middle[-1]==backward[-1]
 path=left+middle[1:]+list(reversed(backward))[1:]
 assert path[0]==S and path[-1]==T
 return path

def U_path(a,w,A,d,HL,HR,S,T):
 if (S[0]<a and T[0]<a) or (S[0]>w and T[0]>w) or (S[1]<d and T[1]<d):return [S,T]
 if S[1]>=d and T[1]>=d:return U_opposite(a,w,A,d,HL,HR,S,T)
 high=S if S[1]>=d else T
 if high[0]<a:return L_vertical(A,a,d,HL,S,T)
 assert high[0]>w
 path=L_vertical(A,A-w,d,HR,(A-S[0],S[1]),(A-T[0],T[1]))
 return [(A-x,y) for x,y in path]

def run(params,S,T,region):
 a,l,w,A,b,c,h,H=map(F,params);S=point(S);T=point(T)
 assert 0<a<l<w<A and 0<b<c<h<H
 P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)];simple(P)
 assert location(P,S)==location(P,T)==1
 def inG(p):return p[0]<a or p[1]>=h or(p[0]>w and p[1]>=c)
 def inR(p):return (l<p[0]<A and 0<p[1]<c)or(w<p[0]<A and 0<p[1]<H)
 if region=='G':
  assert inG(S) and inG(T)
  path=U_path(a,w,A,H-h,H-b,H,(S[0],H-S[1]),(T[0],H-T[1]));path=[(x,H-y) for x,y in path]
 else:
  assert inR(S) and inR(T)
  path=L_horizontal(A-l,A-w,c,H,(A-S[0],S[1]),(A-T[0],T[1]));path=[(A-x,y) for x,y in path]
 assert path[0]==S and path[-1]==T
 result=path_check(P,path)
 assert (w,c) not in path and (w,h) not in path
 return {'parameters':params,'source':S,'target':T,'region':region,'points':len(path),**result}
fixtures=[
 ((4,12,20,28,4,8,20,28),(2,6),(24,8),'G'),
 ((4,12,20,28,4,8,20,28),(2,20),(24,20),'G'),
 ((4,12,20,28,4,8,20,28),(2,6),(14,24),'G'),
 ((4,12,20,28,4,8,20,28),(24,8),(14,24),'G'),
 ((4,12,20,28,4,8,20,28),(2,6),(20,24),'G'),
 ((4,12,20,28,4,8,20,28),(24,8),(22,24),'G'),
 ((4,12,20,28,4,8,20,28),(14,2),(24,24),'R'),
 ((4,12,20,28,4,8,20,28),(20,2),(24,8),'R'),
 ((4,12,20,28,4,8,20,28),(F(81,4),24),(14,2),'R'),
 ((F(1,3),2,5,7,F(1,2),F(3,4),5,F(17,3)),(F(1,6),2),(6,F(3,4)),'G'),
 ((1,3,4,10,1,2,90,100),(F(1,2),2),(5,2),'G')]
rows=[run(*f) for f in fixtures]
# Actual interior source on the artificial R cut is not a legal interior R mark.
Pcut=[(F(x),F(y)) for x,y in [(4,4),(4,20),(20,20),(20,8),(12,8),(12,0),(28,0),(28,28),(0,28),(0,4)]]
Rcut=[(F(x),F(y)) for x,y in [(12,0),(28,0),(28,28),(20,28),(20,8),(12,8)]]
Scut=(F(20),F(24));Tbottom=(F(14),F(2))
assert location(Pcut,Scut)==location(Pcut,Tbottom)==1
assert location(Rcut,Scut)==0 and location(Rcut,Tbottom)==1
assert not(Tbottom[0]<4 or Tbottom[1]>=20 or(Tbottom[0]>20 and Tbottom[1]>=8))
out={'status':'PASS_PRESCRIBED_TR01_FORMULAS_IN_ORIGINAL_ROOM','source_pin_checks':pins,'controls':rows,'total_reflections':sum(x['reflections'] for x in rows),'total_wall_leg_guards':sum(x['wall_leg_guards'] for x in rows),'method':'Own U finite-step matching and L target-image formulas plus existing reviewer-only pure all-wall guards; no author code or direction/word search.','general_real_quantifiers':'Hand proof, not finite replay.','whole_r3_theorem':False,'whole_goal_complete':False,'search_used':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({'status':out['status'],'controls':len(rows),'reflections':out['total_reflections'],'wall_leg_guards':out['total_wall_leg_guards'],'search_used':False}))
