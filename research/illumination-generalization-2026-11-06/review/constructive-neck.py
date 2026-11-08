"""Fixed sqrt(2) first-mouth beams in two prescribed rational chambers; exact arithmetic."""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime,timezone
from dataclasses import dataclass
import json,signal,time,importlib.util
HERE=Path(__file__).resolve().parent
effort=json.loads((HERE/'constructive-neck-effort.json').read_text())
deadline=datetime.fromisoformat(effort['aggregate_deadline_utc']).timestamp()
assert time.time()<deadline,'Original R17 deadline expired; no restart'
signal.alarm(max(1,int(deadline-time.time())))
def clock():assert time.time()<deadline,'Original aggregate deadline reached'
@dataclass(frozen=True)
class K:
    p:Q=Q(0)
    q:Q=Q(0)
    @staticmethod
    def of(v):return v if isinstance(v,K) else K(Q(v))
    def __add__(a,b):
        b=K.of(b);return K(a.p+b.p,a.q+b.q)
    __radd__=__add__
    def __neg__(a):return K(-a.p,-a.q)
    def __sub__(a,b):return a+-K.of(b)
    def __rsub__(a,b):return K.of(b)+-a
    def __mul__(a,b):
        b=K.of(b);return K(a.p*b.p+2*a.q*b.q,a.p*b.q+a.q*b.p)
    __rmul__=__mul__
    def __truediv__(a,b):
        b=K.of(b);den=b.p*b.p-2*b.q*b.q;assert den
        return a*K(b.p/den,-b.q/den)
    def __rtruediv__(a,b):return K.of(b)/a
    def sign(a):
        if not a.p:return (a.q>0)-(a.q<0)
        if not a.q:return (a.p>0)-(a.p<0)
        if a.p*a.q>0:return (a.p>0)-(a.p<0)
        s=(a.p*a.p>2*a.q*a.q)-(a.p*a.p<2*a.q*a.q)
        return s if a.p>0 else -s
    def __lt__(a,b):return (a-K.of(b)).sign()<0
    def __le__(a,b):return (a-K.of(b)).sign()<=0
    def __gt__(a,b):return (a-K.of(b)).sign()>0
    def __ge__(a,b):return (a-K.of(b)).sign()>=0
    def __eq__(a,b):
        b=K.of(b);return a.p==b.p and a.q==b.q
    def encoded(a):return [str(a.p),str(a.q)]

def first_mouth(poly,mark,vx,magnitude):
    point=tuple(K.of(x) for x in mark);velocity=(K.of(vx),magnitude)
    path=[point];word=[];virtual=tuple(map(Q,mark));virtuals=[virtual];comparisons=0
    while True:
        clock();events=[]
        for i,a in enumerate(poly):
            b=poly[(i+1)%len(poly)]
            axis=0 if a[0]==b[0] else 1;other=1-axis
            assert a[axis]==b[axis]
            t=(a[axis]-point[axis])/velocity[axis]
            if t<=0:continue
            z=point[other]+t*velocity[other]
            comparisons+=1
            if min(a[other],b[other])<=z<=max(a[other],b[other]):events.append((t,i,axis,z))
        assert events
        event=min(events,key=lambda z:z[0]);t,i,axis,z=event
        assert sum(e[0]==t for e in events)==1,'Corner collision'
        a=poly[i];b=poly[(i+1)%len(poly)];other=1-axis
        assert min(a[other],b[other])<z<max(a[other],b[other])
        point=tuple(point[k]+t*velocity[k] for k in (0,1));path.append(point)
        if point[0]==0 and 0<point[1]<2:
            sign_vertical=velocity[1].sign()
            return {'word':word,'virtual':virtual,'virtuals':virtuals,'sign_vertical':sign_vertical,'path':path,'wall_event_comparisons':comparisons}
        word.append(i)
        vv=list(velocity);vv[axis]=-vv[axis];velocity=tuple(vv)
        v=list(virtual);v[axis]=2*a[axis]-v[axis];virtual=tuple(v);virtuals.append(virtual)

