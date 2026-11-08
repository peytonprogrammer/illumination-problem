"""Prescribed overlap-margin and four-term arithmetic; no surface discovery."""
from fractions import Fraction as F
from pathlib import Path
import json
b=Path(__file__).resolve().parent
# These are formal positive-area tables, not asserted surface data.
# Each has integer strip areas and a prescribed signed determinant m.
tables=[(2,[[F(1,2),F(1,2)],[F(1,2),F(1,2)]]),
        (1,[[F(2),F(0)],[F(0),F(2)]]),
        (-2,[[F(3,2),F(1,2)],[F(1,2),F(3,2)]])]
rows=[]
for m,A in tables:
 nE=[sum(r) for r in A];nD=[sum(A[i][j] for i in range(2)) for j in range(2)]
 assert all(x.denominator==1 and x>0 for x in nE+nD)
 # Scalar x loads chosen to have exact zero area mean; y component is zero.
 Qcore=[F(1),F(-1)]
 flux=[Qcore[i]/nE[i] for i in range(2)]
 assert sum(nE[i]*flux[i] for i in range(2))==0
 intersections=[[m*A[i][j] for j in range(2)] for i in range(2)]
 assert all(x.denominator==1 for r in intersections for x in r)
 averages=[sum(A[i][j]*flux[i] for i in range(2))/nD[j] for j in range(2)]
 kappa=12;epsilon=-1
 # z=epsilon*kappa*(core_Dt/n_t-core_Ds/n_s).
 left=epsilon*kappa*kappa*sum(Qcore[i]/nE[i]*(intersections[i][1]/nD[1]-intersections[i][0]/nD[0]) for i in range(2))
 right=epsilon*kappa*kappa*m*(averages[1]-averages[0])
 assert left==right
 rows.append(dict(signed_determinant=m,areas=[[str(x) for x in r] for r in A],
  flux_means=[str(x) for x in averages],contrast=str(averages[1]-averages[0]),
  tested_increment=str(left)))
assert rows[0]['contrast']=='0' and rows[1]['contrast']!='0'
# Symbolic four-image coefficient identity, represented on basis {eta,Nveta,Nthetaeta,NthetaNveta}.
eta=[1,0,0,0];tau=[1,1,0,0];phi=[1,0,1,0];phitau=[1,1,1,1]
assert [phitau[i]-tau[i]-phi[i]+eta[i] for i in range(4)]==[0,0,0,1]
out=dict(status='PRESCRIBED_OVERLAP_LOAD_ALGEBRA_PASS',controls=rows,
 four_event_identity=True,zero_mean_does_not_force_selected_contrast=True,
 scope='Formal margin/intersection arithmetic only; no overlap table is asserted realizable and no cylinders are computed.',
 universal_actual_strip_separation='OPEN',optical_discovery_runs=0)
(b/'pocket-overlap.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
