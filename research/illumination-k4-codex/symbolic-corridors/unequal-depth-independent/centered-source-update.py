"""Reconcile the announced parent certificate update; no peer execution."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent;BASE=HERE.parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=json.loads((HERE/'centered-check.json').read_text())
    parent=json.loads((BASE/'unequal-depth/centered-check.json').read_text())
    assert sha(BASE/'unequal-depth/centered-theorem.md')==old['source_sha256']['unequal-depth/centered-theorem.md']=='6264849d4f985b42bcdfa5f770b777b35c6fd6be8914c2cc0c5160ec315c876d'
    fields=['line','p','q','alpha','beta','witness_n']
    assert old['rows']==[{k:r[k] for k in fields} for r in parent['rows']]
    assert parent['finite_rows']==40 and len(parent['rows'])==40
    expected=[p for p in old['physical'] if p['kind'] in ('finite residual row','isolated repair')]
    assert len(expected)==len(parent['physical_records'])==37
    for own,p in zip(expected,parent['physical_records']):
        assert p['contacts']==own['contacts_per_path']
        if p['kind']=='prescribed table chart':
            al,be=__import__('fractions').Fraction(p['alpha']),__import__('fractions').Fraction(p['beta'])
            a,b=al/(be-al),(1-be)/(be-al)
            assert (str(a),str(b))==(own['a'],own['b'])
        else:assert (p['a'],p['b'])==(own['a'],own['b'])
    assert parent['physical_paths']==74 and parent['wall_contacts']==2*sum(p['contacts'] for p in parent['physical_records'])==186
    changes={}
    announced={'unequal-depth/centered-check.py':'d64a7a222b1ddccec32f1136718e0ee384ea7305bf28ac36b22a23b1871368b5','unequal-depth/centered-check.json':'2ec4adbdb7c6725263f4c34c0bf0e4e4039fac24807a3d4ad2a3e7f0d115cc97'}
    for rel,new in announced.items():
        assert sha(BASE/rel)==new
        assert old['source_sha256'][rel]==new
        changes[rel]={'already_pinned':new,'announced':new}
    out={'status':'ANNOUNCED_FINAL_CERTIFICATES_ALREADY_PINNED','theorem_source_unchanged':True,'theorem_sha256':sha(BASE/'unequal-depth/centered-theorem.md'),'changes':changes,'all_40_rows_unchanged':True,'physical_records_matched_to_independent_checks':37,'old_acceptance_preserved':sha(HERE/'centered-acceptance.json'),'review':'centered-source-update.md','limits':'Parent code was read, not executed. Main mathematical acceptance is unchanged; the original independent receipt already captured these final source hashes; no hash replacement is required.'}
    (HERE/'centered-source-update.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))
if __name__=='__main__':main()
