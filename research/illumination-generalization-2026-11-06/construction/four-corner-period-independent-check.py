"""Prescribed R36 exact base and rank-section audit; no discovery or peer imports."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent/'review'
req=json.loads((P/'four-corner-critical-review-request.json').read_text())
for name,expected in req['source_sha256'].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==expected,name
d=json.loads((P/'four-corner-critical-check.json').read_text());V=[tuple(map(F,z)) for z in d['polygon']];path=[tuple(map(F,z)) for z in d['witness']['path']];edges=list(zip(V,V[1:]+V[:1]))
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
assert path[0]==tuple(d['source']) and path[-1]==tuple(d['target']) and len(edges)==20
assert det(sub(path[1],path[0]),tuple(d['physical_direction']))==0 and dot(sub(path[1],path[0]),tuple(d['physical_direction']))>0
guards=0;walls=[]
for leg,(a,b) in enumerate(zip(path,path[1:])):
    delta=sub(b,a);hits=[]
    for k,(x,y) in enumerate(edges):
        guards+=1;e=sub(y,x);den=det(delta,e)
        if not den:
            assert det(sub(x,a),delta)!=0;continue
        t=F(det(sub(x,a),e),den);z=F(det(sub(x,a),delta),den)
        assert not(0<t<1 and 0<=z<=1)
        if t==1 and 0<=z<=1:hits.append((k,z))
    if leg<len(path)-2:assert len(hits)==1 and 0<hits[0][1]<1;walls.append(hits[0][0])
    else:assert not hits
    v=tuple(d['physical_direction']);incoming=delta
    target=tuple(d['target']);tt=F(target[0]-a[0],incoming[0]) if incoming[0] else F(target[1]-a[1],incoming[1])
    if 0<tt<=1 and tuple(a[k]+tt*incoming[k] for k in (0,1))==target:assert leg==len(path)-2 and tt==1
for j,wall in enumerate(walls,1):
    v=sub(path[j],path[j-1]);out=sub(path[j+1],path[j]);e=sub(edges[wall][1],edges[wall][0]);n=(-e[1],e[0]);ref=tuple(v[k]-2*F(dot(v,n),dot(n,n))*n[k] for k in (0,1))
    assert det(ref,out)==0 and dot(ref,out)>0
X=[-1,0,1,2,3];Y=[0,1,2,3,6,8,10,12,13,14,15,16]
def sections(axis,cut):
    coords=[]
    for a,b in edges:
        if (a[axis]>cut)!=(b[axis]>cut):
            t=F(cut-a[axis],b[axis]-a[axis]);coords.append(a[1-axis]+t*(b[1-axis]-a[1-axis]))
    coords.sort();assert len(coords)%2==0
    return list(zip(coords[::2],coords[1::2]))
y_sections=[sections(1,F(a+b,2)) for a,b in zip(Y,Y[1:])]
x_sections=[sections(0,F(a+b,2)) for a,b in zip(X,X[1:])]
assert {b-a for ss in y_sections for a,b in ss}=={F(1),F(2),F(3)}
assert x_sections==[[(6,8),(10,12)],[(0,16)],[(1,3),(13,15)],[(1,3),(13,15)]]
assert all(F(24,2*(b-a)).denominator==1 for ss in y_sections for a,b in ss)
height_coefficients={}
for ss in x_sections:
    for a,b in ss:
        active=[i for i in range(11) if a<=Y[i] and Y[i+1]<=b]
        height_coefficients[str((int(a),int(b)))]=active
assert height_coefficients=={'(6, 8)':[4],'(10, 12)':[6],'(0, 16)':list(range(11)),'(1, 3)':[1,2],'(13, 15)':[8,9]}
assert [i for i in range(11) if Y[i+1]<=2]==[0,1]
assert [i for i in range(11) if Y[i+1]<=14]==list(range(9))
assert [i for i in range(4) if X[i+1]<=2]==[0,1,2]
out={'status':'EXACT_BASE_AND_ALL_RANK_SECTION_FORMULAS_PASS','base_reflections':len(walls),'base_all_wall_leg_guards':guards,'vertical_gap_count':len(y_sections),'horizontal_gap_count':len(x_sections),'actual_horizontal_section_widths':[1,2,3],'current_height_gap_coefficients':height_coefficients,'all_n_congruence':'DeltaY14n gives24n, multiple of2W; DeltaX24Km gives14Km, multiple of2U sinceU|K','source_pins_verified':len(req['source_sha256']),'discovery':False,'grown_control_paths_replayed':False,'whole_goal_complete':False}
(R/'four-corner-period-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
