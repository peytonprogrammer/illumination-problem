"""Long-term replay of the already complete fixed finite proof.
Imports ONLY frozen own homogeneous functions, never initial timed main or
peer code. Writes replay.json; preserves original result/progress/effort.
"""
from pathlib import Path
from fractions import Fraction as F
from importlib.util import spec_from_file_location,module_from_spec
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    initial=json.loads((HERE/'result.json').read_text());assert initial['status']=='COMPLETE_INDEPENDENT_FINITE_SUPPORT_CLASSIFICATION_PASS'
    for rel,h in initial['source_sha256'].items():assert sha(BASE/rel)==h,rel
    sp=spec_from_file_location('own_frozen_homogeneous',HERE/'check.py');M=module_from_spec(sp);sp.loader.exec_module(M)
    M.sanity();eligible,counts=M.phases();assert counts==initial['eligible_counts']
    n=full=negative=clauses=0
    expected={tuple((r['phase'][2],r['phase'][0],r['phase'][1])):r for r in initial['records']}
    for (q,A,C),group in sorted(eligible.items()):
        if A+C>q:continue
        saved=expected[q,A,C];assert group==saved['group'];pieces=[M.DOMAIN];used=0
        for gs in M.charts(A,C,q):
            out={}
            for p in pieces:
                for z in M.subtract(p,gs):out[tuple(sorted(set(z)))]=z
            pieces=list(out.values());used+=1
            if not pieces:break
        assert used==saved['clauses_applied']
        assert bool(pieces)==(saved['result']=='nonempty_failure_complement')
        residual=[[[str(F(x,w)),str(F(y,w))] for x,y,w in p] for p in pieces]
        assert residual==saved['failure_pieces']
        for p,wanted in zip(pieces,saved['failure_witnesses']):
            s=sum((F(x,w) for x,y,w in p),F(0))/len(p);t=sum((F(y,w) for x,y,w in p),F(0))/len(p)
            assert [str(s),str(t)]==wanted;negative+=M.verify_failure(A,C,q,s,t)
        weight=1 if A+C==q else 2;assert weight==saved['mirror_weight'];full+=weight;n+=1;clauses+=used
        if n%10000==0:print(json.dumps({'canonical_checked':n,'full_phase_cases':full}),flush=True)
    assert n==59950 and full==119740 and negative==944 and clauses==1102472
    out={'status':'COMPLETE_FIXED_FINITE_PROOF_REPLAY_PASS','canonical_phases':n,'full_phase_classifications':full,'integer_guard_clauses':clauses,'negative_chart_tests':negative,'source_sha256':{str(p.relative_to(BASE)):sha(p) for p in (HERE/'result.json',HERE/'check.py',HERE/'replay.py')},'limits':'Prescribed finite domains only, no new discovery or original expired effort clock. Full original-room optical closure remains open.'}
    (HERE/'replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
