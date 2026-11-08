"""Prescribed exact residue-table identities for EQROOF01; no ray search."""
from fractions import Fraction as Q
from math import floor
from pathlib import Path
import json
def centered(x):return x-8*floor((x+4)/8)
expected={
    (1,0):([-1,0,2],2),
    (-1,0):([-2,0,1],-2),
    (1,1):([Q(-1,2),Q(3,2)],-2),
    (-1,1):([Q(-3,2),Q(1,2)],2),
}
rows=[]
for (sign,half),(deltas,Eoffset) in expected.items():
    # The proof forces |delta|<4 and delta in (1/2)Z: these 15 classes
    # exhaust a derived finite set, not a cutoff on physical ray length.
    allowed=[]
    for k in range(-7,8):
        delta=Q(k,2)
        if (k%2)!=half:continue
        z0=centered(2*sign+2*delta);z1=z0+2*delta
        if abs(z0)==4 or abs(z1)>=4:continue
        allowed.append(delta)
    assert allowed==list(map(Q,deltas))
    for delta in allowed:
        z0=centered(2*sign+2*delta);z1=z0+2*delta
        z2=centered(z1+3*delta)
        assert max(abs(z0),abs(z1),abs(z2))<4
        assert delta+z2==Eoffset
        rows.append(dict(source_sign=sign,delta=delta,z0=z0,z1=z1,z2=z2,
            E_minus_Q=Eoffset))
assert len(rows)==10
parities=[]
for nparity in (0,1):
    phases={(16*nparity+r['E_minus_Q'])%32 for r in rows}
    assert not phases.intersection({10,22})
    folded={min(x,32-x) for x in phases}
    assert folded==({2} if nparity==0 else {14})
    parities.append(dict(n_mod2=nparity,possible_E_mod32=sorted(phases),
        folded_bottom_distance=sorted(folded),target_images_excluded=[10,22]))
out=dict(status='PASS_EQROOF01_EXACT_FORCED_RESIDUE_TABLE',rows=rows,
    parity_cases=parities,derived_finite_classes=15,source_signs=2,
    physical_ray_search=False,room_search=False,author_code_executed=False,
    no_legal_one_roof_path=True,darkness_claim=False,independent_review_pending=True,
    whole_goal_complete=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2,default=str)+'\n')
print('PASS: all 10 strict table entries; both n parities exclude BOTH target images')
