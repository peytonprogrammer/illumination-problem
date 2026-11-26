import csv
from pathlib import Path

def main():
    source=Path('raw-counts.tsv').read_text().splitlines(keepends=True)
    rows=list(csv.DictReader(source,delimiter='\t'))
    observed={(int(r['area']),int(r['W'])):int(r['discs']) for r in rows if r['bucket']=='EMBEDDED' and int(r['area'])<=11}
    expected={}
    for line in Path('../../d205-census-a21/validation/optimized.counts').read_text().splitlines():
        f=line.split()
        if f[:2]==['#','count'] and int(f[5])<=20:
            expected[int(f[3]),int(f[5])]=int(f[7])
    assert observed==expected, [(k,observed.get(k),expected.get(k)) for k in sorted(expected.keys()|observed.keys()) if observed.get(k)!=expected.get(k)]
    Path('counts.tsv').write_text(source[0]+''.join(l for l in source[1:] if int(l.split()[0])<=10))
    print('G1 PASS',len(expected),sum(expected.values()))
    for b in ('EMBEDDED','TOUCHING','OVERLAP'):
        subset=[r for r in rows if r['bucket']==b and int(r['area'])<=10]
        print(b,*(sum(int(r[k]) for r in subset) for k in ('discs','pairs')))
if __name__=='__main__': main()
