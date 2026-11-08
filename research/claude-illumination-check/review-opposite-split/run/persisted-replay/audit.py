"""Independent exact replay of supplied paths and universal U/Z conditions.
No peer geometry imports, no direction/path search, no room enumeration.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
import hashlib, json, time

HERE=Path(__file__).resolve().parent
INPUT=HERE/'inputs'

def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def dot(a,b): return a[0]*b[0]+a[1]*b[1]
def triangles(raw): return frozenset(tuple(sorted(map(tuple,t))) for t in raw)

@lru_cache(maxsize=120000)
def cell(x,y):
    square=((x,y),(x+1,y),(x+1,y+1),(x,y+1))
    a=next(p for p in square if p[0]%2==p[1]%2==0)
    b=next(p for p in square if p[0]%2==p[1]%2==1)
    return tuple(tuple(sorted((a,b,c))) for c in square if c not in (a,b))

@lru_cache(maxsize=200000)
def incident(p):
    """All closed canonical triangles containing p, using exact half planes."""
    x,y=p; ix=x//1;iy=y//1; found=set()
    for i in (ix-1,ix):
        for j in (iy-1,iy):
            for t in cell(i,j):
                cs=[cross(sub(t[(k+1)%3],t[k]), sub(p,t[k])) for k in range(3)]
                if all(c>=0 for c in cs) or all(c<=0 for c in cs): found.add(t)
    assert found, ('no triangle',p)
    return frozenset(found)

@lru_cache(maxsize=100000)
def segment(a,b):
    assert a!=b, 'zero-length segment'
    delta=sub(b,a); cuts={F(0),F(1)}
    # These four line families contain every canonical triangle edge.
    for fa,fb,step in ((a[0],b[0],1),(a[1],b[1],1),
                       (a[0]-a[1],b[0]-b[1],2),(a[0]+a[1],b[0]+b[1],2)):
        if fa==fb:continue
        for n in range(int(min(fa,fb)//step)-1,int(max(fa,fb)//step)+2):
            t=(n*step-fa)/(fb-fa)
            if 0<t<1:cuts.add(t)
    cuts=sorted(cuts)
    point=lambda t:(a[0]+t*delta[0],a[1]+t*delta[1])
    need=set()
    for t in cuts[1:-1]:need.update(incident(point(t)))
    for lo,hi in zip(cuts,cuts[1:]):need.update(incident(point((lo+hi)/2)))
    return frozenset(need)

@lru_cache(maxsize=100000)
def bounce(prev,p,nxt):
    incoming=sub(p,prev); outgoing=sub(nxt,p)
    assert incoming!=(0,0) and outgoing!=(0,0)
    matches=[]
    for tangent in ((1,0),(0,1),(1,1),(1,-1)):
        norm=dot(tangent,tangent)
        reflected=tuple(2*dot(incoming,tangent)*tangent[k]-norm*incoming[k] for k in (0,1))
        if cross(reflected,outgoing)==0 and dot(reflected,outgoing)>0:
            if cross(tangent,sub(prev,p))!=0: matches.append(tangent)
    assert len(matches)==1, ('not specular',prev,p,nxt,matches)
    tangent=matches[0];sign=cross(tangent,sub(prev,p))
    assert sign*cross(tangent,sub(nxt,p))>0, 'crosses mirror'
    used=set();absent=set()
    for tri in incident(p):
        center=tuple(F(sum(v[k] for v in tri),3) for k in (0,1))
        side=cross(tangent,sub(center,p))
        assert side!=0, ('mirror splits tile centroid',p,tangent,tri)
        # Verify the proposed mirror does not cross a triangle interior.
        sides=[cross(tangent,sub(v,p)) for v in tri]
        assert all(s>=0 for s in sides) or all(s<=0 for s in sides), ('mirror splits tile',p,tangent,tri)
        (used if sign*side>0 else absent).add(tri)
    assert used and absent, ('mirror not at tiling edge',p)
    return frozenset(used),frozenset(absent)

def path_requirements(path):
    need=set();forbid=set()
    for a,b in zip(path,path[1:]):need.update(segment(a,b))
    for prev,p,nxt in zip(path,path[1:],path[2:]):
        u,z=bounce(prev,p,nxt);need.update(u);forbid.update(z)
    assert not need & forbid, 'path constraints contradictory'
    return need,forbid

def check_record(rec,q,learned):
    U=triangles(rec['U']);Z=triangles(rec['Z'])
    assert not U&Z, 'U/Z overlap'
    path=tuple(tuple(F(*c) for c in p) for p in rec['path'])
    assert len(path)>=2 and path[0]==(0,0) and path[-1]==q, 'wrong marks'
    stars=incident((F(0),F(0)))|incident(tuple(map(F,q)))
    assert all(len(incident(tuple(map(F,p))))==8 for p in ((0,0),q)), 'marks not A'
    need,forbid=path_requirements(path)
    vacuous=bool(Z&stars)
    # For non-vacuous guards, necessary constraints must all be forced.
    if not vacuous:
        assert need<=U|stars, ('missing used',sorted(need-(U|stars)))
        assert forbid<=Z, ('missing absent',sorted(forbid-Z))
    if learned:
        room=triangles(rec['room'])
        assert stars<=room and U<=room and not Z&room, 'room disagrees with guard'
        assert need<=room and not forbid&room, 'path invalid in physical room'
        assert not vacuous
    return dict(vacuous=vacuous, reflections=len(path)-2,
                vertex_bounces=sum(p[0].denominator==p[1].denominator==1 for p in path[1:-1]))

def guard_key(U,Z):return (triangles(U),triangles(Z))

def main():
    start=time.monotonic();result=dict(status='RUNNING', files=[],failures=[])
    manifest=json.loads((HERE/'manifest.json').read_text())
    for m in manifest:
        assert hashlib.sha256((INPUT/m['file']).read_bytes()).hexdigest()==m['sha256']
    print('manifest verified',len(manifest),flush=True)
    for p in sorted(INPUT.glob('certs-paths-*.json')):
        q=tuple(map(int,p.stem.removeprefix('certs-paths-').split('_')))
        recs=json.loads(p.read_text());cached=json.loads((INPUT/p.name.replace('certs-paths-','certs-')).read_text())
        assert Counter(guard_key(r['U'],r['Z']) for r in recs)==Counter(guard_key(u,z) for u,z in cached), ('cache/path mismatch',p.name)
        counters=Counter()
        for i,rec in enumerate(recs):
            try:
                out=check_record(rec,q,False);counters['checked']+=1;counters['vacuous']+=out['vacuous'];counters['vertex_bounces']+=out['vertex_bounces']
            except Exception as e:
                result['failures'].append(dict(file=p.name,record=i,error=repr(e)))
        result['files'].append(dict(file=p.name,kind='precomputed',q=q,**counters))
        print(p.name,dict(counters),'failures',len(result['failures']),flush=True)
    for p in sorted(INPUT.glob('claude-k4-w21-learned-*.jsonl')):
        q=tuple(map(int,p.stem.split('-L')[1].split(',')));counters=Counter()
        for i,line in enumerate(p.read_text().splitlines()):
            try:
                out=check_record(json.loads(line),q,True);counters['checked']+=1;counters['vertex_bounces']+=out['vertex_bounces']
            except Exception as e:result['failures'].append(dict(file=p.name,record=i,error=repr(e)))
            if (i+1)%1000==0:print(p.name,i+1,'failures',len(result['failures']),flush=True)
        stats=json.loads((INPUT/f'claude-k4-w21-stats-L{q[0]},{q[1]}.json').read_text())
        assert counters['checked']+sum(f['file']==p.name for f in result['failures'])==stats['stats']['learned']
        result['files'].append(dict(file=p.name,kind='learned',q=q,**counters))
        print(p.name,dict(counters),'failures',len(result['failures']),flush=True)
    result['status']='FAIL' if result['failures'] else 'PASS'
    result['seconds']=round(time.monotonic()-start,2)
    result['precomputed_checked']=sum(r.get('checked',0) for r in result['files'] if r['kind']=='precomputed')
    result['learned_checked']=sum(r.get('checked',0) for r in result['files'] if r['kind']=='learned')
    result['coverage']='Universal path implication and learned-room path validity only; no complete enumeration replay.'
    (HERE/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('files','failures')},indent=2),flush=True)
    if result['failures']: print('first failures',result['failures'][:5],flush=True)

if __name__=='__main__':main()
