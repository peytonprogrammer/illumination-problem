"""Independent replay of three prescribed equal-block controls; no discovery."""
from fractions import Fraction as Q
from pathlib import Path
from math import floor
import ast,json,hashlib

HERE=Path(__file__).parent
REQ=Path('.context/codex-proof-verification/specialist-ideas/terminal-resumption-2026-11-07/equal-block-review-request.json')
request=json.loads(REQ.read_text())
def pins():
    out=[]
    for p in request['source_pins']:
        actual=hashlib.sha256(Path(p['path']).read_bytes()).hexdigest();assert actual==p['sha256']
        out.append(dict(p,actual=actual,passed=True))
    return out
before=pins()
old=ast.parse((HERE/'resumed-exact-check.py').read_text())
ns={'Q':Q,'F':Q}
names={'vec','det','dot','edges','on','location','intersect','simple','path_check','fold'}
exec(compile(ast.Module(body=[f for f in old.body if isinstance(f,ast.FunctionDef)
    and f.name in names],type_ignores=[]),'<own-geometry>','exec'),ns)
old=ast.parse((HERE/'three-reflex-coprime-independent-check.py').read_text())
own={'Q':Q,'ns':ns}
exec(compile(ast.Module(body=[f for f in old.body if isinstance(f,ast.FunctionDef)
    and f.name=='replay_actual'],type_ignores=[]),'<own-prescribed-firsthit-replay>','exec'),own)

rows=[]
a=Q(4);N=5;L=3;b,c,h,H=1,4,6,7;S=(Q(2),Q(4));D=8;r=2
A=N*a;l=(N-L)*a;w=A-a
P=[(a,b),(a,h),(w,h),(w,c),(l,c),(l,0),(A,0),(A,H),(0,H),(0,b)]
for t in [10,12,16]:
    T=(Q(t),Q(2));s,u=S;z=A-T[0]
    forbidden=[[],[],[]];good=[]
    for q in range(D):
        tau=(A+z-s+2*a*q)/D
        phases=[s+r*tau,s+2*r*tau-A,s+3*r*tau-A]
        bad=[((x-a)/(2*a)).denominator==1 for x in phases]
        for i,v in enumerate(bad):
            if v:forbidden[i].append(q)
        if not any(bad):good.append(q)
    assert good
    if forbidden[1]:
        assert not forbidden[0]
        J=(s+z)/a;assert J.denominator==1 and (int(J)-N)%2==0
        assert 0<2*s/a<2
    q=good[-1];tau0=(A+z-s+2*a*q)/D
    n0=floor((s+r*tau0+a)/(2*a));z0=s+r*tau0-2*n0*a
    X0=z0+r*tau0
    M=(pow(r,-1,N)*((N-1)//2-floor(X0/(2*a))))%N
    tau=tau0+2*a*M;X=z0+r*tau;m=floor(X/(2*A));z1=X-(2*m+1)*A
    k=floor((z1+r*tau+a)/(2*a));z2=z1+r*tau-2*k*a
    assert max(abs(x) for x in (z0,z1,z2))<a
    J=(z2+r*tau-z)/(2*a);assert J.denominator==1
    shift=(-int(J)*pow(N*r,-1,L))%L
    corrected=tau+2*a*N*shift
    assert ns['fold'](z2+r*corrected,L*a)==z
    result=own['replay_actual'](P,S,T,corrected,D)
    rows.append(dict(S=S,T=T,q=q,cap_M=M,target_modulus=L,target_shift=shift,
        slope=corrected,forbidden=forbidden,**result))
assert any(row['forbidden'][1] for row in rows)
out=dict(status='PASS_INDEPENDENT_EQUAL_BLOCK_CONTROLS',source_pins_before=before,
    source_pins_after=pins(),request_sha256=hashlib.sha256(REQ.read_bytes()).hexdigest(),
    rows=rows,cases=len(rows),reflections=sum(row['reflections'] for row in rows),
    wall_leg_guards=sum(row['wall_leg_guards'] for row in rows),
    author_code_executed=False,discovery_search_used=False,
    full_general_bottom_theorem_reviewed=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['source_pins_before','source_pins_after','rows']}))