root=K(0,Q(1))
left=list(map(lambda z:tuple(map(Q,z)),[(-6,0),(0,0),(0,2),(-2,2),(-2,4),(-4,4),(-4,1),(-6,1)]))
right=list(map(lambda z:tuple(map(Q,z)),[(0,0),(4,0),(4,4),(2,4),(2,2),(0,2)]))
rows=[]
for poly,mark,vx in [(left,(-3,3),1),(right,(3,3),-1)]:
    result=first_mouth(poly,mark,vx,root)
    critical={Q(1),Q(2)}
    # Include mouth endpoints even if they were merely smooth points of a longer cap.
    for sx,sy in result['virtuals']:
        for cx,cy in poly+[(Q(0),Q(0)),(Q(0),Q(2))]:
            if cx!=sx:
                m=abs((cy-sy)/(cx-sx))
                if m>0:critical.add(m)
    low=max(v for v in critical if K.of(v)<root)
    high=min(v for v in critical if root<K.of(v))
    assert low<high
    controls=[]
    for numerator in (1,2,3):
        rational=(numerator*low+(4-numerator)*high)/4
        trial=first_mouth(poly,mark,vx,K.of(rational))
        assert trial['word']==result['word'] and trial['virtual']==result['virtual']
        assert trial['sign_vertical']==result['sign_vertical']
        controls.append(str(rational))
    rows.append({'polygon':poly,'actual_mark':mark,'initial_vx':vx,'initial_vy':'sqrt(2)','wall_word':result['word'],'virtual':result['virtual'],'sign_vertical':result['sign_vertical'],'path_Qsqrt2':[[a.encoded(),b.encoded()] for a,b in result['path']],'rational_magnitude_interval':[low,high],'rational_control_magnitudes':controls,'finite_critical_slopes':sorted(critical),'wall_event_comparisons':result['wall_event_comparisons']})
lo=max(r['rational_magnitude_interval'][0] for r in rows);hi=min(r['rational_magnitude_interval'][1] for r in rows)
emin,eplus=(r['sign_vertical'] for r in rows);sigma=-emin*eplus
u,v=(lo,hi) if emin==1 else (-hi,-lo)
a=-rows[0]['virtual'][0];b=rows[1]['virtual'][0]
alpha=rows[0]['virtual'][1];beta=rows[1]['virtual'][1]
assert a>0 and b>0
for tau in (u+(v-u)/4,u+3*(v-u)/4):
    assert 0<alpha+a*tau<2 and 0<beta-b*sigma*tau<2
threshold=max(Q(0),Q(4)/(v-u)-a-b)
assert emin==1 and sigma==1 # This prescribed pair; not a general-sign implementation claim.
length=threshold+1
c=sigma*beta-alpha;total=length+a+b
n=((total*u-c)/4)//1+1
tau=(c+4*n)/total
assert u<tau<v
left_beam=first_mouth(left,(-3,3),1,K.of(tau))
right_beam=first_mouth(right,(3,3),-1,K.of(tau))
assert left_beam['word']==rows[0]['wall_word'] and right_beam['word']==rows[1]['wall_word']
def rational_path(result):
    assert all(not x.q and not y.q for x,y in result['path'])
    return [(x.p,y.p) for x,y in result['path']]
lp,rp=rational_path(left_beam),rational_path(right_beam)
zleft=alpha+a*tau;zlast=zleft+length*tau
neck=[]
for k in range(int(zleft//2)-1,int(zlast//2)+2):
    clock();x=(2*k-zleft)/tau
    if 0<x<length:neck.append((x,Q(0 if k%2==0 else 2)))
neck.sort()
full=lp+neck+[(length+x,y) for x,y in reversed(rp)]
polygon=[(-6,0),(length+4,0),(length+4,4),(length+2,4),(length+2,2),(-2,2),(-2,4),(-4,4),(-4,1),(-6,1)]
sp=importlib.util.spec_from_file_location('own_audit',HERE/'resumed-exact-check.py')
audit=importlib.util.module_from_spec(sp);sp.loader.exec_module(audit)
audit.simple(polygon);guards=audit.path_check(polygon,full)
physical={'neck_length':length,'slope':tau,'phase_integer':n,'path':full,'actual_source':full[0],'actual_target':full[-1],**guards}
out={'status':'EXACT_CONSTRUCTIVE_ARITHMETIC_BEAMS_PASS','rows':rows,'signed_interval':[u,v],'relative_sigma':sigma,'virtual_source':[-a,alpha],'virtual_target':[b,beta],'rational_threshold':threshold,'prescribed_physical_join':physical,'ended_utc':datetime.now(timezone.utc).isoformat(),'within_original_deadline':time.time()<deadline,'whole_goal_complete':False,'universal_runtime_or_W_bound':False,'independent_acceptance':False}
(HERE/'constructive-neck.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
effort.update(status='computational_part_complete',running_processes=[],ended_utc=out['ended_utc'])
(HERE/'constructive-neck-effort.json').write_text(json.dumps(effort,indent=2)+'\n')
signal.alarm(0)
print(json.dumps({'status':out['status'],'word_lengths':[len(r['wall_word']) for r in rows],'threshold':str(threshold),'interval':list(map(str,[u,v])),'sigma':sigma,'joined_reflections':guards['reflections'],'wall_leg_guards':guards['wall_leg_guards']}))
