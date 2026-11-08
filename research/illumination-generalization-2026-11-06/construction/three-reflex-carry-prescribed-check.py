"""Two prescribed exact hand countercontrols; no discovery or ray engine."""
from fractions import Fraction as Q
from pathlib import Path
import json


def evaluate(tau, scale):
    a,l,w,A,b,c,h,H=map(lambda x:Q(x)*scale,(4,12,20,28,4,8,20,28))
    s,u=Q(2)*scale,Q(6)*scale
    t,v=Q(25,2)*scale,Q(2)*scale
    assert 0<s<a and b<u<h and l<t<A and 0<v<c
    R,B,z,D=A-w,A-l,A-t,2*H-u-v
    n=(s+(h-u)*tau+a)//(2*a)
    z0=s+(h-u)*tau-2*n*a
    m=(z0+2*(H-h)*tau)//(2*A)
    z1=z0+2*(H-h)*tau-(2*m+1)*A
    k=(z1+(h-c)*tau+R)//(2*R)
    z2=z1+(h-c)*tau-2*k*R
    end=z2+(c-v)*tau
    j=(end-z+B)//(2*B)
    assert abs(z0)<a and abs(z1)<R and abs(z2)<R
    assert abs(end-z-2*j*B)<B
    root=(2*n*a+(2*m+1)*A+2*k*R+2*j*B+z-s)/D
    if scale==4:
        assert all(x.denominator==1 and x%2==0 for x in (s,u,t,v))
    return {'tau':tau,'scale':scale,'indices':[int(x) for x in (n,m,k,j)],
            'residuals':[z0,z1,z2],'terminal_trial_phase':end,'root_update':root}


if __name__=='__main__':
    rows=[]
    for scale in (1,4):
        left=evaluate(Q(499,420),scale)
        right=evaluate(Q(501,420),scale)
        assert left['indices']==[2,0,0,0]
        assert right['indices']==[2,0,1,-1]
        assert left['root_update']==Q(115,96)
        assert right['root_update']==Q(83,96)
        assert right['root_update']-left['root_update']==-Q(1,3)
        rows.extend([left,right])
    out={'decision':'REFUTES_PRECISE_NEAREST_PERIOD_GLOBAL_MONOTONICITY_PREMISE',
         'prescribed_evaluations':rows,'native_even_even_scaled_control':True,
         'search_used':False,'old_clock_renewed':False,'illumination_refuted':False,
         'TR02_universal_feasibility_settled':False,'whole_goal_complete':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='prescribed_evaluations'}))
