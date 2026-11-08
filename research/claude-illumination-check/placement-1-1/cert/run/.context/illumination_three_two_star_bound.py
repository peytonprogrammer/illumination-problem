"""Complete necessary supports for two full A stars / exactly3 B/C exceptions.

W=14+Q-E<=23, E+m<=6, Q>=2P-6+m give 2(P+m)<=21, hence
P+m<=10. For distance D>=3 the required external neighborhood has b=8;
a connection needs D-3 outside cells, of which <=10-b=2 exist. Thus D<=5.
All occupied cells lie within radius10-b of the mandatory neighborhood.
"""
import json
from pathlib import Path
from illumination_family_bound import support
from illumination_transparent_bound import counts
from illumination_geometry import label

BASE=Path(__file__).parent
TARGETS=tuple((x,n-x) for n in range(2,6) for x in range((n+1)//2,n+1))


def complete_support(target):
    assert tuple(target) in TARGETS
    return support(target,10)


def validate(room,target):
    c=counts(room)
    assert c['interior_A']==2 and c['interior_nonA']+c['smooth_boundary_nonA']==3
    assert c['walls']<=23 and c['triangles']<=36
    assert room['marked']==[[0,0],[2*v for v in target]]
    used={(p[0]//2,p[1]//2) for t in room['triangles'] for p in t if label(p)=='A'}
    bounded=complete_support(target);m=len(bounded['mandatory']-used);P=len(used)-2
    assert m<=3 and c['defect_credit']+m<=6
    assert c['charge']>=2*P-6+m and P+m<=10
    assert used<=bounded['allowed']
    return dict(c,missing_mandatory_cells=m,partial_cells=P)


if __name__=='__main__':
    results=[dict(target_A_cell=t,required_partial_cells=complete_support(t)['partial_required'],
                  extra_A_cell_radius=complete_support(t)['extra_budget'],
                  available_A_cells=len(complete_support(t)['allowed'])) for t in TARGETS]
    data=dict(status='NECESSARY_REDUCTION',maximum_triangles=36,maximum_partial_plus_missing=10,
              maximum_mark_Manhattan_distance=5,cases=results,
              scope='I=2, exactly3 exceptions, simple canonical45-degree rooms with interior A marks and <=23 walls. No feasibility or darkness claim.')
    (BASE/'three-two-star'/'bounds.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data))
