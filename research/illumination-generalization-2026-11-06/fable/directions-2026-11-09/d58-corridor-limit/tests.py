"""d58 exact tests. Usage: python3 -B tests.py > logs/tests.log"""
import time, resource
from fractions import Fraction as Fr
from build import instance, config, DOOR
from families import light, window_exists, h_fail_formula
resource.setrlimit(resource.RLIMIT_CPU, (480, 480))
t0 = time.process_time()

def fams(geo, info, back=None):
    a, b, p, q, d, S, T = geo
    D, h, ell = d - S[1], T[1] - d, info['ell']
    out = {'H': (h, D, 1), 'E': (2 * ell - h, D, 1)}
    if back is not None:
        c = back
        out['B'] = (h, D + 2 * (S[1] - c), -1)
        out['BE'] = (2 * ell - h, D + 2 * (S[1] - c), -1)
    return out

def tpos(info):
    return 'row-interior' if info['C'][1] % 2 else 'grid-line'

print('# T1/T2: generic parameters, thin corridor w = 2^-k (A) and thin viewer gap D = 2^-k (B)')
base = dict(L=Fr(4), pi=Fr(3, 2), u=Fr(2, 3), beta=Fr(2, 5), ell=Fr(1), fh=Fr(3, 7))
nH = nok = 0
for mask, S, T in DOOR:
    for deg in ('A', 'B'):
        row = []
        for k in range(1, 13):
            e = Fr(1, 2 ** k)
            prm = dict(base, w=e if deg == 'A' else Fr(1, 3), D=Fr(5, 7) if deg == 'A' else e, h=None)
            room, geo, info = instance(mask, S, T, **prm)
            f = fams(geo, info)
            st, nref, vec, tried = light(room, geo, f['H'])
            pred_fail = h_fail_formula(geo, f['H'][0])
            ex = window_exists(geo, f['H'][0], f['H'][1])
            assert ex != pred_fail
            nH += 1; nok += st == 'valid'
            row.append(f"{k}:{nref if st == 'valid' else st}")
        print(mask, S, T, deg, 'H reflections by k:', ' '.join(row))
print(f'T1/T2 summary: {nok}/{nH} instances lit by a traced Lemma H path')

print('\n# T3: resonant instances where Lemma H fails (n = L h/(w D) integer, D = 16 h)')
from tests_lib import resonant

for mode in ('long', 'double'):
    for mask, S, T in DOOR:
        for k in (4, 8, 12):
            try:
                room, geo, info = resonant(mask, S, T, k, mode)
            except AssertionError as ex:
                print(mask, S, T, mode, k, 'construction n/a', ex); continue
            back = None
            a, b, p, q, d, Sv, Tc = geo
            f = fams(geo, info)
            hH = f['H'][0]
            res = [f'{mask} {S} {T} {mode} k={k} n={int(4 * hH / ((q - p) * (d - Sv[1])))} {tpos(info)}',
                   f"Hwin={window_exists(geo, hH, f['H'][1])} Hpred_fail={h_fail_formula(geo, hH)}"]
            for nm in ('H', 'E'):
                st, nref, vec, tried = light(room, geo, f[nm])
                h2, DD = f[nm][0], f[nm][1]
                n2 = 4 * h2 / ((q - p) * DD)
                res.append(f"{nm}:{st}/{nref} (n={n2 if n2.denominator == 1 else 'non-int'}, kappa={'>=1' if h2 >= DD else '<1'}, tried {tried})")
            print(' '.join(res))
print('cpu', round(time.process_time() - t0, 1))
