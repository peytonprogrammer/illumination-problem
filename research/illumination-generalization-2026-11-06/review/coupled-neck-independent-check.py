"""Prescribed exact residue and chart identities. No optical search or scope extrapolation."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json
H=Path(__file__).resolve().parent
def fold(q,w):
    r=q%(2*w);return min(r,2*w-r)
residues=[]
for a,b,eta,n in product((1,3),(1,3),(-1,1),(0,1)):
    e=Q(a-b,2);phase=Q(3+eta+8*n,2)
    assert e in (-1,0,1) and fold(phase,Q(4)) in (1,2,3)
    # Coefficients of 2A-D in M: 2(M+4+a)-(2M+8+a+b).
    assert 2-2==0 and 2*(4+a)-(8+a+b)==a-b
    residues.append({'a':a,'b':b,'eta':eta,'n_mod2':n,'e':e,'folded_base_phase':fold(phase,Q(4))})
signs=[]
for es,et,e0,e1 in product((-1,1),repeat=4):
    w,a,b,d,L1,L2=map(Q,(2,3,5,7,11,17));m=Q(2,9)
    z,zout=Q(3,4),Q(5,4);n1,n2=-2,3;N=n1+n2
    tau=es*m;kappa=e0*e1;sigma1=es*e0;sigmaout=sigma1*kappa;sigma2=-es*et
    c0=z+e0*m*d-kappa*zout
    alpha=2*n1*w+sigma1*z-tau*(L1+a)
    D=L1+L2+a+b+d
    beta=sigma2*(alpha+tau*D-2*N*w-sigma1*c0)
    K=sigma1*c0+sigma2*beta-alpha
    assert tau==(K+2*N*w)/D
    rho=(L1+a)/D
    phase=alpha/(2*w)+(K/(2*w)+N)*rho
    assert phase==n1+sigma1*z/(2*w)
    B0=2*n1*w+sigma1*c0
    Ymid=alpha+tau*(a+L1+d)
    assert Ymid==B0+sigmaout*zout
    ztarget=beta-b*sigma2*tau
    Yfar=alpha+tau*(a+L1+d+L2)
    assert Yfar==B0+2*n2*w+sigma2*ztarget
    assert sigma1*tau==e0*m and sigmaout*tau==e1*m and sigma2*tau==-et*m
    signs.append({'signs':[es,et,e0,e1],'all_affine_and_velocity_identities':True})
def gap(points):
    p=sorted(set(x%1 for x in points));return max([b-a for a,b in zip(p,p[1:])]+[1+p[0]-p[-1]])
nets=[];ell=Q(1,4)
for p,q in [(2,5),(7,17)]:
    r=Q(p,q);m=q-1
    assert gap([j*r for j in range(q)])==Q(1,q)<ell
    epsilon=(ell-Q(1,q))/(4*m)
    for step in (r-epsilon,r,r+epsilon):
        assert gap([j*step for j in range(q)])<ell
    nets.append({'step':r,'indices':q,'perturbation':epsilon,'max_gap_strict':True})
out={'status':'INDEPENDENT_COUPLED_NECK_IDENTITIES_PASS','A17_complete_residue_cases':residues,'A18_sign_identity_cases':signs,'rotation_controls':nets,'physical_darkness_claim':False,'whole_goal_complete':False,'scope':'Algebra controls only; universal conclusions require the independent hand proofs.'}
(H/'coupled-neck-independent-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({'status':out['status'],'residue_cases':len(residues),'sign_cases':len(signs),'net_controls':len(nets)}))
