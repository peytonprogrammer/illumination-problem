"""Independent prescribed 10^4 affine classifications; never runs peer code."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, hashlib

HERE=Path(__file__).resolve().parent
PEER=HERE.parent/'unequal-depth'
def read(name): return json.loads((PEER/name).read_text())
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dot(x,y): return sum(a*b for a,b in zip(x,y))

def affine(equations):
    # Intersect an affine parametrization with one hyperplane at a time.
    origin=[F(0)]*4
    basis=[[F(i==j) for i in range(4)] for j in range(4)]
    for normal,rhs in equations:
        weights=[dot(normal,v) for v in basis]
        residual=rhs-dot(normal,origin)
        nonzero=[j for j,w in enumerate(weights) if w]
        if not nonzero:
            if residual:return None
            continue
        j=nonzero[-1]; direction=basis[j]; w=weights[j]
        origin=[x+residual*y/w for x,y in zip(origin,direction)]
        basis=[[x-weights[k]*y/w for x,y in zip(v,direction)] for k,v in enumerate(basis) if k!=j]
    return origin,basis

def strict_feasible(origin,basis):
    normals=((1,0,0,0),(0,0,1,0),(-1,1,0,0),(0,0,-1,1))
    constraints=[([dot(n,v) for v in basis],dot(n,origin)) for n in normals]
    # Eliminate the LAST free variable, using unnormalized positive multipliers.
    for _ in basis:
        positive=[(v,c) for v,c in constraints if v[-1]>0]
        negative=[(v,c) for v,c in constraints if v[-1]<0]
        keep=[(v[:-1],c) for v,c in constraints if not v[-1]]
        for p,pc in positive:
            for n,nc in negative:
                keep.append(([-n[-1]*x+p[-1]*y for x,y in zip(p[:-1],n[:-1])],-n[-1]*pc+p[-1]*nc))
        constraints=keep
    return all(c>0 for _,c in constraints)

def canonical_equations(equations):
    # Row-space signature only, separate from the affine solving/feasibility.
    rows=[[F(x) for x in n]+[F(r)] for n,r in equations]; at=0
    for col in range(4):
        choices=[j for j in range(at,len(rows)) if rows[j][col]]
        if not choices:continue
        j=choices[-1]; rows[at],rows[j]=rows[j],rows[at]
        z=rows[at][col]; rows[at]=[x/z for x in rows[at]]
        for k in range(len(rows)):
            if k!=at:
                z=rows[k][col]; rows[k]=[x-z*y for x,y in zip(rows[k],rows[at])]
        at+=1
    return tuple(tuple(r) for r in rows[:at])

def on(p,seg):
    a,b=seg[0],seg[-1]
    return (b[0]-a[0])*(p[1]-a[1])==(b[1]-a[1])*(p[0]-a[0]) and all(min(x,y)<=z<=max(x,y) for x,y,z in zip(a,b,p))

def intersection(a,b):
    candidates=set(p for p in a if on(p,b))|set(p for p in b if on(p,a))
    if len(a)>1 and len(b)>1:
        p,q=a; r,s=b; u=(q[0]-p[0],q[1]-p[1]); v=(s[0]-r[0],s[1]-r[1])
        det=u[0]*v[1]-u[1]*v[0]
        if det:
            tau=((r[0]-p[0])*v[1]-(r[1]-p[1])*v[0])/det
            z=(p[0]+tau*u[0],p[1]+tau*u[1])
            if on(z,a) and on(z,b):candidates.add(z)
    return sorted(candidates)

def common_blind(indices,rows):
    current=[[(F(0),F(0)),(F(1),F(0))],[(F(0),F(0)),(F(0),F(1))],[(F(1),F(0)),(F(1),F(1))],[(F(0),F(1)),(F(1),F(1))]]
    for i in indices:
        pieces=[[tuple(map(F,p)) for p in piece] for piece in rows[i]['closed_blind_pieces']]
        current=[z for a,b in product(current,pieces) if (z:=intersection(a,b))]
    return sorted(set(tuple(x) for x in current))

def equations_for(indices,rows):
    result=[]
    for j,i in enumerate(indices):
        p,q,r=map(F,rows[i]['depth_line']); n=[F(0)]*4
        n[j%2]=p;n[2+j//2]=q;result.append((n,r))
    return result

def main():
    rows=[r for r in read('short-line-margin.json')['rows'] if r['closed_blind_pieces']]
    source=read('critical-rectangles.json'); actual={}; stats={'inconsistent':0,'strict_infeasible':0,'feasible_assignments':0}
    for indices in product(range(10),repeat=4):
        eq=equations_for(indices,rows); solution=affine(eq)
        if solution is None:stats['inconsistent']+=1;continue
        o,b=solution
        if not strict_feasible(o,b):stats['strict_infeasible']+=1;continue
        stats['feasible_assignments']+=1
        key=canonical_equations(eq); blind=common_blind(indices,rows)
        assert all(len(z)==1 for z in blind),('unreported blind continuum',indices,blind)
        if key in actual and b:assert actual[key]['blind']==blind,('family assignment-dependent blind set',indices)
        actual[key]={'dimension':len(b),'blind':blind}
    expected={}; equality_families=0; blind_families=0; residual_blind=0; interval_checks=0
    for rec in source['positive_dimensional_families']+source['isolated_points']:
        eq=equations_for(rec['supporting_line_indices'],rows);key=canonical_equations(eq)
        assert key not in expected
        expressions=[list(map(F,x)) for x in rec['affine_expressions']]
        k=len(rec['free_variables']);o=[v[-1] for v in expressions];basis=[[v[j] for v in expressions] for j in range(k)]
        assert all(dot(n,o)==r and all(dot(n,v)==0 for v in basis) for n,r in eq)
        assert strict_feasible(o,basis)
        assert actual[key]['dimension']==k
        blind=common_blind(rec['supporting_line_indices'],rows)
        assert sorted(z[0] for z in blind)==sorted(tuple(map(F,p)) for p in rec['common_blind_boundary_points'])
        if k:
            assert k==1
            forms=[expressions[0],expressions[2],[x-y for x,y in zip(expressions[1],expressions[0])],[x-y for x,y in zip(expressions[3],expressions[2])]]
            lower=max((-c/v for v,c in forms if v>0),default=None);upper=min((-c/v for v,c in forms if v<0),default=None)
            assert [str(lower) if lower is not None else None,str(upper) if upper is not None else None]==rec['open_parameter_interval'];interval_checks+=1
            equal=any(expressions[i]==expressions[j] for i in (0,1) for j in (2,3))
            equality_families+=equal;blind_families+=bool(blind);residual_blind+=bool(blind) and not equal
        expected[key]=k
    assert actual.keys()==expected.keys()
    assert (sum(v['dimension']==1 for v in actual.values()),sum(v['dimension']==0 for v in actual.values()))==(90,288)
    assert (equality_families,blind_families,residual_blind)==(16,24,16)
    out={'status':'PASS','assignments':10000,**stats,'families':90,'isolated_points':288,'family_intervals_checked':interval_checks,'identically_equal_effective_depth_families':equality_families,'common_blind_families':blind_families,'non_equality_common_blind_families':residual_blind,'all_common_blind_sets_are_reported_singletons':True,'scope':'Ten critical lines only; mixed finite-point support and optical closure excluded.','source_sha256':{'unequal-depth/'+n:digest(PEER/n) for n in ('critical-rectangles.py','critical-rectangles.json','short-line-margin.json')}}
    (HERE/'critical-rectangles-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
