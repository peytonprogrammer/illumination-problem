"""Named accepted whole-support transfers into mixed single-leaf rows."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent
src=BASE/'surplus-four-local/R23-top6-search/verify.py'
e={'__file__':str(src.resolve())};exec(compile(src.read_text().split('\ndef path(d,nine):')[0],str(src),'exec'),e)
fan,H=e['fan'],e['H'];sources=[src]
def read(rel):
 p=BASE/rel;sources.append(p);return json.loads(p.read_text())
def dec(ts):return {tuple(sorted(map(tuple,t))) for t in ts}
b8=read('surplus-four-local/L670-B12-D1-search/verification.json')
b6=read('fourth-surplus-review/peer-Bunit-six-independent/check.json')
r2=read('surplus-four-local/outside-L0123-D12-search/verification.json')['sigma_two']
c3=read('surplus-four-local/outside-L0123-N45-search/verification.json')
# Accepted optical guard data, no source checker execution.
E8=b8['sigma_eight'];U8,Z8=dec(E8['required']),dec(E8['forbidden'])
# Whole sigma of accepted B12/D2 six.
sigma=e['transform'];u6=sigma(dec(b6['fixed_six']['required']));z6=sigma(dec(b6['fixed_six']['forbidden']))
U2,Z2=dec(r2['required']),dec(r2['forbidden']);U3,Z3=dec(c3['required']),dec(c3['forbidden']);US3,ZS3=dec(c3['sigma_three']['required']),dec(c3['sigma_three']['forbidden'])
apps=[]
def fits(name,low,upper,u,z,bound):
 assert low<=upper and u<=low and not z&upper,name
 apps.append({'name':name,'minimum':sorted(low),'maximum':sorted(upper),'reflections':bound})
# ONE upper B6701 includes BOTH O3/O4; fullD permits either single leaf.
Bmax=fan('B',[6,7,0,1]);Dfull=fan('D',range(8))
base=H|Bmax|Dfull|fan('L',[0])|fan('E',[3,4])|fan('N',[0])
# Lower min independent of the larger B fan/leaf; one upper for each R sign.
fits('ENTIRE_Ecenter_R3',H|fan('E',[3,4])|fan('R',[3]),base|fan('R',[3]),u6,z6,6)
fits('ENTIRE_Ecenter_R4',H|fan('E',[3,4]),base|fan('R',[4]),U8,Z8,8)
# ALL Broot forms, both single Dleaves; ordinaryTc5 (or absent) only.
base=H|fan('B',[6,7,0,1,2])|Dfull|fan('L',[0])|fan('E',[4])|fan('N',[7])|fan('R',[3,4])|fan('Tc',[5])
fits('Rcenter_Tc6abs_ALL_Broot_forms',H|fan('R',[3,4]),base,U2,Z2,2)
# N70 row: each B root, Tc arbitrary allowed, ordinaryR4 or absent.
base=H|fan('B',[6,7,0,1,2])|fan('D',[3,4])|fan('L',[0])|fan('E',[4])|fan('N',[7,0])|fan('R',[4])|fan('Tc',[5,6])
fits('N70_R3abs_ALL_Broot_forms',H,base,U3,Z3,3)
# L70 row: directthree if ordinaryN6 absent/R3 absent.
base=H|Bmax|fan('D',[3,4])|fan('L',[7,0])|fan('E',[4])|fan('N',[0,7])|fan('R',[4])|fan('Tc',[5,6])
fits('L70_N6abs_R3abs',H,base,U3,Z3,3)
# If N6 present, residual condition forces either right N orTc6; N6
# itself is notright, so Tc6 present and ordinary Rempty (two slots used).
base=H|Bmax|fan('D',[3,4])|fan('L',[7,0])|fan('E',[4])|fan('N',[6])|fan('Tc',[6])
fits('L70_N6present_Tc6_Rempty',H,base,US3,ZS3,3)
# Exact already established L12 complementary envelope, no optical re-run.
rootleaf=read('fourth-surplus-review/mixed-e2-e1/root-leaf-check.json')
old=rootleaf['named_implications']['center_L_Nrright_Tplus_absent']
oldU,oldZ=dec(old['required']),dec(old['forbidden'])
base=H|Bmax|fan('D',[3,4])|fan('L',[7,0])|fan('E',[4])|fan('R',[3,4])|fan('N',[6])|fan('Tc',[5])
assert oldU<=H|fan('L',[7,0])|fan('E',[4]) and not oldZ&base

# Every residual row after these covers has an ordinary/unit R3 blocker.
remaining={
 'L70 O3/O4':'ordinaryR3 plus ordinaryN0 orN7, orTc6 (other ordinary slot); both Dleaf variants',
 'Ecenter':'none',
 'Eouter':'H4/D3 ordinaryR3,Tcempty (H4/D4 separateaccepted cover)',
 'Rcenter34':'H4 with ordinaryTc6; both Dleaf variants; unit includesR3',
 'Rupper23':'H4,Tcempty; both Dleaf variants; unit includesR3',
 'N70':'ordinaryR3; O3/O4Tcempty, H4Tc6; both Dleaf variants'}
sources += [BASE/'fourth-surplus-review/mixed-e2-e1/argument.txt',BASE/'fourth-surplus-review/mixed-Eouter-four-transfer/argument.txt',BASE/'surplus-four-local/mixed-Eouter-dispatch-review/review.txt']
out={'status':'PARENT_MIXED_ECENTER_CLOSED_OTHER_SINGLELEAF_ROWS_REDUCED','whole_support_applications':apps,'Ecenter_whole_bound':8,'remaining_necessary_rows':remaining,'source_sha256':{str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'limits':'Named accepted opticalguards and establishedsixrowclassification only. Parentnewrowjoinpendingreview; no capproduct/room/search/worker. Entiremixed/Delta4notclaimed.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS entireEcenter<=8, RcenterTc6abs<=2, N70R3abs<=3, L70R3abs<=3; parentdispatchpendingreview.')
