"""B04 prescribed ALLimage residue proof controls; no slope discovery."""
from pathlib import Path
from fractions import Fraction as Q
import itertools,json,hashlib,importlib.util
R=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('g',R/'resumed-exact-check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
rows=[]
for ex,ey in itertools.product([-1,1],repeat=2):
 X=ex*16-12;Y=ey*18-12;assert X%4==0 and X%3!=0 and Y%3==0 and Y%4==2
 # Fullimagecoefficients48 vanishmod3and4, so these are ALLintegeri/jresidues.
 assert 48%3==48%4==0
 rows.append({'signs':[ex,ey],'X_constant':X,'Y_constant':Y,'X_mod4':X%4,'X_mod3':X%3,'Y_mod3':Y%3,'Y_mod4':Y%4})
V=[(0,0),(24,0),(24,24),(0,24)];S=(12,12);T=(16,18);g.simple(V);d=g.path_check(V,[S,T]);assert d['reflections']==0 and g.vec(S,T)==(4,6)
out={'status':'ALL_SIGN_AND_UNBOUNDED_IMAGE_RESIDUES_PROVED_BY_COEFFICIENTS','whole_goal_complete':False,'discovery':False,'rows':rows,'direct_actual_path':d,'primitive_direct_direction':[2,3],'excluded_entire_families':['(n,1)','(1,n)'],'all_n_proof':'Xnonzero mod3 andY0mod3 excludesX=nY; Y2mod4 andX0mod4 excludesY=nX','source_sha256':{'resumed-exact-check.py':hashlib.sha256((R/'resumed-exact-check.py').read_bytes()).hexdigest()}}
(R/'global-monodromy-independent-check.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
