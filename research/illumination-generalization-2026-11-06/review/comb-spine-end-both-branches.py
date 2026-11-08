"""Both spine target orientations, same original R33 effort/deadline."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import importlib.util,json,time
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('old',R/'comb-spine-end-prefix-check.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)

def criterion(*parameters):
    w=old.criterion(*parameters)
    if w:return {**w,'target_branch':1}
    c,u,v,Ds,Dt,bs,bt,ls,lt,Hg=map(Q,parameters);bt_used=v-bt;H=-lt-ls;den=Ds+Dt+2*c;g0=old.rational_gcd(u,v,Hg);K=old.rational_lcm(2*u/Ds,2*v/Dt,Hg/c);N=den*K/(2*g0);assert N.denominator==1
    for ss,st in ((1,1),(1,-1),(-1,1),(-1,-1)):
        for ell in range(int(N)):
            if ell%128==0:old.deadline()
            tau=(H-ss*bs-st*bt_used+2*g0*ell)/den
            if tau<=0:tau+=K*(int((-tau)//K)+1)
            ks=int((ss*bs+Ds*tau)//(2*u));kt=int((st*bt_used+Dt*tau)//(2*v))
            rs=ss*bs+Ds*tau-2*u*ks;rt=st*bt_used+Dt*tau-2*v*kt
            if not(0<rs<u and 0<rt<v):continue
            jj=(rs+rt+2*c*tau-H)/(2*Hg)
            if jj.denominator!=1:continue
            j=int(jj)
            if min(ks,kt,j)<0:
                tau+=K*(max(0,-ks,-kt,-j)+1);ks=int((ss*bs+Ds*tau-rs)/(2*u));kt=int((st*bt_used+Dt*tau-rt)/(2*v));j=int((rs+rt+2*c*tau-H)/(2*Hg))
            assert min(ks,kt,j)>=0
            return {'sigma_s':ss,'sigma_t':st,'tau':tau,'k_s':ks,'k_t':kt,'j':j,'r_s':rs,'r_t':rt,'target_branch':-1,'period_slope':K,'residue_count_per_sign':int(N)}
    return None

if __name__=='__main__':
    count=0;bad=None;start=time.monotonic()
    for u in (Q(1),Q(2)):
     for v in (Q(1),Q(2)):
      for Ds in (Q(1,2),Q(1),Q(2)):
       for Dt in (Q(1,2),Q(1),Q(2)):
        for bs in (u/3,u/2,2*u/3):
         for bt in (v/3,v/2,2*v/3):
          for gap in (Q(1),Q(2),Q(3)):
           c=Q(1);ls=Q(2);lt=ls+u+gap;Hg=lt+v+3;params=(c,u,v,Ds,Dt,bs,bt,ls,lt,Hg);old.deadline();count+=1
           if criterion(*params) is None:bad={'parameters':params,'actual_source':[c+Ds,ls+bs],'actual_target':[c+Dt,lt+v-bt]};break
          if bad:break
         if bad:break
        if bad:break
       if bad:break
      if bad:break
     if bad:break
    result={'status':'FIRST_BOTH_BRANCH_CRITERION_FAILURE' if bad else 'BOUNDED_BOTH_BRANCH_CRITERION_ALL_POSITIVE','tested_patterns':count,'first_failure':bad,'wall_seconds':time.monotonic()-start,'original_effort_deadline':old.effort['deadline_utc'],'discovery':True,'whole_goal_complete':False,'scope':'One exact finite arithmetic criterion, both target spine orientations; not darkness or universal positivity.'}
    (R/'comb-spine-end-both-branches.json').write_text(json.dumps(result,indent=2,default=str)+'\n');print(json.dumps(result,default=str))
