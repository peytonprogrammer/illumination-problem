"""Render the human census table and bind the local artifact hashes."""
from pathlib import Path
import hashlib
import json

R=Path(__file__).parent
D=json.loads((R/'count.json').read_text())
V=json.loads((R/'verification.json').read_text())
assert V['status']=='PASS'
assert V['count_json_sha256']==hashlib.sha256((R/'count.json').read_bytes()).hexdigest()
lines=['Marked-support census: orthogonal rooms, W<=20, k<=7',
       '4 November 2026 — authorized geometry classification only','',
       '[done] Complete necessary cover:36 support shapes,61 raw marked pairs,56 marked-pair symmetry classes.',
       'No room completion, illumination test, solver or pilot has run. Retained supports are not certified feasible rooms.','',
       'I counts every interior A point, not just the two selected marks. Coordinates below are A/2; multiply by2 for original coordinates.','',
       '| Interior A points | Supports | Raw pairs | Pairs after symmetry |',
       '|---|---:|---:|---:|',
       '|2|18|18|18|','|3|18|43|38|','|4|0|0|0|','|Total|36|61|56|','',
       'What changed from the assessment',
       'Orthogonality gives Q>=2P, tightening P+missing caps from13/11/9 to13/10/7.',
       'The I4 branch is impossible because its external-neighbor count is at least8, above cap7.',
       'The five coarse I2 distance8 placements also fail: the budget would force a seven-cell chain of single-quarter fans, while any connected quarter-only component shares one B corner and has at most four cells. See proof.txt sections3–4.','',
       'The surviving36support shapes and56marked symmetry classes are exactly the old k6 inventory. This is actual shape/pair equality, not just equal totals. I2 allowed-cell windows grow by one layer; I3 windows stay the same. k7 permits NEW ROOM COMPLETIONS inside these supports, so old k6 certificates do not settle the new tranche.','',
       'Complete inventory',
       'Full lists: count.json (36supports, all61rawpairs and safe windows), supports.tsv, marked-cases.json/tsv (56nonredundant actual marked pairs). Raw pair coordinates and orbit multiplicities are explicit. Every neighborhood may contain empty cells; do not force all its cells occupied.','',
       '| Support | Full A cells | b | Outside cap | Allowed A cells | Raw pairs | Pair orbits | Old k6 tag |',
       '|---|---|---:|---:|---:|---:|---:|---|']
for r in D['cases']:
    full='; '.join(f'({x},{y})' for x,y in r['full'])
    lines.append(f"|{r['tag']}|{full}|{r['external_neighbors']}|{r['outside_cell_cap']}|{r['allowed_A_cells']}|{r['marked_pairs_raw']}|{r['marked_pair_orbits']}|{r['previous_k6_tag']}|")
lines.extend(['','Bounds and implementation limits',
              'Every selected room has at most42canonical triangles, equivalently21original unit squares. An allowed-cell universe is larger: I2 has110–162A cells (880–1296triangle variables), I3 has13–55A cells (104–440triangles). These are universe sizes, not rooms, timing estimates or selected-area claims.',
              'Eight I3 supports have disconnected distance-two full-cell overlap graphs and are included. Connected-R plus the budget, not the old connected-overlap premise, justifies completeness.',
              'Only translations, D4 and unordered-mark reversal are quotiented. No affine/scaling equivalence is assumed.',
              'The tranche uses the fixed grid with interior A marks and k<=7; a later pilot may restrict to exactly7 because k<=6 is already covered. Arbitrary marks, arbitrary real lengths and nonorthogonal boundaries are outside this census.','',
              'Verification',
              'verify.py independently reconstructs the support sets by connected growth, checks a different canonicalization, every marked pair/orbit and every allowed cell by direct Manhattan distance. It checks12orthogonal fan masks and64neighboring-quarter pairs, with8actual edge connections. verification.json PASS binds count.json.',
              'These are separate implementations by the SAME agent. The new hand arguments are not independently reviewed or formally verified. Optional peer hand challenge requested on the shared board; no review is claimed live or accepted.','',
              'Reproduce',
              '  python3 -B count.py',
              '  python3 -B verify.py',
              '  python3 -B report.py','',
              'Next move: retain this inventory for the separately authorized pilot. No pilot, SAT, room assignment, optical guard, ray/direction/word or origami-orbit run is queued.'])
(R/'findings.txt').write_text('\n'.join(lines)+'\n')
files=['count.py','verify.py','report.py','proof.txt','count.json','verification.json','findings.txt',
       'supports.tsv','marked-cases.json','marked-cases.tsv','inputs/k6-count.json']
manifest={'status':'COMPLETE_NECESSARY_CENSUS','scope':'Step1 only; no feasibility or illumination campaign.',
          'sha256':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in files}}
(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':'PASS','supports':36,'raw_pairs':61,'marked_orbits':56,'files_bound':len(files)},indent=2))
