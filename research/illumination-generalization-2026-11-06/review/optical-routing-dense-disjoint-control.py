#!/usr/bin/env python3
"""Exact coefficient verification of the specified sqrt(2) square control."""
from pathlib import Path
import json
from fractions import Fraction as F

# In Q(sqrt2), equality a+b*sqrt2=0 iff a=b=0; x^2-2 is irreducible
# over Q (the usual parity proof). No floating orbit is used.
def field_zero(a,b):return F(a)==0 and F(b)==0
image_rows=[]
for ex in [-1,1]:
 for ey in [-1,1]:
  # alpha*(ex*4+16n-2) -(ey*6+16k-2)=0.
  alpha_residue=(ex*4-2)%16
  assert alpha_residue!=0
  image_rows.append({'epsilon_x':ex,'epsilon_y':ey,'sqrt2_coefficient_constant':ex*4-2,'sqrt2_coefficient_n':16,'constant_term':2-ey*6,'constant_term_k':-16,'sqrt2_coefficient_mod16':alpha_residue,'all_integer_n_k_excluded':True})
assert (2%16)!=0
assert (-2%8)!=0
assert not field_zero(0,2)
assert F(6-2,4-2)==2
result={'status':'PASS_EXACT_ALL_INTEGER_COEFFICIENT_CONTROL','arithmetic_model':'Q(sqrt2), coefficient comparison; symbolic congruences cover all integer word translations','room':[[0,0],[8,0],[8,8],[0,8]],'r':0,'S':[2,2],'T':[4,6],'target_image_rows':image_rows,'corner_coefficient':{'constant':-2,'n':8,'nonzero_mod8':6},'source_target_section_difference':{'sqrt2_constant':2,'sqrt2_integer_multiplier':16,'rational_constant':-4,'rational_integer_multiplier':-16,'sqrt2_coefficient_never_zero':True},'density':'Proved by irrational-circle-rotation hand argument in paired markdown, not finite sampling','actual_pair_directly_lit_slope':'2','whole_goal_complete':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
