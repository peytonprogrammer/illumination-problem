"""Fixed central-cap midpoint/reflection differentiation; no optical discovery."""
from pathlib import Path
import json
base=Path(__file__).resolve().parent
w=(2,1);u=(1,0);source=(0,0);target=(4,0);corner=(2,1)
def horizontal_reflect(point):return (point[0],2-point[1])
def det(a,b):return a[0]*b[1]-a[1]*b[0]
target_image=horizontal_reflect(target)
assert tuple(target_image[i]-2*corner[i]+source[i] for i in range(2))==(0,0)
Q=tuple(-2*x for x in u)
assert horizontal_reflect((corner[0]+u[0],corner[1]+u[1]))==(corner[0]+u[0],corner[1]+u[1])
assert Q==(-2,0) and det(w,Q)==2
controls=[]
# All eight prescribed D4 coordinate symmetries, applied to this ONE formula.
for swap in (False,True):
 for sx in (-1,1):
  for sy in (-1,1):
   def transform(a):
    x,y=(a[1],a[0]) if swap else a
    return (sx*x,sy*y)
   transformed_Q=transform(Q);transformed_u=transform(u)
   assert transformed_Q==tuple(-2*x for x in transformed_u)
   assert abs(det(transform(w),transformed_Q))==2
   controls.append(dict(swap=swap,sx=sx,sy=sy,Q=transformed_Q))
out=dict(status='PRESCRIBED_CENTRAL_CAP_DETECTION_ALGEBRA_PASS',
         controls=controls,defect=Q,opening_determinant=2,
         scope='Supplied shared-neighbor configuration with the specified literal central cap only.',
         universal_detection='OPEN',optical_discovery_runs=0)
(base/'pocket-cap-detection.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
