"""Affine line reflection derivation of the fixed twenty-wall candidate."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,time
HERE=Path(__file__).resolve().parent;d=json.loads((HERE/'verification.json').read_text());deadline=json.loads((HERE/'effort.json').read_text())['deadline_unix'];assert time.time()<deadline
# Affine scalar in parameter d: constant plus slope*d.
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def scale(x,k):return tuple(a*k for a in x)
def ev(x,t):return x[0]+x[1]*t
A=(F(1),F(0));B=(F(0),F(-1));C=(F(0),F(0)) # x-d*y=0
root=F(4,5);lo=F(799,1000);hi=F(801,1000);rows=[]
for i,(w0,w1)in enumerate(d['walls'],1):
 a,b=map(F,w0);c,e=map(F,w1);nx=e-b;ny=a-c;norm=nx*nx+ny*ny;wallc=nx*a+ny*b
 den=add(scale(A,ny),scale(B,-nx));xn=add(scale(C,ny),scale(B,-wallc));yn=add(scale(A,wallc),scale(C,-nx))
 x=ev(xn,root)/ev(den,root);y=ev(yn,root)/ev(den,root)
 assert[x,y]==[F(q)for q in d['path'][i]]
 # Exact finite segment parameter at interval endpoints. Linear fractional
 # with no pole, derivative fixed sign: endpoint bounds imply all interior.
 assert ev(den,lo)*ev(den,hi)>0
 for t in (lo,hi):
  xx=ev(xn,t)/ev(den,t);yy=ev(yn,t)/ev(den,t)
  u=((xx-a)*(c-a)+(yy-b)*(e-b))/norm
  assert 0<u<1,(i,t,u)
 rows.append({'contact':i,'x_numerator':list(map(str,xn)),'y_numerator':list(map(str,yn)),'denominator':list(map(str,den)),'actual':[str(x),str(y)],'finite_open_gate':True})
 # Reflect the line covector through wall n dot p=wallc.
 dot=add(scale(A,nx),scale(B,ny))
 Anew=add(A,scale(dot,-2*nx/norm));Bnew=add(B,scale(dot,-2*ny/norm));Cnew=add(C,scale(dot,-2*wallc/norm))
 A,B,C=Anew,Bnew,Cnew
endpoint=add(C,scale(B,-2));eq=add(endpoint,scale(A,-2));assert ev(eq,root)==0 and eq!=(0,0)
assert -eq[0]/eq[1]==root
out={'status':'AFFINE_HAND_TWENTY_CONTACT_DERIVATION_PASS','parameter':'launch(-d,-1)','root':'4/5','strict_sufficient_finite_wall_gate':['799/1000','801/1000'],'contact_mobius_rows':rows,'final_line':{'A':list(map(str,A)),'B':list(map(str,B)),'C':list(map(str,C))},'target_equation_affine_coefficients':list(map(str,eq)),'limits':'Gate certifies finite contact intervals; complete openleg support/firstT are verified at exactroot independently. Not an interval-wide room claim.','source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [HERE/'verification.json',Path(__file__)]}}
(HERE/'hand.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS20 affinecontacts, strictgate799/1000..801/1000, final2A+2B=C equation',eq,'root',root)
