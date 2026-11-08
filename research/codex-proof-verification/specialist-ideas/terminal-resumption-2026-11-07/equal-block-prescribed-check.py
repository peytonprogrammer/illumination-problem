"""Three predeclared equal-block cases of the new hand supplement."""
from fractions import Fraction as F
from math import gcd,floor,ceil
from pathlib import Path
import ast,json,importlib.util
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('frozen_core',HERE/'prescribed-check.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
L=3

def select_general(a,N,b,c,h,H,S,T):
 s,u=map(F,S);t,v=map(F,T);a=F(a);A=N*a;z=A-t
 d0,G,g1,d2=h-u,2*(H-h),h-c,c-v;D=int(d0+G+g1+d2)
 assert N>=L+2 and gcd(int(G),N)==1 and gcd(N*int(d2),L)==1
 assert 0<s<a and b<u<=h and (N-L)*a<t<A and 0<v<c
 assert d0==G==g1==d2 # The exact exceptional case under examination.
 forbidden=[[],[],[]];good=[]
 for q in range(D):
  tau=(A+z-s+2*a*q)/D
  phases=[s+d0*tau,s+(d0+G)*tau-A,s+(D-d2)*tau-A]
  bad=[(p-a)%(2*a)==0 for p in phases]
  for i,x in enumerate(bad):
   if x:forbidden[i].append(q)
  if not any(bad):good.append(q)
 assert good
 if forbidden[1]:assert not forbidden[0]
 q=good[0];tau0=(A+z-s+2*a*q)/D;n0=floor((s+d0*tau0+a)/(2*a));z0=s+d0*tau0-2*n0*a
 cap=[]
 for M in range(N):
  tau=tau0+2*a*M;X=z0+G*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
  if abs(z1)<a:cap.append((M,tau,m,z1))
 assert len(cap)==1
 M,tau,m,z1=cap[0];n=floor((s+d0*tau+a)/(2*a));k=floor((z1+g1*tau+a)/(2*a));z2=z1+g1*tau-2*k*a
 J=(z2+d2*tau-z)/(2*a);assert J.denominator==1
 shift=next(e for e in range(L) if (J+N*d2*e)%L==0)
 tau+=2*a*N*shift;n+=int(N*d0*shift);m+=int(G*shift);k+=int(N*g1*shift)
 z0=s+d0*tau-2*n*a;z1=z0+G*tau-(2*m+1)*A;z2=z1+g1*tau-2*k*a
 assert abs(z0)<a and abs(z1)<a and abs(z2)<a
 j=(z2+d2*tau-z)/(2*L*a);assert j.denominator==1
 return {'tau':tau,'residuals':[z0,z1,z2],'q':q,'cap_M':M,'target_orbit_shift':shift,'indices':[n,m,k,int(j)],'forbidden_classes':forbidden,'good_q':good}

# Retain the frozen core's actual path sampler and all wall predicates, changing
# ONLY l=(N-L)a and the last band's width La. This is our own formula replay,
# not an independent mathematical review or a peer-source edit.
tree=ast.parse((HERE/'prescribed-check.py').read_text());func=next(f for f in tree.body if isinstance(f,ast.FunctionDef) and f.name=='replay')
class BottomWidth(ast.NodeTransformer):
 def visit_BinOp(self,node):
  node=self.generic_visit(node)
  if ast.unparse(node)=='(N - 2) * a':return ast.parse('(N-L)*a',mode='eval').body
  return node
 def visit_Tuple(self,node):
  node=self.generic_visit(node)
  if len(node.elts)==5 and ast.unparse(node.elts[2])=='2 * a' and isinstance(node.elts[4],ast.Constant) and node.elts[4].value is True:
   node.elts[2]=ast.parse('L*a',mode='eval').body
  return node
func=BottomWidth().visit(func)
scope={'F':F,'floor':floor,'ceil':ceil,'L':L,'fold':core.fold,'ns':core.ns,'select':select_general}
exec(compile(ast.fix_missing_locations(ast.Module(body=[func],type_ignores=[])),'<own-formula-last-band-adaptation>','exec'),scope)
rows=[scope['replay'](label,4,5,1,4,6,7,(2,4),(t,2)) for label,t in [('cap-bad-nonempty',10),('other-target-phase',12),('target-on-w',16)]]
out={'status':'PASS_EQUAL_BLOCK_EXCLUDED_CASE_WITH_ACTUAL_TARGETS','cases':len(rows),'rows':rows,'reflections':sum(r['reflections'] for r in rows),'wall_leg_guards':sum(r['wall_leg_guards'] for r in rows),'discovery_search_used':False,'independent_review':'pending','whole_r3_complete':False}
(HERE/'equal-block-prescribed-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
