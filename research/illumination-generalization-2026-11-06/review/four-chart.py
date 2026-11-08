"""One fixed room, sixteen frozen pairs, four exact extremal charts. No scope expansion."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from math import gcd,lcm
import json,signal,time,importlib.util

HERE=Path(__file__).resolve().parent
effort=json.loads((HERE/'four-chart-effort.json').read_text())
deadline=datetime.fromisoformat(effort['aggregate_deadline_utc']).timestamp()
assert time.time()<deadline,'Original effort expired; no restart'
signal.alarm(max(1,int(deadline-time.time())))
spec=importlib.util.spec_from_file_location('own_audit',HERE/'resumed-exact-check.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
w=list(map(Q,[10,3,2,1]));y=list(map(Q,[0,3,4,5,10]))
polygon=audit.nested_polygon(w,y)

def checktime():assert time.time()<deadline,'Original aggregate deadline reached'
def rational_lcm(values):
    return Q(lcm(*(v.numerator for v in values)),gcd(*(v.denominator for v in values)))
def state(s,start,tau):
    C={0:Q(0)}
    for j in range(1,4):
        phase=s+tau*(y[j]-start)-C[j-1]
        k=(phase/(2*w[j-1])+Q(1,2))//1
        residual=phase-2*k*w[j-1]
        if abs(residual)>=w[j]:return None
        C[j]=C[j-1]+2*k*w[j-1]
    return C
def physical_path(S,T,start,end,tau,C,floor,roof):
    s,ys=S;t,yt=T
    events={start,end}
    bounds=[start,Q(3),Q(4),Q(5),end]
    for j in range(4):
        a,b=bounds[j:j+2];events.update((a,b))
        lo=s+tau*(a-start)-C[j];hi=s+tau*(b-start)-C[j]
        for n in range(int(lo//w[j])-1,int(hi//w[j])+2):
            checktime()
            if tau:
                q=start+(n*w[j]+C[j]-s)/tau
                if a<q<b:events.add(q)
    begin,finish=start,end
    floor_corner=False;roof_corner=False
    if floor:
        events.add(Q(0));events.add(ys)
        floor_phase=s+tau*(-start)
        floor_corner=(floor_phase/w[0]).denominator==1
        if floor_corner:begin=ys
    if roof:
        events.add(Q(10));events.add(yt)
        roof_phase=s+tau*(10-start)-C[3]
        roof_corner=(roof_phase/w[3]).denominator==1
        if roof_corner:finish=yt
    points=[]
    for q in sorted(events):
        if not begin<=q<=finish:continue
        j=max(i for i in range(4) if y[i]<=q) if q>=0 else 0
        x=audit.fold(s+tau*(q-start)-C[j],w[j])
        h=abs(q) if q<3 else (20-q if q>10 else q)
        points.append((x,h))
    assert points[0]==S and points[-1]==T
    return points,floor_corner,roof_corner

def chart(S,T,floor,roof):
    s,ys=S;t,yt=T
    start=-ys if floor else ys
    end=20-yt if roof else yt
    D=end-start
    gaps=[3-start,Q(1),Q(1),end-5]
    assert min(gaps)>0
    P=rational_lcm([2*width/gap for width,gap in zip(w,gaps)])
    assert all((P*gap/(2*width)).denominator==1 for width,gap in zip(w,gaps))
    tested=0
    for sg in (-1,1):
        # All C_j are in 2Z because all four widths are integers with gcd1.
        low=(s-sg*t)/2
        first=-((-low)//1)
        last=(P*D+s-sg*t)/2
        k=first
        while k<last:
            checktime();tau=(2*k+sg*t-s)/D;k+=1
            assert 0<=tau<P;tested+=1
            C=state(s,start,tau)
            if C is None:continue
            assert audit.fold(s+tau*D-C[3],w[3])==t
            points,fc,rc=physical_path(S,T,start,end,tau,C,floor,roof)
            guards=audit.path_check(polygon,points)
            return {'floor':floor,'roof':roof,'period':str(P),'tested':tested,'status':'WITNESS','slope':str(tau),'removed_floor_corner':fc,'removed_roof_corner':rc,'path':points,**guards}
    return {'floor':floor,'roof':roof,'period':str(P),'tested':tested,'status':'COMPLETE_CHART_FAILURE'}

rows=[]
for s,ys,t,yt in product([Q(7),Q(9)],[Q(1),Q(2)],[Q(1,4),Q(3,4)],[Q(6),Q(9)]):
    checktime();S=(s,ys);T=(t,yt);trials=[]
    for floor,roof in [(True,True),(True,False),(False,True),(False,False)]:
        row=chart(S,T,floor,roof);trials.append(row)
        if row['status']=='WITNESS':break
    rows.append({'S':S,'T':T,'charts':trials,'all_four_fail':all(r['status']=='COMPLETE_CHART_FAILURE' for r in trials)})
    if rows[-1]['all_four_fail']:break
out={'status':'EXACT_RESTRICTED_CHART_OBSTRUCTION' if rows[-1]['all_four_fail'] else 'ALL_PRESCRIBED_PAIRS_HAVE_WITNESSES','rows':rows,'ended_utc':datetime.now(timezone.utc).isoformat(),'within_original_deadline':time.time()<deadline,'all_real_or_all_pairs_proved':False,'darkness_claim':False,'whole_goal_complete':False}
(HERE/'four-chart.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
effort.update(status='completed',ended_utc=out['ended_utc'],within_original_deadline=out['within_original_deadline'],running_processes=[])
(HERE/'four-chart-effort.json').write_text(json.dumps(effort,indent=2)+'\n')
signal.alarm(0)
print(json.dumps({'status':out['status'],'pairs':len(rows),'candidate_slopes_tested':sum(c['tested'] for r in rows for c in r['charts']),'physical_reflections':sum(c.get('reflections',0) for r in rows for c in r['charts']),'purified_floor_corners':sum(c.get('removed_floor_corner',False) for r in rows for c in r['charts'])}))
