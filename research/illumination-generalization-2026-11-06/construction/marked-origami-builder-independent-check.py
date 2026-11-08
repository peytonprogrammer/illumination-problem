"""Read-only independent validation of the prescribed R34 stored certificate.
No orbit generation, discovery directions, or peer-output writes.
"""
from pathlib import Path
from fractions import Fraction as F
import gzip,hashlib,json,sys,importlib.util,re,time
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
PEER=ROOT.parent/'review'
started=time.monotonic()
def deadline():
    if time.monotonic()-started>120:raise TimeoutError('prescribed certificate review timeout')
def inverse(p):
    return tuple(sorted(range(len(p)),key=p.__getitem__))
def rooted(h,v,labels,start=0):
    queue=[start];index={start:0}
    for i in queue:
        for j in (h[i],v[i]):
            if j not in index:index[j]=len(queue);queue.append(j)
    return bytes(index[h[i]] for i in queue),bytes(index[v[i]] for i in queue),bytes(labels[i] for i in queue)
def step(state,which):
    h,v,labels=state
    if which==0:
        back=inverse(h);v=tuple(v[back[i]] for i in range(len(h)))
    else:
        back=inverse(v);h=tuple(h[back[i]] for i in range(len(h)))
    return rooted(h,v,labels)
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
req=json.loads((PEER/'marked-origami-decision-review-request.json').read_text())
pins={}
for relative,expected in req['source_sha256'].items():
    actual=hashlib.sha256((PEER/relative).read_bytes()).hexdigest();assert actual==expected,relative;pins[relative]=actual
spec=importlib.util.spec_from_file_location('frozen_readonly',PEER/'../../illumination-k4-codex/origami-decider-review/inputs/origami_dark.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
text=(PEER/'../../illumination-k4-codex/preprint-review-codex/revised.tex').read_text().split(r'\label{eq:vertices}',1)[1].split(r'\end{equation}',1)[0]
V=[tuple(map(int,p)) for p in re.findall(r'\((-?\d+),\s*(-?\d+)\)',text)];assert len(V)==22
h,v,lab,root=old.build(V,(0,0),(2,2));codes={'.':0,'S':1,'T':2,'block':3};initial=rooted(h,v,[codes[x] for x in lab],root)
N=len(initial[0]);assert N==60
raw=gzip.decompress((PEER/'marked-origami-known22-closure.gz').read_bytes())
assert hashlib.sha256(raw).hexdigest()=='2f5540623e3d0a7c08b2d1bbe4487d607e9024cef82263de175c30bec7b7a346'
assert len(raw)%(3*N)==0
states=set()
for offset in range(0,len(raw),3*N):
    states.add(tuple(raw[offset+i*N:offset+(i+1)*N] for i in range(3)))
assert len(states)==len(raw)//(3*N)==10368 and initial in states
transitions=horizontal=vertex_labels=0
for state in states:
    deadline();h,v,labels=state;assert set(h)==set(v)==set(range(N)) and labels[0]==1 and 2 in labels
    assert rooted(h,v,labels)==state
    hi,vi=inverse(h),inverse(v)
    for i in range(N):
        k=v[h[vi[hi[i]]]]
        assert labels[i]==labels[k]
        if labels[i] in (1,2):assert k==i
        vertex_labels+=1
    at=h[0];visited={0}
    while at not in visited:
        if labels[at]==3:break
        assert labels[at]!=2
        visited.add(at);at=h[at]
    horizontal+=1
    for which in (0,1):assert step(state,which) in states;transitions+=1
# Independent exact physical path supplied by the peer; no optical helper import.
P=[(0,0),(4,0),(4,2),(2,2),(2,4),(0,4)]
path=[tuple(map(F,p)) for p in [(1,3),(0,F(7,2)),(1,4),(2,F(7,2)),(0,F(5,2)),(3,1)]]
edges=list(zip(P,P[1:]+P[:1]));wall_hits=[];guards=0
for leg,(a,b) in enumerate(zip(path,path[1:])):
    direction=sub(b,a);hits=[]
    for k,(x,y) in enumerate(edges):
        guards+=1;edge=sub(y,x);den=det(direction,edge)
        if not den:
            assert det(sub(x,a),direction)!=0,'unexpected wall collinearity';continue
        t=F(det(sub(x,a),edge),den);s=F(det(sub(x,a),direction),den)
        assert not(0<t<1 and 0<=s<=1),'earlier physical boundary hit'
        if t==1 and 0<=s<=1:hits.append((k,s))
    if leg<len(path)-2:
        assert len(hits)==1 and 0<hits[0][1]<1;wall_hits.append(hits[0][0])
    else:assert not hits
for j,wall in enumerate(wall_hits,1):
    incoming=sub(path[j],path[j-1]);outgoing=sub(path[j+1],path[j]);edge=sub(edges[wall][1],edges[wall][0]);normal=(-edge[1],edge[0])
    reflected=tuple(incoming[k]-2*F(dot(incoming,normal),dot(normal,normal))*normal[k] for k in (0,1))
    assert det(reflected,outgoing)==0 and dot(reflected,outgoing)>0
out={'status':'INDEPENDENT_STORED_CLOSURE_AND_ACTUAL_PATH_PASS','source_pins':pins,'source_component_squares':N,'stored_states':len(states),'closure_transitions':transitions,'horizontal_no_target_checks':horizontal,'vertex_label_checks':vertex_labels,'actual_L_reflections':len(wall_hits),'actual_L_wall_leg_guards':guards,'discovery':False,'limitations':'Initial geometric builder imported from frozen accepted code; full R34 affine builder inspected by hand, not independently rerun. No new room/orbit generated.','elapsed_seconds':time.monotonic()-started}
(ROOT/'marked-origami-builder-independent-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='source_pins'}))
