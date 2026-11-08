"""ER01 fixed two-parity actual earliest-wall replays; no discovery."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib
HERE=Path(__file__).parent
source=(HERE/'three-reflex-parity-free-floor-check.py').read_text()
prefix=source[:source.index('# Fixed author ordinary-floor calibration')]
prefix=prefix.replace('three-reflex-parity-free-floor-review-request.json',
    'three-reflex-equal-arm-obstruction-repair-review-request.json')
setup={'__file__':__file__};exec(compile(prefix,'<own-first-hit-floor-setup>','exec'),setup)
ns=setup['ns'];replay=setup['env']['replay_actual']
rows=[]
for n in (1,2):
    A=32*n;S=(2,4);T=(A-10,2)
    P=setup['polygon'](4,4,A,16,1,3,6,7)
    ns['simple'](P);assert ns['location'](P,S)==ns['location'](P,T)==1
    if n%2:
        tau=16*n-Q(20,7);i=16*n-3;k=6*n-1;D=14;horiz=2
        expected=[Q(22,7),-Q(18,7),-Q(22,7)]
    else:
        tau=16*n+Q(4,3);i=16*n+2;k=6*n;D=18;horiz=3
        expected=[-Q(10,3),-Q(2,3),Q(10,3)]
    z0=2+8*tau-8*i;z1=z0+2*tau-A;z2=z1+3*tau-8*k
    assert [z0,z1,z2]==expected and max(map(abs,expected))<4
    floor_phase=2+3*tau;floor_x=ns['fold'](floor_phase,4)
    roof_x=z0+tau;assert 0<floor_x<4 and 0<roof_x<A
    E=z2+(1 if n%2 else 5)*tau
    assert E%32==10 and ns['fold'](E,16)==10
    actual=replay(P,S,T,tau,D,initial_vy=Q(-1),horizontal_count=horiz)
    assert actual['roof']['point']==(roof_x,Q(7)) and actual['roof']['time']==9
    assert any(e['point']==(floor_x,Q(1)) and e['time']==3 for e in actual['events'])
    if not n%2:
        bottom_phase=z2+3*tau;bottom_x=A-ns['fold'](bottom_phase,16)
        assert ns['fold'](bottom_phase,16)==Q(22,3)
        assert any(e['point']==(bottom_x,Q(0)) and e['time']==16 for e in actual['events'])
        descending_phase=z2+tau
        assert descending_phase%32==Q(14,3) and ns['fold'](descending_phase,16)!=10
    rows.append(dict(n=n,S=S,T=T,slope=tau,indices=[i,0,k],
        residuals=expected,floor_x=floor_x,roof_x=roof_x,E=E,**actual))
assert setup['request_hash']==hashlib.sha256(setup['REQ'].read_bytes()).hexdigest()
out=dict(status='PASS_ER01_BOTH_PRESCRIBED_ORIGINAL_ROOM_PARITIES',rows=rows,
    source_pins_before=setup['before'],source_pins_after=setup['pins'](),
    request_sha256=setup['request_hash'],cases=2,
    reflections=sum(r['reflections'] for r in rows),
    wall_leg_guards=sum(r['wall_leg_guards'] for r in rows),
    author_code_executed=False,discovery_search_used=False,
    all_n_from_hand_algebra_not_samples=True,whole_native_pair_family_claim=False,
    whole_r3_complete=False,whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','source_pins_before','source_pins_after']}))
