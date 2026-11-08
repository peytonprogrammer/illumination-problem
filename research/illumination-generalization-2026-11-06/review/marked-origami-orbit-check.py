"""Prescribed full negative closure certificate and physical positive witness."""
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as Q
from collections import deque
import importlib.util,json,hashlib,gzip,re
R=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('ownbuilder',R/'marked-origami-builder-check.py');build=importlib.util.module_from_spec(sp);sp.loader.exec_module(build)
def deadline():build.deadline()
def inverse(p):out=[0]*len(p);[(out.__setitem__(v,k)) for k,v in enumerate(p)];return out

def canonical(h,v,labels):
    order=[0];seen={0:0}
    for a in order:
        for b in(h[a],v[a]):
            if b not in seen:seen[b]=len(order);order.append(b)
    return bytes(seen[h[a]] for a in order),bytes(seen[v[a]] for a in order),bytes(labels[a] for a in order)
def transform(state,letter):
    h,v,labels=state
    if letter=='T':hi=inverse(h);return canonical(h,[v[hi[i]] for i in range(len(h))],labels)
    vi=inverse(v);return canonical([h[vi[i]] for i in range(len(h))],v,labels)
def horizontal(state):
    h,v,labels=state;a=h[0];steps=1
    while a:
        if labels[a]==3:return None
        if labels[a]==2:return steps
        a=h[a];steps+=1
    return None

def orbit(initial,cap=20000):
    queue=deque([initial]);seen={initial};parents={initial:None}
    while queue:
        deadline();state=queue.popleft();hit=horizontal(state)
        if hit:
            word=[];at=state
            while parents[at] is not None:
                at,letter=parents[at];word.append(letter)
            return {'status':'LIT','state_count':len(seen),'word':list(reversed(word)),'horizontal_length':hit},seen
        for letter in('T','U'):
            nxt=transform(state,letter)
            if nxt not in seen:
                seen.add(nxt);parents[nxt]=(state,letter);queue.append(nxt)
                if len(seen)>cap:return {'status':'UNDECIDED','reason':'state_cap','state_count':len(seen)},seen
    return {'status':'DARK_COMPLETE_ORBIT','state_count':len(seen)},seen

def encode(result):
    h,v,labels=result['permutations'];root=result['independent_root'];state=build.canonical(h,v,labels,root)
    codes={'.':0,'S':1,'T':2,'block':3};return tuple(bytes(z) for z in(state[0],state[1],tuple(codes[x] for x in state[2])))

def physical_trace(V,S,T,velocity,end_time):
    p=tuple(map(Q,S));target=tuple(map(Q,T));vel=tuple(map(Q,velocity));path=[p];elapsed=Q(0)
    while elapsed<end_time:
        deadline();events=[]
        for i,(a,b) in enumerate(build.geo.edges(V)):
            e=build.geo.vec(a,b);den=build.geo.det(vel,e)
            if not den:continue
            t=Q(build.geo.det(build.geo.vec(p,a),e),den);r=Q(build.geo.det(build.geo.vec(p,a),vel),den)
            if t>0 and 0<=r<=1:events.append((t,i,r))
        tmin=min(t for t,i,r in events)
        dt=Q(target[0]-p[0],vel[0]) if vel[0] else Q(target[1]-p[1],vel[1])
        if dt>0 and tuple(p[k]+dt*vel[k] for k in(0,1))==target and dt<tmin:
            path.append(target);elapsed+=dt;break
        assert elapsed+tmin<end_time
        hits=[(i,r) for t,i,r in events if t==tmin];assert len(hits)==1 and 0<hits[0][1]<1
        p=tuple(p[k]+tmin*vel[k] for k in(0,1));path.append(p);elapsed+=tmin
        a,b=build.geo.edges(V)[hits[0][0]];e=build.geo.vec(a,b);normal=(-e[1],e[0]);f=2*build.geo.dot(vel,normal)/build.geo.dot(normal,normal);vel=tuple(vel[k]-f*normal[k] for k in(0,1))
    assert path[-1]==target and elapsed<=end_time
    return {'path':path,'arrival_time':elapsed,**build.geo.path_check(V,path)}

