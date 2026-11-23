"""D112 claim 2: test the common-period lemma exactly on sealed DBas and DB55 chambers.

For each chamber, mark, initial sign pair and slope s, trace the first-hit leg at s
and at s + kK (k = 1, 2, 3), K the slab period from cuts at every vertex abscissa
and the mark abscissa. The recorded data (signed state at every cut crossing and
vertical-wall contact, exit height and signs, and regular/irregular) must agree.
Negative controls: K/2, and the period of the uncut chamber slabs (no mark cut).
"""
from fractions import Fraction as F
from chamber import leg, slab_period, Irregular

CH = {  # sealed chambers in local coordinates; mouth = (x, ylo, yhi)
    'DB55-A': ([(0, 0), (5, 0), (5, 2), (5, 3), (5, 5), (0, 5)], (5, 2, 3)),
    'DB55-B': ([(0, 0), (5, 0), (5, 5), (0, 5), (0, 3), (0, 2)], (0, 2, 3)),
    'DBas-A': ([(0, 0), (5, 0), (5, 1), (5, 2), (5, 4), (0, 4)], (5, 1, 2)),
    'DBas-B': ([(0, -1), (4, -1), (4, 5), (0, 5), (0, 2), (0, 1)], (0, 1, 2)),
    # nonrectangular: chamber plus a corridor stub (DBas left + 3, DB55 right + 2)
    'DBas-A+3': ([(0, 0), (5, 0), (5, 1), (8, 1), (8, 2), (5, 2), (5, 4), (0, 4)], (8, 1, 2)),
    'DB55-B+2': ([(0, 0), (5, 0), (5, 5), (0, 5), (0, 3), (-2, 3), (-2, 2), (0, 2)], (-2, 2, 3)),
}
MARKS = {
    'DB55-A': [(1, 1), (3, 4), (F(5, 2), F(1, 1013))],
    'DB55-B': [(4, 1), (1, 3), (F(7, 3), F(4999, 1000))],
    'DBas-A': [(1, 3), (4, 1), (F(1, 2), F(3, 2))],
    'DBas-B': [(1, 3), (2, 4), (F(7, 2), F(-1, 2))],
    'DBas-A+3': [(1, 3), (4, 2), (F(13, 2), F(3, 2))],
    'DB55-B+2': [(4, 1), (2, 2), (F(-1), F(5, 2))],
}
SLOPES = [F(3, 10), F(2, 7), F(5, 13), F(1, 9), F(7, 3), F(11, 4), F(13, 17), F(1, 1), F(9, 2), F(17, 40)]


def data(V, mouth, cuts, S, s, hx, hy):
    try:
        r = leg(V, mouth, cuts, S, s, hx, hy)
        return ('ok', tuple(r['states']), r['exit']), r
    except Irregular as e:
        return ('irr', str(e)), None


def main():
    tot = agree = reg = 0
    neg = {'K/2': [0, 0], 'uncut': [0, 0]}
    nh_changed = 0
    for name, (V, mouth) in CH.items():
        vx = sorted(set(x for x, _ in V))
        for S in MARKS[name]:
            cuts = vx + [S[0]]
            K, rects = slab_period(V, cuts)
            K0, _ = slab_period(V, vx)  # without the mark cut
            print(f"{name} S={S} K={K} (uncut-slab period {K0}) rects={len(rects)}")
            for s in SLOPES:
                for hx in (1, -1):
                    for hy in (1, -1):
                        base, r0 = data(V, mouth, cuts, S, s, hx, hy)
                        reg += base[0] == 'ok'
                        for k in (1, 2, 3):
                            cur, r1 = data(V, mouth, cuts, S, s + k * K, hx, hy)
                            tot += 1
                            same = (cur[0] == base[0] == 'irr') or cur == base
                            agree += same
                            if not same:
                                print("  MISMATCH", name, S, s, hx, hy, k, base[:1], cur[:1])
                            if r0 and r1 and r0['nh'] != r1['nh']:
                                nh_changed += 1
                        if base[0] == 'ok':
                            for lab, KK in (('K/2', K / 2), ('uncut', K0)):
                                if lab == 'uncut' and K % K0 == 0 and K0 == K:
                                    continue
                                cur, _ = data(V, mouth, cuts, S, s + KK, hx, hy)
                                neg[lab][0] += 1
                                neg[lab][1] += cur != base
    print(f"\nperiod K: {agree}/{tot} translate comparisons agree; {reg} regular base legs; "
          f"horizontal-reflection count changed in {nh_changed}")
    for lab, (n, bad) in neg.items():
        print(f"negative control {lab}: {bad}/{n} regular legs change data")


if __name__ == '__main__':
    main()
