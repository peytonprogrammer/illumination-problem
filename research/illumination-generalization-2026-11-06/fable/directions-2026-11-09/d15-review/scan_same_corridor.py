"""Side check (r = 3, 4 share Lemma C): does lemmas.py ever issue a C-same
certificate in which both "arms" are the same corridor with the two flat ends
swapped? The proof of the same form assumes two disjoint corridors.
Usage: python3 -B scan_same_corridor.py r"""
import os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
AUTH = os.path.join(HERE, "..", "d15-small-r")
sys.path.insert(0, AUTH)
import lemmas as AL
r = sys.argv[1]
bad = tot = 0
first = None
for line in open(os.path.join(AUTH, f"types_r{r}.txt")):
    nx, ny, W, mask = map(int, line.split())
    ot = AL.OT.from_mask(nx, ny, mask)
    certs, unc = AL.certify_type(ot)
    for (S, T), c in certs.items():
        if c.get('form') == 'same':
            tot += 1
            (_, F1, E1), (_, F2, E2) = c['p1'], c['p2']
            if (F1, E1) == (E2, F2) and c['cons'][0][1] == c['cons'][1][2]:
                bad += 1
                if first is None:
                    first = (nx, ny, mask, S, T, c)
print("r", r, "C-same certificates", tot, "with one corridor used as both arms", bad, first)
