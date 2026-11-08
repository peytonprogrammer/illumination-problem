"""Supporting-line stress identity on one frozen event packet. No new rays."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parent;I=ROOT/'inputs'
spec=importlib.util.spec_from_file_location('fixed_event_model',I/'event_model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
room=json.loads((I/'room.json').read_text());events=json.loads((I/'events.json').read_text())['rows']
stored=json.loads((I/'funcs.json').read_text());old=m.EventModel(room)
W=old.W;dim=W+4;zero=(F(0),)*dim
unit=lambda i:tuple(F(i==j) for j in range(dim))
add=lambda a,b:tuple(x+y for x,y in zip(a,b))
scale=lambda a,v:tuple(a*x for x in v)
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
cross=lambda a,b:a[0]*b[1]-a[1]*b[0]
matmul=m.matmul
ID=((F(1),F(0)),(F(0),F(1)))

def mv(A,v):return tuple(sum(A[j][k]*v[k] for k in (0,1)) for j in (0,1))
def mf(A,v):return tuple(add(scale(A[j][0],v[0]),scale(A[j][1],v[1])) for j in (0,1))
def pf(A,b,p):return tuple(add(x,y) for x,y in zip(mf(A,p),b))
def evaluate(p):return tuple(dot(row,theta) for row in p)
def formcross(w,p):return tuple(w[0]*p[1][j]-w[1]*p[0][j] for j in range(dim))
normals=[(-d[1],d[0]) for d in old.dirs]
theta=tuple(F(dot(n,c)) for n,c in zip(normals,old.vertices))+tuple(map(F,old.s+old.t))
sform=(unit(W),unit(W+1));tform=(unit(W+2),unit(W+3))
cornerforms=[]
for c in range(W):
    p=(c-1)%W;a=normals[p];b=normals[c];det=cross(a,b);assert det
    cornerforms.append((scale(1/F(det),add(scale(b[1],unit(p)),scale(-a[1],unit(c)))),
                        scale(1/F(det),add(scale(-b[0],unit(p)),scale(a[0],unit(c))))))
assert all(evaluate(p)==tuple(map(F,c)) for p,c in zip(cornerforms,old.vertices))
reflect=[]
for j,n in enumerate(normals):
    nn=dot(n,n)
    R=tuple(tuple(F(int(a==b))-F(2*n[a]*n[b],nn) for b in (0,1)) for a in (0,1))
    b=tuple(scale(F(2*n[a],nn),unit(j)) for a in (0,1))
    reflect.append((R,b))
# Pullback of offsets and marks to the prior edge-length/closure chart.
K=[add(scale(n[0],p[0]),scale(n[1],p[1])) for n,p in zip(normals,old.vforms)]+list(old.sform)+list(old.tform)
pullback=lambda g:tuple(sum(g[j]*K[j][k] for j in range(dim)) for k in range(old.dim))
records=[]
for index,e in enumerate(events):
    w=tuple(e['dir']);side=e['side'];corner=old.vertices.index(tuple(e['corner']))
    replay=old.event(w,side,maxhits=2000)
    assert replay['status']=='EVENT',(index,replay)
    assert replay['corner']==tuple(e['corner'])
    assert tuple(map(F,replay['unfolded_target_minus_s']))==tuple(2*v for v in w)
    word=replay['word'];O=ID;shift=(zero,zero);states=[(O,shift)];translations=[]
    for wall in word:
        R,b=reflect[wall];translations.append(mf(O,b))
        shift=tuple(add(x,y) for x,y in zip(shift,translations[-1]));O=matmul(O,R);states.append((O,shift))
    target=pf(O,shift,tform)
    matches=[r for r,(Or,br) in enumerate(states) if evaluate(pf(Or,br,cornerforms[corner]))==tuple(old.s[k]+w[k] for k in (0,1))]
    assert matches,(index,word)
    r=replay['corner_prefix_hits'];assert r in matches
    Or,br=states[r];C=pf(Or,br,cornerforms[corner])
    assert all(old.project(pullback(C[k]))==old.project(tuple(map(F,replay['corner_image_forms'][k]))) for k in (0,1))
    equivalent=[k for k in matches if pf(states[k][0],states[k][1],cornerforms[corner])==C]
    E=tuple(add(add(scale(2,C[k]),scale(-1,target[k])),scale(-1,sform[k])) for k in (0,1))
    assert evaluate(E)==(0,0)
    local=tuple(add(add(scale(2,mf(Or,cornerforms[corner])[k]),scale(-1,mf(O,tform)[k])),scale(-1,sform[k])) for k in (0,1))
    walls=(zero,zero);counts=[F(0)]*W
    for j,(wall,tj) in enumerate(zip(word,translations)):
        eps=1 if j<r else -1
        walls=tuple(add(walls[k],scale(eps,tj[k])) for k in (0,1))
        Oj=states[j][0];n=normals[wall];nn=dot(n,n)
        coeff=side*F(2*eps,nn)*cross(w,mv(Oj,n))
        v=mv(tuple(zip(*Oj)),w);det=cross(Oj[0],Oj[1])
        assert coeff==side*F(2*eps,nn)*det*dot(v,old.dirs[wall])
        counts[wall]+=coeff
    assert tuple(add(local[k],walls[k]) for k in (0,1))==E
    full=scale(side,formcross(w,E));glocal=scale(side,formcross(w,local));gwalls=scale(side,formcross(w,walls))
    assert tuple(counts)+tuple(F(0) for _ in range(4))==gwalls
    expected=tuple(map(F,replay['gradient']))
    assert old.project(pullback(full))==old.project(expected),(index,'chart pullback')
    saved=tuple(map(F,stored['funcs'][index]));assert m.canon(old.project(saved))==m.canon(old.project(expected)),(index,'saved row')
    # Actual chart symmetries: two translations and uniform scale.
    for axis in (0,1):
        trans=tuple(F(n[axis]) for n in normals)+tuple(F(j%2==axis) for j in range(4))
        assert dot(full,trans)==0
    assert dot(full,theta)==0
    records.append({'index':index,'direction':w,'side':side,'corner':e['corner'],'word':word,
                    'prefix_hits':r,'all_hits':len(word),'equivalent_split_positions':equivalent,'base_coincident_split_positions':matches,
                    'offset_gradient':list(map(str,full)),
                    'corner_image_forms':[[str(x) for x in row] for row in C],
                    'target_image_forms':[[str(x) for x in row] for row in target],
                    'local_corner_and_marks_gradient':list(map(str,glocal)),
                    'first_minus_second_wall_gradient':list(map(str,gwalls))})
out={'status':'PASS','tag':room['tag'],'walls':W,'offset_dimension':dim,'length_chart_dimension':old.dim,
     'events_checked':len(records),'scope':'Exact new wall-stress identity and chart pullback on fixed saved events; no positive-span theorem or optical discovery.',
     'room':room,'offset_normals':normals,'offset_base_point':list(map(str,theta)),
     'events':records,'input_hashes':{str(p.relative_to(I)):hashlib.sha256(p.read_bytes()).hexdigest() for p in I.rglob('*') if p.is_file() and '__pycache__' not in p.parts}}
(ROOT/'coupling.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('events','room','offset_base_point','input_hashes','offset_normals')},indent=2))