def main():
    tex=R.parents[1]/'illumination-k4-codex/preprint-review-codex/revised.tex';text=tex.read_text().split(r'\label{eq:vertices}',1)[1].split(r'\end{equation}',1)[0];V=[tuple(map(int,m)) for m in re.findall(r'\((-?\d+),\s*(-?\d+)\)',text)];assert len(V)==22
    b=build.certify(V,(0,0),(2,2));initial=encode(b);negative,states=orbit(initial);assert negative['status']=='DARK_COMPLETE_ORBIT'
    N=len(initial[0]);ordered=sorted(states);raw=b''.join(h+v+lab for h,v,lab in ordered);payload=gzip.compress(raw,mtime=0);file=R/'marked-origami-known22-closure.gz';file.write_bytes(payload)
    # Fresh closure readback: no reliance on the traversal queue or visited set.
    read=gzip.decompress(file.read_bytes());assert len(read)%(3*N)==0;cert={tuple(read[k+i*N:k+(i+1)*N] for i in range(3)) for k in range(0,len(read),3*N)};assert len(cert)==negative['state_count'] and initial in cert
    hguards=transitions=0
    for state in cert:
        deadline();h,v,lab=state;assert sorted(h)==sorted(v)==list(range(N)) and lab[0]==1
        hi=inverse(h);vi=inverse(v);kap=[v[h[vi[hi[i]]]] for i in range(N)]
        assert all(lab[i]==lab[kap[i]] for i in range(N)) and all(kap[i]==i for i in range(N) if lab[i] in(1,2))
        assert horizontal(state) is None;hguards+=1
        for letter in('T','U'):assert transform(state,letter) in cert;transitions+=1
    LV=[(0,0),(4,0),(4,2),(2,2),(2,4),(0,4)];S=(1,3);T=(3,1);bb=build.certify(LV,S,T);positive,_=orbit(encode(bb));assert positive['status']=='LIT'
    A=((1,0),(0,1));generators={'T':((1,1),(0,1)),'U':((1,0),(1,1))}
    for letter in positive['word']:A=build.mul(generators[letter],A)
    chart_direction=(A[1][1],-A[1][0]);g=bb['source_root_matrix'];physical=(g[0][0]*chart_direction[0]+g[1][0]*chart_direction[1],g[0][1]*chart_direction[0]+g[1][1]*chart_direction[1])
    witness=physical_trace(LV,S,T,physical,Q(positive['horizontal_length']))
    out={'status':'PRESCRIBED_DARK_CLOSURE_AND_PHYSICAL_LIT_WITNESS_PASS','known22':{**negative,'source_component_squares':N,'closed_transition_checks':transitions,'horizontal_no_target_checks':hguards,'certificate_file':file.name,'certificate_gzip_sha256':hashlib.sha256(payload).hexdigest(),'certificate_raw_sha256':hashlib.sha256(raw).hexdigest()},'L_positive':{**positive,'linear_matrix':A,'chart_direction':chart_direction,'physical_direction':physical,'physical_witness':witness},'whole_goal_complete':False,'discovery':False,'limits':'Prescribed known22 negative control and L positive control only; no new dark candidate, W-uniform bound or full-prefix completion.','source_sha256':{'marked-origami-builder-check.py':hashlib.sha256((R/'marked-origami-builder-check.py').read_bytes()).hexdigest(),'../../illumination-k4-codex/preprint-review-codex/revised.tex':hashlib.sha256(tex.read_bytes()).hexdigest()}}
    (R/'marked-origami-orbit-check.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({'status':out['status'],'known22':out['known22'],'L_positive':{k:v for k,v in out['L_positive'].items() if k!='physical_witness'},'L_reflections':witness['reflections']}))
if __name__=='__main__':main()
