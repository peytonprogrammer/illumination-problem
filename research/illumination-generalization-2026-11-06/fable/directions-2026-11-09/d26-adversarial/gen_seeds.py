"""Seed rooms: 22-wall room with one rectangle added or removed (W <= 20), their 2x scalings,
spirals, combs, staircases. Output: one room per line "A x y ...". adv re-validates each."""
import random, itertools
random.seed(26)
R22 = [(0,2),(0,3),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,4),(2,5),(3,4),(3,5),(4,3),(4,4),(5,3)]
def walls(c):
    pts = {(x + i, y + j) for x, y in c for i in (0, 1) for j in (0, 1)}
    W = 0
    for X, Y in pts:
        k = [(X - 1, Y - 1) in c, (X, Y - 1) in c, (X - 1, Y) in c, (X, Y) in c]
        if sum(k) == 2 and k[0] == k[3]: return 99
        W += sum(k) in (1, 3)
    return W
def norm(c):
    x0 = min(x for x, _ in c); y0 = min(y for _, y in c)
    return frozenset((x - x0, y - y0) for x, y in c)
def scale(c, k): return {(k * x + i, k * y + j) for x, y in c for i in range(k) for j in range(k)}
out = set()
base = set(R22)
for x0, y0 in itertools.product(range(-1, 7), repeat=2):
    for a, b in itertools.product(range(1, 5), repeat=2):
        rect = {(x0 + i, y0 + j) for i in range(a) for j in range(b)}
        for c in (base | rect, base - rect):
            if c and c != base and walls(c) <= 20:
                out.add(norm(c)); out.add(norm(scale(c, 2)))
n22 = len(out)
def rect(x0, y0, x1, y1): return {(x, y) for x in range(min(x0, x1), max(x0, x1) + 1) for y in range(min(y0, y1), max(y0, y1) + 1)}
for _ in range(60):                       # spirals
    w = random.choice([2, 2, 3, 4]); s = random.choice([1, 1, 2, 3]); arms = random.randint(5, 9)
    L = random.randint(arms * (w + s) // 2 + w + 2, 40); x = y = 0; c = set()
    D = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for i in range(arms):
        ln = L - ((i + 1) // 2) * (w + s)
        if ln < w + 1: break
        dx, dy = D[i % 4]; nx, ny = x + dx * ln, y + dy * ln
        c |= rect(x, y, nx + w - 1, ny + w - 1); x, y = nx, ny
    if walls(c) <= 20: out.add(norm(c))
for _ in range(40):                       # combs
    t = random.randint(3, 5); tw = random.randint(2, 5); gw = random.randint(1, 4); tl = random.randint(2, 30); sp = random.randint(2, 5)
    c = rect(0, 0, t * tw + (t - 1) * gw - 1, sp - 1)
    for i in range(t): c |= rect(i * (tw + gw), sp, i * (tw + gw) + tw - 1, sp + tl + random.choice([0, 0, 1, 2]) - 1)
    if walls(c) <= 20: out.add(norm(c))
for _ in range(40):                       # staircases (Young-diagram type and shifted stacks)
    n = random.randint(4, 9); c = set(); a = random.randint(2, 6); b = random.randint(2, 6)
    if random.random() < 0.5:
        for i in range(n): c |= rect(0, i * b, (n - i) * a - 1, i * b + b - 1)
    else:
        n = min(n, 5); sh = random.randint(1, 5); ln = random.randint(sh + 2, 20)
        for i in range(n): c |= rect(i * sh, i * b, i * sh + ln - 1, i * b + b - 1)
    if walls(c) <= 20: out.add(norm(c))
rooms = sorted(out, key=lambda c: (len(c), sorted(c)))
for c in rooms: print(len(c), " ".join("%d %d" % p for p in sorted(c)))
import sys; print("22-wall variants incl. 2x:", n22, "total", len(rooms), file=sys.stderr)
