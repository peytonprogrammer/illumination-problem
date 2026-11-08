"""The ONE authorized R20 comb/pair; exact positive witness search with original deadline."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
from math import gcd
import importlib.util,json,time,signal
H=Path(__file__).resolve().parent
effort=json.loads((H/'strip-tree-propagation-effort.json').read_text())
deadline=datetime.fromisoformat(effort['aggregate_deadline_utc']).timestamp()
assert time.time()<deadline,'Original R20 deadline expired; no restart'
signal.alarm(max(1,int(deadline-time.time())))
sp=importlib.util.spec_from_file_location('own',H/'resumed-exact-check.py')
own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
P=[(0,0),(20,0),(20,4),(4,4),(4,8),(20,8),(20,12),(4,12),(4,16),(20,16),(20,20),(4,20),(4,24),(20,24),(20,28),(4,28),(4,32),(20,32),(20,36),(0,36)]
P=[tuple(map(Q,z)) for z in P];S=(Q(8),Q(2));T=(Q(8),Q(34))
own.simple(P);assert own.location(P,S)==own.location(P,T)==1
assert all(c%2==0 for c in (*S,*T))
def clock():assert time.time()<deadline,'Original R20 aggregate deadline reached'
def trace(v):
    point=S;path=[S];seen=set()
    for contact in range(1000):
        clock()
        if (point,v) in seen:return None,'PERIODIC'
        seen.add((point,v));events=[]
        for wall,(a,b) in enumerate(own.edges(P)):
            axis=0 if a[0]==b[0] else 1;other=1-axis
            if not v[axis]:continue
            dt=(a[axis]-point[axis])/v[axis]
            if dt<=0:continue
            z=point[other]+dt*v[other]
            if min(a[other],b[other])<=z<=max(a[other],b[other]):events.append((dt,wall,axis))
        assert events
        dt,wall,axis=min(events)
        moving=0 if v[0] else 1;tt=(T[moving]-point[moving])/v[moving]
        if 0<tt<dt and all(point[k]+tt*v[k]==T[k] for k in (0,1)):
            return path+[T],'WITNESS'
        point=tuple(point[k]+dt*v[k] for k in (0,1));path.append(point)
        if sum(e[0]==dt for e in events)!=1 or point in P:return None,'CORNER'
        vv=list(v);vv[axis]=-vv[axis];v=tuple(vv)
    return None,'CONTACT_CAP_UNDECIDED'
count=0;out=None;reasons={}
for norm in range(1,25):
    for p in range(-norm,norm+1):
        for q in range(-norm,norm+1):
            if max(abs(p),abs(q))!=norm or gcd(abs(p),abs(q))!=1:continue
            clock();count+=1;path,reason=trace((Q(p),Q(q)))
            reasons[reason]=reasons.get(reason,0)+1
            if path:
                guards=own.path_check(P,path)
                out={'status':'EXACT_ACTUAL_WITNESS_VERIFIED','initial_direction':[p,q],'polygon':P,'actual_source':S,'actual_target':T,'path':path,**guards}
                break
        if out:break
    if out:break
if out is None:out={'status':'NO_WITNESS_WITHIN_AUTHORIZED_FINITE_SEARCH','not_a_darkness_result':True}
out.update(directions_tested=count,stopping_reasons=reasons,ended_utc=datetime.now(timezone.utc).isoformat(),within_original_deadline=time.time()<deadline,whole_goal_complete=False,independent_acceptance=False)
(H/'comb-one-pattern.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
effort.update(search_status='terminal',search_ended_utc=out['ended_utc'],running_processes=[])
(H/'strip-tree-propagation-effort.json').write_text(json.dumps(effort,indent=2)+'\n')
signal.alarm(0)
print(json.dumps({k:v for k,v in out.items() if k not in ('polygon','path','actual_source','actual_target')}))
