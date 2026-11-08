"""Validate colored simultaneous-conjugacy keys and exact direction closure."""
import itertools,json,random
from collections import deque
from pathlib import Path
from illumination_code_quotient import canonical,conjugate
from illumination_cover import build,then,inverse,visibility,solve
from illumination_geometry import save


def brute(a,b,colors):
    n=len(colors);keys=[]
    for f in itertools.permutations(range(n)):
        c=[0]*n
        for i in range(n):c[f[i]]=colors[i]
        keys.append((tuple(c),conjugate(a,f),conjugate(b,f)))
    return min(keys)


def close(a,b,colors,quotient):
    key=lambda a,b:canonical(a,b,colors) if quotient else (a,b)
    seen={key(a,b)};queue=deque([(a,b)]);representatives=[]
    while queue:
        a,b=queue.popleft();representatives.append((a,b));c=then(a,b)
        for x,y in [(a,c),(c,b)]:
            k=key(x,y)
            if k not in seen:seen.add(k);queue.append((x,y))
    return seen,representatives


def main():
    base=Path(__file__).parent;forward={};reverse={};count=0
    for a,b in itertools.product(itertools.permutations(range(3)),repeat=2):
        for colors in itertools.product(range(3),repeat=3):
            k=canonical(a,b,colors);v=brute(a,b,colors)
            if k in forward:assert forward[k]==v
            if v in reverse:assert reverse[v]==k
            forward[k]=v;reverse[v]=k;count+=1
    closures=[]
    for a,b,colors in [((1,2,0),(1,0,2),(1,3,2)),((1,2,3,0),(1,0,3,2),(1,3,2,0)),((1,0,3,2),(0,1,3,2),(1,2,1,2))]:
        raw,reps=close(a,b,colors,False);quo,qreps=close(a,b,colors,True)
        assert quo=={canonical(x,y,colors) for x,y in reps}
        # Any representatives merged by a key must have equally colored action
        # for the medial code and both canonical successor states.
        mapping={}
        for x,y in reps:
            m=then(x,y);key=canonical(x,y,colors);observed=(bool(visibility(dict(colors=colors),m)),canonical(x,m,colors),canonical(m,y,colors))
            if key in mapping:assert observed==mapping[key]
            mapping[key]=observed
        closures.append(dict(raw_pairs=len(raw),quotient_pairs=len(quo)))
    rng=random.Random(7);relabeled=0;real=[]
    for name in ['illumination-20','illumination-22','illumination-search-simple-unrestricted','transparent-one-exhaust-survivor','transparent-simple-screen-survivor','cover-mixed-sector-1','cover-mixed-sector-2']:
        data=json.loads((base/(name+'.json')).read_text());c=build(data);a=c['H'];b=then(then(inverse(a),c['V']),a);colors=c['colors'];n=len(colors)
        for k in range(20):
            f=list(range(n));rng.shuffle(f);newcolors=[0]*n
            for i in range(n):newcolors[f[i]]=colors[i]
            aa,bb=conjugate(a,f),conjugate(b,f);assert canonical(a,b,colors)==canonical(aa,bb,newcolors);assert bool(visibility(c,then(a,b)))==bool(visibility(dict(colors=newcolors),then(aa,bb)));relabeled+=1
            if k%2:a=then(a,b)
            else:b=then(a,b)
        if name not in ['illumination-20','illumination-22','illumination-search-simple-unrestricted']:
            r=solve(data,20000,30,quotient=True);assert r['status']=='ILLUMINATED';real.append(dict(room=name,status=r['status'],direction=r['witness']['direction'],bounces=r['witness']['bounces'],processed_pairs=r.get('processed_pairs',0)))
    result=dict(status='PASS',brute_force_colored_systems=count,small_system_closures=closures,real_cover_relabelings=relabeled,positive_controls=real);save(base/'cover-code-quotient-audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
