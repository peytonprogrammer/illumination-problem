"""Independent finite proof-table, Fourier algebra and actual-wall checks.
No peer program imports/execution. Universal analysis is in centered-review.md.
"""
from fractions import Fraction as F
from pathlib import Path
from math import gcd
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
spec=spec_from_file_location('own_geometry',BASE/'arbitrary-endpoints-independent/check.py')
G=module_from_spec(spec);spec.loader.exec_module(G)
LINES=['beta=3alpha','3alpha+beta=2','alpha+3beta=2','3beta-alpha=2']

def pair(line,z):
    if line==LINES[0]:return z,3*z
    if line==LINES[1]:return z,2-3*z
    if line==LINES[2]:return 2-3*z,z
    return 3*z-2,z

def csign(z):
    r=z%2
    if r in (F(1,2),F(3,2)):return 0
    return -1 if F(1,2)<r<F(3,2) else 1

def positive(n,al,be):return (n*al)%1!=0 and (n*be)%1!=0 and csign(n*al)*csign(n*be)>0

def path(al,be,n):
    if not 1<(1+2*n*al)%4<3:n=-n
    e1=(1+2*n*al)%4;e2=(1+2*n*be)%4
    assert 1<e1<3 and e1!=2
    c=1 if e1<2 else 3
    if c==1:
        assert 0<e2<2 and e2!=1;u=2 if e2<1 else 0
    else:
        assert 2<e2<4 and e2!=3;u=0 if e2<3 else 2
    L=1+2*n;eps=1 if (L-u)%4==1 else -1
    M=(L-u-eps)//4;assert L==u+eps+4*M
    a,b=al/(be-al),(1-be)/(be-al)
    P,_=G.chart_path(F(1),F(1),a,b,F(1),F(1),M,F(c),F(u),eps)
    return P,a,b

