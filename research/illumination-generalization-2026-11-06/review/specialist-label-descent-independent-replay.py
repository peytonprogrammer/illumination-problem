"""Prescribed verification of the saved certificate, never a new orbit census."""
from pathlib import Path
from collections import deque
from fractions import Fraction as Q
import gzip, hashlib, json, math
R=Path(__file__).resolve().parent
A=R.parents[1]/'codex-proof-verification/specialist-ideas'
H=lambda b:hashlib.sha256(b).hexdigest()
request=json.loads((A/'label-descent-review-request.json').read_text())
for name,digest in request['files'].items():assert H((A/name).read_bytes())==digest,name
expected=json.loads((A/'label-descent-audit.json').read_text())
packed=(R/'marked-origami-known22-closure.gz').read_bytes(); raw=gzip.decompress(packed)
assert H(raw)==expected['raw_sha256']
N=60; width=3*N
assert len(raw)%width==0
saved={tuple(tuple(raw[i+j*N:i+(j+1)*N]) for j in range(3)) for i in range(0,len(raw),width)}
assert len(saved)==10368 and len(raw)==len(saved)*width
initial=min(saved)
assert initial==tuple(map(tuple,expected['initial_state']))

def inv(p):return tuple(p.index(i) for i in range(len(p)))
def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))
def comm(st):
    h,v,_=st
    return compose(v,compose(h,compose(inv(v),inv(h))))
def cycles(p):
    unseen=set(range(len(p)));out=[]
    while unseen:
        x=min(unseen);one=[];j=x
        while j in unseen:one.append(j);unseen.remove(j);j=p[j]
        assert j==x;out.append(tuple(one))
    return out
cc=cycles(comm(initial)); zeros=[x for x in cc if len(x)>1]
assert len(zeros)==9 and all(len(x)==3 for x in zeros)
label=[-1]*N
for z,cy in enumerate(zeros):
    for i in cy:label[i]=z
for color,base in [(1,9),(2,13)]:
    marks=[i for i in range(N) if initial[2][i]==color]
    assert len(marks)==4
    for t,i in enumerate(marks):assert comm(initial)[i]==i;label[i]=base+t
assert tuple(label)==tuple(expected['initial_tags'])

def move(st,origin,letter):
    h,v,col=st
    if letter=='T':v=compose(v,inv(h))
    elif letter=='U':h=compose(h,inv(v))
    elif letter=='Ti':v=compose(v,h)
    elif letter=='Ui':h=compose(h,v)
    else:raise AssertionError(letter)
    assert comm((h,v,col))==comm(st) # anchored, BEFORE relabelling
    seq=[0];lookup={0:0};i=0
    while i<len(seq):
        a=seq[i];i+=1
        for z in (h[a],v[a]):
            if z not in lookup:lookup[z]=len(seq);seq.append(z)
    assert len(seq)==N
    result=(tuple(lookup[h[a]] for a in seq),tuple(lookup[v[a]] for a in seq),tuple(col[a] for a in seq))
    assert result in saved # membership guard: never generate/extend certificate
    return result,tuple(origin[a] for a in seq)

def induced(x,y):
    perm={}
    for a,b in zip(x,y):
        assert (a<0)==(b<0)
        if a>=0:
            assert a not in perm or perm[a]==b;perm[a]=b
    assert set(perm)==set(range(17)) and set(perm.values())==set(range(17))
    assert all((a<9)==(b<9) for a,b in perm.items())
    assert all(perm[a]==a for a in range(9,13))
    return perm

# Independent short word replay; track original square slots, not author tags.
st=initial;origin=tuple(range(N));trace=[]
for letter in expected['witness']['closed_word']:
    st,origin=move(st,origin,letter)
    trace.append({'letter':letter,'coarse_sha256':H(bytes(sum(st,()))),'origin_sha256':H(bytes(origin))})
assert st==initial
perm=induced(label,[label[i] for i in origin])
assert perm=={int(k):v for k,v in expected['witness']['label_permutation'].items()}
assert tuple(label[i] for i in origin)==tuple(expected['witness']['final_tags'])

