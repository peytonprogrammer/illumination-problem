#!/usr/bin/env python3
"""Exact finite residues in the analytic all-M/all-target-image argument; no search."""
from fractions import Fraction as F
from itertools import product
import json
fold=lambda x:min(x%8,8-x%8)
rows=[]
for a,b,eta,parity in product((1,3),(1,3),(1,-1),(0,1)):
 e=F(a-b,2);base=F(3+eta+8*parity,2)
 assert e in (-1,0,1)
 zbase=fold(base);assert zbase in (1,2,3)
 assert zbase-abs(e)*F(1,8)>=F(7,8)>F(3,8)
 rows.append({'a':a,'b':b,'eta':eta,'n_parity':parity,'e':str(e),'folded_unperturbed_phase':str(zbase),'lower_bound_if_abs_tau_lt_one_eighth':str(zbase-abs(e)*F(1,8))})
print(json.dumps({'status':'ALL_RESIDUE_AND_STRICT_GAP_IDENTITIES_PASS','method':'Complete finite residue reduction in a hand all-parameter proof; no direction/room/word search','rows':rows,'symbolic_cancellation':'L1-L2=h implies L1+a-(L1+L2+h+a+b)/2=(a-b)/2 for ALL real lengths','straight_bridge_bound':'|tau|<1/8 and z<3/8','target_phase_bound':'z>7/8','physical_darkness':False,'whole_goal_complete':False},indent=2))
