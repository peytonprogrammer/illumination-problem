"""Verify ONLY prescribed q14 failure and short-annihilator counterexample.
No parent clipper execution or broader parameter classification.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
BOXES=((0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4)))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def main():
    saved=json.loads((BASE/'unequal-depth/finite-short-cover.json').read_text());assert saved['status']=='NORM4_FAILURE_PREMISE_REFUTED_BY_EXACT_CELL'
    assert saved['phase']==[5,6,14]
    A,C,q=5,6,14;al,be=F(A,q),F(C,q);assert gcd(gcd(A,C),q)==1
    assert al/(be-al)==5 and (1-be)/(be-al)==8
    points=[(F(7,10),F(1,100)),(F(saved['s']),F(saved['t']))];tables=[]
    for s,t in points:
        assert 0<s<1 and 0<t<1
        rows=[]
        for u,c,I,J in BOXES:
            for eps in (-1,1):
                for j in range(q):
                    D=F(u)+eps*t+4*j-s;x=(s+al*D)%4;y=(s+be*D)%4
                    success=I[0]<x<I[1] and J[0]<y<J[1]
                    assert not success,(s,t,u,c,eps,j)
                    rows.append({'u':u,'c':c,'eps':eps,'M':j,'x':str(x),'y':str(y)})
        assert 4*q*al%4==0 and 4*q*be%4==0
        tables.append({'s':str(s),'t':str(t),'all_four_chart_sign_period_tests':len(rows),'rows':rows})
    normals=[]
    for m in range(-4,5):
        for n in range(-4,5):
            if 0<abs(m)+abs(n)<=4:
                residue=(m*A+n*C)%q;assert residue!=0;normals.append([m,n,residue])
    assert len(normals)==40
    assert 4*al-be==1 and gcd(gcd(4,1),1)==1
    min5=[]
    for m in range(-5,6):
        for n in range(-5,6):
            if abs(m)+abs(n)==5 and (m*A+n*C)%q==0:min5.append([m,n,(m*A+n*C)//q])
    assert [4,-1,1] in min5
    tri=[tuple(map(F,v)) for v in saved['failure_cell']]
    simple=points[0];cs=[cross(sub(b,a),sub(simple,a)) for a,b in zip(tri,tri[1:]+tri[:1])]
    assert all(x>0 for x in cs) or all(x<0 for x in cs)
    # Exact fixed old /16 grid has no strictly interior point in this supplied cell.
    oldhits=[]
    for i in range(1,17):
        for j in range(1,17):
            p=(F(i,16),F(j,16));ss=[cross(sub(b,a),sub(p,a)) for a,b in zip(tri,tri[1:]+tri[:1])]
            if all(x>0 for x in ss) or all(x<0 for x in ss):oldhits.append(p)
    assert not oldhits
    names=['unequal-depth/finite-short-cover.py','unequal-depth/finite-short-cover.json','unequal-depth-independent/vertical-completeness-review.md','unequal-depth-independent/finite-short-counterexample-check.py']
    out={'status':'NORM4_NECESSITY_PREMISE_INDEPENDENTLY_REFUTED','phase':[A,C,q],'depths':['5','8'],'prescribed_failure_points':2,'explicit_chart_evaluations':sum(r['all_four_chart_sign_period_tests'] for r in tables),'short_annihilator_pairs_excluded':len(normals),'minimum_annihilator_l1':5,'minimum_relations':min5,'old_grid_hits_in_supplied_open_cell':0,'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names},'tables':tables,'short_normal_residues':normals,'limits':'Proves no vertical-only path for the two fixed endpoint pairs, and disproves necessity of an l1<=4 relation. Does not assert the whole supplied polygon fails, test four cap sheets, or prove darkness. q>100 lattice lemma unaffected.'}
    (HERE/'finite-short-counterexample-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','tables','short_normal_residues')}))
if __name__=='__main__':main()
