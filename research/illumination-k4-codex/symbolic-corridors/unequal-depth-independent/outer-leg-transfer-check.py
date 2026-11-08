"""Independent cap transfer of prescribed outer-simple auxiliary paths.
Middle reflections are retained unchanged; no peer executable is imported.
Also records the exact nonfatal q4portal-coordinate erratum.
"""
from pathlib import Path
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
def load(name,path):
    sp=spec_from_file_location(name,path);m=module_from_spec(sp);sp.loader.exec_module(m);return m
M=load('own_tracer',HERE/'horizontal-parity-check.py');G=M.G
Eq=load('own_equal_depth',BASE/'equal-depth-independent/check.py')
def aty(path,z):
    hits=set()
    for A,B in zip(path,path[1:]):
        if A[1]!=B[1] and min(A[1],B[1])<=z<=max(A[1],B[1]):
            t=(z-A[1])/(B[1]-A[1]);hits.add((A[0]+t*(B[0]-A[0]),z))
    assert len(hits)==1,(z,hits)
    return hits.pop()
def portals(path):
    lo=next(aty([A,B],F(0)) for A,B in zip(path,path[1:]) if A[1]<0<=B[1])
    hi=next(aty([A,B],F(1)) for A,B in reversed(list(zip(path,path[1:]))) if A[1]<=1<B[1])
    assert 1<lo[0]<2 and 1<hi[0]<2
    return lo,hi
def transfer(aux,a,b,hm,hp,lc,uc):
    aux=[tuple(map(F,p)) for p in aux];s,A=aux[0][0],-aux[0][1];t,B=aux[-1][0],aux[-1][1]-1
    assert A==(2*hm-a if lc else a) and B==(2*hp-b if uc else b)
    assert G.verify(aux,F(1),F(1),A,B,s,t,A+1,B+1)==len(aux)-2
    portals(aux)
    for x,y in aux[1:-1]:
        if y<0 or y>1:assert x in (0,2)
        else:assert 1<=x<=3
    lowerbad=bool(lc and aty(aux,-hm)[0] in (0,2));upperbad=bool(uc and aty(aux,1+hp)[0] in (0,2))
    start=-a if lowerbad else -A;end=1+b if upperbad else 1+B
    assert aty(aux,start)==(s,start) and aty(aux,end)==(t,end)
    cuts={start,end}
    if lc:cuts.add(-hm)
    if uc:cuts.add(1+hp)
    points=[aux[0]]
    for U,V in zip(aux,aux[1:]):
        mids=[]
        if U[1]!=V[1]:
            for z in cuts:
                theta=(z-U[1])/(V[1]-U[1])
                if 0<theta<1:mids.append((theta,(U[0]+theta*(V[0]-U[0]),z)))
        points.extend(p for _,p in sorted(mids));points.append(V)
    clean=[]
    for p in points:
        if not clean or p!=clean[-1]:clean.append(p)
    i=clean.index((s,start));j=clean.index((t,end));assert i<j
    def Y(z):return -2*hm-z if lc and z<-hm else 2*(1+hp)-z if uc and z>1+hp else z
    path=M.prefix([(x,Y(y)) for x,y in clean[i:j+1]])
    n=G.verify(path,F(1),F(1),a,b,s,t,hm,hp)
    rev=M.prefix([(x,1-y) for x,y in reversed(path)]);rn=G.verify(rev,F(1),F(1),b,a,t,s,hp,hm)
    d,g=F(2,3),F(5,7);scaled=[(d*x,g*y) for x,y in path]
    assert G.verify(scaled,d,g,g*a,g*b,d*s,d*t,g*hm,g*hp)==n
    return {'source_effective_depth':str(A),'target_effective_depth':str(B),'lc':lc,'uc':uc,'lower_corner_removed':lowerbad,'upper_corner_removed':upperbad,'contacts':n,'reverse_contacts':rn,'auxiliary_middle_contacts':sum(0<=y<=1 for x,y in aux[1:-1]),'portals':[[str(x),str(y)] for x,y in portals(aux)],'path':[[str(x),str(y)] for x,y in path]}
