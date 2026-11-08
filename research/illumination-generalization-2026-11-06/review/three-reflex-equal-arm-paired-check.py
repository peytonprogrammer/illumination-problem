"""EA05 two prescribed actual targets, both full folded target images."""
from pathlib import Path
from fractions import Fraction as Q
import ast,json,hashlib
HERE=Path(__file__).parent
REQ=HERE.parent/'construction/three-reflex-equal-arm-paired-review-request.json'
def pins():
 rows=[]
 for pin in json.loads(REQ.read_text())['source_pins']:
  digest=hashlib.sha256(Path(pin['path']).read_bytes()).hexdigest()
  assert digest==pin['sha256'];rows.append(dict(pin,actual=digest,passed=True))
 return rows
before=pins();request_hash=hashlib.sha256(REQ.read_bytes()).hexdigest()
def v2(n):
 out=0
 while n%2==0:out+=1;n//=2
 return out
source=(HERE/'three-reflex-lower-equal-arm-check.py').read_text()
env={'__file__':__file__,'v2':v2}
prefix=source.split('\ndef check')[0]
prefix=prefix[:prefix.index('REQUEST=')]+prefix[prefix.index("ns={'Q':Q,'F':Q}"):]
exec(compile(prefix,'<own-original-wall-setup>','exec'),env)
fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='check')
code=ast.get_source_segment(source,fn)
code=code.replace('and N%2 and h%2==0','and v2(N)==v2(P)+1 and h%2==0')
code=code.replace('al=int((h-u)/2);be=H-h;f=int((h-v)/2);d=al+be+f',
 'al=int((h-u)/2);be=H-h;f=int((h-v)/2);d=al+be+f\n    assert P&(P-1)==0 and L>=4*P and be%2==0')
code=code.replace('di,dm,dj=N*al//hh,P*be//hh,N*f//hh;dq=P*di+N*dm+P*dj',
 'di,dm,dj=N*al//hh,P*be//hh,N*f//hh;dq=P*di+N*dm+P*dj\n    assert v2(hh)>=v2(N)')
code=code.replace('assert P%Gamma==0 and J%Gamma==0',
 '''assert Gamma==2*P
    Z=z/(e*P);assert Z.denominator==1 and int(Z)%2
    target_sign=1 if (J//P)%2==0 else -1
    target_index=Q(J) if target_sign==1 else J+z/e
    assert target_index.denominator==1 and int(target_index)%Gamma==0''')
code=code.replace('(-J//Gamma*pow(Lam*int(c-v)//Gamma,-1,mod))%mod',
 '(-int(target_index)//Gamma*pow(Lam*int(c-v)//Gamma,-1,mod))%mod')
code=code.replace("roof=x+be*final;assert (roof/A).denominator>1",
 '''E=w+(c-v)*final
    assert ((E-target_sign*z)/(2*L*e)).denominator==1
    roof=x+be*final;assert (roof/A).denominator>1''')
code=code.replace('Gamma=Gamma,J=J,p=p','Gamma=Gamma,J=J,target_sign=target_sign,target_index=target_index,p=p')
exec(compile(code,'<own-actual-paired-target-selector>','exec'),env)
rows=[env['check']('EA05-negative-actual-target-image',4,1,6,4,1,3,6,8,(2,4),(12,2),Q(269,5)),
      env['check']('EA05-positive-actual-target-image',4,1,6,4,1,3,6,8,(2,4),(20,2),Q(29,5))]
assert rows[0]['target_sign']==-1 and rows[0]['target_index']==2 and rows[0]['p']==1
assert rows[0]['indices']==[14,4,20] and rows[0]['roof']['point']==(Q(46,5),Q(8))
assert rows[1]['target_sign']==1 and rows[1]['target_index']==0 and rows[1]['p']==0
assert request_hash==hashlib.sha256(REQ.read_bytes()).hexdigest()
out=dict(status='PASS_EA05_BOTH_ACTUAL_TARGET_IMAGE_BRANCHES_FULL_PERIOD',
 source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,
 rows=rows,cases=2,reflections=sum(row['reflections'] for row in rows),
 wall_leg_guards=sum(row['wall_leg_guards'] for row in rows),
 author_code_executed=False,discovery_search_used=False,
 whole_native_room_claim=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
