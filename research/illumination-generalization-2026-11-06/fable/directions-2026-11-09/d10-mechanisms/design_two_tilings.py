"""One design attempt for a second kind of dark room (theory.md, section 3.8).  Not a room search.

Design: the room is a union of whole mirror copies of the vertical S-tetromino (a base with
every b- and c-point a corner and one flat d-point) and, at the same time, a union of whole
mirror copies of the transposed pattern (every d- and c-point a corner, one flat b-point).
Mirror copies of one base sit in a fixed box lattice, so the candidate cells form a periodic
set.  The script removes every cell whose copy is incomplete, on the 12 x 12 torus, for each
of the six class-preserving offsets.  Result: nothing survives, so no room has this design.

The first loop works in a finite window and is kept only as a cross-check; window edges can
remove cells wrongly, so the torus loop is the result.
"""
def vcopy_cells(i, j):
    if (i % 2, j % 2) == (0, 0): return [(2*i, 3*j-1), (2*i, 3*j), (2*i+1, 3*j), (2*i+1, 3*j+1)]
    if (i % 2, j % 2) == (1, 0): return [(2*i+1, 3*j-1), (2*i+1, 3*j), (2*i, 3*j), (2*i, 3*j+1)]
    if (i % 2, j % 2) == (0, 1): return [(2*i, 3*j+1), (2*i, 3*j), (2*i+1, 3*j), (2*i+1, 3*j-1)]
    return [(2*i+1, 3*j+1), (2*i+1, 3*j), (2*i, 3*j), (2*i, 3*j-1)]

def vcopy_of(cell):
    x, y = cell
    i, j = x // 2, (y + 1) // 3
    cs = vcopy_cells(i, j)
    return (i, j) if cell in cs else None

def hcopy_cells(i, j, u, v):
    return [(y + u, x + v) for (x, y) in vcopy_cells(i, j)]

def hcopy_of(cell, u, v):
    x, y = cell
    c = vcopy_of((y - v, x - u))
    return c

L = 36
for u in (0, 2, 4):
    for v in (0, 2):
        R = set()
        for x in range(-L, L):
            for y in range(-L, L):
                if vcopy_of((x, y)) is not None and hcopy_of((x, y), u, v) is not None:
                    R.add((x, y))
        changed = True
        while changed:
            changed = False
            for c in list(R):
                if c not in R: continue
                vc = vcopy_cells(*vcopy_of(c))
                hc = hcopy_cells(*hcopy_of(c, u, v), u, v)
                if not all(k in R for k in vc) or not all(k in R for k in hc):
                    # only trust removals away from the window edge
                    R.discard(c); changed = True
        core = {c for c in R if abs(c[0]) < 12 and abs(c[1]) < 12}
        print('offset', (u, v), 'cells surviving in the central window:', len(core))

print('torus computation (period 12 x 12, no window edge)')
M = 12
def mod(c): return (c[0] % M, c[1] % M)
for u in (0, 2, 4):
    for v in (0, 2):
        R = {(x, y) for x in range(M) for y in range(M)
             if vcopy_of((x, y)) is not None and hcopy_of((x, y), u, v) is not None}
        n0 = len(R)
        changed = True
        while changed:
            changed = False
            for c in list(R):
                vc = [mod(k) for k in vcopy_cells(*vcopy_of(c))]
                hc = [mod(k) for k in hcopy_cells(*hcopy_of(c, u, v), u, v)]
                if not all(k in R for k in vc) or not all(k in R for k in hc):
                    R.discard(c); changed = True
        print('offset', (u, v), 'cells in both patterns:', n0, 'after closure:', len(R))
