"""Prescribed B-junction triangle incidence, no room or path enumeration."""
from pathlib import Path
import json
b=Path(__file__).resolve().parent
ring=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(a,start,count):
 return [(a,(a[0]+ring[j%8][0],a[1]+ring[j%8][1]),
          (a[0]+ring[(j+1)%8][0],a[1]+ring[(j+1)%8][1]))
         for j in range(start,start+count)]
def angle_at_B(point,triangles):
 assert point[0]%2==point[1]%2==1
 for tri in triangles:
  if point in tri:
   a=tri[0]
   assert a[0]%2==a[1]%2==0
   assert (abs(point[0]-a[0]),abs(point[1]-a[1]))==(1,1)
 return 45*sum(point in tri for tri in triangles)
T=fan((4,0),0,8);M=fan((2,0),0,4)
end_upper=fan((6,0),3,1)
assert set(end_upper[0])=={(6,0),(5,0),(5,1)}
Tup_right_rectangle=fan((4,2),6,2)
Tup_left_triangle=fan((4,2),5,1)
assert angle_at_B((5,1),T+end_upper)==135
assert angle_at_B((5,1),T+end_upper+Tup_right_rectangle)==225
# FOUR prescribed local N fans, not global room choices or searches.
N_cases=[('left_triangle',fan((2,2),5,1)),
         ('left_rectangle',fan((2,2),4,2)),
         ('right_triangle',fan((2,2),6,1)),
         ('right_rectangle',fan((2,2),6,2))]
receipts=[]
for name,N in N_cases:
 end_junction=angle_at_B((3,1),T+M+Tup_right_rectangle+N)
 corridor_literal=angle_at_B((3,1),T+M+Tup_left_triangle+N)
 assert end_junction== (180 if name.startswith('left') else (225 if name.endswith('triangle') else 270))
 assert corridor_literal==(225 if name.startswith('left') else (270 if name.endswith('triangle') else 315))
 receipts.append(dict(local_N=name,end_pocket_junction=end_junction,
                      corridor_literal_B=corridor_literal))
out=dict(status='PRESCRIBED_JUNCTION_INCIDENCE_PASS',receipts=receipts,
 end_leaf_fixed_right_central_flank='INCOMPATIBLE_WITH_RAWNESS',
 corridor_lower_case='FORCES_N_LEFT_PORTAL_BUT_NOT_TRIANGLE_SIZE',
 scope='Local prescribed fan incidences; no global room realization or census.',discovery_runs=0)
(b/'pocket-junction.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
