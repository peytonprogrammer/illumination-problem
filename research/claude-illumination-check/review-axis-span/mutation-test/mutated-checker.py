"""One frozen room's existing axis-period forms; no cylinder/path discovery."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
b=Path(__file__).resolve().parent
pins={'coupling.json':'9f81b7bf93b258958fa3d6347631e50f8165e57ad32166547431a3be9ed26bec',
 'twist-action.json':'b500e3b59ba262a81655d60441f31d6c7da74e022d308761f171cc7459f81e27',
 'twist-pf.json':'0bbe693ff7e0e3e9a47541a253027cb433e6b301b52c152a469289356c71fd92'}
for name,h in pins.items():assert hashlib.sha256((b/name).read_bytes()).hexdigest()==h
c=json.loads((b/'coupling.json').read_text());a=json.loads((b/'twist-action.json').read_text())
assert c['tag']=='parity-W25-24'
vertices=c['room']['vertices'];assert vertices[1:6]==[[1,0],[1,1],[2,2],[1,2],[1,3]]
assert c['offset_normals'][1]==c['offset_normals'][4]==[-1,0]
dim=c['offset_dimension'];forms=[]
assert len(c['offset_normals'])==c['walls']==dim-4
assert F(c['offset_base_point'][1])==F(c['offset_base_point'][4])==-1
for orientation in ['horizontal','vertical']:
 for core in a['core_period_derivatives'][orientation]:
  assert len(core)==2 and all(len(row)==dim for row in core)
  assert all(isinstance(x,(int,str)) and not isinstance(x,bool) for row in core for x in row)
  forms.append([F(x) for row in core for x in row])
assert len(forms)==40
saved_pf=json.loads((b/'twist-pf.json').read_text())
pf=next(room for room in saved_pf['rooms'] if room['tag']==c['tag'])
assert pf['horizontal_rows']==pf['vertical_columns']==20
assert sum(pf['row_widths'])==sum(pf['column_lengths'])==pf['squares']==112
assert [sum(row) for row in pf['intersection_matrix']]==pf['row_widths']
assert [sum(row[j] for row in pf['intersection_matrix']) for j in range(20)]==pf['column_lengths']
# Completeness is inherited from the frozen cycles(r)/cycles(u) construction;
# the current audit does not rebuild an origami or enumerate any cylinder.

# b0 = alpha - V alpha with endpoints on the two flank lines. Hence
# hol(b0)=(2*(c1-c4),0), and b1 has the quarter-turned period form.
targets=[]
for component in [0,1]:
 target=[F(0)]*(2*dim);target[component*dim+1]=2;target[component*dim+4]=-2
 targets.append(target)
targets=[forms[0][:],forms[20][:]]
basis={}
for index,v in enumerate(forms):
 v=v[:];coeff=[F(int(j==index)) for j in range(len(forms))]
 for pivot,(row,recombination) in sorted(basis.items()):
  scalar=v[pivot]
  v=[x-scalar*y for x,y in zip(v,row)]
  coeff=[x-scalar*y for x,y in zip(coeff,recombination)]
 pivot=next((i for i,x in enumerate(v) if x),None)
 if pivot is not None:
  scale=v[pivot];basis[pivot]=([x/scale for x in v],[x/scale for x in coeff])
results=[]
for target in targets:
 residual=target[:];coeff=[F(0)]*len(forms)
 for pivot,(row,recombination) in sorted(basis.items()):
  scalar=residual[pivot]
  residual=[x-scalar*y for x,y in zip(residual,row)]
  coeff=[x+scalar*y for x,y in zip(coeff,recombination)]
 if not any(residual):
  assert [sum(coeff[j]*forms[j][i] for j in range(len(forms))) for i in range(2*dim)]==target
  certificate=None
 if any(residual):
  free=next(i for i,x in enumerate(residual) if x and i not in basis)
  dual=[F(0)]*(2*dim);dual[free]=1
  for pivot,(row,_) in sorted(basis.items(),reverse=True):
   dual[pivot]=-sum(row[j]*dual[j] for j in range(pivot+1,2*dim))
  assert all(sum(x*y for x,y in zip(form,dual))==0 for form in forms)
  value=sum(x*y for x,y in zip(target,dual));assert value
  certificate=dict(linear_functional=list(map(str,dual)),on_every_saved_axis_form='0',on_neck_form=str(value))
 results.append(dict(in_period_image=not any(residual),residual=list(map(str,residual)),
  coefficients=list(map(str,coeff)),nonmembership_certificate=certificate))
# Stronger scalar-form test: can an actual room deformation fix BOTH
# components of EVERY saved axis core but change a neck period?
scalar_rows=[row[k*dim:(k+1)*dim] for row in forms for k in [0,1]]
assert all(row[4]==row[20] for row in scalar_rows)
scalar_basis={}
for vector in scalar_rows:
 row=vector[:]
 for pivot,old in sorted(scalar_basis.items()):
  factor=row[pivot];row=[x-factor*y for x,y in zip(row,old)]
 pivot=next((i for i,x in enumerate(row) if x),None)
 if pivot is not None:
  factor=row[pivot];scalar_basis[pivot]=[x/factor for x in row]
neck=targets[0][:dim];residual=neck[:]
for pivot,row in sorted(scalar_basis.items()):
 factor=residual[pivot];residual=[x-factor*y for x,y in zip(residual,row)]
actual_deformation=None
if any(residual):
 free=next(i for i,x in enumerate(residual) if x and i not in scalar_basis)
 delta=[F(0)]*dim;delta[free]=1
 for pivot,row in sorted(scalar_basis.items(),reverse=True):
  delta[pivot]=-sum(row[j]*delta[j] for j in range(pivot+1,dim))
 assert all(sum(x*y for x,y in zip(row,delta))==0 for row in scalar_rows)
 value=sum(x*y for x,y in zip(neck,delta));assert value
 assert delta[c['walls']:]==[0]*4
 block_duals=[delta+[F(0)]*dim,[F(0)]*dim+delta]
 assert all(sum(x*y for x,y in zip(row,dual))==0 for row in forms for dual in block_duals)
 assert [[sum(x*y for x,y in zip(target,dual)) for dual in block_duals] for target in targets]==[[2,0],[0,2]]
 actual_deformation=dict(offset_velocity=list(map(str,delta)),axis_core_derivatives='all 80 scalar forms zero',
  neck_x_period_derivative=str(value),marks_fixed=True)
out=dict(status='FROZEN_AXIS_PERIOD_IMAGE_CHECK_COMPLETE',tag=c['tag'],saved_axis_cores=40,
 axis_coverage_binding=dict(squares=112,horizontal_unit_annuli=20,vertical_unit_annuli=20,
  provenance='frozen twist-pf.py cycles(r)/cycles(u); not independently rebuilt in this audit'),
 image_rank=len(basis),boundary_period_form_results=results,input_sha256=pins,
 scalar_axis_form_rank=len(scalar_basis),actual_axis_isoperiodic_deformation=actual_deformation,
 homology_membership_proved=False,neck_axis_inclusion_refuted=True,
 neck_plane_axis_span_intersection='zero, by this same nonzero vector-period witness',
 independent_review='ACCEPTED_SCOPED_HAND_REVIEW64930',
 universal_detection_proved=False,discovery_runs=0,
 scope='One fixed room; ONLY necessary period-image test of axis-core inclusion. No cylinder discovery or full homology inference.')
(b/'pocket-structural-axis-forms.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status=out['status'],image_rank=len(basis),membership=[r['in_period_image'] for r in results],
 homology_membership_proved=False,scalar_axis_form_rank=len(scalar_basis),
 actual_deformation_found=actual_deformation is not None,discovery_runs=0),indent=2))
