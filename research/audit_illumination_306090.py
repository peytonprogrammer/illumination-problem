"""Independent angular-slot checks for the 30–60–90 model."""
import itertools,json,math
from fractions import Fraction as F
from pathlib import Path
from illumination_306090 import patch,check,sub,dot,add,sectors
from illumination_geometry import owners_of,save
DIRS=[(1,0),(3,1),(1,1),(0,1),(-1,1),(-3,1),(-1,0),(-3,-1),(-1,-1),(0,-1),(1,-1),(3,-1)]
def ray(p,q):
    a,b=sub(q,p);g=math.gcd(abs(a),abs(b));return DIRS.index((a//g,b//g))
def angular(ts,p,opens):
    occupied=set();transitions=set()
    for t in ts:
        if p not in t:continue
        a,b=[ray(p,q) for q in t if q!=p]
        if (b-a)%12>6:a,b=b,a
        slots=[(a+k)%12 for k in range((b-a)%12)];occupied.update(slots);transitions.update((s+1)%12 for s in slots[:-1])
    for e in opens:
        if p in e:transitions.add(ray(p,next(q for q in e if q!=p)))
    if len(occupied)==len(transitions)==12:return [],True
    seen=set();sizes=[]
    for j in occupied:
        if j in seen:continue
        seen.add(j);todo=[j];size=0
        while todo:
            s=todo.pop();size+=1
            for q,r in [((s+1)%12,(s+1)%12),((s-1)%12,s)]:
                if r in transitions and q in occupied and q not in seen:seen.add(q);todo.append(q)
        sizes.append(size)
    return sorted(sizes),False

def main():
    ts,labels=patch(2);owners=owners_of(ts);shared={e:o for e,o in owners.items() if len(o)==2};reflections=0
    for e,(a,b) in shared.items():
        p,q=e;u=next(v for v in ts[a] if v not in e);v=next(v for v in ts[b] if v not in e);d=sub(q,p);w=sub(u,p)
        assert add(p,tuple(2*F(dot(w,d),dot(d,d))*d[k]-w[k] for k in (0,1)))==v
        assert labels[u]==labels[v];reflections+=1
    cases=0
    # One full star per label, every subset, with zero/one closed eligible edge.
    for kind,degree in [('A',12),('B',6),('C',4)]:
        p=next(p for p in sorted(labels) if labels[p]==kind and sum(p in t for t in ts)==degree)
        ids=[i for i,t in enumerate(ts) if p in t];es=[e for e in shared if p in e]
        for mask in range(1<<degree):
            chosen={i for j,i in enumerate(ids) if (mask>>j)&1};local=[ts[i] for i in chosen];lo=owners_of(local);eligible=[e for e in es if set(shared[e])<=chosen]
            for closed in [None]+eligible:
                opens=set(eligible)-({closed} if closed else set());assert sectors(local,p,opens,lo,labels)==angular(local,p,opens);cases+=1
    results={}
    for f in sorted(Path(__file__).parent.glob('306090-*.json')):
        data=json.loads(f.read_text())
        if 'triangles' not in data:continue
        r=check(data)
        local=[tuple(map(tuple,t)) for t in data['triangles']];lo=owners_of(local);cuts={tuple(sorted(map(tuple,e))) for e in data['slits']};opens={e for e,o in lo.items() if len(o)==2 and e not in cuts};turns=0
        for p in {p for t in local for p in t}:
            sizes,full=angular(local,p,opens);assert (labels[p]=='A' or not full and 6 not in sizes);turns+=sum(s!=6 for s in sizes)
        assert turns==r['walls'];results[f.name]=r
    result=dict(status='PASS',local_configurations=cases,shared_reflections=reflections,rooms=results);save(Path(__file__).parent/'306090-audit.json',result);print(json.dumps(result))
if __name__=='__main__':main()
