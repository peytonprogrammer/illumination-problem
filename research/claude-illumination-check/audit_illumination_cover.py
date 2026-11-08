"""Independent certificate closure and cover-versus-billiard checks."""
import itertools,json,math
from pathlib import Path
from illumination_cover import build,then,inverse,left_code,physical_direction,solve
from illumination_cover_certificate import certify,relation
from illumination_paths import trace as global_trace,room
from illumination_sector_paths import trace,prepare,verify as verify_path
from illumination_geometry import save,edge,owners_of


def verify_certificate(data,result):
    assert result['status']=='DARK' and result['all_directions_covered']
    cert=result['certificate'];c=build(data);H,V=tuple(cert['H']),tuple(cert['V']);colors=tuple(cert['colors']);n=len(H)
    assert (H,V,colors)==(c['H'],c['V'],c['colors']);R=list(map(int,cert['palindrome_rows']));assert len(R)==n
    for i in range(n):
        assert R[i]>=0 and R[i]>>n==0
        for j in (i,H[i],V[i]):assert R[i]>>j&1
        for j in range(n):
            if R[i]>>j&1:
                # For a -> b in R, H^-1(a) -> H(b) must be in R.
                for P in (H,V):assert R[inverse(P)[i]]>>P[j]&1
    seen=set(cert['reachable']);assert {i for i,c in enumerate(colors) if c==1}<=seen
    assert not any(colors[i] in (2,3) for i in seen)
    for i in seen:
        for j in range(n):
            if R[i]>>j&1:
                k=H[V[j]]
                if colors[k]!=3:assert k in seen
    # Verify both actual axis permutations directly, without visibility().
    for P in (H,V):
        for source in [i for i,c in enumerate(colors) if c==1]:
            visited={source};i=source
            while True:
                i=P[i];assert colors[i]!=2
                if colors[i]==3 or i in visited:break
                visited.add(i)
    return True


def classify_from_sector(c,code,source):
    seen={source};i=source
    while True:
        i=code[i]
        if c['colors'][i]==2:return True
        if c['colors'][i]==3 or i in seen:return False
        seen.add(i)


def audit_room(name,bound=10):
    data=json.loads((Path(__file__).parent/(name+'.json')).read_text());c=build(data);H,V=c['H'],c['V'];prep=prepare(data);global_prep=room(data);disagreements=0;sources=[i for i,v in enumerate(c['colors']) if v==1];physical_checks=0;codes=0
    # Build exactly the same primitive directions in two independent ways:
    # Farey addition of codes, and exact chronological grid intersections.
    stack=[(H,then(then(inverse(H),V),H),(1,0),(0,1))]
    while stack:
        a,b,u,v=stack.pop();x,y=u[0]+v[0],u[1]+v[1]
        if max(x,y)>bound:continue
        code=then(a,b);assert code==left_code(H,V,x,y);codes+=1
        for s in sources:
            expected=classify_from_sector(c,code,s);direction=physical_direction(c,s,x,y);actual=trace(data,direction,30000,prep)
            if actual['status']=='illuminated':verify_path(data,actual)
            other=global_trace(data,direction,3000,global_prep)
            disagreements+=int((actual['status']=='illuminated')!=(other['status']=='illuminated'))
            assert actual['status'] not in ('escaped','limit'),(name,direction,actual)
            assert expected==(actual['status']=='illuminated'),(name,direction,expected,actual)
            physical_checks+=1
        stack.extend([(a,code,u,(x,y)),(code,b,(x,y),v)])
    for code,(x,y) in [(H,(1,0)),(V,(0,1))]:
        for s in sources:
            actual=trace(data,physical_direction(c,s,x,y),3000,prep);assert classify_from_sector(c,code,s)==(actual['status']=='illuminated');physical_checks+=1
    result=certify(data,True)
    if result['status']=='DARK':
        verify_certificate(data,result)
        # Real certificate corruptions must fail the independent verifier.
        for field in ['remove_relation','add_target']:
            bad=json.loads(json.dumps(result))
            if field=='remove_relation':bad['certificate']['palindrome_rows'][0]='0'
            else:bad['certificate']['reachable'].append(next(i for i,v in enumerate(c['colors']) if v==2))
            try:verify_certificate(data,bad)
            except AssertionError:pass
            else:raise AssertionError(('accepted corrupt certificate',field))
    return dict(room=name,cover_squares=len(H),primitive_positive_codes=codes,exact_physical_ray_comparisons=physical_checks,certificate=result['status'],global_corner_convention_disagreements=disagreements)


def main():
    base=Path(__file__).parent;results=[]
    for name in ['illumination-20','illumination-22','illumination-search-simple-unrestricted','transparent-one-exhaust-survivor','transparent-simple-screen-survivor','cover-mixed-sector-1','cover-mixed-sector-2']:
        r=audit_room(name);results.append(r);print(json.dumps(r),flush=True)
    # Direct least-fixed-point implementation versus independent inward peeling
    # on every pair of a small noncommuting permutation system.
    H=(1,2,0,3);V=(1,0,3,2);R,count=relation(H,V)
    for a,b in itertools.product(range(4),repeat=2):
        todo=[(a,b)];seen=set(todo);found=False
        while todo:
            i,j=todo.pop()
            if j in (i,H[i],V[i]):found=True;break
            for P in (H,V):
                q=(P[i],inverse(P)[j])
                if q not in seen:seen.add(q);todo.append(q)
        assert found==bool(R[a]>>b&1)
    summary=dict(status='PASS',rooms=results,total_exact_ray_comparisons=sum(r['exact_physical_ray_comparisons'] for r in results),independent_small_relation_pairs=16,corrupt_certificates_rejected=6)
    save(base/'cover-final-audit.json',summary);print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
