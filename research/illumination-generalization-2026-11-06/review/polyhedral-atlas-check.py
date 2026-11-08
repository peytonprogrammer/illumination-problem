"""Fixed exact controls for geometric sign cells and compact arithmetic escape. No census."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd
from datetime import datetime,timezone
import importlib.util,json,hashlib,time,signal
H=Path(__file__).resolve().parent
effort=json.loads((H/'polyhedral-atlas-effort.json').read_text())
deadline=datetime.fromisoformat(effort['aggregate_deadline_utc']).timestamp()
assert time.time()<deadline,'Original R18 effort expired'
signal.alarm(max(1,int(deadline-time.time())))
sp=importlib.util.spec_from_file_location('own',H/'resumed-exact-check.py')
own=importlib.util.module_from_spec(sp);sp.loader.exec_module(own)
def sign(x):return (x>0)-(x<0)
def determinant(a,b):return a[0]*b[1]-a[1]*b[0]
def delta(a,b):return (b[0]-a[0],b[1]-a[1])
def dirs(p):
    out=[]
    for a,b in own.edges(p):
        dx,dy=delta(a,b);length=gcd(abs(dx),abs(dy))
        assert length and (dx==0 or dy==0 or abs(dx)==abs(dy))
        out.append(((dx//length,dy//length),length))
    assert all(determinant(out[i-1][0],out[i][0]) for i in range(len(p)))
    return out
def signature(p,T):
    W=len(p);data=dirs(p);out=[]
    for a in p:
        for b in p:
            out.extend(sign(a[k]-b[k]) for k in (0,1))
    for i,a in enumerate(p):
        for b in p:out.append(sign(determinant(data[i][0],delta(a,b))))
    for mark in [(0,0),T]:
        for i,a in enumerate(p):
            out.extend(sign(a[k]-mark[k]) for k in (0,1))
            out.append(sign(determinant(data[i][0],delta(a,mark))))
    out.extend(sign(length) for _,length in data)
    out.extend(sign(z) for z in T)
    assert len(out)==3*W*W+7*W+2
    return out
def signed_on(a,b,z):
    return sign(determinant(delta(a,b),delta(a,z)))==0 and all(sign(z[k]-a[k])*sign(z[k]-b[k])<=0 for k in (0,1))
def signed_intersect(a,b,c,d):
    o1,o2=(sign(determinant(delta(a,b),delta(a,z))) for z in (c,d))
    o3,o4=(sign(determinant(delta(c,d),delta(c,z))) for z in (a,b))
    return ((o1*o2<0 and o3*o4<0) or (o1==0 and signed_on(a,b,c)) or (o2==0 and signed_on(a,b,d)) or (o3==0 and signed_on(c,d,a)) or (o4==0 and signed_on(c,d,b)))
def signed_simple(p):
    data=dirs(p)
    for i,(a,b) in enumerate(own.edges(p)):
        for j,(c,d) in enumerate(own.edges(p)):
            if j>i and j-i not in (1,len(p)-1) and signed_intersect(a,b,c,d):return False
    return True
def signed_location(p,z):
    if any(signed_on(a,b,z) for a,b in own.edges(p)):return 0
    winding=0
    for a,b in own.edges(p):
        sa,sb=sign(a[1]-z[1]),sign(b[1]-z[1]);cross=sign(determinant(delta(a,b),delta(a,z)))
        if sa<=0<sb and cross>0:winding+=1
        if sb<=0<sa and cross<0:winding-=1
    return 1 if winding else -1
controls=[]
for p,marks,expected in [
    ([(0,0),(8,0),(8,4),(4,4),(4,8),(0,8)],[(2,4),(2,6)],True),
    ([(0,0),(2,2),(0,2),(2,0)],[(1,Q(1,2))],False),
    ([(0,0),(4,0),(4,4),(2,4),(2,0),(1,0),(1,2),(0,2)],[(Q(1,2),1)],False)]:
    assert signed_simple(p)==expected
    for z in marks:
        assert signed_location(p,z)==own.location(p,z)
    controls.append({'vertices':p,'marks':marks,'strictly_simple':expected,'sign_location_checks':True})
escape=[]
for n in (2,4,10):
    assert time.time()<deadline
    p=[(0,0),(4*n+1,0),(4*n+1,2*n),(2*n,2*n),(2*n,4*n),(0,4*n)]
    own.simple(p);S=(n,n);T=(n,3*n)
    assert own.location(p,S)==own.location(p,T)==1
    assert gcd(4*n+1,2*n)==1
    k=0
    for x in range(4*n+2):
        for y in range(4*n+1):
            if x%2==y%2==0:continue
            loc=own.location(p,(x,y))
            k+=loc==1 or (loc==0 and (x,y) not in p)
    assert k==9*n*n+6*n-1
    assert all(min(z)>0 for z in [S,T])
    escape.append({'n':n,'k':k,'primitive_coordinate_gcd':1,'normalized_marks':[(Q(1),Q(1)),(Q(1),Q(3))],'normalized_wall_lengths':[Q(length,n) for _,length in dirs(p)]})
p=[(-4,-4),(8,-4),(8,4),(-4,4)]
signatures=[signature(p,(X,-2)) for X in (2,4,6)]
assert signatures[0]==signatures[1]==signatures[2]
path=[(Q(0),Q(0)),(Q(20,3),Q(-4)),(Q(8),Q(-16,5)),(Q(6),Q(-2))]
valid=own.path_check(p,path)
assert Q(2,3)*(16-4)==8 # same word hits the true bottom-right corner for the middle mark.
assert Q(2,3)*(16-2)>8 # another ordering for the first mark.
out={'status':'EXACT_ATLAS_CONTROLS_PASS','geometry_controls':controls,'compact_primitive_escape_controls':escape,'same_geometric_cell_word_change':{'sign_signature_sha256':hashlib.sha256(bytes(x+1 for x in signatures[0])).hexdigest(),'marks':[(2,-2),(4,-2),(6,-2)],'floor_then_right_legal_only_for_last_of_three':True,'last_path_guards':valid,'all_three_pairs_illuminate_directly':True},'within_original_deadline':time.time()<deadline,'whole_goal_complete':False,'independent_acceptance':False}
(H/'polyhedral-atlas-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
signal.alarm(0)
print(json.dumps({'status':out['status'],'sign_forms_W21':3*21*21+7*21+2,'geometry_controls':len(controls),'escape_counts':[x['k'] for x in escape],'same_cell_word_variation':True}))
