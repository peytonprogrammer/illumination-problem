# Owned copy of Codex's arithmetic/audit.py. Changes: OWN path and SRC for read-only inputs; receipts written here.
"""Bind independently reconstructed arithmetic encodings to saved base CNFs.

No SAT solver is constructed. Source-level extension proof is in findings.txt.
Run with bounded-proof/venv/bin/python -B from the workspace root.
"""
from pathlib import Path
from collections import Counter
from itertools import product
import hashlib
import importlib.util
import importlib.metadata
import json
import sys
import time

HERE = Path(__file__).resolve().parent
OWN = HERE.parents[1] / "illumination-k4-codex"
SRC = OWN / "lower-bound-proof-audit/arithmetic"
PEER = OWN.parent / "claude-illumination-check/k6-run"
sys.path.insert(0, str(OWN / "k5-proof-pilot/inputs"))
from pysat.card import CardEnc
from pysat.pb import PBEnc
import pysat.card, pysat.pb, pysat.formula, pycard, pindakaas


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def clauses_key(clauses):
    # Preserve duplicates and tautologies; only literal/clause order is ignored.
    return Counter(tuple(sorted(c)) for c in clauses)


def counter(lits, bound, top):
    """Knuth's reduced prefix-threshold construction, independently emitted."""
    result = []
    ids = {}
    def cell(k, j):
        nonlocal top
        if (k, j) not in ids:
            top += 1
            ids[k, j] = top
        return ids[k, j]
    n = len(lits)
    if bound >= n:
        return result, top
    if bound == n - 1:
        return [[-v for v in lits]], top
    if bound == 0:
        return [[-v] for v in lits], top
    assert 0 < bound < n - 1
    for j in range(n - bound):
        result.append([-lits[j], cell(0, j)])
        for k in range(bound - 1):
            a = cell(k, j)
            if j < n - bound - 1:
                result.append([-a, cell(k, j + 1)])
            result.append([-lits[j + k + 1], -a, cell(k + 1, j)])
        a = cell(bound - 1, j)
        if j < n - bound - 1:
            result.append([-a, cell(bound - 1, j + 1)])
        result.append([-lits[j + bound], -a])
    return result, top


def neg(x):
    return not x if isinstance(x, bool) else -x


