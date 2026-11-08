"""Independent30relation closed-square and eta1/8cover verification.
Own planar sign-cell arrangement, not peer complement/subtraction algorithm.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
sp=spec_from_file_location('own_frozen_arrangement',HERE/'phase-lines-check.py');P=module_from_spec(sp);sp.loader.exec_module(P)
DOMAIN=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1)),(F(0),F(1))]
BOXES=((0,(1,2),(1,2)),(0,(2,3),(2,3)),(2,(1,2),(0,1)),(2,(2,3),(3,4)))
def clauses(m,n,r,eta):
    w=abs(m)+abs(n);cs=[]
    for u,I,J in BOXES:
        lo=min(m*I[0],m*I[1])+min(n*J[0],n*J[1])+eta*w
        hi=max(m*I[0],m*I[1])+max(n*J[0],n*J[1])-eta*w
        assert lo<hi
        for eps in (-1,1):
            for k in range(-9,10):
                a,b,c=m+n-r,r*eps,r*u+4*k
                guards=((F(a),F(b),F(c)-lo),(F(-a),F(-b),hi-c))
                # A strict clause with no feasible square point cannot help.
                if any(max(P.val(g,x) for x in DOMAIN)<=0 for g in guards):continue
                cs.append(guards)
    return cs
def representatives(cs):
    lines=sorted({P.linekey(g) for gs in cs for g in gs if (g[0] or g[1]) and min(P.val(g,x) for x in DOMAIN)<=0<=max(P.val(g,x) for x in DOMAIN)})
    faces=[DOMAIN]
    for line in lines:faces=[Q for face in faces for Q in (P.clip(face,line,1),P.clip(face,line,-1)) if Q]
    points=set()
    for face in faces:
        points.add(tuple(sum(x[j] for x in face)/len(face) for j in (0,1)))
        for a,b in zip(face,face[1:]+face[:1]):points.add(a);points.add(tuple((x+y)/2 for x,y in zip(a,b)))
    assert set(DOMAIN)<=points
    return sorted(points),len(faces),len(lines)
def in_piece(x,raw):
    pts=[tuple(map(F,p)) for p in raw]
    if len(pts)==1:return x==pts[0]
    assert len(pts)==2,('unexpected parent blind-piece dimension',pts)
    a,b=pts;return (x[0]-a[0])*(b[1]-a[1])==(x[1]-a[1])*(b[0]-a[0]) and all(min(v,w)<=p<=max(v,w) for p,v,w in zip(x,a,b))
def phase_on(m,n,r):
    verts=[(F(0),F(0)),(F(0),F(1)),(F(1),F(1))];xs=set()
    for a,b in zip(verts,verts[1:]+verts[:1]):
        u=m*a[0]+n*a[1]-r;v=m*b[0]+n*b[1]-r
        if not u:xs.add(a)
        if u*v<0:
            t=u/(u-v);xs.add(tuple(x+t*(y-x) for x,y in zip(a,b)))
    assert len(xs)==2
    a,b=sorted(xs);al,be=tuple((x+y)/2 for x,y in zip(a,b));assert 0<al<be<1 and m*al+n*be==r
    return al,be
def main():
    source=json.loads((BASE/'unequal-depth/short-line-margin.json').read_text());assert source['status']=='COMPLETE_CLOSED_ENDPOINT_SHORT_LINE_MARGIN_CLASSIFICATION'
    parent={tuple(row['relation']):row for row in source['rows']};relations=[]
    # Independent canonical integer enumeration of the phase-triangle range.
    for m in range(-4,5):
        for n in range(-4,5):
            if not 0<abs(m)+abs(n)<=4 or not (m>0 or m==0 and n>0):continue
            levels=(0,n,m+n)
            for r in range(-4,5):
                if min(levels)<r<max(levels) and gcd(gcd(abs(m),abs(n)),abs(r))==1:relations.append((m,n,r))
    assert len(relations)==len(parent)==30 and set(relations)==set(parent)
    records=[];total=0;good=[];critical=[];identities=0
    for m,n,r in relations:
        row=parent[m,n,r];line=[m+n-r,-r,r-n];assert row['depth_line']==line
        al,be=phase_on(m,n,r);a,b=al/(be-al),(1-be)/(be-al);assert line[0]*a+line[1]*b==line[2]
        for u,_,_ in BOXES:
            for eps in (-1,1):
                for s,t,M in ((F(0),F(0),-7),(F(1),F(1),0),(F(2,7),F(5,11),9)):
                    E1=(1-al)*s+al*(eps*t+u+4*M);E2=(1-be)*s+be*(eps*t+u+4*M)
                    C=(m+n-r)*s+r*eps*t+r*u
                    assert m*E1+n*E2==C+4*M*r;identities+=1
        zero=clauses(m,n,r,F(0));points,faces,lines=representatives(zero);blind=[]
        for x in points:
            covered=any(all(P.val(g,x)>0 for g in gs) for gs in zero)
            expected=any(in_piece(x,p) for p in row['closed_blind_pieces'])
            assert (not covered)==expected,(m,n,r,x,covered,expected)
            if not covered:blind.append(list(map(str,x)))
        total+=len(points);rec={'relation':[m,n,r],'depth_line':line,'eta0_faces':faces,'eta0_lines':lines,'eta0_closed_sign_cells':len(points),'blind_cell_representatives':blind}
        if row['closed_blind_pieces']:
            assert blind;critical.append(line)
        else:
            assert row['uniform_margin']=='1/8' and row['rational_phase_cutoff']==16*(abs(m)+abs(n))
            shrunk=clauses(m,n,r,F(1,8));ss,ff,ll=representatives(shrunk)
            for x in ss:assert any(all(P.val(g,x)>0 for g in gs) for gs in shrunk),(m,n,r,x)
            total+=len(ss);good.append([m,n,r]);rec.update({'eta1_8_faces':ff,'eta1_8_lines':ll,'eta1_8_closed_sign_cells':len(ss),'safe_phase_cutoff':16*(abs(m)+abs(n))})
        records.append(rec)
    expected={(1,0,1),(0,1,1),(1,-1,-1),(1,-1,1),(2,-1,-1),(1,-2,1),(2,-1,-2),(1,-2,2),(3,-1,-1),(1,-3,1)}
    assert len(good)==20 and len(critical)==10 and set(map(tuple,critical))==expected
    assert set(map(tuple,critical))==set(map(tuple,source['unbounded_critical_lines']))
    names=['unequal-depth/short-line-margin.md','unequal-depth/short-line-margin.py','unequal-depth/short-line-margin.json','unequal-depth-independent/phase-lines-check.py','unequal-depth-independent/lattice-sampling-acceptance.json','unequal-depth-independent/short-line-margin-check.py']
    out={'status':'INDEPENDENT_CLOSED_SHORT_RELATION_MARGIN_COVER_PASS','primitive_relations':len(relations),'uniform_margin_lines':len(good),'unbounded_candidate_lines':len(critical),'complete_closed_sign_cells':total,'portal_coefficient_identity_controls':identities,'source_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in names},'records':records,'critical_depth_lines':critical,'limits':'Exact finite affine-cover proof includes every closed-square axis/edge/vertex sign cell. Orbit cutoff relies on separately reviewed finite-component spacing lemma. Finite low-qexceptions and four-cap global closure still unproved.'}
    (HERE/'short-line-margin-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','records')}))
if __name__=='__main__':main()
