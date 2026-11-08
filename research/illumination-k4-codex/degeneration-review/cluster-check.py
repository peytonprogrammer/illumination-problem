"""Exact all-k modular diagnostic for one corridor-to-exterior word.
No tracing, direction search, room generation or global darkness assertion.
"""
from fractions import Fraction as F
from pathlib import Path
import json
B=Path(__file__).resolve().parent
ell=F(1);d=F(1,2);X=F(1);Y=F(10);eta=F(1,10)
rows=[]
for n in [0,1,2,10,100]:
 e=F(1,40*n+24);depths=[]
 for D in [d,2*ell-d]:
  # w/e = Y/(D+Y) * (sigma*eta + 2k + D X/(Y e)).
  # A strict interior mouth crossing requires bracket in (0,1+D/Y).
  phase=D*X/(Y*e);bound=1+D/Y;phases=[]
  for sigma in [-1,1]:
   x=phase+sigma*eta;integer=x//2;residue=x-2*integer
   assert 0<residue<2 and residue>bound
   # Every other k shifts by 2, so misses this interval as well.
   assert residue-2<0
   phases.append({'sign':sigma,'residue_mod_2':str(residue),'required_upper_bound':str(bound),'all_integer_k_excluded':True})
  depths.append({'depth':str(D),'phases':phases})
 rows.append({'n':n,'epsilon':str(e),'valid_depths':depths})
# The rejected extra image is indeed capable of inventing a crossing.
# At n=0, D=2ell+d is unavailable before first mouth exit.
e=F(1,24);D=2*ell+d;phase=D*X/(Y*e);x=phase+eta;residue=x-2*(x//2)
assert 0<residue<1+D/Y
def ceil(x):return -((-x.numerator)//x.denominator)
def end_images(ell,d,Y,X,xi):
 D=2*ell-d;rho=Y/(D+Y);lam=(ell+Y)/(D+Y);beta=(ell-d)/(D+Y)
 items=[]
 for sigma in [-1,1]:
  lo=(-D*X/Y-sigma*xi)/2
  hi=((D+Y-D*X)/Y-sigma*xi)/2
  for k in range(lo.numerator//lo.denominator+1,ceil(hi)):
   x=sigma*xi+2*k;w=rho*x+(1-rho)*X;end=lam*x+beta*X
   assert 0<w<1
   items.append((x,w,end))
 return sorted(items)

def repair(ell,d,Y,X,xi):
 D=2*ell-d;assert 0<d<ell and 0<Y<D and 0<xi<1
 rho=Y/(D+Y);lam=(ell+Y)/(D+Y);rho0=Y/(d+Y)
 assert F(1,2)<lam<1 and rho<F(1,2)
 assert rho0*(1-F(1,2)/lam)==Y/(2*(ell+Y))
 items=end_images(ell,d,Y,X,xi);assert len(items)>=2
 good=[x for x in items if x[2].denominator!=1]
 if good:return 'end_reflection'
 assert len(items)==2
 (xL,wL,m),(xR,wR,mR)=items
 assert mR==m+1 and xR-xL==1/lam
 j=(xL+xR)/2;assert j.denominator==1
 h=m+F(1,2)-j;p=h-F(1,2);assert p.denominator==1
 c=(wL+wR)/2;r=Y/(2*(ell+Y));assert r<c<1-r
 x0=xR+2*p
 assert any(((x0-sign*xi)/2).denominator==1 for sign in [-1,1])
 w0=rho0*x0+(1-rho0)*X
 assert w0==c-r and 0<w0<1
 return 'no_end_fallback'

repairs={'end_reflection':0,'no_end_fallback':0}
for ell in [F(1),F(2)]:
 for d in [ell/4,ell/2,3*ell/4]:
  D=2*ell-d
  for Y in [D/4,D/2,3*D/4,9*D/10]:
   for xi in [F(1,10),F(1,2),F(5,8),F(9,10)]:
    for a in range(-12,13):
     mode=repair(ell,d,Y,F(a,4),xi);repairs[mode]+=1
assert repair(F(1),F(1,2),F(1),F(-1,2),F(5,8))=='no_end_fallback'
repairs['no_end_fallback']+=1
out={'status':'PASS','model':{'corridor':'0<x<epsilon, -1<y<0; open mouth y=0','source':'(epsilon/10, -1/2)','exterior_target':'(1,10)','epsilon_sequence':'1/(40n+24), n>=0','physical_depths':['1/2','3/2']},'symbolic_residues':{'depth_1/2':['11/10','13/10'],'depth_3/2':['3/2','17/10'],'required_bounds':['21/20','23/20'],'reason_for_all_n':'Increasing n adds 2n or 6n to the phase, so these residues are independent of n.'},'exact_controls':rows,'strict_height_repair_controls':repairs,'explicit_fallback_example':{'ell':'1','d':'1/2','Y':'1','X_over_epsilon':'-1/2','source_x_over_epsilon':'5/8','end_candidates':[{'image_x':'11/8','mouth':'1/4','end_x':'1'},{'image_x':'21/8','mouth':'3/4','end_x':'2'}],'no_end_image_x':'5/8','no_end_mouth':'1/4'},'unavailable_depth_invents_crossing':{'n':0,'depth':str(D),'residue':str(residue),'upper_bound':str(1+D/Y)},'scope':'Exact diagnostics and constructive strict-height repair. The Y=10 counterexample concerns the prescribed corridor-to-plain-exterior transfer outside the strict-height regime. The open half-plane local model has no external reflections. A bounded room may have other exterior reflection words, which are not tested or excluded. No counterexample to global polygon illumination or dark-sequence theorem.'}
(B/'cluster-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
