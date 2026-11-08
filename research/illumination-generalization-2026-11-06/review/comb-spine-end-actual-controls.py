"""Prescribed genuine spine/tooth-end reflection controls; no ray search."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import importlib.util,json,hashlib
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('both',R/'comb-spine-end-both-branches.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);own=m.old.own

def fold(z,w):r=z%(2*w);return min(r,2*w-r)
def realize(params,width_s,width_t,w):
    c,u,v,ds,dt,bs,bt,ls,lt,Hg=map(Q,params);ws,wt=map(Q,(width_s,width_t));ss,st,tau,ks,kt,j,rs,rt,branch=(w[k] for k in ('sigma_s','sigma_t','tau','k_s','k_t','j','r_s','r_t','target_branch'))
    De_s=w.get('effective_source_depth',ds);De_t=w.get('effective_target_depth',dt);bt_used=bt if branch==1 else v-bt
    assert De_s in (ds,2*ws-ds) and De_t in(dt,2*wt-dt)
    def leg(De,b,ht,k,sg,ww):
        events={Q(0),De}
        for ii in range(1 if sg==1 else 0,2*k+1):
            d=(ii*ht-sg*b)/tau;assert 0<d<De;events.add(d)
        if De>ww:
            d=De-ww;assert 0<d<De
            assert (sg*b+tau*d)%ht!=0 # actual far-end corner forbidden
            events.add(d)
        return [(c+fold(De-d,ww),fold(sg*b+tau*d,ht)) for d in sorted(events)]
    lower=[(x,ls+y) for x,y in leg(De_s,bs,u,ks,ss,ws)]
    backward=leg(De_t,bt_used,v,kt,st,wt)
    upper=[(x,lt+v-y if branch==1 else lt+y) for x,y in backward]
    Ps=ls+rs;Pt=lt+v-rt if branch==1 else lt+rt
    image=Pt+2*Hg*j if branch==1 else -Pt+2*Hg*j
    assert Ps+2*c*tau==image
    cuts={Q(0),c,2*c}
    for ii in range(int(Ps//Hg)+1,int(image//Hg)+1):
        d=(ii*Hg-Ps)/tau
        if 0<d<2*c:cuts.add(d)
    center=[(abs(c-d),fold(Ps+tau*d,Hg)) for d in sorted(cuts)]
    assert center[0]==lower[-1] and center[-1]==upper[-1]
    path=lower+center[1:]+list(reversed(upper))[1:]
    # Retain the first actual target encounter if a far-end bounce revisits it.
    T=upper[0];first=None
    for ii,(a,b) in enumerate(zip(path,path[1:])):
        if own.on(a,b,T):first=ii;break
    assert first is not None
    path=path[:first+1]+[T]
    teeth=[(Q(0),Q(1),c+max(ws,wt)),(ls,ls+u,c+ws),(lt,lt+v,c+wt),(Hg-1,Hg,c+max(ws,wt))]
    poly=[(Q(0),Q(0)),(teeth[0][2],Q(0))]
    for ii,(_,hi,right) in enumerate(teeth):
        poly.append((right,hi))
        if ii<3:
            nxt=teeth[ii+1];assert hi<nxt[0];poly.extend([(c,hi),(c,nxt[0]),(nxt[2],nxt[0])])
    poly.append((Q(0),Hg));own.simple(poly)
    guard=own.path_check(poly,path)
    return {'path':path,'polygon':poly,'source':path[0],'target':path[-1],**guard}

params_odd=(1,1,1,Q(1,2),Q(1,2),Q(1,3),Q(2,3),2,4,8)
w=m.criterion(*params_odd);assert w and w['target_branch']==-1
odd=realize(params_odd,Q(3),Q(3),w)
params_far=(2,1,4,Q(1,2),1,Q(4,5),Q(16,5),2,7,16)
assert m.criterion(*params_far) is None
farw={'sigma_s':1,'sigma_t':1,'tau':Q(42,29),'k_s':4,'k_t':1,'j':0,'r_s':Q(111,145),'r_t':Q(354,145),'target_branch':1,'effective_source_depth':Q(11,2),'effective_target_depth':Q(5)}
far=realize(params_far,3,3,farw)
scaled=own.path_check([(20*x,20*y) for x,y in far['polygon']],[(20*x,20*y) for x,y in far['path']]);assert (20*far['source'][0],20*far['source'][1])==(50,56) and (20*far['target'][0],20*far['target'][1])==(60,156)
# Independent literal finite exhaustion for the no-tooth-end counterexample.
rejects={};count=0
for branch,Heff,btarget in [(1,Q(9),Q(16,5)),(-1,Q(-9),Q(4,5))]:
    for ss in (-1,1):
     for st in (-1,1):
      for ell in range(22):
        tau=(Heff-ss*Q(4,5)-st*btarget+2*ell)/Q(11,2)
        aa=ss*Q(4,5)+Q(1,2)*tau;bb=st*btarget+tau
        rs=aa%2;rt=bb%8;count+=1
        reason='source_portal' if not 0<rs<1 else 'target_portal' if not 0<rt<4 else 'spine_image'
        if reason=='spine_image':assert ((rs+rt+4*tau-Heff)/32).denominator!=1
        rejects[reason]=rejects.get(reason,0)+1
assert count==176
out={'status':'ODD_SPINE_AND_TOOTH_END_ACTUAL_REPAIRS_PASS','odd_target_branch':{'witness':w,**odd},'tooth_end_repair':{'witness':farw,**far},'scaled_A_control':{'source':[50,56],'target':[60,156],**scaled},'restricted_no_tooth_end_exhaustion':{'period_tau':'8','slope_residues_per_sign':22,'checks':count,'rejection_counts':rejects},'whole_goal_complete':False,'discovery':False,'source_sha256':{'comb-spine-end-prefix-check.py':hashlib.sha256((R/'comb-spine-end-prefix-check.py').read_bytes()).hexdigest(),'comb-spine-end-both-branches.py':hashlib.sha256((R/'comb-spine-end-both-branches.py').read_bytes()).hexdigest(),'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()},'limits':'Prescribed positive repairs and exact restricted arithmetic criterion rejection, not all-comb theorem or darkness.'}
(R/'comb-spine-end-actual-controls.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({'status':out['status'],'odd_reflections':odd['reflections'],'tooth_end_reflections':far['reflections'],'restricted_residue_checks':count,'actual_guard_total':odd['wall_leg_guards']+far['wall_leg_guards']+scaled['wall_leg_guards']}))