class Adder:
    """Literal bucket compression with direct parity and majority clauses."""
    def __init__(self, top):
        self.top = top
        self.clauses = []
        self.branches = Counter()

    def fresh(self):
        self.top += 1
        return self.top

    def clause(self, *lits):
        if any(x is True for x in lits):
            return
        cl = [x for x in lits if x is not False]
        assert cl, "unexpected contradiction in an actual arithmetic call"
        self.clauses.append(cl)

    def parity(self, xs, out):
        vals = list(xs) + [out]
        target = sum(v is True for v in vals) % 2
        lits = [v for v in vals if not isinstance(v, bool)]
        assert len(lits) <= 4
        for mask in range(1 << len(lits)):
            if mask.bit_count() % 2 != target:
                self.clause(*(neg(v) if mask >> i & 1 else v
                              for i, v in enumerate(lits)))

    def carry(self, xs, out):
        assert len(xs) in (2, 3) and all(type(x) is int for x in xs)
        if len(xs) == 2:
            x, y = xs
            self.clause(-x, -y, out)
            self.clause(x, neg(out))
            self.clause(y, neg(out))
        else:
            x, y, z = xs
            for a, b in ((x, y), (x, z), (y, z)):
                self.clause(a, b, neg(out))
            for a, b in ((x, y), (x, z), (y, z)):
                self.clause(-a, -b, out)

    @staticmethod
    def carry_to(buckets, column, x):
        while column < len(buckets) and x in buckets[column]:
            column += 1
        if column == len(buckets) or -x not in buckets[column]:
            return column
        return None

    def carry_into(self, buckets, column, x):
        rest = self.carry_to(buckets, column, x)
        if rest is None:
            return False
        for c in range(column, min(rest, len(buckets))):
            buckets[c].remove(x)
        if rest < len(buckets):
            buckets[rest].append(x)
        else:
            self.clause(-x)
        return True

    def other(self, buckets, column, bit, xs, circuit):
        y = buckets[column].pop()
        circuit(xs, -y if bit else y)
        if not bit:
            assert self.carry_into(buckets, column + 1, y)

    def encode(self, lits, weights, rhs):
        assert len(set(map(abs, lits))) == len(lits), "repeated PB variable"
        assert set(weights) == {1, 2, 4}
        assert 4 < rhs < sum(weights), "outside audited normalization branch"
        # Aggregation preserves each coefficient/polarity and sorts by variable.
        terms = sorted(zip(lits, weights), key=lambda lw: abs(lw[0]))
        bits = rhs.bit_length()
        target = [bool(rhs >> i & 1) for i in range(bits)]
        buckets = [[lit for lit, w in terms if w >> i & 1]
                   for i in range(bits)]
        forced = set()
        fixed = set()
        for column in range(bits):
            if not buckets[column]:
                assert not target[column]
                self.branches['empty'] += 1
                continue
            if len(buckets[column]) == 1:
                x = buckets[column].pop()
                unit = x if target[column] else -x
                if unit not in forced:
                    self.clause(unit)
                    forced.add(unit)
                self.branches['unit'] += 1
                continue
            while len(buckets[column]) >= 2:
                last = len(buckets[column]) <= 3
                start = 0 if last else len(buckets[column]) - 3
                group = buckets[column][start:]
                del buckets[column][start:]
                if last:
                    key = (tuple(sorted(group)), target[column])
                    if key not in fixed:
                        self.parity(group, target[column])
                        fixed.add(key)
                    self.branches['parity_fixed'] += 1
                elif len(buckets[column]) == 1 and (
                    target[column] or self.carry_to(
                        buckets, column + 1, buckets[column][0]) is not None
                ):
                    self.other(buckets, column, target[column], group, self.parity)
                    self.branches['parity_other'] += 1
                else:
                    out = self.fresh()
                    self.parity(group, out)
                    buckets[column].append(out)
                    self.branches['parity_new'] += 1

                known = last and len(group) == 2
                carried = False
                if known and not target[column]:
                    for x in group:
                        if self.carry_into(buckets, column + 1, x):
                            carried = True
                            break
                if known and (target[column] or carried):
                    self.branches['carry_known'] += 1
                elif column + 1 >= bits:
                    self.carry(group, False)
                    self.branches['carry_top'] += 1
                elif last and not buckets[column + 1]:
                    self.carry(group, target[column + 1])
                    target[column + 1] = False
                    self.branches['carry_fixed'] += 1
                elif (last and len(buckets[column + 1]) == 1
                      and all(abs(x) != abs(buckets[column + 1][0]) for x in group)
                      and (target[column + 1] or self.carry_to(
                          buckets, column + 2, buckets[column + 1][0]) is not None)):
                    self.other(buckets, column + 1, target[column + 1],
                               group, self.carry)
                    target[column + 1] = False
                    self.branches['carry_other'] += 1
                else:
                    out = self.fresh()
                    self.carry(group, out)
                    buckets[column + 1].append(out)
                    self.branches['carry_new'] += 1
            assert not buckets[column]
        return self.clauses, self.top


def gate_controls():
    checks = 0
    for n in (2, 3):
        for kind in ('parity', 'carry'):
            for output in (n + 1, False, True):
                a = Adder(n + 1)
                getattr(a, kind)(list(range(1, n + 1)), output)
                for values in product((False, True), repeat=n + 1):
                    def val(lit):
                        return values[abs(lit) - 1] == (lit > 0)
                    holds = all(any(val(l) for l in cl) for cl in a.clauses)
                    out = values[n] if type(output) is int else output
                    want = (sum(values[:n]) % 2 == out) if kind == 'parity' else (
                        (sum(values[:n]) >= 2) == out)
                    assert holds == want
                    checks += 1
    return checks