def main():
    sources=['unequal-depth/centered-theorem.md','unequal-depth/centered-check.py','unequal-depth/centered-check.json','unequal-depth/midpoint-repair.md','unequal-depth-independent/repair-acceptance.json','unequal-depth-independent/vertical-completeness-review.md','arbitrary-endpoints-independent/check.py']
    pins={r:hashlib.sha256((BASE/r).read_bytes()).hexdigest() for r in sources}
    # Independently expand (cos(t)-cos(3t))/4 in exponentials, then multiply.
    f={1:F(1,8),-1:F(1,8),3:F(-1,8),-3:F(-1,8)}
    fourier={(m,n):x*y for m,x in f.items() for n,y in f.items()}
    assert len(fourier)==16 and set(fourier.values())=={F(1,64),F(-1,64)}
    assert sum(fourier.values())==0 # C_0=0, independent algebra check
    cosine={}
    for (m,n),c in fourier.items():
        key=(m,n) if m>0 else (-m,-n)
        cosine[key]=cosine.get(key,F(0))+c
    expected={(1,1):1,(1,-1):1,(3,3):1,(3,-3):1,(1,3):-1,(1,-3):-1,(3,1):-1,(3,-1):-1}
    assert cosine=={k:F(v,32) for k,v in expected.items()}
    rows=[];fails=set();physical=[];contacts=0
    def physical_checks(P,a,b,kind):
        nonlocal contacts
        n=G.verify(P,F(1),F(1),a,b,F(1),F(1),a+F(1,10**6),b+F(1,10**6))
        d,g=F(7,3),F(2,5);Q=[(d*x,g*y) for x,y in P]
        assert G.verify(Q,d,g,a*g,b*g,d,d,a*g+F(1,10**6),b*g+F(1,10**6))==n
        Q=[(x,1-y) for x,y in P[::-1]]
        assert G.verify(Q,F(1),F(1),b,a,F(1),F(1),b+1,a+2)==n
        contacts+=3*n;physical.append({'kind':kind,'a':str(a),'b':str(b),'contacts_per_path':n,'paths':3})
    for q in range(2,13):
        for p in range(1,q):
            if gcd(p,q)!=1:continue
            z=F(p,q)
            for line in LINES:
                al,be=pair(line,z)
                if not 0<al<be<1 or F(1,2) in (al,be):continue
                values=[positive(n,al,be) for n in range(2*q)]
                assert values==[positive(n,z,3*z) for n in range(2*q)]
                witness=next((i for i,x in enumerate(values) if x),None)
                if witness is None:fails.add((al,be))
                else:
                    P,a,b=path(al,be,witness);physical_checks(P,a,b,'finite residual row')
                rows.append({'line':line,'p':p,'q':q,'alpha':str(al),'beta':str(be),'witness_n':witness})
    assert len(rows)==40
    assert fails=={(F(1,4),F(3,4)),(F(1,5),F(3,5)),(F(2,5),F(4,5))}
    parent=json.loads((BASE/'unequal-depth/centered-check.json').read_text())
    fields=['line','p','q','alpha','beta','witness_n']
    assert rows==[{k:r[k] for k in fields} for r in parent['rows']]
    # Independently reconcile every entry in the WRITTEN hand-proof table.
    text=(BASE/'unequal-depth/centered-theorem.md').read_text();printed={}
    for line in text.splitlines():
        fields=line.split('|')
        if len(fields)>=4 and fields[1] in LINES:
            for entry in fields[2].split(';'):
                z,n=entry.strip().split(':');printed[(fields[1],F(z))]=None if n in ('–','—','-') else int(n)
    assert printed=={(r['line'],F(r['p'],r['q'])):r['witness_n'] for r in rows}
    # Constructive grid representative, exact controls of the general proof.
    grid=0
    for q in (13,17,32):
        for p in range(1,q):
            if gcd(p,q)!=1:continue
            if p%2:n=pow(p,-1,2*q);r=F(1,q)
            else:n=pow(p//2,-1,q);r=F(2,q)
            assert (n*F(p,q))%2==r and 0<r<F(1,6)
            assert positive(n,F(p,q),3*F(p,q));grid+=1
    for a,b in [(F(1,2),F(1,2)),(F(1,2),F(1)),(F(1),F(1,2))]:
        v=4/(a+b+3);ps=1+(a+1)*v;pt=1+(b+1)*v;eta=1-(3-ps)/v
        assert 1<1+a*v<2 and 1<1+b*v<2 and 2<ps<3 and 2<pt<3 and 0<eta<1
        assert ps+pt+v==6
        P=[(F(1),-a),(ps,F(1)),(F(3),eta),(pt,F(0)),(F(1),1+b)]
        physical_checks(P,a,b,'isolated repair')
    for a,b,n in [(F(1),F(3),1),(F(3),F(1),1),(F(7,10),F(4,5),2)]:
        al=a/(a+1+b);be=(a+1)/(a+1+b);assert positive(n,al,be)
        P,aa,bb=path(al,be,n);assert (a,b)==(aa,bb);physical_checks(P,a,b,'off-line prescribed chart')
    K=G.K;al=K((0,F(1,10),0,0));be=K((0,0,F(1,4),0))
    a,b=al/(be-al),(1-be)/(be-al);d=g=K(1)
    assert 0<al<be<K(F(1,2))
    P,_=G.chart_path(d,g,a,b,d,d,1,d,K(0),-1)
    assert G.verify(P,d,g,a,b,d,d,a+1,b+1,K)==1
    Q=[(x,1-y) for x,y in P[::-1]];assert G.verify(Q,d,g,b,a,d,d,b+1,a+1,K)==1
    contacts+=2
    for n,h in pins.items():assert hashlib.sha256((BASE/n).read_bytes()).hexdigest()==h,n
    pins['unequal-depth-independent/centered-check.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out={'status':'INDEPENDENT_CENTERED_CHECKS_PASS','fourier_exponential_coefficients':16,'cosine_terms':8,'finite_proof_table_rows':len(rows),'finite_table_failures':[[str(x),str(y)] for x,y in sorted(fails)],'written_proof_table_reconciled':True,'large_q_grid_formula_controls':grid,'actual_paths':3*len(physical)+2,'wall_contacts':contacts,'exact_irrational_paths':2,'source_sha256':pins,'rows':rows,'physical':physical,'limits':'Finite proof table after hand universal reduction, and prescribed actual-wall controls. No discovery extrapolation or arbitrary-horizontal theorem.'}
    (HERE/'centered-check.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('rows','physical','source_sha256')}))
if __name__=='__main__':main()
