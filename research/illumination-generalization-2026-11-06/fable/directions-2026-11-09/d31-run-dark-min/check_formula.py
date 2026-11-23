"""Check W(P) = d (W(R) - 4) + 4 + 2 n3 on every strictly simple glued room
(bases area <= 8, d <= 7), where n3 counts reflex corners of P over convex
corners of R. Also confirm the W = 28 room is P6 of d30 up to symmetry."""
import sys; sys.argv = ['glue.py', '8', '7']
import glue as G
n = bad = 0
for b in G.bases(8):
    R = set(b['cells']); Rp = G.points(R); tR = G.room_ok(R)[0]
    level = {((1, 1, 0, 0),)}
    lines = sorted({('x', x + dx) for (x, y) in R for dx in (0, 1)} | {('y', y + dy) for (x, y) in R for dy in (0, 1)})
    for d in range(2, 8):
        nxt = set()
        for gs in level:
            cells = {G.gc(g, c) for g in gs for c in R}
            fold = {G.gp(g, p): p for g in gs for p in Rp}
            for g in gs:
                for k, a in lines:
                    g2 = G.gmul(g, (-1, 1, 2 * a, 0) if k == 'x' else (1, -1, 0, 2 * a))
                    if g2 in gs or any(G.gc(g2, c) in cells for c in R): continue
                    if any(fold.get(G.gp(g2, p), p) != p for p in Rp): continue
                    nxt.add(tuple(sorted(gs + (g2,))))
        level = nxt
        for gs in level:
            cells = {G.gc(g, c) for g in gs for c in R}
            fold = {G.gp(g, p): p for g in gs for p in Rp}
            ok = G.room_ok(cells)
            if not ok: continue
            t, W, r = ok
            n3 = sum(v == 'reflex' and tR[fold[p]] == 'convex' for p, v in t.items())
            n += 1; bad += W != d * (b['W'] - 4) + 4 + 2 * n3
print("rooms checked", n, "formula failures", bad)
P6 = [(0,0),(1,0),(1,1),(2,1),(2,2),(0,-1),(1,-1),(1,-2),(2,-2),(2,-3),(5,-1),(4,-1),(4,-2),(3,-2),(3,-3),(0,5),(1,5),(1,4),(2,4),(2,3)]
import json
f = json.load(open('found.json'))[0]
print("W28 room == P6 up to symmetry:", G.canon(P6) == G.canon([tuple(c) for c in f['cells']]))
