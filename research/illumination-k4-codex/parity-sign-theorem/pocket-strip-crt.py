"""Eight prescribed CRT and absolute-cycle algebra controls; no geometry discovery."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd,lcm
import json
base=Path(__file__).resolve().parent
# Circumferences/phases here are arithmetic controls, not asserted room data.
data=[(2,4,1,1),(4,6,1,3),(4,6,1,2),(6,18,2,4),
      (6,18,2,2),(8,12,3,5),(2,2,0,0),(10,14,3,1)]
rows=[]
for minus,plus,a_s,a_t in data:
    g=gcd(minus,plus);L=lcm(minus,plus)
    compatible=(a_s+a_t)%g==0
    row=dict(m_minus=minus,m_plus=plus,a_s=a_s,a_t=a_t,
             compatible=compatible,gcd=g,lcm=L)
    if compatible:
        reduced=plus//g
        h=0 if reduced==1 else ((a_s+a_t)//g)*pow(minus//g,-1,reduced)%reduced
        n0=(-a_s+minus*h)%L
        assert (-n0-a_s)%minus==0 and (n0-a_t)%plus==0
        for k in (-2,-1,0,1,2):
            n=n0+k*L
            assert (-n-a_s)%minus==0 and (n-a_t)%plus==0
        # Basis (v,u)=( (1,0),(0,1) ); holonomy cancellation is symbolic.
        assert F(L,plus)*plus-F(L,minus)*minus==0
        # Fixed test cochain on the two abstract cores.
        q_plus=(F(2),F(-1));q_minus=(F(0),F(1))
        D=[F(L,plus)*q_plus[j]-F(L,minus)*q_minus[j] for j in range(2)]
        assert D==[L*(q_plus[j]/plus-q_minus[j]/minus) for j in range(2)]
        # Gauge invariance under a fixed Bezout-basis change.
        gauge=3;new_s=a_s+gauge;new_t=a_t-gauge
        assert (new_s+new_t)%g==0
        assert (-(n0-gauge)-new_s)%minus==0
        assert ((n0-gauge)-new_t)%plus==0
        row.update(n0=n0,absolute_core_coefficients=[L//plus,-L//minus],
                   defect_increment=[str(x) for x in D])
    else:
        assert a_s%g!=(-a_t)%g
    rows.append(row)
out=dict(status='PRESCRIBED_STRIP_CRT_ALGEBRA_PASS',controls=rows,
         universal_strip_incidence='OPEN',universal_flux_contrast='OPEN',
         optical_discovery_runs=0,room_enumeration_runs=0,
         scope='Pure congruence and absolute homology arithmetic; no strips or endpoint phases discovered.')
(base/'pocket-strip-crt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
