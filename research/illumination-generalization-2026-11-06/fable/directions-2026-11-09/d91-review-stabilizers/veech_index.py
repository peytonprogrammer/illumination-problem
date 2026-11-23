"""Count the SL(2,Z)-orbit of the marked, sigma-equipped origami of Q (= index of the
Q-Veech group in SL(2,Z)). Run: python3 -B veech_index.py b cap"""
import sys
import time
import hashlib
from array import array
from origami import Surface, cross_cells, sigma_squares, stepT, stepV, canon

b, cap = int(sys.argv[1]), int(sys.argv[2])
S = Surface(cross_cells(b))
mk = [1 if S.vtype[S.LL[q][0]] == 'convex' else 0 for q in range(S.N)]
starts = [q for q in range(S.N) if mk[q]]
T0 = time.process_time()


def pack(st):
    return array('H', st[0] + st[1] + st[2]).tobytes()


def unpack(bs):
    a = array('H')
    a.frombytes(bs)
    N = S.N
    a = a.tolist()
    return a[:N], a[N:2 * N], a[2 * N:]


st0 = (S.r, S.u, sigma_squares(S))
key0 = hashlib.blake2b(repr(canon(st0, mk, starts)[0]).encode(), digest_size=16).digest()
seen = {key0}
queue = [pack(st0)]
i = 0
while i < len(queue) and len(seen) <= cap:
    st = unpack(queue[i])
    queue[i] = None
    i += 1
    for step in (stepT, stepV):
        n = step(st, 1)
        k = hashlib.blake2b(repr(canon(n, mk, starts)[0]).encode(), digest_size=16).digest()
        if k not in seen:
            seen.add(k)
            queue.append(pack(n))
    if i % 20000 == 0:
        print(f'  expanded {i}, seen {len(seen)}, cpu {time.process_time() - T0:.0f}s', flush=True)
done = i == len(queue)
print(f'cross b={b}: orbit {"complete" if done else "INCOMPLETE"}; size {len(seen)}; '
      f'cpu {time.process_time() - T0:.0f}s')
