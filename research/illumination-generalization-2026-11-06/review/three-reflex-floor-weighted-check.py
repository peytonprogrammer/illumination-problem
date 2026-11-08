"""Independent FR02 weighted selector, six prescribed original-wall rays."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd
import json,hashlib
HERE=Path(__file__).parent;AUTHOR=HERE.parent/'construction';REQUEST=AUTHOR/'three-reflex-floor-weighted-review-request.json'
def pins():
 items=json.loads(REQUEST.read_text())['source_pins']
 for p in items:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p
 return items
before=pins();request_hash=hashlib.sha256(REQUEST.read_bytes()).hexdigest()
base=(HERE/'three-reflex-floor-return-check.py').read_text().split('\nrows=')[0]
changes={
 "and H==h+1 and d==2*P and D%2==0":"and d%2==0 and D%2==0",
 ' good=[]\n assert D.denominator==1':' epsilon=H-h;den=gcd(P,int(d)//2);a0=P//den;ell=(int(d)//2)//den\n assert a0%2 and gcd(epsilon*a0,N)==1\n good=[]\n assert D.denominator==1',
 'for index in range(int(D)):':'for index in range(P*int(D)):',
 'X0=z0+2*tau0':'X0=z0+C*tau0',
 'M0=int(shift)%N':'M0=(int(shift)*pow(epsilon*a0,-1,N))%N',
 'tau=tau0+e*M;X=z0+2*tau':'tau=tau0+e*a0*M;X=z0+C*tau',
 'n+=M;J=':'n+=ell*M;J=',
 'assert gcd(N*int(d2),L)==1;p=(-int(J)*pow(N*int(d2),-1,L))%L':'assert gcd(a0*N*int(d2),L)==1;p=(-int(J)*pow(a0*N*int(d2),-1,L))%L',
 'final=tau+2*e*N*p':'final=tau+2*e*a0*N*p',
 's+d*final-2*a*(n+2*N*p)==z0 and z0+2*final-(2*(m+2*p)+1)*A==z1 and z1+g1*final-2*e*(k+N*g1*p)==z2':'s+d*final-2*a*(n+2*ell*N*p)==z0 and z0+C*final-(2*(m+2*epsilon*a0*p)+1)*A==z1 and z1+g1*final-2*e*(k+N*g1*a0*p)==z2',
 'return dict(q=q,cap_M0=':'return dict(q=q,a0=a0,source_height=d,weighted_source_index_step=ell,source_bad_period=P*int(D)//gcd(int(d),P*int(D)),seed_search_common_period=P*int(D),good_seed_q=good,cap_M0='
}
for old,new in changes.items():
 assert base.count(old)==1,(old,base.count(old))
 base=base.replace(old,new)
ns={'__file__':str(HERE/'three-reflex-floor-return-check.py'),'__name__':'own_weighted_floor'}
exec(compile(base,'<own-weighted-floor-original-walls>','exec'),ns)
fixtures=[
 ('author-A-weighted-source3',4,3,4,11,1,3,6,8,(8,4),(36,2),0),
 ('existing-FR01-flip',2,2,4,7,1,3,4,5,(2,2),(10,2),0),
 ('same-A-lower-height2',4,3,4,11,1,3,6,8,(8,2),(36,2),0),
 ('same-A-mouth-height6',4,3,4,11,1,3,6,8,(8,6),(36,2),0),
 ('source-period2-nonempty',4,1,4,7,1,3,6,8,(2,4),(26,2),0),
 ('even-P-nonunit-depth-new-sourceheight',2,2,4,7,1,3,6,8,(2,4),(10,2),0)]
rows=[ns['family'](*f) for f in fixtures]
assert rows[0]['slope']==Q(299,4) and rows[0]['a0']==3 and rows[0]['cap_M']==6 and rows[0]['target_shift']==0
assert rows[1]['slope']==20 and rows[1]['N_flip_used'] and rows[1]['cap_M0']==2 and rows[1]['cap_M']==9
assert rows[4]['source_bad_period']==2 and 1 not in rows[4]['good_seed_q'] and rows[4]['slope']==Q(535,4)
assert rows[5]['a0']==1 and rows[5]['source_height']==8 and rows[5]['slope']==3
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_INDEPENDENT_FR02_WEIGHTED_ALL_LOWER_SOURCE_CONTROLS',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_pins_before','source_pins_after')}))