def main():
    started = time.monotonic()
    # Fail closed: these observations must match the reviewed source releases.
    assert importlib.metadata.version('python-sat') == '1.9.dev17'
    assert importlib.metadata.version('pindakaas') == '0.6.1'
    inventory = json.loads((SRC / 'source-inventory.json').read_text())
    for row in inventory:
        assert digest(SRC / Path(row['archive']).name) == row['sha256']
    source = SRC / 'sources/python_sat-1.9.dev17/pysat'
    installed = []
    for m in (pysat.card, pysat.pb, pysat.formula, pycard, pindakaas):
        installed.append(dict(path=m.__file__, sha256=digest(m.__file__)))
    for m in (pysat.card, pysat.pb, pysat.formula):
        assert digest(m.__file__) == digest(source / Path(m.__file__).name)

    card_real = CardEnc.atmost
    pb_real = PBEnc.equals
    call_receipts = []
    current_case = None

    def wrap(kind, original, **kwargs):
        pool = kwargs['vpool']
        assert not pool._occupied, 'unreviewed occupied-range variable remapping'
        before = pool.top
        lits = kwargs['lits']
        assert len(set(map(abs, lits))) == len(lits)
        top = max([before] + list(map(abs, lits)))
        assert top == before
        if kind == 'cardinality':
            assert kwargs['encoding'] == 1
            predicted, last = counter(lits, kwargs['bound'], top)
            branches = None
        else:
            assert kwargs['encoding'] == 4
            a = Adder(top)
            predicted, last = a.encode(lits, kwargs['weights'], kwargs['bound'])
            branches = dict(a.branches)
        actual = original(**kwargs)
        assert actual.nv == last == pool.top, (current_case, kind, last, actual.nv)
        want, got = clauses_key(predicted), clauses_key(actual.clauses)
        if want != got:
            raise AssertionError((current_case, kind, 'clause mismatch',
                                  list((want - got).items())[:3],
                                  list((got - want).items())[:3]))
        call_receipts.append(dict(case=current_case, kind=kind, inputs=len(lits),
                                  bound=kwargs['bound'], top_before=top,
                                  top_after=last, clauses=len(predicted), branches=branches,
                                  input_sha256=hashlib.sha256(json.dumps(
                                      {'lits': lits, 'weights': kwargs.get('weights'),
                                       'bound': kwargs['bound']}, sort_keys=True).encode()).hexdigest()))
        return actual

    CardEnc.atmost = staticmethod(lambda **kw: wrap('cardinality', card_real, **kw))
    PBEnc.equals = staticmethod(lambda **kw: wrap('weighted_equality', pb_real, **kw))
    path = OWN / 'k5-proof-pilot/inputs/encode.py'
    spec = importlib.util.spec_from_file_location('audited_geometry', path)
    encoder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(encoder)
    cases = json.loads((PEER / 'cases.json').read_text())
    i4_shapes = {'O': [(0,0),(1,0),(0,1),(1,1)],
                 'T': [(0,1),(1,0),(1,1),(2,1)],
                 'S': [(0,0),(1,0),(1,1),(2,1)]}
    cases += [dict(tag='I4_'+name, full=full, i4=name)
              for name, full in i4_shapes.items()]
    frozen = json.loads((OWN / 'k6-final-review/encoder-binding.json').read_text())
    assert digest(path) == frozen['encoder_sha256']
    case_receipts = []
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(cases)
    for case in cases[:limit]:
        current_case = case['tag']
        full = case['full']
        if 'i4' in case:
            allowed = sorted(set(map(tuple, full)) | {
                (a+dx,b+dy) for a,b in full
                for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))})
        else:
            allowed = [(a+dx, b+dy) for a,b in full
                       for dx in range(-14,15) for dy in range(-14,15)
                       if abs(dx)+abs(dy) <= 14]
        start_calls = len(call_receipts)
        cnf, pool, x, ts = encoder.geometry(dict(full=full, allowed=allowed), 21, 6)
        if 'i4' in case:
            saved = PEER.parent / 'k6-i4' / (case['i4'] + '.cnf')
            previous = json.loads((OWN / 'k6-i4-review/check.json').read_text())
            bound = next(r for r in previous['cases'] if r['shape'] == case['i4'])
            assert digest(saved) == bound['cnf_sha256']
        else:
            bound = next(r for r in frozen['cases'] if r['tag'] == current_case)
            assert len(cnf.clauses) == bound['base_clauses']
            saved = PEER / 'cases' / current_case / 'formula.cnf'
        with saved.open() as f:
            assert next(f).startswith('p cnf ')
            for i, cl in enumerate(cnf.clauses):
                assert list(map(int, next(f).split())) == cl + [0], (current_case, i)
            if 'i4' in case:
                assert not f.read().strip(), 'unexpected I4 suffix'
        row = dict(case=current_case, base_clauses=len(cnf.clauses),
                   arithmetic_calls=len(call_receipts)-start_calls, prefix_identical=True)
        case_receipts.append(row)
        print(json.dumps(row), flush=True)
    result = dict(status='PASS', scope='I2/I3 and I4 arithmetic clauses and saved base prefixes',
                  cases=len(case_receipts), full_run=len(case_receipts) == len(cases),
                  calls=call_receipts, case_receipts=case_receipts,
                  elementary_gate_checks=gate_controls(), installed=installed,
                  seconds=round(time.monotonic()-started, 3), solver_calls=0)
    (HERE / 'receipts.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()
                      if k not in ('calls', 'case_receipts','installed')}), flush=True)


if __name__ == '__main__':
    main()
