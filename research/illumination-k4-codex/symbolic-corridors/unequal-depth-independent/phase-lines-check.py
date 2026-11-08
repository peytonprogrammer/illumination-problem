"""Independent exact polygon-arrangement proof of the 30 affine covers.
No discovery or parent execution. Whole-cell sign constancy is hand-reviewed.
"""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
from itertools import product
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
V=[(F(0),F(0)),(F(1),F(0)),(F(1),F(1))]
BOXES=[(0,1,(1,2),(1,2)),(0,3,(2,3),(2,3)),(2,1,(1,2),(0,1)),(2,3,(2,3),(3,4))]

def val(line,p):return line[0]*p[0]+line[1]*p[1]+line[2]
def linekey(g):
    x=next(z for z in g if z);return tuple(z/x for z in g)
def area(P):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(P,P[1:]+P[:1])))
def clip(P,L,sign):
    out=[]
    for a,b in zip(P,P[1:]+P[:1]):
        va,vb=sign*val(L,a),sign*val(L,b)
        if va>=0:out.append(a)
        if (va<0<vb) or (vb<0<va):
            z=va/(va-vb);out.append(tuple(x+z*(y-x) for x,y in zip(a,b)))
    clean=[]
    for p in out:
        if not clean or p!=clean[-1]:clean.append(p)
    if len(clean)>1 and clean[0]==clean[-1]:clean.pop()
    return clean if len(clean)>=3 and area(clean)>0 else []

def triples():
    normals={(m,n) for m,n in product(range(-4,5),repeat=2) if 0<abs(m)+abs(n)<=4 and (m>0 or m==0<n)}
    out=[]
    for m,n in sorted(normals):
        lo,hi=min(0,n,m+n),max(0,n,m+n)
        for r in range(lo+1,hi):
            if gcd(gcd(abs(m),abs(n)),abs(r))==1:out.append((m,n,r))
    return out

def clauses(m,n,r):
    out=[]
    for u,c,I,J in BOXES:
        lo=sum(min(z*a,z*b) for z,(a,b) in [(m,I),(n,J)])
        hi=sum(max(z*a,z*b) for z,(a,b) in [(m,I),(n,J)])
        assert hi-lo==abs(m)+abs(n)
        for eps in (1,-1):
            C=(F(m+n-r),F(r*eps),F(r*u))
            # Independent universal bound: |C|<=16, |mx+ny|<16 => |k|<8.
            for k in range(-7,8):
                gs=[(C[0],C[1],C[2]+4*k-lo),(-C[0],-C[1],hi-C[2]-4*k)]
                if any(max(val(g,p) for p in V)<=0 for g in gs):continue
                out.append((u,c,eps,k,gs))
    return out

def check_relation(m,n,r):
    cs=clauses(m,n,r)
    lines=sorted({linekey(g) for u,c,e,k,gs in cs for g in gs if g[0] or g[1]})
    cells=[V]
    for L in lines:
        pieces=[]
        for P in cells:
            pieces.extend(Q for Q in (clip(P,L,1),clip(P,L,-1)) if Q)
        cells=pieces
    representatives=set();faces=0
    for P in cells:
        # Strict convex combination lies in the open two-dimensional cell.
        representatives.add((sum(p[0] for p in P)/len(P),sum(p[1] for p in P)/len(P)));faces+=1
        for a,b in zip(P,P[1:]+P[:1]):
            representatives.add(a)
            representatives.add(tuple((x+y)/2 for x,y in zip(a,b)))
    bad=set();tested=0
    for s,t in representatives:
        if not 0<t<=s<=1:continue
        tested+=1
        if not any(all(val(g,(s,t))>0 for g in gs) for u,c,e,k,gs in cs):bad.add((s,t))
    expected={(F(1),F(1))} if (m,n,r) in [(0,2,1),(2,0,1)] else set()
    assert bad==expected,((m,n,r),bad)
    # Every potential interval witness preserved by endpoint reversal maps to
    # another enumerated primitive short relation after a sign normalization.
    mm,nn,rr=-n,-m,r-m-n
    if mm<0 or mm==0 and nn<0:mm,nn,rr=-mm,-nn,-rr
    assert (mm,nn,rr) in triples()
    return {'relation':[m,n,r],'clauses':len(cs),'guard_lines':len(lines),'open_faces':faces,'domain_representatives':tested,'uncovered':[[str(s),str(t)] for s,t in sorted(bad)]}

def egcd(a,b):
    if not b:return abs(a),(1 if a>=0 else -1),0
    g,x,y=egcd(b,a%b);return g,y,x-(a//b)*y

def main():
    sources=['unequal-depth/phase-lines.md','unequal-depth/phase-lines-check.py','unequal-depth/phase-lines-check.json','unequal-depth-independent/centered-acceptance.json','unequal-depth-independent/midpoint-review.md','arbitrary-endpoints-independent/acceptance.json']
    pins={r:hashlib.sha256((BASE/r).read_bytes()).hexdigest() for r in sources}
    T=triples();assert len(T)==30
    rows=[check_relation(*t) for t in T]
    parent=json.loads((BASE/'unequal-depth/phase-lines-check.json').read_text())
    pdata={tuple(r['relation']):r for r in parent['results']}
    assert set(pdata)==set(T)
    for r in rows:
        old=pdata[tuple(r['relation'])]
        assert r['clauses']==old['clauses'] and r['uncovered']==old['uncovered']
    # Reconcile the COMPLETE displayed table in the hand argument.
    printed={}
    for line in (BASE/'unequal-depth/phase-lines.md').read_text().splitlines():
        a=line.split('|')
        if len(a)<5 or ',' not in a[1]:continue
        try:m,n=map(int,a[1].split(','));rs=list(map(int,a[2].split(',')))
        except ValueError:continue
        for r in rs:printed[(m,n,r)]=a[3].strip()
    assert set(printed)==set(T)
    for r in rows:assert (printed[tuple(r['relation'])]=='empty')==(not r['uncovered'])
    for m,n,r in T:
        g=gcd(abs(m),abs(n));m0,n0=m//g,n//g
        h,p,q=egcd(m0,n0);assert h==1 and m0*p+n0*q==1
        assert gcd(g,abs(r))==1
        # U=((m0,n0),(-q,p)) has determinant1: includes disconnected kernels.
        assert m0*p+n0*q==1
        residues={(j*r)%g for j in range(g)};assert residues==set(range(g))
    for rel,h in pins.items():assert hashlib.sha256((BASE/rel).read_bytes()).hexdigest()==h,rel
    pins['unequal-depth-independent/phase-lines-check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'INDEPENDENT_CONTINUOUS_AFFINE_COVERS_PASS','primitive_relations':len(rows),'covered_rows':28,'exceptional_rows':2,'open_polygon_faces':sum(r['open_faces'] for r in rows),'tested_sign_cell_representatives':sum(r['domain_representatives'] for r in rows),'method':'Incremental rational polygon half-plane arrangement; test all open faces, edges and vertices, not parent vertical slabs','written_table_reconciled':True,'reversal_closed':True,'source_sha256':pins,'results':rows,'limits':'Complete finite affine proof after the hand irrational-orbit reduction. Counts are sign-cell certificates, not sampled rays or rational-orbit coverage. No peer execution or discovery.'}
    (HERE/'phase-lines-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('results','source_sha256')}))
if __name__=='__main__':main()
