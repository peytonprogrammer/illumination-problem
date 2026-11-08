"""Regression check of a rejected HAND candidate; no discovery or replay."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
d=F(11,24)
floor=(1/d,F(-1))
# Reflection at y=-1 sends y=-d*x to y=d*x-2, not d*x-1.
actual_U_right=(F(3),3*d-2)
actual_R_far_y=4*d-2
assert floor==(F(24,11),F(-1))
assert actual_U_right==(F(3),F(-5,8)) and -1<actual_U_right[1]<0
assert actual_R_far_y==F(-1,6)
assert actual_R_far_y!=F(5,6)
assert 3*d-2!=3*d-1
out={'status':'REJECTED_INVALID_HAND_CANDIDATE_NO_PATH','proposed_root':'11/24','first_floor':list(map(str,floor)),'correct_after_floor':'y=d*x-2','incorrect_after_floor':'y=d*x-1','actual_next_wall':['3','-5/8'],'reason':'The ray hits lower U right wall x3,y in(-1,0), before reaching the R23 upper-square inlet. Earlier candidate also fails first post-floor specularity.','limits':'No valid ten path, full support certificate or O3 closure. No search/room construction/parameter scan. Standalone R/source-corner map was not enough: its assumed initial height was wrong.'}
(HERE/'O3-R23-ten.json').write_text(json.dumps(out,indent=2)+'\n')
print('REJECTED: corrected y=dx-2 hits Uright(3,-5/8), not R23. No ten path or new closure.')
