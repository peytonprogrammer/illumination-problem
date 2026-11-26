"""Check production disposition totals against counts and publish completed files."""
from collections import Counter
import csv
from pathlib import Path
import shutil

here = Path(__file__).resolve().parent
prod = here / 'production'
def read(path):
    with path.open() as file:
        return list(csv.DictReader(file,delimiter='\t'))

def reconcile():
    rows=read(prod/'raw-counts.tsv')
    baseline=read(here/'pilot/raw-counts.tsv')
    assert [r for r in rows if int(r['area'])<=12]==baseline
    assert {int(r['area']) for r in rows}==set(range(1,17))
    expected,actual=Counter(),Counter()
    for r in rows:
        if r['bucket']!='EMBEDDED':
            expected[int(r['area']),r['bucket']]+=int(r['pairs'])
    dispositions=read(prod/'lighting.tsv')
    for r in dispositions:
        actual[int(r['area']),r['bucket']]+=int(r['pairs'])
    for k in actual.keys()|expected.keys():
        assert actual[k]==expected[k],(k,actual[k],expected[k])
    for name,kind in [('dark.tsv',{'FULL'}),('undecided.tsv',{'CAP','CRASH'})]:
        cases=read(prod/name)
        assert all(r['status'] in kind for r in cases)
        assert len(cases)==sum(int(r['pairs']) for r in dispositions if r['result'] in kind)
    for source,target in [('raw-counts.tsv','counts.tsv'),('dark.tsv','dark.tsv'),('undecided.tsv','undecided.tsv')]:
        shutil.copyfile(prod/source,here/target)
    for a in range(1,17):
        print(a,actual[a,'TOUCHING'],actual[a,'OVERLAP'])
    for b in ['EMBEDDED','TOUCHING','OVERLAP']:
        print(b,*(sum(int(r[key]) for r in rows if r['bucket']==b) for key in ('discs','pairs')))
if __name__=='__main__':reconcile()
