"""Finite far-end certificate program, SAME original R33 aggregate deadline."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm
from datetime import datetime,timezone
import random,importlib.util,json,time
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('base',R/'comb-spine-end-prefix-check.py');base=importlib.util.module_from_spec(sp);sp.loader.exec_module(base)
def qlcm(values):
    numerator=1;denominator=0
    for z in values:numerator=lcm(numerator,z.numerator);denominator=gcd(denominator,z.denominator)
    return Q(numerator,denominator)
def solve(params,ws,wt):
    c,u,v,ds,dt,bs,bt,ls,lt,Hg=map(Q,params);ws,wt=map(Q,(ws,wt));assert 0<ds<ws and 0<dt<wt
    g0=base.rational_gcd(u,v,Hg);rejections=[]
    for De_s in (ds,2*ws-ds):
     for De_t in(dt,2*wt-dt):
      den=De_s+De_t+2*c;periods=[2*u/De_s,2*v/De_t,Hg/c]
      if De_s>ws:periods.append(u/(De_s-ws))
      if De_t>wt:periods.append(v/(De_t-wt))
      K=qlcm(periods);NN=den*K/(2*g0);assert NN.denominator==1;N=int(NN);counts={};total=0
      for branch,Heff,btarget in ((1,lt+v-ls,bt),(-1,-lt-ls,v-bt)):
       for ss,st in ((1,1),(1,-1),(-1,1),(-1,-1)):
        for ell in range(N):
            if ell%128==0:base.deadline()
            tau=(Heff-ss*bs-st*btarget+2*g0*ell)/den
            if tau<=0:tau+=K*(int((-tau)//K)+1)
            ks=int((ss*bs+De_s*tau)//(2*u));kt=int((st*btarget+De_t*tau)//(2*v));rs=ss*bs+De_s*tau-2*u*ks;rt=st*btarget+De_t*tau-2*v*kt;total+=1
            reason=None
            if not 0<rs<u:reason='source_portal'
            elif not 0<rt<v:reason='target_portal'
            elif ((rs+rt+2*c*tau-Heff)/(2*Hg)).denominator!=1:reason='spine_image'
            elif De_s>ws and (ss*bs+tau*(De_s-ws))%u==0:reason='source_far_corner'
            elif De_t>wt and (st*btarget+tau*(De_t-wt))%v==0:reason='target_far_corner'
            if reason:counts[reason]=counts.get(reason,0)+1;continue
            j=int((rs+rt+2*c*tau-Heff)/(2*Hg))
            if min(ks,kt,j)<0:
                tau+=K*(max(0,-ks,-kt,-j)+1);ks=int((ss*bs+De_s*tau-rs)/(2*u));kt=int((st*btarget+De_t*tau-rt)/(2*v));j=int((rs+rt+2*c*tau-Heff)/(2*Hg))
            assert min(ks,kt,j)>=0
            return {'sigma_s':ss,'sigma_t':st,'tau':tau,'k_s':ks,'k_t':kt,'j':j,'r_s':rs,'r_t':rt,'target_branch':branch,'effective_source_depth':De_s,'effective_target_depth':De_t,'period_tau':K,'slope_residues_per_sign':N},rejections
      rejections.append({'effective_depths':[De_s,De_t],'period_tau':K,'slope_residues_per_sign':N,'checks':total,'rejections':counts})
    return None,rejections

if __name__=='__main__':
    rng=random.Random(3302);start=time.monotonic();count=0;bad=None;max_seconds=100
    for index in range(600):
        base.deadline()
        if time.monotonic()-start>max_seconds:break
        c=Q(rng.randrange(1,4));u=Q(rng.randrange(1,5));v=Q(rng.randrange(1,5));ds=rng.choice([Q(1,2),Q(1),Q(2),Q(3)]);dt=rng.choice([Q(1,2),Q(1),Q(2),Q(3)])
        ws=ds+rng.choice([Q(1,2),Q(1),Q(2)]);wt=dt+rng.choice([Q(1,2),Q(1),Q(2)])
        bs=u*Q(rng.randrange(1,5),5);bt=v*Q(rng.randrange(1,5),5);ls=Q(2);lt=ls+u+rng.randrange(1,5);Hg=lt+v+rng.randrange(2,5)
        params=(c,u,v,ds,dt,bs,bt,ls,lt,Hg);count+=1;w,reject=solve(params,ws,wt)
        if w is None:bad={'parameters':params,'actual_widths':[ws,wt],'source':[c+ds,ls+bs],'target':[c+dt,lt+v-bt],'full_class_rejections':reject};break
    out={'status':'FIRST_ONE_EXCURSION_CERTIFICATE_CLASS_FAILURE' if bad else 'BOUNDED_ONE_EXCURSION_CHALLENGE_POSITIVE_INCONCLUSIVE','tested_patterns':count,'seed':3302,'first_failure':bad,'wall_seconds':time.monotonic()-start,'original_effort_deadline':base.effort['deadline_utc'],'discovery':True,'whole_goal_complete':False,'scope':'Finite expanded algebraic certificate classes including genuine far-end corner guards. No bounded success is a universal proof; failure is not darkness.'}
    (R/'comb-one-excursion-completeness.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps(out,default=str))
