import sys,glob,json,random,importlib.util
sys.path.insert(0,'../folded'); from exact import run1, run
K='../../illumination-k4-codex/k5-proof-pilot/'
spec=importlib.util.spec_from_file_location('ow',K+'orbit-witness.py'); ow=importlib.util.module_from_spec(spec); spec.loader.exec_module(ow)
fs=sorted(glob.glob('../../illumination-k4-codex/k5-proof-continuation/cases/*/generations/*/vertices.json'))
random.seed(1); fs=random.sample(fs,12)
for f in fs:
    j=json.load(open(f)); V=[tuple(p) for p in j['vertices']]; S,T=map(tuple,j['marked'])
    r=ow.direction(V,S,T); d=tuple(r['direction'])
    print(f.split("cases/")[1][:30],len(V),d,r["shear_word"][:12],flush=True)
    try: p=ow.trace_direction(V,S,T,d); ct="lit %d"%(len(p)-2)
    except AssertionError as e: ct='ERR '+str(e)[:80]
    mine=run(V,S,T,B=2000,dirs=[d]); 
    print(f.split('cases/')[1][:30], len(V), d, r['shear_word'][:12], 'codex-trace:',ct,'| mine:', 'lit' if mine[0] else 'no', '| -d mine:', 'lit' if run(V,S,T,B=2000,dirs=[(-d[0],-d[1])])[0] else 'no')
