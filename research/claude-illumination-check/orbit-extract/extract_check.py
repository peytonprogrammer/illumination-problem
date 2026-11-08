"""Replay Codex's orbit-extracted direction with my own exact tracer (folded/exact.py).
Control: the same extraction with the frame NOT transposed, and with B^T instead of B."""
import sys,glob,json,random,importlib.util,math
sys.path.insert(0,'../folded'); from exact import run1
K='../../illumination-k4-codex/k5-proof-pilot/'
spec=importlib.util.spec_from_file_location('ow',K+'orbit-witness.py'); ow=importlib.util.module_from_spec(spec); spec.loader.exec_module(ow)
o=ow.o
fs=sorted(glob.glob('../../illumination-k4-codex/k5-proof-continuation/cases/*/generations/*/vertices.json'))
random.seed(int(sys.argv[1])); fs=random.sample(fs,min(int(sys.argv[2]),len(fs)))+sorted(glob.glob(K+'cases/*/vertices.json'))
from collections import Counter; C=Counter()
for f in fs:
    j=json.load(open(f)); V=[tuple(p) for p in j['vertices']]; S,T=map(tuple,j['marked'])
    r=ow.direction(V,S,T)
    if r['status']!='LIT': C[r['status']]+=1; continue
    d=tuple(r['direction']); B=r['inverse_matrix']; fr=r['source_frame']; dev=(B[0][0],B[1][0])
    C['codex '+('lit' if run1(V,S,T,d,B=2000) else 'FAIL')]+=1
    alt=o.ap(fr,dev)                                   # frame not transposed
    if alt!=d: C['ctl-frame '+('lit' if run1(V,S,T,alt,B=2000) else 'fail')]+=1
    alt2=o.ap(tuple(zip(*fr)),(B[0][0],B[0][1]))       # row instead of column
    if alt2!=d and math.gcd(*alt2)==1: C['ctl-row '+('lit' if run1(V,S,T,alt2,B=2000) else 'fail')]+=1
print(len(fs),'rooms',dict(C))
