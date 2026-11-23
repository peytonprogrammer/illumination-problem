import sys, json, collections
from lemmas import OT, certify_type
def show(ot):
    return "/".join("".join("#" if ot.ins(i,j) else "." for i in range(ot.nx)) for j in reversed(range(ot.ny)))
r = sys.argv[1]
tot = collections.Counter(); unc_types = 0; rows = []
for line in open(f"types_r{r}.txt"):
    nx, ny, W, mask = map(int, line.split())
    ot = OT.from_mask(nx, ny, mask)
    assert ot.walls() == W
    certs, unc = certify_type(ot)
    c = collections.Counter(v['lem'] + ('-' + v['form'] if 'form' in v else '') for v in certs.values())
    tot.update(c); tot['uncovered'] += len(unc); tot['pairs'] += len(certs) + len(unc)
    if unc: unc_types += 1
    rows.append(dict(nx=nx, ny=ny, mask=mask, shape=show(ot), counts=dict(c), uncovered=unc))
    if len(sys.argv) > 2: print(nx, ny, mask, show(ot), dict(c), "UNCOVERED", len(unc), unc[:6])
print("r", r, "types", len(rows), "types with uncovered pairs", unc_types, dict(tot))
json.dump(rows, open(f"cert_r{r}.json", "w"))
