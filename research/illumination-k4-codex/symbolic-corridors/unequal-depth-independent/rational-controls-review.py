"""Validate ONLY14prescribed failure rows, never enumerate new depth pairs.
Independent Fraction chart evaluation; no peer code import or execution.
"""
from pathlib import Path
from fractions import Fraction as F
from math import lcm,gcd
import json,hashlib
H=Path(__file__).resolve().parent;BASE=H.parent
BOXES=((0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4)))

def main():
    src=BASE/'unequal-depth/rational-rectangle.json'
    saved=json.loads(src.read_text());assert saved['status']=='NO_RECTANGLE_IN_BOUNDED_PHASE_CONTROLS'
    s,t=F(1,2),F(1,4);out=[];total=0;edges=set()
    for row in saved['failure_rows']:
        a,b=F(row['a']),F(row['b']);assert a>0 and b>0
        al=a/(a+1+b);be=(a+1)/(a+1+b)
        q=lcm(al.denominator,be.denominator)
        A,C,Q=row['phase'];assert (al,be)==(F(A,Q),F(C,Q))
        assert q==Q and gcd(gcd(A,C),Q)==1 and 0<A<C<Q<=40
        checks=0
        for u,c,I,J in BOXES:
            for sign in (1,-1):
                for M in range(q):
                    displacement=F(u)+sign*t+4*M-s
                    x=(s+al*displacement)%4;y=(s+be*displacement)%4
                    assert not (I[0]<x<I[1] and J[0]<y<J[1]),(row,u,c,sign,M)
                    checks+=1
        # M->M+q preserves both phase coordinates modulo4, so all integers covered.
        assert (4*q*al).denominator==1 and (4*q*be).denominator==1
        assert (4*q*al)%4==0 and (4*q*be)%4==0
        edges.add((a,b));total+=checks
        out.append({'a':str(a),'b':str(b),'full_M_period':q,'direct_chart_tests':checks,'all_vertical_only_paths_fail':True})
    assert len(edges)==len(saved['failure_rows'])==14
    # Every candidate rectangle would need TWO distinct b values shared by TWO a values.
    neighbors={}
    for a,b in edges:neighbors.setdefault(a,set()).add(b)
    pairs=[]
    aa=sorted(neighbors)
    for i,a in enumerate(aa):
        for A in aa[i+1:]:
            common=neighbors[a]&neighbors[A];assert len(common)<2
            pairs.append({'a':str(a),'A':str(A),'shared_b_values':list(map(str,sorted(common)))})
    # Prescribed iteration bounds count, without rerunning its successful-ray search.
    count=sum(gcd(gcd(A,C),q)==1 for q in range(3,41) for A in range(1,q-1) for C in range(A+1,q))
    assert count==saved['phase_pairs_tested']==8410
    sources=['unequal-depth/rational-rectangle.py','unequal-depth/rational-rectangle.json','unequal-depth/rational-rectangle-effort.json','unequal-depth-independent/vertical-completeness-review.md']
    sources.append('unequal-depth-independent/rational-controls-review.py')
    result={'status':'PRESCRIBED14VERTICAL_FAILURES_AND_FINITE_GRAPH_VERIFIED','prescribed_failure_rows':len(out),'exact_chart_evaluations':total,'enumerator_primitive_phase_triples':count,'rectangle_in_recorded_graph':False,'failure_records':out,'pairwise_neighbor_checks':pairs,'source_sha256':{r:hashlib.sha256((BASE/r).read_bytes()).hexdigest() for r in sources},'limits':'Independently validates all14negative rows and absence of rectangles in their recorded graph. Does not independently rerun8410positive/negative classifications, prove global rectangle absence, exclude cap corners for positive charts, or establish darkness.'}
    (H/'rational-controls-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('failure_records','pairwise_neighbor_checks','source_sha256')}))
if __name__=='__main__':main()
