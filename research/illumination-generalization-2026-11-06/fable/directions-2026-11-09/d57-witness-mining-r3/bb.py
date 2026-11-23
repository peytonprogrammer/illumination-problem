"""Branch and bound cover of a truncated type region by certified boxes.

Normalization (charts): A: X_nx = 1, Y_ny <= 1.  B: Y_ny = 1, X_nx <= 1.
Truncated region R_delta: every grid gap >= delta and every odd point
coordinate at distance >= delta/2 from both grid lines of its gap.
A box is dropped when some region form is < its threshold on the whole box
(then the box misses R_delta). A box is certified when it lies in the open
type region and one itinerary passes the interval certifier on it.
All box endpoints are integers on the scale 2^N (dyadic rationals)."""
import random, time, math
import wm

N = 24
SC = 1 << N


class Cover:
    """Truncated region R_delta: gx0 = 1 (scale); every other gap in
    [1/D, D]; every odd point offset within gap/dp of neither end."""
    def __init__(self, par, D=4, dp=8, nang=1500, maxref=12, seed=1):
        self.par = par
        self.nv = len(par.names)
        self.reg = par.region(dp)
        self.D, self.dp = D, dp
        b = []
        for nm in par.names:
            if nm == 'gx0': b.append((SC, SC))
            elif nm[0] == 'g': b.append((SC // D, SC * D))
            else: b.append((0, SC * D))
        self.box0 = b
        self.pool = {}            # itin -> [conds, sx, sy, wins]
        self.nang, self.maxref = nang, maxref
        self.rng = random.Random(seed)
        self.cert, self.unc = [], []
        self.stats = dict(boxes=0, dropped=0, mined=0, certs=0, tries=0)

    def classify(self, box):
        inside = True; self.edgevars = set()
        for fo, ft in self.reg:
            if wm.iv(ft, box)[1] < 0: return 'out'
            if wm.iv(fo, box)[0] <= 0:
                inside = False; self.edgevars |= {v for v, c in fo}
        return 'in' if inside else 'edge'

    def center(self, box):
        return {k: (l + h) // 2 for k, (l, h) in enumerate(box)}

    def add_mined(self, box):
        c = self.center(box)
        vals = {k: v / SC for k, v in c.items()}
        got = []
        for it, sx, sy in wm.mine(self.par, vals, self.nang, self.maxref, seed=self.rng.random()):
            if it not in self.pool:
                conds, _ = wm.conditions(self.par, it, sx, sy)
                self.pool[it] = [conds, sx, sy, 0]
            got.append(it)
        self.stats['mined'] += 1
        return got

    def try_its(self, box, its, limit):
        cb = [(v, v) for v in (self.center(box)[k] for k in range(self.nv))]
        tried = 0
        for it in its:
            rec = self.pool[it]
            if not wm.certify(rec[0], cb): continue        # exact check at the centre
            self.atc.append(it); tried += 1; self.stats['tries'] += 1
            if wm.certify(rec[0], box):
                rec[3] += 1
                return it
            if self.hint is None: self.hint = wm.split_hint(wm.LAST_FAIL[0], box)
            if tried >= limit: break
        return None

    def try_box(self, box, inherited=(), top=10, limit=12):
        """Returns (certified itinerary or None, itineraries valid at the centre)."""
        self.atc = []; self.hint = None
        it = self.try_its(box, list(inherited), limit)
        if it is None:
            best = sorted(self.pool, key=lambda i: (-self.pool[i][3], len(i)))[:top]
            it = self.try_its(box, [i for i in best if i not in inherited], limit)
        if it is None and not self.atc:
            it = self.try_its(box, self.add_mined(box)[:40], limit)
        return it, self.atc

    def run(self, maxboxes=2000, maxdepth=60, cpu=60.0):
        t0 = time.process_time()
        import heapq
        stack = [(0, 0, self.box0, ())]; cnt = 0
        while stack:
            d, _, box, inh = heapq.heappop(stack)
            if self.stats['boxes'] >= maxboxes or d > maxdepth or time.process_time() - t0 > cpu:
                if self.classify(box) != 'out': self.unc.append(box)
                continue
            self.stats['boxes'] += 1
            cl = self.classify(box)
            if cl == 'out':
                self.stats['dropped'] += 1; continue
            self.hint = None
            if cl == 'in':
                it, inh = self.try_box(box, inh)
                if it is not None:
                    self.cert.append((box, it)); self.stats['certs'] += 1; continue
            cand = [k for k in range(self.nv) if box[k][0] < box[k][1]]
            if cl == 'edge': cand = [k for k in cand if k in self.edgevars] or cand
            k = max(cand, key=lambda k: box[k][1] - box[k][0])
            if cl == 'in' and self.hint is not None and box[self.hint][0] < box[self.hint][1]:
                k = self.hint
            l, h = box[k]; m = (l + h) // 2
            b1 = list(box); b1[k] = (l, m); b2 = list(box); b2[k] = (m, h)
            inh = tuple(inh)[:12]
            cnt += 2
            heapq.heappush(stack, (d + 1, cnt, b1, inh)); heapq.heappush(stack, (d + 1, cnt + 1, b2, inh))
        self.stats['cpu'] = round(time.process_time() - t0, 2)
        return self

    # ---- Monte Carlo estimate of the certified fraction of R_delta (COMPUTED)
    def sample_region(self):
        """Gaps log-uniform in [1/D, D], offsets uniform in the truncated range."""
        par, rng = self.par, self.rng
        v = [0] * self.nv
        for k, nm in enumerate(par.names):
            if nm == 'gx0': v[k] = SC
            elif nm[0] == 'g': v[k] = int(SC * self.D ** rng.uniform(-1, 1))
        for k, nm in enumerate(par.names):
            if nm[0] == 'a':
                g = v[par.gapvar(nm)]
                v[k] = rng.randrange(-(-g // self.dp), g - g // self.dp)
        return v

    def covered(self, v):
        for box, it in self.cert:
            if all(l <= x <= h for x, (l, h) in zip(v, box)): return it
        return None

    def fraction(self, n=400):
        hits = 0; miss = []
        for _ in range(n):
            v = self.sample_region()
            if self.covered(v) is not None: hits += 1
            else: miss.append(v)
        return hits / n, miss
