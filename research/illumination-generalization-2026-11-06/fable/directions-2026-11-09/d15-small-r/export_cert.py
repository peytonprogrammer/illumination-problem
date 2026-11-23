"""Write the certificate tables of all order types with r reflex corners in
the text format read by verify.c.  Usage: export_cert.py r > file"""
import sys
from lemmas import OT, certify_type
CODE = {'A': 1, 'A2': 2, 'B': 3, 'B2': 4, 'par': 5, 'perp': 6, 'same': 7, 'D': 8}
def lines_for(nx, ny, mask):
    ot = OT.from_mask(nx, ny, mask)
    certs, unc = certify_type(ot)
    out = []
    for (S, T), c in certs.items():
        code = CODE[c.get('form', c['lem'])]
        p1 = c['p1'] or (-1, -1, -1); p2 = c['p2'] or (-1, -1, -1); r2 = c['r2'] or (-1, -1)
        f = [*S, *T, code, c['swap'], *p1, *p2, *r2, len(c['cons'])]
        for con in c['cons']: f += list(con)
        out.append(" ".join(map(str, f)))
    for (S, T) in unc:
        out.append(" ".join(map(str, [*S, *T, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, 0])))
    return [f"TYPE {nx} {ny} {mask} {len(out)}"] + out
if __name__ == "__main__":
    r = sys.argv[1]; B = sys.argv[2]
    for line in open(f"types_r{r}.txt"):
        nx, ny, W, mask = map(int, line.split())
        print("\n".join(lines_for(nx, ny, mask)))
        print("ALL", B)
    print("END")
