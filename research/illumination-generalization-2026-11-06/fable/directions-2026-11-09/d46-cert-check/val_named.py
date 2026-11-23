"""d46 requirement 3a: named rooms through cert_check (C, stdin mode) and verify_room.py
(two Python implementations).  Room definitions copied from ../d44-cert-check-sizing/validate_named.py.
Expected (d44): 22-wall POSITIVE at S (0,0) T (2,2); P6 POSITIVE at S (1,0) T (3,-2);
cross, cross x2, cross x3 negative.  Also every one of the 8 lattice images of each room
must give the same number of positive pairs and the same multiset of block counts.
"""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verify_room import verify, rt  # noqa: E402

R22 = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1),
       (5, 0), (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]
Q = {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)}
P6 = Q | {(i, -j - 1) for i, j in Q} | {(5 - i, -j - 1) for i, j in Q} | {(i, 5 - j) for i, j in Q}
cross = {(i, j) for i in range(4) for j in range(1, 3)} | {(i, j) for i in range(1, 3) for j in range(4)}
def scale(c, k):
    return {(k * i + u, k * j + v) for (i, j) in c for u in range(k) for v in range(k)}
ROOMS = [('22-wall', rt.cells_from_vertices(R22)), ('P6', P6), ('cross', cross),
         ('cross x2', scale(cross, 2)), ('cross x3', scale(cross, 3))]

def images(cells):
    """the 8 lattice images (cell (i,j) = [i,i+1]x[j,j+1])"""
    out = []
    for sw in (0, 1):
        for fx in (0, 1):
            for fy in (0, 1):
                im = set()
                for (i, j) in cells:
                    a, b = (-i - 1 if fx else i), (-j - 1 if fy else j)
                    im.add((b, a) if sw else (a, b))
                out.append(im)
    return out

def line(c):
    return ' '.join([str(len(c))] + ['%d %d' % p for p in sorted(c)])

def run_c(rooms):
    out = subprocess.run([str(HERE / 'cert_check'), 'stdin', 'v'], input='\n'.join(line(c) for c in rooms) + '\n',
                         capture_output=True, text=True, check=True).stdout
    res, cur = [], None
    for ln in out.splitlines():
        if ln.startswith('room'):
            cur = {'line': ln, 'pos': []}; res.append(cur)
        elif 'POSITIVE' in ln:
            cur['pos'].append(ln.strip())
    return res

fail = 0
for name, cells in ROOMS:
    c = run_c([cells])[0]
    v = verify(cells)
    print('==', name, 'n', v['n'], 'r', v['r'], 'W', 2 * v['r'] + 4, 'rho', v['rho'], 'fstar(no r cap)', v['fstar'])
    print('  C  :', c['line'])
    for p in c['pos']:
        print('      ', p)
    print('  I  : blocks', v['blocksI'], 'positives', v['posI'])
    print('  II : blocks', v['blocksII'], 'positives', v['posII'])
    cpos = sorted(p.split('S ')[1] for p in c['pos'])
    ipos = sorted('%s T %s' % (('(%d,%d)' % s), ('(%d,%d)' % t)) for _, s, t in v['posI'])
    agree = v['posI'] == v['posII'] and v['blocksI'] == v['blocksII'] and cpos == ipos
    # C block counts per origin class (only classes with >= 2 marks; C stops at the first one-block B_x)
    print('  C vs I vs II positives agree:', agree)
    fail += not agree
    # symmetry invariance
    ims = images(cells)
    cres = run_c(ims)
    npos = [len(x['pos']) for x in cres]
    vb = [sorted(tuple(sorted(b)) for b in verify(im)['blocksI'].values()) for im in ims]
    sym_ok = len(set(npos)) == 1 and all(x == vb[0] for x in vb)
    print('  8 images: C positive pairs', npos, '| block multisets equal (I):', all(x == vb[0] for x in vb), '->', 'OK' if sym_ok else 'FAIL')
    fail += not sym_ok
print('FAILURES', fail)
