"""Independent paired-image half-grid selector and prescribed actual rays."""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json
HERE=Path(__file__).parent;AUTHOR=HERE.parent/'construction';REQUEST=AUTHOR/'three-reflex-coprime-extension-halfgrid-review-request.json'
def pins():
 items=json.loads(REQUEST.read_text())['source_pins']
 for p in items:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'],p
 return items
before=pins();request_hash=hashlib.sha256(REQUEST.read_bytes()).hexdigest()
# Reuse the reviewer's exact reduced-grid constructor, not author code.
base=(HERE/'three-reflex-coprime-reduced-grid-check.py').read_text().split('\nfixtures=')[0]
env={'__file__':str(HERE/'three-reflex-coprime-reduced-grid-check.py'),'__name__':'own_reduced_grid_dependency'}
exec(compile(base,'<own-reduced-grid-formulas>','exec'),env)
source=env['source']
changes={
 '2<=K<L':'1<=K<L',
 'assert P%g==0 and K%g==0 and K>=2*g':'assert P%g==0 and K==g;paired=2*z/(e*g);assert paired.denominator==1 and int(paired)%2==1',
 'ep=e*g;Pp=P//g;Kp=K//g':'ep=e*g/2;Pp=2*P//g;Kp=2',
 'q=residue+g*j':'q=residue+Q(g,2)*j',
 'assert (q_fixed-residue)%g==0;j=(q_fixed-residue)//g;assert j in good':'jj=2*(Q(q_fixed)-residue)/g;assert jj.denominator==1;j=int(jj);assert j in good',
 'J=(z2+d2*tau-z)/(2*e);assert J.denominator==1;initialJ=int(J)':'J=(z2+d2*tau-z)/(2*e);assert (2*J/g).denominator==1;initialJ=J;targetsign=1 if (J/g).denominator==1 else -1;I=J if targetsign==1 else J+z/e;assert I.denominator==1 and (I/g).denominator==1;initialI=int(I)',
 'assert int(J)%g==0;mod=L//g;p=0 if mod==1 else (-int(J)//g*pow(Lam*d2//g,-1,mod))%mod':'mod=L//g;p=0 if mod==1 else (-int(I)//g*pow(Lam*d2//g,-1,mod))%mod',
 'E=z2+d2*tau;J=(E-z)/(2*e);assert J.denominator==1 and int(J)%L==0 and ns[\'fold\'](E,L*e)==z':'E=z2+d2*tau;J=(E-z)/(2*e);Iend=(E-targetsign*z)/(2*e);assert Iend.denominator==1 and int(Iend)%L==0 and ns[\'fold\'](E,L*e)==z',
 'finalJ=int(J)':'finalJ=J,initial_target_index=initialI,final_target_index=int(Iend),selected_target_sign=targetsign'
}
for old,new in changes.items():
 assert source.count(old)==1,(old,source.count(old))
 source=source.replace(old,new)
ns={'__file__':str(HERE/'three-reflex-coprime-source-width-check.py'),'__name__':'own_halfgrid_actual_target','ceil':env['ceil']}
exec(compile(source,'<own-LC04-paired-target-grid>','exec'),ns)
fixtures=[
 ('author-A-native-K1-upper',4,3,1,4,9,1,3,5,7,(6,6),(30,2),Q(7,2)),
 ('author-B-native-K1-lower',4,3,1,4,9,1,3,5,7,(6,4),(30,2),21),
 ('author-C-regular-mouth',4,3,1,4,9,1,3,5,7,(6,5),(30,2),Q(37,2)),
 ('author-D-native-g2',2,2,2,4,7,1,3,6,9,(2,4),(8,2),16),
 ('same-A-deeper-source',4,3,1,4,9,1,3,5,7,(6,2),(30,2)),
 ('same-D-upper-g2-source',2,2,2,4,7,1,3,6,9,(2,8),(8,2))]
rows=[ns['ray'](*f) for f in fixtures]
assert [r['slope'] for r in rows[:4]]==[Q(464,3),Q(339,2),Q(184,7),Q(41,6)]
assert [r['selected_target_sign'] for r in rows[:4]]==[-1,1,-1,-1]
assert [r['initialJ'] for r in rows[:4]]==[Q(1,2),2,Q(5,2),1]
assert [r['initial_target_index'] for r in rows[:4]]==[2,2,4,4]
assert [r['jstar'] for r in rows[:4]]==[8,43,38,17]
assert request_hash==hashlib.sha256(REQUEST.read_bytes()).hexdigest()
out=dict(status='PASS_INDEPENDENT_LC04_HALFGRID_TARGET_IMAGE_ACTUAL_RAYS',source_pins_before=before,source_pins_after=pins(),request_sha256=request_hash,rows=rows,cases=len(rows),reflections=sum(r['reflections'] for r in rows),wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),author_code_executed=False,discovery_search_used=False,whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('rows','source_pins_before','source_pins_after')}))
