"""Exact local pocket-map algebra and TWO frozen event-word developments; no search."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import sys
import subprocess

if not __debug__:
    raise SystemExit('Optimized Python disables proof assertions; rerun without -O.')
B = Path(__file__).resolve().parent
SHEAR_PIN = 'b500e3b59ba262a81655d60441f31d6c7da74e022d308761f171cc7459f81e27'
PIN = '9f81b7bf93b258958fa3d6347631e50f8165e57ad32166547431a3be9ed26bec'
assert hashlib.sha256((B/'coupling.json').read_bytes()).hexdigest() == PIN
I = ((F(1), F(0)), (F(0), F(1)))
O = (F(0), F(0))
u = (F(0), F(-1))

def ap(A, v):
    return tuple(sum(A[i][j]*v[j] for j in range(2)) for i in range(2))

def mm(A, C):
    return tuple(tuple(sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)) for i in range(2))

def add(a, b): return tuple(x+y for x,y in zip(a,b))
def sub(a, b): return tuple(x-y for x,y in zip(a,b))
def times(k, a): return tuple(k*x for x in a)
def det(a, b): return a[0]*b[1]-a[1]*b[0]

def reflection(n, h, dh):
    n = tuple(map(F, n)); den = sum(x*x for x in n)
    R = tuple(tuple(I[i][j]-2*n[i]*n[j]/den for j in range(2)) for i in range(2))
    return R, times(2*h/den, n), times(2*dh/den, n)

def develop(mirrors):
    L, b, db = I, O, O
    for R, q, dq in mirrors:
        b = add(b, ap(L,q)); db = add(db, ap(L,dq)); L = mm(L,R)
    return L,b,db

D = reflection((-1,1), F(0), F(-1))
H = reflection((0,1), F(1), F(-1))
assert D[2] == (1,-1) and H[2] == (0,-2)
# At e=1/2 these prescribed slopes lie in the six derived open exit intervals.
fixtures = [('D',F(-2),'bottom-left'),('DH',F(-3,8),'bottom-right'),
            ('DHD',F(0),'right-lower'),('DHDH',F(2,5),'right-upper'),
            ('HDH',F(6,5),'top-right'),('HD',F(2),'top-left')]
expected = [(1,-1),(-1,-1),(0,0),(0,-2),(-1,-1),(1,-1)]
local=[]
for (word, m, side), want in zip(fixtures, expected):
    R,b,db = develop([{'D':D,'H':H}[c] for c in word])
    assert db == sub(u,ap(R,u)) == want
    assert tuple(int(x)%2 for x in db) == (word.count('D')%2,)*2
    e=F(1,2)
    assert m != 1-e
    if side.startswith('bottom'):
        x,y=-e/m,F(0)
        assert m < -e/2 and 0 < x < 2
        assert (x < 1) == (side=='bottom-left')
    elif side.startswith('top'):
        x,y=(2-e)/m,F(2)
        assert m > (2-e)/2 and 0 < x < 2
        assert (x < 1) == (side=='top-left')
    else:
        x,y=F(2),e+2*m
        assert -e/2 < m < (2-e)/2 and 0 < y < 2
        assert (y < 1) == (side=='right-lower')
    Rt=tuple(zip(*R))
    portal = ap(Rt,sub((x,y),b))
    assert portal[0] == 0 and 0 < portal[1] < 1
    local.append(dict(map=word,side=side,slope=m,exit=(x,y),derivative=db,
                      diagonal_count=word.count('D'),portal_image_check=True))
assert sum(x['derivative']==O for x in local)==1

saved=json.loads((B/'coupling.json').read_text())
V=[tuple(map(F,p)) for p in saved['room']['vertices']]
S,T=[tuple(map(F,p)) for p in saved['room']['marked']]
W=len(V); normals=saved['offset_normals']; base=list(map(F,saved['offset_base_point']))
assert V[2:5]==[(1,1),(2,2),(1,2)]
assert V[1][0]==V[2][0]==V[4][0]==V[5][0]==1
assert V[1][1]<V[2][1] and V[5][1]>V[4][1]
assert all(tuple(n) in ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)) for n in normals)
for i,n in enumerate(normals):
    assert sum(F(a)*v for a,v in zip(n,V[i]))==base[i]
    assert sum(F(a)*v for a,v in zip(n,V[(i+1)%W]))==base[i]
assert all(not (1<=x<=2 and x<=y<=2) for x,y in (S,T))
delta=[F(0)]*len(base);delta[2]=F(-1);delta[3]=F(1)
mirrors=[reflection(normals[i],base[i],delta[i]) for i in range(W)]
assert mirrors[2][2]==(1,-1) and mirrors[3][2]==(0,-2)
assert all(mirrors[i][2]==O for i in range(W) if i not in (2,3))

# Check the stronger raw-grid premise in this one frozen polygon, not new rooms.
def on_wall(z,a,c):
    return det(sub(z,a),sub(c,a))==0 and all(min(a[i],c[i])<=z[i]<=max(a[i],c[i]) for i in range(2))
def interior(z):
    x,y=z; answer=False
    for a,c in zip(V,V[1:]+V[:1]):
        if (a[1]>y)!=(c[1]>y) and x<a[0]+(y-a[1])*(c[0]-a[0])/(c[1]-a[1]):
            answer=not answer
    return answer
for x in range(int(min(v[0] for v in V)),int(max(v[0] for v in V))+1):
    for y in range(int(min(v[1] for v in V)),int(max(v[1] for v in V))+1):
        z=(F(x),F(y))
        if z in V or x%2==y%2==0: continue
        assert not interior(z) and not any(on_wall(z,a,c) for a,c in zip(V,V[1:]+V[:1]))

def form_value(forms, point):
    return tuple(sum(F(x)*y for x,y in zip(row,point)) for row in forms)

records=[]
for idx,want in [(0,O),(1,(F(-1),F(-1)))]:
    e=saved['events'][idx]; assert e['index']==idx
    assert tuple(map(F,e['corner'])) in V
    word=e['word']; p=e['prefix_hits']; c=tuple(map(F,e['corner']))
    vc=u if c in (V[2],V[3],V[4]) else O
    L,b,db=develop([mirrors[i] for i in word[:p]])
    C_image=add(ap(L,c),b); C_prime=add(ap(L,vc),db)
    A,q,dq=develop([mirrors[i] for i in word])
    T_image=add(ap(A,T),q); T_prime=dq
    assert C_image==form_value(e['corner_image_forms'],base)
    assert T_image==form_value(e['target_image_forms'],base)
    assert C_prime==form_value(e['corner_image_forms'],delta)
    assert T_prime==form_value(e['target_image_forms'],delta)
    w=sub(C_image,S)
    assert sub(T_image,C_image)==w and tuple(w)==tuple(e['direction'])
    defect=sub(T_prime,times(2,C_prime))
    # Independently sum signed wall loads, retaining the corner's physical velocity.
    signed=O; linear=I; loads=[]
    for j,i in enumerate(word):
        load=ap(linear,mirrors[i][2])
        signed=add(signed,times(-1 if j<p else 1,load))
        if i in (2,3): loads.append(dict(position=j,wall=i,before_corner=j<p,transported=load))
        linear=mm(linear,mirrors[i][0])
    signed=sub(signed,times(2,ap(L,vc)))
    assert signed==defect==want
    odd=sum(i==2 for i in word)%2
    assert all(x.denominator==1 for x in defect)
    assert tuple(int(x)%2 for x in defect)==(odd,odd)
    opening=-e['side']*det(w,defect)
    assert opening==sum(F(a)*b for a,b in zip(e['offset_gradient'],delta))
    records.append(dict(index=idx,physical_source=S,physical_target=T,physical_corner=c,
                        prefix_hits=p,half_displacement=w,pocket_wall_loads=loads,
                        defect=defect,diagonal_hit_parity=odd,signed_opening=opening,
                        actual_saved_endpoint_forms_match=True))
assert records[1]['signed_opening']==-17
assert records[1]['diagonal_hit_parity']==1
assert records[0]['pocket_wall_loads']==[]
assert len(records[1]['pocket_wall_loads'])==2
assert records[1]['pocket_wall_loads'][1]['position']==records[1]['pocket_wall_loads'][0]['position']+1
assert all(q['before_corner'] for q in records[1]['pocket_wall_loads'])
assert [q['wall'] for q in records[1]['pocket_wall_loads']]==[3,2]

# One explicitly prescribed shear image: determinant algebra, not optical tracing.
assert hashlib.sha256((B/'twist-action.json').read_bytes()).hexdigest()==SHEAR_PIN
a=F(json.loads((B/'twist-action.json').read_text())['summary']['horizontal_shear'])
assert a==48
base_event=records[1]; w=base_event['half_displacement']; defect=base_event['defect']
shear_w=(w[0]+a*w[1],w[1]); shear_row=-saved['events'][1]['side']*det(shear_w,defect)
assert shear_w==(228,5) and shear_row==223
assert shear_w[0]!=0 and shear_w[1]!=0 and abs(shear_w[0])!=abs(shear_w[1])

# Mod-2 transport argument: every D4 signed permutation preserves (1,1) mod 2.
D4=[]
for swap in [False,True]:
    for a in [-1,1]:
        for b in [-1,1]:
            R=((F(0),F(a)),(F(b),F(0))) if swap else ((F(a),F(0)),(F(0),F(b)))
            assert tuple(int(x)%2 for x in ap(R,D[2]))==(1,1)
            assert tuple(int(x)%2 for x in ap(R,H[2]))==(0,0)
            assert tuple(int(x)%2 for x in times(2,ap(R,u)))==(0,0)
            D4.append(R)

def clean(x):
    if isinstance(x,F): return x.numerator if x.denominator==1 else str(x)
    if isinstance(x,(tuple,list)): return [clean(a) for a in x]
    if isinstance(x,dict): return {k:clean(v) for k,v in x.items()}
    return x
# Prescribed copy-colour identities, not billiard path discovery.
Vlin=((-F(1),F(0)),(F(0),F(1)))
Hlin=H[0]; Dlin=D[0]
def colour(R): return int(R[0][0]==0)
for R in D4:
    assert colour(mm(R,Hlin))==colour(R)
    assert colour(mm(R,Vlin))==colour(R)
    assert colour(mm(R,Dlin))==1-colour(R)
assert mm(Dlin,Dlin)==I
opposite=tuple(tuple(-x for x in row) for row in Dlin)
assert mm(mm(mm(Dlin,opposite),Hlin),Vlin)==I
for seam_product in (mm(Vlin,Dlin),mm(Dlin,Hlin)):
    power=I
    for n in range(1,5):
        power=mm(power,seam_product)
        assert (power==I)==(n==4)
# Each endpoint's eight-copy cyclic seam word therefore contains four D factors.
assert ('VD'*4).count('D')==('DH'*4).count('D')==4
negative=subprocess.run([sys.executable,'-B','-O',str(Path(__file__).resolve())],capture_output=True,text=True)
assert negative.returncode!=0 and 'Optimized Python disables proof assertions' in negative.stderr
out=clean(dict(status='PASS',input_sha256=PIN,twist_action_sha256=SHEAR_PIN,optimized_mode_rejection=True,raw_grid_premise_checked=True,local_return_maps=local,
               D4_transport_controls=len(D4),copy_colour_controls=8,prescribed_odd_copy_loops=2,seam_degrees=[4,4],saved_events=records,prescribed_shear_image=dict(shear=a,half_displacement=shear_w,signed_opening=shear_row,scope='Determinant algebra; admissibility from earlier affine-event theorem, no new tracing.'),
               scope='Local exact mirror algebra and two frozen labeled developments only. No discovery or optical tracing; universal event existence remains open.'))
(B/'pocket-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
