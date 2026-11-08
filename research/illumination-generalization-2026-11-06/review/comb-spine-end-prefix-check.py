"""Finite exact arithmetic criterion and actual spine-end witness validation."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm
from datetime import datetime,timezone
import json,importlib.util
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('own',R/'resumed-exact-check.py');own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
effort=json.loads((R/'comb-spine-end-prefix-effort.json').read_text())
def deadline():assert datetime.now(timezone.utc)<datetime.fromisoformat(effort['deadline_utc'])
def rational_gcd(*values):
    den=lcm(*(x.denominator for x in values));nums=[int(x*den) for x in values];a=nums[0]
    for b in nums[1:]:a=gcd(a,b)
    return Q(a,den)
def rational_lcm(*values):
    a=values[0].numerator
    for b in values[1:]:a=lcm(a,b.numerator)
    return Q(a,gcd(gcd(values[0].denominator,values[1].denominator),values[2].denominator))
def criterion(c,u,v,Ds,Dt,bs,bt,ls,lt,Hg):
    c,u,v,Ds,Dt,bs,bt,ls,lt,Hg=map(Q,(c,u,v,Ds,Dt,bs,bt,ls,lt,Hg));assert ls+u<lt and 0<=ls and lt+v<=Hg
    assert min(c,u,v,Ds,Dt)>0 and 0<bs<u and 0<bt<v
    H=lt+v-ls;den=Ds+Dt+2*c;g0=rational_gcd(u,v,Hg);K=rational_lcm(2*u/Ds,2*v/Dt,Hg/c);N=den*K/(2*g0);assert N.denominator==1
    period=int(N)
    for ss,st in ((1,1),(1,-1),(-1,1),(-1,-1)):
        for ell in range(period):
            if ell%128==0:deadline()
            tau=(H-ss*bs-st*bt+2*g0*ell)/den
            if tau<=0:tau+=K*(int((-tau)//K)+1)
            ks=int((ss*bs+Ds*tau)//(2*u));kt=int((st*bt+Dt*tau)//(2*v))
            rs=ss*bs+Ds*tau-2*u*ks;rt=st*bt+Dt*tau-2*v*kt
            if not(0<rs<u and 0<rt<v):continue
            j=(rs+rt+2*c*tau-H)/(2*Hg)
            if j.denominator!=1:continue
            j=int(j)
            shift=max(0,-ks,-kt,-j)+1
            # One positive common period increases ALL winding indices by positive integers.
            if min(ks,kt,j)<0:
                tau+=K*shift;ks=int((ss*bs+Ds*tau-rs)/(2*u));kt=int((st*bt+Dt*tau-rt)/(2*v));j=int((rs+rt+2*c*tau-H)/(2*Hg))
            assert min(ks,kt,j)>=0 and tau>0
            return {'sigma_s':ss,'sigma_t':st,'tau':tau,'k_s':ks,'k_t':kt,'j':j,'r_s':rs,'r_t':rt,'period_slope':K,'residue_count_per_sign':period}
    return None

def actual_path(c,u,v,Ds,Dt,bs,bt,ls,lt,Hg,w):
    c,u,v,Ds,Dt,bs,bt,ls,lt,Hg=map(Q,(c,u,v,Ds,Dt,bs,bt,ls,lt,Hg));ss,st,tau,ks,kt,j,rs,rt=(w[k] for k in ('sigma_s','sigma_t','tau','k_s','k_t','j','r_s','r_t'))
    def tooth(D,b,height,k,sg):
        return [(c+D,b)]+[(c+D-(i*height-sg*b)/tau,height if i%2 else Q(0)) for i in range(1 if sg==1 else 0,2*k+1)]
    low=[(x,ls+y) for x,y in tooth(Ds,bs,u,ks,ss)]
    top=[(x,lt+v-y) for x,y in reversed(tooth(Dt,bt,v,kt,st))]
    Ps=ls+rs;Pt=lt+v-rt;distance=2*c
    assert Ps+distance*tau==Pt+2*Hg*j
    def fold(z):r=z%(2*Hg);return min(r,2*Hg-r)
    events={Q(0),c,2*c}
    for n in range(int(Ps//Hg)+1,int((Pt+2*Hg*j)//Hg)+1):
        d=(n*Hg-Ps)/tau
        if 0<d<distance:events.add(d)
    middle=[(abs(c-d),fold(Ps+tau*d)) for d in sorted(events)]
    assert middle[0]==(c,Ps) and middle[-1]==(c,Pt)
    path=low+middle+top
    # Include strict portals as nonreflecting points, remove coincident points if any.
    assert all(a!=b for a,b in zip(path,path[1:]))
    right=c+max(Ds,Dt)+2
    teeth=[(Q(0),Q(1),right),(ls,ls+u,right),(lt,lt+v,right),(Hg-1,Hg,right)]
    assert teeth[0][1]<ls and lt+v<Hg-1
    poly=[(Q(0),Q(0)),(right,Q(0))]
    for k,(_,hi,end) in enumerate(teeth):
        poly.append((end,hi))
        if k<3:
            nxt=teeth[k+1];poly.extend([(c,hi),(c,nxt[0]),(nxt[2],nxt[0])])
    poly.append((Q(0),Hg));own.simple(poly)
    guard=own.path_check(poly,path)
    assert all(not own.on(a,b,path[-1]) for a,b in zip(path[:-2],path[1:-1]))
    return {'path':path,'polygon':poly,'source':path[0],'target':path[-1],**guard}

def main():
    params=(1,1,1,Q(1,2),Q(1,2),Q(1,3),Q(2,3),2,8,11)
    w=criterion(*params);assert w
    prescribed={'sigma_s':1,'sigma_t':1,'tau':Q(36),'k_s':9,'k_t':9,'j':3,'r_s':Q(1,3),'r_t':Q(2,3)}
    control=actual_path(*params,prescribed)
    scaled_poly=[(12*x,12*y) for x,y in control['polygon']];scaled_path=[(12*x,12*y) for x,y in control['path']]
    own.simple(scaled_poly);scaled=own.path_check(scaled_poly,scaled_path)
    assert scaled_path[0]==(18,28) and scaled_path[-1]==(18,100)
    out={'status':'ACTUAL_SPINE_END_PATH_REPAIRS_A29_CONTROL','criterion_first_witness':w,'prescribed_witness':prescribed,'control':control,'scaled_A_control':{'source':scaled_path[0],'target':scaled_path[-1],**scaled},'whole_goal_complete':False,'discovery':False,'scope':'One prescribed shallow control and finite algebra criterion, not all canonical combs.'}
    (R/'comb-spine-end-prefix-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('control','criterion_first_witness','prescribed_witness','scaled_A_control')}));print(json.dumps({'reflections':control['reflections'],'wall_leg_guards':control['wall_leg_guards']}))
if __name__=='__main__':main()