def main():
    rows=[]
    prescribed=[(1,3,F(1,3),F(2,3)),(1,3,F(1),F(1)),(1,3,F(1,10),F(9,10)),(1,4,F(1),F(1)),(1,5,F(2,3),F(1,3)),(2,5,F(2,3),F(1,3)),(1,7,F(2,3),F(1,3)),(2,7,F(2,3),F(1,3)),(3,7,F(2,3),F(1,3)),(1,6,F(2,3),F(1,3)),(3,11,F(2,3),F(1,3))]
    for p,q,s,t in prescribed:
        aux,A,choice=Eq.construct(p,q,s,t)
        for lc in (0,1):
            for uc in (0,1):
                a=A/2 if lc else A;b=3*A/4 if uc else A
                hm=(A+a)/2 if lc else A+1;hp=(A+b)/2 if uc else A+1
                row=transfer(aux,a,b,hm,hp,lc,uc);row.update({'phase':[p,q],'auxiliary_kind':str(choice)});rows.append(row)
    # Already accepted fixed both-corner chart, now through the outer-only constructor.
    aux,_=G.chart_path(F(1),F(1),F(5,2),F(5,2),F(1),F(1),-2,F(1),F(2),-1)
    for lc in (0,1):
        for uc in (0,1):
            A=F(5,2);hm=F(7,4) if lc else A+1;hp=F(7,4) if uc else A+1
            a=2*hm-A if lc else A;b=2*hp-A if uc else A
            row=transfer(aux,a,b,hm,hp,lc,uc);assert row['lower_corner_removed']==bool(lc) and row['upper_corner_removed']==bool(uc)
            row['auxiliary_kind']='prescribed both-corner vertical chart';rows.append(row)
    parent=json.loads((BASE/'unequal-depth/outer-leg-transfer-check.json').read_text());match=next(r for r in rows if r.get('phase')==[1,3] and r['lc']==r['uc']==1 and r['path'][0]==['1/3','-1/2'])
    assert match['path']==parent['original_path'] and match['contacts']==5
    center,A,_=Eq.construct(1,4,F(1),F(1));lo,hi=portals(center)
    assert lo[0]==hi[0]==F(3,2) and lo[0]!=F(7,4)
    source_names=['equal-depth/proof.md','equal-depth-independent/review.md','equal-depth-independent/check.py','unequal-depth-independent/outer-leg-transfer-check.py']
    err={'status':'Q4_PORTAL_COORDINATE_CORRECTED_NONFATAL','phase':['1/4'],'auxiliary_depth':'1/2','horizontal_marks':['1','1'],'claimed_coordinate':'7/4','correct_lower_portal':list(map(str,lo)),'correct_upper_portal':list(map(str,hi)),'original_path':[[str(x),str(y)] for x,y in center],'strict_legality_preserved':True,'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in source_names},'limits':'Frozen parent proof and old independent review both repeat numericaltypo. Explicit path and theorem remain valid; no original frozen file changed.'}
    (HERE/'equal-depth-portal-erratum.json').write_text(json.dumps(err,indent=2)+'\n')
    names=['unequal-depth/outer-leg-transfer.md','unequal-depth/outer-leg-transfer-check.json','equal-depth/proof.md','equal-depth-independent/acceptance.json','equal-depth-independent/check.py','unequal-depth-independent/corner-removal-acceptance.json','unequal-depth-independent/horizontal-parity-check.py','unequal-depth-independent/outer-leg-transfer-check.py']
    out={'status':'INDEPENDENT_OUTER_SIMPLE_CAP_TRANSFER_CONTROLS_PASS','prescribed_auxiliary_families':len(prescribed)+1,'prescribed_forward_paths':len(rows),'actual_paths_including_reverse_and_scaling':3*len(rows),'wall_contacts_including_reverse_and_scaling':sum(2*r['contacts']+r['reverse_contacts'] for r in rows),'parent_five_bounce_path_matches':True,'q4_portal_erratum':'equal-depth-portal-erratum.json','source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names},'records':rows,'limits':'Universal outerleg transfer and exhaustive equaldepth formula structure hand-reviewed separately. Exact prescribed paths only; no discovery or full rational theorem.'}
    (HERE/'outer-leg-transfer-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','records')}))
if __name__=='__main__':main()
