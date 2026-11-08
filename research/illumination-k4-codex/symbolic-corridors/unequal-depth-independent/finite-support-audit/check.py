"""Complete independent prescribed finite-support proof validation.
Integer homogeneous clipping; no peer executable imports or calls.
One persisted840second aggregate deadline includes setup and every rerun.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import hashlib,json,time,signal
HERE=Path(__file__).resolve().parent;REVIEW=HERE.parent;BASE=REVIEW.parent;PEER=BASE/'unequal-depth'
DOMAIN=((0,0,1),(1,0,1),(1,1,1),(0,1,1))
BOXES=((0,(1,2),(1,2)),(0,(2,3),(2,3)),(2,(1,2),(0,1)),(2,(2,3),(3,4)))
state={};records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def normalize(x,y,w):
    assert w
    if w<0:x,y,w=-x,-y,-w
    g=gcd(gcd(abs(x),abs(y)),w);return x//g,y//g,w//g
def value(g,p):return g[0]*p[0]+g[1]*p[1]+g[2]*p[2]
def clean(ps):
    out=[]
    for p in ps:
        if not out or p!=out[-1]:out.append(p)
    if len(out)>1 and out[-1]==out[0]:out.pop()
    return tuple(out)
def clip(poly,line):
    if not poly:return ()
    out=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        va,vb=value(line,a),value(line,b)
        if va>=0:out.append(a)
        if va*vb<0:out.append(normalize(va*b[0]-vb*a[0],va*b[1]-vb*a[1],va*b[2]-vb*a[2]))
    return clean(out)
def admissible(poly):return bool(poly) and any(x>0 for x,y,w in poly) and any(y>0 for x,y,w in poly)
def subtract(poly,guards):
    if any(all(value(g,p)<=0 for p in poly) for g in guards):return [poly]
    if all(all(value(g,p)>0 for p in poly) for g in guards):return []
    out=[];inside=poly
    for g in guards:
        q=clip(inside,tuple(-x for x in g))
        if admissible(q):out.append(q)
        inside=clip(inside,g)
        if not inside:break
    return out

def charts(A,C,q):
    mod=4*q
    for M in range(q):
        for u,I,J in BOXES:
            for eps in (-1,1):
                x=(q-A,eps*A,A*(u+4*M));y=(q-C,eps*C,C*(u+4*M))
                xlo=x[2]+min(0,x[0])+min(0,x[1]);xhi=x[2]+max(0,x[0])+max(0,x[1])
                ylo=y[2]+min(0,y[0])+min(0,y[1]);yhi=y[2]+max(0,y[0])+max(0,y[1])
                # Strict interval intersections give these exact integer bounds.
                for k in range((xlo-q*I[1])//mod+1,(xhi-q*I[0]-1)//mod+1):
                    gx=((x[0],x[1],x[2]-q*I[0]-mod*k),(-x[0],-x[1],q*I[1]+mod*k-x[2]))
                    for l in range((ylo-q*J[1])//mod+1,(yhi-q*J[0]-1)//mod+1):
                        gy=((y[0],y[1],y[2]-q*J[0]-mod*l),(-y[0],-y[1],q*J[1]+mod*l-y[2]))
                        yield gx+gy

def verify_failure(A,C,q,s,t):
    checks=0
    for u,I,J in BOXES:
        for eps in (-1,1):
            for M in range(q):
                D=F(u)+eps*t+4*M-s;x=(s+F(A,q)*D)%4;y=(s+F(C,q)*D)%4
                assert not (I[0]<x<I[1] and J[0]<y<J[1]);checks+=1
    return checks

def sanity():
    assert normalize(-2,-4,-6)==(1,2,3)
    assert clip(((1,1,2),),(2,0,-1))==((1,1,2),)
    assert clip(((1,1,2),),(1,0,-1))==()
    seg=((0,1,1),(1,0,1));assert admissible(seg)
    assert set(clip(seg,(2,0,-1)))=={(1,1,2),(1,0,1)}
    assert not any(admissible(p) for p in subtract(DOMAIN,((1,0,0),(0,1,0))))
    left=subtract(DOMAIN,((2,0,-1),));assert left
    assert all(2*x<=w for p in left for x,y,w in p)
    assert subtract(((1,1,2),),((2,0,-1),))==[((1,1,2),)]
    assert subtract(((1,1,2),),((2,0,1),))==[]

def phases():
    rows=json.loads((REVIEW/'short-line-margin-check.json').read_text())['records']
    rels=[tuple(r['relation']) for r in rows]
    crit=[tuple(r['relation']) for r in rows if 'safe_phase_cutoff' not in r]
    good=[(tuple(r['relation']),r['safe_phase_cutoff']) for r in rows if 'safe_phase_cutoff' in r]
    assert len(rels)==30 and len(crit)==10 and len(good)==20
    normals=[(m,n) for m in range(-4,5) for n in range(-4,5) if 0<abs(m)+abs(n)<=4]
    eligible={};counts={'outside_short_lines':0,'good_short_lines':0}
    for q in range(3,101):
        for A in range(1,q-1):
            for C in range(A+1,q):
                if gcd(gcd(A,C),q)!=1:continue
                matching=[r for r in rels if r[0]*A+r[1]*C==r[2]*q]
                assert bool(matching)==any((m*A+n*C)%q==0 for m,n in normals)
                if not matching:group='outside_short_lines'
                else:
                    if q>64 or any(r in crit for r in matching):continue
                    cuts=[cut for r,cut in good if r in matching]
                    assert cuts
                    if q>min(cuts):continue
                    group='good_short_lines'
                eligible[q,A,C]=group;counts[group]+=1
    assert counts=={'outside_short_lines':115408,'good_short_lines':4332},counts
    for (q,A,C),group in eligible.items():assert eligible[q,q-C,q-A]==group
    return eligible,counts

def timeout(*_):raise TimeoutError('persisted complete-proof audit deadline reached')
def save(status,effort,counts,expected):
    pins={str((PEER/n).relative_to(BASE)):h for n,h in effort['source_sha256'].items()}
    for p in (REVIEW/'short-line-margin-check.json',REVIEW/'lattice-sampling-acceptance.json',HERE/'check.py'):
        pins[str(p.relative_to(BASE))]=sha(p)
    changed=[n for n,h in effort['source_sha256'].items() if sha(PEER/n)!=h]
    out={'status':status,'scope':'Complete prescribed finite domains; canonical phase representatives use proved endpoint-swap symmetry','progress':dict(state),'eligible_counts':counts,'expected_exception_phases':sorted(map(list,expected)),'source_changes':changed,'source_sha256':pins,'effort':effort,'records':records,'limits':'If partial, no complete support theorem follows. Positive phase classification uses exact strict-complement proof on full admissible endpoint square. No peer code, discovery, raysearch or full optical room conclusion.'}
    if changed:out['status']='SOURCE_CHANGED_RECONCILIATION_REQUIRED'
    (HERE/'result.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','source_sha256','effort')}),flush=True)
    return out

def main():
    effort=json.loads((HERE/'effort.json').read_text());remaining=effort['deadline']-time.time()
    if remaining<=0:raise TimeoutError('setup exhausted persisted audit deadline')
    signal.signal(signal.SIGALRM,timeout);signal.setitimer(signal.ITIMER_REAL,remaining)
    for n,h in effort['source_sha256'].items():assert sha(PEER/n)==h,n
    sanity();eligible,counts=phases();expected=set()
    for name in ('exceptional-phase-support.json','short-line-finite.json'):
        d=json.loads((PEER/name).read_text());assert d['status'].startswith('COMPLETE_')
        for row in d['exceptions']:
            A,C,q=row['phase'];expected.add((q,A,C))
    assert len(expected)==11
    canonical=[(key,group) for key,group in sorted(eligible.items()) if key[1]+key[2]<=key[0]]
    state.update(canonical_planned=len(canonical),canonical_completed=0,full_phase_classifications=0,positive_full_phase_classifications=0,exception_full_phase_classifications=0,clauses_applied=0,negative_chart_checks=0,q_completed=2,started=time.time())
    lastq=2;observed=set()
    try:
        for (q,A,C),group in canonical:
            if q!=lastq:
                state['q_completed']=lastq;(HERE/'progress.json').write_text(json.dumps(state,indent=2)+'\n');print(json.dumps(state),flush=True);lastq=q
            pieces=[DOMAIN];applied=0
            for gs in charts(A,C,q):
                out={}
                for poly in pieces:
                    for pp in subtract(poly,gs):out[tuple(sorted(set(pp)))]=pp
                pieces=list(out.values());applied+=1
                if not pieces:break
            exceptional=bool(pieces);weight=1 if A+C==q else 2
            if exceptional:
                assert (q,A,C) in expected and (q,q-C,q-A) in expected,('unreported failure phase',q,A,C)
                witnesses=[]
                for pp in pieces:
                    s=sum((F(x,w) for x,y,w in pp),F(0))/len(pp);t=sum((F(y,w) for x,y,w in pp),F(0))/len(pp)
                    assert 0<s<=1 and 0<t<=1
                    state['negative_chart_checks']+=verify_failure(A,C,q,s,t);witnesses.append([str(s),str(t)])
                observed.add((q,A,C));observed.add((q,q-C,q-A))
                residual=[[[str(F(x,w)),str(F(y,w))] for x,y,w in pp] for pp in pieces]
            else:
                assert (q,A,C) not in expected,('reported failure phase covered',q,A,C)
                witnesses=[];residual=[]
            records.append({'phase':[A,C,q],'group':group,'mirror_weight':weight,'result':'nonempty_failure_complement' if exceptional else 'full_admissible_square_covered','clauses_applied':applied,'failure_witnesses':witnesses,'failure_pieces':residual})
            state['canonical_completed']+=1;state['full_phase_classifications']+=weight;state['clauses_applied']+=applied
            state['exception_full_phase_classifications' if exceptional else 'positive_full_phase_classifications']+=weight
        state['q_completed']=100;assert observed==expected
        assert state['full_phase_classifications']==sum(counts.values())==119740
        result=save('COMPLETE_INDEPENDENT_FINITE_SUPPORT_CLASSIFICATION_PASS',effort,counts,expected)
        assert not result['source_changes']
    except TimeoutError:
        state['elapsed_since_effort_start']=time.time()-effort['start'];save('ORIGINAL_DEADLINE_PARTIAL_PROOF_ONLY',effort,counts,expected)
    finally:signal.setitimer(signal.ITIMER_REAL,0)
if __name__=='__main__':main()
