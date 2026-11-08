"""Independent BOX1/BOX2 exact selection and prescribed physical replays.

Uses only earlier reviewer-owned pure geometry/replay functions. No author
execution, direction/room search, or discovery effort.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import floor, ceil, gcd
import ast, hashlib, json

HERE = Path(__file__).parent
AUTHOR = HERE.parent / 'construction'
REQUESTS = [AUTHOR / ('three-reflex-lower-joint-box' + suffix + '-review-request.json')
            for suffix in ['', '-divisibility']]

def pins():
    rows = []
    for request in REQUESTS:
        for pin in json.loads(request.read_text())['source_pins']:
            actual = hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
            assert actual == pin['sha256'], pin
            rows.append(dict(pin, actual=actual, passed=True))
    return rows

before = pins()
request_pins = [{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                for p in REQUESTS]
ns = {'Q': Q, 'F': Q}
text = (HERE / 'resumed-exact-check.py').read_text()
names = {'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[n for n in ast.parse(text).body
    if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[]),
    '<reviewer-pure-geometry>', 'exec'), ns)
text = (HERE / 'three-reflex-coprime-independent-check.py').read_text()
fn = next(n for n in ast.parse(text).body
          if isinstance(n, ast.FunctionDef) and n.name == 'replay_actual')
rns = {'Q': Q, 'ns': ns}
exec(compile(ast.get_source_segment(text, fn), '<reviewer-earliest-original-wall>', 'exec'), rns)

def select(e, N, L, b, c, h, H, S, T, tie='up', require_divisibility=True):
    e = Q(e); s, u = map(Q, S); t, v = map(Q, T)
    A = N*e; z = A-t
    assert 0<e<A-L*e<A-e<A and 0<b<c<h<H
    assert 0<s<e and b<u<h and A-L*e<t<A and 0<v<c
    assert N%2 and L>=2 and not L&(L-1) and h%2==0 and c%2
    assert u.denominator==v.denominator==1 and int(u)%2==int(v)%2==0
    a=Q(h-u,2); beta=H-h; f=Q(h-v,2); d=a+beta+f
    assert a.denominator==f.denominator==1 and a>0 and f>0
    a, f, d = int(a), int(f), int(d)
    if require_divisibility: assert (beta*s/e).denominator>1
    # Independent triangular elimination of r=lambda*vi+mu*vj gives these
    # two coefficients directly, avoiding the author's determinant inversion.
    la = -s/(2*e)-Q(a*N,2*beta)
    mu = z/(2*e)-Q(f*N,2*beta)
    near = (lambda x: floor(x+Q(1,2))) if tie=='up' else (lambda x: ceil(x-Q(1,2)))
    i, j, m = -near(la), -near(mu), 0
    M=gcd(gcd(a*N,beta),N*f)
    di, dm, dj = a*N//M, beta//M, N*f//M
    dq=di+N*dm+dj
    assert dq==N*d//M
    q=i+N*m+j
    kpos=max(0,ceil(Q(-i,di)),ceil(Q(-m,dm)),ceil(Q(-q,dq)))
    i+=di*kpos; m+=dm*kpos; j+=dj*kpos; q+=dq*kpos
    def chart(i,m,j,q):
        tau=(A+z-s+2*e*q)/(2*d)
        x=s+2*a*tau-2*e*i
        y=x+2*beta*tau-(2*m+1)*A
        assert tau>0 and i>=0 and m>=0 and q>=0 and abs(x)<e and abs(y)<e
        assert floor((s+2*a*tau+e)/(2*e))==i
        assert floor((x+2*beta*tau)/(2*A))==m
        Y=y+(h-c)*tau
        k=floor((Y+e)/(2*e)); w=Y-2*e*k
        return tau,x,y,k,w
    tau,x,y,k,w=chart(i,m,j,q)
    repair=abs(w)==e
    if repair:
        i+=di;m+=dm;j+=dj;q+=dq
        tau,x,y,k,w=chart(i,m,j,q)
    assert abs(w)<e
    assert Q((h-c)*N,2*M).denominator>1
    J=j-k; d2=int(c-v)
    assert w+d2*tau==z+2*e*J
    p=(-J*pow(N*d2,-1,L))%L
    final=tau+2*e*N*p
    fi=i+2*a*N*p;fm=m+2*beta*p;fk=k+(h-c)*N*p
    assert s+2*a*final-2*e*fi==x
    assert x+2*beta*final-(2*fm+1)*A==y
    assert y+(h-c)*final-2*e*fk==w
    E=w+d2*final
    assert (J+N*d2*p)%L==0 and ns['fold'](E,L*e)==z
    assert ((x+beta*final)/A).denominator>1
    polygon=[(e,b),(e,h),(A-e,h),(A-e,c),(A-L*e,c),
             (A-L*e,0),(A,0),(A,H),(0,H),(0,b)]
    replay=rns['replay_actual'](polygon,(s,u),(t,v),final,2*d)
    return dict(e=e,N=N,L=L,b=b,c=c,h=h,H=H,S=S,T=T,
                coefficients=[la,mu],tie=tie,positive_steps=kpos,
                source_divisibility=beta*s/e,repair=repair,
                final_slope=final,indices=[fi,fm,fk],residuals=[x,y,w],
                target_E=E,**replay)

# Fixed author controls, plus the SAME BOX1 input with the other consistent
# tie rule. This changes its seed and provides an independently selected ray.
rows=[
    select(4,9,4,1,3,6,9,(2,4),(24,2)),
    select(4,9,4,1,3,6,9,(2,4),(24,2),tie='down'),
    select(5,9,4,1,3,6,12,(2,4),(32,2))]
assert rows[0]['final_slope']==Q(467,6)
assert rows[2]['final_slope']==Q(281,3)
assert rows[0]['final_slope']!=rows[1]['final_slope']
out=dict(status='PASS_BOX1_BOX2_INDEPENDENT_SELECTION_AND_ACTUAL_WALLS',
         source_pins_before=before,source_pins_after=pins(),request_pins=request_pins,
         rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),
         wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
         author_code_executed=False,discovery_search_used=False,
         whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
