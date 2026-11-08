"""Reconcile all11prescribed failure-piece unions by a separate arrangement.
Uses own full proof output and own frozen planar arrangement helper only.
"""
from pathlib import Path
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]
sp=spec_from_file_location('own_planar_arrangement',HERE.parent/'phase-lines-check.py');P=module_from_spec(sp);sp.loader.exec_module(P)
BOXES=((0,(1,2),(1,2)),(0,(2,3),(2,3)),(2,(1,2),(0,1)),(2,(2,3),(3,4)))
DOMAIN=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def inside(x,poly):
    poly=list(dict.fromkeys(poly));assert poly
    if len(poly)==1:return x==poly[0]
    a,b=min(poly),max(poly)
    if all(cross(sub(y,a),sub(b,a))==0 for y in poly):
        return cross(sub(x,a),sub(b,a))==0 and all(min(u,v)<=z<=max(u,v) for z,u,v in zip(x,a,b))
    signs=[cross(sub(v,u),sub(x,u)) for u,v in zip(poly,poly[1:]+poly[:1])]
    return all(z>=0 for z in signs) or all(z<=0 for z in signs)
def vertical_success(A,C,q,s,t):
    for u,I,J in BOXES:
        for eps in (-1,1):
            for M in range(q):
                D=F(u)+eps*t+4*M-s;x=(s+F(A,q)*D)%4;y=(s+F(C,q)*D)%4
                if I[0]<x<I[1] and J[0]<y<J[1]:return True
    return False

def main():
    initial=json.loads((HERE/'result.json').read_text());assert initial['status']=='COMPLETE_INDEPENDENT_FINITE_SUPPORT_CLASSIFICATION_PASS'
    own={tuple(r['phase']):r for r in initial['records'] if r['failure_pieces']};parent=[]
    for name in ('exceptional-phase-support.json','short-line-finite.json'):
        parent+=json.loads((BASE/'unequal-depth'/name).read_text())['exceptions']
    assert len(parent)==11;records=[];total=0
    for row in parent:
        A,C,q=row['phase'];canonical=(A,C,q) if A+C<=q else (q-C,q-A,q)
        mine=own[canonical]['failure_pieces'];mine=[[tuple(map(F,x)) for x in poly] for poly in mine]
        if A+C>q:mine=[[(y,x) for x,y in poly] for poly in mine]
        theirs=[[tuple(map(F,x)) for x in poly] for poly in row['closed_failure_pieces']]
        lines=set()
        for poly in mine+theirs:
            for x,y in poly:
                lines.add((F(1),F(0),-x));lines.add((F(0),F(1),-y))
            for a,b in zip(poly,poly[1:]+poly[:1]):
                if a!=b:lines.add(P.linekey((a[1]-b[1],b[0]-a[0],a[0]*b[1]-b[0]*a[1])))
        polygons=[DOMAIN]
        for line in sorted(lines):
            if min(P.val(line,x) for x in DOMAIN)<=0<=max(P.val(line,x) for x in DOMAIN):
                polygons=[z for poly in polygons for z in (P.clip(poly,line,1),P.clip(poly,line,-1)) if z]
        reps=set()
        for poly in polygons:
            reps.add(tuple(sum(x[j] for x in poly)/len(poly) for j in (0,1)))
            for a,b in zip(poly,poly[1:]+poly[:1]):reps.add(a);reps.add(tuple((x+y)/2 for x,y in zip(a,b)))
        cells=failed=0
        for s,t in sorted(reps):
            if not 0<s<=1 or not 0<t<=1:continue
            p=(s,t);x=any(inside(p,z) for z in mine);y=any(inside(p,z) for z in theirs)
            assert x==y,(A,C,q,s,t,'union mismatch')
            assert x==(not vertical_success(A,C,q,s,t)),(A,C,q,s,t,'direct chart mismatch')
            cells+=1;failed+=x
        assert failed>0
        total+=cells;records.append({'phase':[A,C,q],'depths':row['depths'],'parent_pieces':len(theirs),'own_pieces':len(mine),'admissible_relative_cells':cells,'failure_cells':failed,'all_memberships_and_direct_chart_results_match':True})
    names=['unequal-depth/exceptional-phase-support.json','unequal-depth/short-line-finite.json','unequal-depth-independent/phase-lines-check.py','unequal-depth-independent/finite-support-audit/result.json','unequal-depth-independent/finite-support-audit/failure-unions.py']
    out={'status':'ALL_ELEVEN_FAILURE_UNIONS_INDEPENDENTLY_RECONCILED','phase_pairs':len(records),'complete_admissible_relative_cells':total,'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names},'records':records,'limits':'Complete finite failure-union equivalence on0<s,t<=1, including edges/vertices; no four-cap rectangle or full optical room closure.'}
    (HERE/'failure-unions.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','records')}))
if __name__=='__main__':main()
