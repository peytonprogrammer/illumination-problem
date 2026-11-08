"""LJ05 prescribed actual-ray challenge using only reviewer-owned algebra."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm
import ast,json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-lower-residue-transport-review-request.json'
def pins():
 rows=[]
 for pin in json.loads(REQ.read_text())['source_pins']:
  actual=hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
  assert actual==pin['sha256'];rows.append(dict(pin,actual=actual,passed=True))
 return rows
before=pins();request_hash=hashlib.sha256(REQ.read_bytes()).hexdigest()
source=(HERE/'three-reflex-lower-equal-arm-check.py').read_text()
env={'__file__':__file__}
exec(compile(source.split('\ndef check')[0].split('before=pins()')[0],'<imports-only>','exec'),env)
# Initialize only the pure geometry/replay portion of the own earlier checker.
prefix=source[source.index("ns={'Q':Q,'F':Q}"):source.index('\ndef check')]
exec(compile(prefix,'<reviewer-pure-geometry>','exec'),env)
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='check')
code=ast.get_source_segment(source,fn)
code=code.replace('e,P,N,L,b,c,h,H,S,T','e,P,K,N,L,b,c,h,H,S,T')
code=code.replace('R=a;B=L*e','R=K*e;B=L*e')
code=code.replace('assert P<L','assert P<=K<L')
code=code.replace('tau,x,y,k,w=state();repair=abs(w)==R',
 '''assert f%2 and hh%2 and dj%2
    Lam=lcm(P,N,K);Gamma=gcd(Lam*int(c-v),L)
    assert Gamma%gcd(P,Gamma)==0 and K%Gamma==0
    rho=Gamma//gcd(P,Gamma)
    ell=0 if rho==1 else (-j*pow(dj,-1,rho))%rho
    i+=di*ell;m+=dm*ell;j+=dj*ell;q+=dq*ell
    assert j%rho==0
    tau,x,y,k,w=state();repair=abs(w)==R''')
code=code.replace('i+=di;m+=dm;j+=dj;q+=dq;tau,x,y,k,w=state()',
 'i+=di*rho;m+=dm*rho;j+=dj*rho;q+=dq*rho;tau,x,y,k,w=state()')
code=code.replace('Q((h-c)*N,2*hh).denominator>1',
 '(Q((h-c)*P*N*rho,2*K*hh)).denominator>1')
code=code.replace('J=P*(j-k);Lam=lcm(P,N);Gamma=gcd(Lam*int(c-v),L)',
 'J=P*j-K*k;Lam=lcm(P,N,K);Gamma=gcd(Lam*int(c-v),L)')
code=code.replace('assert P%Gamma==0 and J%Gamma==0','assert J%Gamma==0')
code=code.replace('fk=k+(h-c)*Lam*p//P','fk=k+(h-c)*Lam*p//K')
code=code.replace('Gamma=Gamma,J=J,p=p','Gamma=Gamma,rho=rho,null_target_steps=ell,J=J,p=p')
exec(compile(code,'<own-exact-residue-transport>','exec'),env)
rows=[env['check']('author-Gamma4-P3',2,3,4,13,8,1,3,8,14,(2,6),(20,2),Q(7047,10)),
      env['check']('even-P2-Gamma4-smooth-cap-zero',2,2,4,11,8,1,3,8,14,(2,6),(10,2),Q(178))]
assert rows[0]['null_target_steps']==1 and rows[0]['p']==1
assert rows[1]['rho']==2 and rows[1]['residuals'][1]==0 and rows[1]['p']==1
assert request_hash==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_LJ05_ODD_F_GENERAL_SOURCE_RESIDUE_AND_ACTUAL_RAYS',
 source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,
 rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),
 wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,
 discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