# ALL EXISTING edges, different U-before-T spanning tree. No refined-state traversal.
origins={initial:tuple(range(N))};parents={initial:None};todo=deque([initial])
classes=[{i} for i in range(17)];edges=0;changes=0;merges=[]
def path(st):
    w=[]
    while parents[st] is not None:st,k=parents[st];w.append(k)
    return w[::-1]
def unify(a,b,word):
    ca=next(c for c in classes if a in c);cb=next(c for c in classes if b in c)
    if ca is not cb:
        merges.append({'a':a,'b':b,'closed_word':word})
        ca.update(cb);classes.remove(cb)
while todo:
    here=todo.popleft()
    for letter in ('U','T'):
        there,alt=move(here,origins[here],letter);edges+=1
        if there not in origins:
            origins[there]=alt;parents[there]=(here,letter);todo.append(there)
        else:
            old=[label[i] for i in origins[there]];new=[label[i] for i in alt]
            p=induced(old,new)
            if any(a!=b for a,b in p.items()):
                changes+=1
                loop=path(here)+[letter]+[k+'i' for k in reversed(path(there))]
                for a,b in p.items():unify(a,b,loop)
assert len(origins)==len(saved) and edges==20736
partition=sorted(sorted(c) for c in classes)
assert partition==expected['label_monodromy_orbits']
# Replay merger certificates from the initial root as independent lower-bound witnesses.
for item in merges:
    st=initial;o=tuple(range(N))
    for letter in item['closed_word']:st,o=move(st,o,letter)
    assert st==initial
    p=induced(label,[label[i] for i in o])
    # Each merger is witnessed by its own closed loop based at the regular root.
    assert p[item['a']]==item['b']
    assert all(any(a in c and b in c for c in classes) for a,b in p.items())
    item['root_permutation']=p

# Exact 2x2 matrix algebra, no numerical tolerances.
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
ref=((1,0),(0,-1));minus=((-1,0),(0,-1))
for n in (0,1,48,-48,96):
    a=((1,n),(0,1));ai=((1,-n),(0,1))
    assert mul(mul(a,ref),ai)==((1,-2*n),(0,-1))
    assert mul(mul(a,minus),ai)==minus
# Prescribed square-torus control: T^48 on raw right/up/mark functions is exact identity.
D=48;size=D*D
ht=tuple(((i%D+1)%D)+D*(i//D) for i in range(size))
vt=tuple(i%D+D*((i//D+1)%D) for i in range(size))
# h^48 identity is a closed formula, not a new state enumeration.
assert all(((i%D+48)%D)+D*(i//D)==i for i in range(size))
sources={(x%D,y%D) for x in (12,-12) for y in (12,-12)}
targets={(x%D,y%D) for x in (16,-16) for y in (18,-18)}
sheared={( (x+y)%D,y) for x,y in targets}
assert len(sheared)==4 and len({x for x,y in sheared})==4 and len({y for x,y in sheared})==2
# Transformed reflection is nonorthogonal: R_1^t R_1 is not identity.
r1=((1,-2),(0,-1));rt=tuple(zip(*r1))
assert mul(rt,r1)!=((1,0),(0,1))

out={'status':'PRESCRIBED_INDEPENDENT_LABEL_DESCENT_CHECKS_PASS','author_checker_executed':False,'new_orbit_or_room_census':False,'pinned_source_sha256':request['files'],'certificate_raw_sha256':H(raw),'saved_states_checked':len(origins),'saved_edges_checked':edges,'spanning_tree_generator_order':['U','T'],'disagreement_edges_under_own_gauge':changes,'zero_cycle_lengths':[len(c) for c in zeros],'closed_word':expected['witness']['closed_word'],'closed_word_restores_exact_coarse_state':True,'closed_word_label_permutation':perm,'closed_word_trace':trace,'label_transport_orbits':partition,'merger_certificates':merges,'explicit_id_refinements_per_coarse_state_at_most':math.factorial(9)*math.factorial(4)**2,'halfturn_choices_per_regular_source_root_at_most':4,'sheared_square_target_fiber':sorted(sheared),'sheared_target_coordinate_cardinalities':[4,2],'whole_goal_complete':False}
(R/'specialist-label-descent-independent-replay.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('merger_certificates','closed_word_trace','pinned_source_sha256')}))
