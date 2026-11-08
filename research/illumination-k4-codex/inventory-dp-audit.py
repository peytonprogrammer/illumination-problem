"""Independent solver-free verification of the vertex-inventory table.

At A/B a nonsmooth boundary fan has angle 1,2,3,5,6,7 in pi/4
units. Odd angles have one stub of each color; even angles have two
stubs of either color. Smooth fans have angle 4 and two same-color
stubs. At C, angles in pi/2 units are 1,2,3, with 2 smooth.
No triangle/fan helpers or OR-Tools are imported.
"""
import hashlib
import json
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAN_TYPES = ((1, 1), (2, 0), (2, 2), (3, 1),
             (5, 1), (6, 0), (6, 2), (7, 1))


def main():
    start = time.monotonic()
    p = HERE/'table.json'
    data = json.loads(p.read_text())
    assert data['status'] == 'COMPLETE'
    max_n = max(c['N'] for t in data['tables'] for c in t['cells'])
    # dp[angle][corner_count] is a bitset of possible stubs to the other acute label.
    dp = [{0: 1}]+[{} for _ in range(max_n)]
    for angle in range(1, max_n+1):
        for size, stubs in FAN_TYPES:
            if size > angle:
                continue
            for count, bits in dp[angle-size].items():
                if count < 23:
                    dp[angle][count+1] = dp[angle].get(count+1, 0) | bits << stubs

    @lru_cache(None)
    def fans(angle, smooth):
        if angle < 0:
            return {}
        return {count: sum_bits(bits, smooth) for count, bits in dp[angle].items()}

    def sum_bits(bits, smooth):
        result = 0
        for same in range(smooth+1):
            result |= bits << (2*same)
        return result

    def decide(c):
        i, j, sn, q, n, w = (c[key] for key in ('I', 'J', 's_N', 'Q', 'N', 'W'))
        sa = n-8*i-q
        if sa < 0 or 3*sa > q or n < w+6 or w != 2+6*i+q-2*j-sn:
            return None
        a = fans(n-8*i-4*sa, sa)
        for jb in range(j+1):
            jc = j-jb
            for sb in range(sn+1):
                sc = sn-sb
                b = fans(n-8*jb-4*sb, sb)
                kc = n-4*jc-2*sc
                if not b or kc < 0:
                    continue
                for c3 in range(kc//3+1):
                    c1 = kc-3*c3
                    cc = c1+c3
                    if cc > w:
                        continue
                    ab = w-2*cc+sa+sb-sc
                    if not 0 <= ab <= n or (n-ab)%2:
                        continue
                    for ca, a_bits in a.items():
                        cb = w-cc-ca
                        if not (a_bits & b.get(cb, 0)) >> ab & 1:
                            continue
                        ac = 2*(ca+sa)-ab
                        bc = 2*(cb+sb)-ab
                        if not (0 <= ac <= n and 0 <= bc <= n):
                            continue
                        if (n-ac)%2 or (n-bc)%2 or (ac-cc)%2:
                            continue
                        zc = (ac-cc)//2
                        if 0 <= zc <= sc and bc == cc+2*(sc-zc):
                            return dict(J_B=jb, J_C=jc, s_B=sb, s_C=sc,
                                        corners_A=ca, corners_B=cb, corners_C=cc,
                                        C_angle1=c1, C_angle3=c3,
                                        boundary_AB=ab, boundary_AC=ac, boundary_BC=bc)
        return None

    result = dict(status='RUNNING', scope='Independent solver-free audit of inventory feasibility, not polygon geometry or darkness.',
                  table_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  tables=[], disagreements=[])
    for table in data['tables']:
        counts = Counter()
        for c in table['cells']:
            witness = decide(c)
            expected = c['status'] in ('OPTIMAL', 'FEASIBLE')
            assert c['status'] in ('OPTIMAL', 'FEASIBLE', 'INFEASIBLE')
            if (witness is not None) != expected:
                result['disagreements'].append(dict(cell=c, dp_witness=witness))
            counts['feasible' if witness is not None else 'infeasible'] += 1
        result['tables'].append(dict(k=table['k'], checked=len(table['cells']), **counts))
        print(json.dumps(result['tables'][-1]), flush=True)
    result['status'] = 'PASS' if not result['disagreements'] else 'FAIL'
    result['seconds'] = time.monotonic()-start
    (HERE/'dp-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    assert result['status'] == 'PASS', 'Independent inventory verdict disagrees'


if __name__ == '__main__':
    main()
