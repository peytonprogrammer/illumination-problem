"""Independent witness check of Codex's clause-provenance packet (item B), claimed on the board 2026-11-02.

No solver, tracer, guard search, or optical computation. For each of the 61 I2/I3 formulas:
1. The first len(geometry) clauses equal the frozen encoder's geometry(case, 21, 6) clauses, in order.
2. Every later clause is the clause of exactly one witness in clause-witnesses.jsonl.gz. This script
   recomputes that clause from the cited guard record, D4 matrix, and endpoint, with the encoder's own
   triangle variables and the encoder's own patch() as the definition of a canonical tile.
3. Guard files and formulas have the same SHA-256 here, in Codex's provenance freeze, and in the
   full-replay manifest whose records were physically replayed.
Run: .context/illumination-k4-codex/bounded-proof/venv/bin/python -B <this file>
"""
import gzip
import hashlib
import importlib.util
import json
import struct
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CTX = HERE.parents[1]
CODEX = CTX / "illumination-k4-codex"
PROV = CODEX / "lower-bound-proof-audit/provenance"
INPUTS = CODEX / "k5-proof-pilot/inputs"
K6 = CTX / "claude-illumination-check/k6-run"
T0 = time.time()


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def packed(clause):
    return struct.pack("<" + "i" * len(clause), *clause)


sys.path.insert(0, str(INPUTS))
spec = importlib.util.spec_from_file_location("enc", INPUTS / "encode.py")
enc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(enc)
binding = json.load(open(CODEX / "k6-final-review/encoder-binding.json"))
assert sha(INPUTS / "encode.py") == binding["encoder_sha256"], "encoder changed"

frozen = {r["path"]: r["sha256"] for r in json.load(open(PROV / "frozen-inputs.json"))["inputs"]}
manifest = json.load(open(CODEX / "lower-bound-proof-audit/full-replay/manifest.json"))
summary = json.load(open(PROV / "summary.json"))

guardfiles = [CODEX / "k5-proof-continuation/learned.jsonl", CODEX / "k5-proof-continuation/peer-guards.json",
              CODEX / "k5-proof-pilot/orbit-guard.json"] + sorted(K6.glob("cases/*/guards*.jsonl"))
assert [str(p) for p in guardfiles] == [g["path"] for g in manifest["guards"]] == [g["path"] for g in summary["guard_files"]]
for p, g in zip(guardfiles, manifest["guards"]):
    assert sha(p) == g["sha256"] == frozen[str(p)], f"guard hash {p}"

cases = json.load(open(K6 / "cases.json"))
assert len(cases) == 61 == len(manifest["proofs"])
cnf_sha = {r["tag"]: r["cnf_sha256"] for r in manifest["proofs"]}

# Per case: encoder variable map, exact base prefix, and the suffix keyed by the witness digest.
X, PAIR, SUFFIX, rows = [], [], [], []
for c in cases:
    tag = c["tag"]
    full = [tuple(p) for p in c["full"]]
    case = {"full": full, "allowed": [(a + dx, b + dy) for a, b in full for dx in range(-14, 15)
                                      for dy in range(-14, 15) if abs(dx) + abs(dy) <= 14]}
    cnf, pool, x, ts = enc.geometry(case, 21, 6)
    assert sorted(x.values()) == list(range(1, len(x) + 1)), "triangle variables are not 1..n"
    path = K6 / "cases" / tag / "formula.cnf"
    assert sha(path) == cnf_sha[tag] == frozen[str(path)], f"cnf hash {tag}"
    base, suffix, n, header = cnf.clauses, {}, 0, None
    with open(path) as f:
        for line in f:
            s = line.split()
            if not s or s[0] == "c":
                continue
            if s[0] == "p":
                assert header is None and n == 0 and s[1] == "cnf"
                header = (int(s[2]), int(s[3]))
                continue
            lits = list(map(int, s))
            assert lits[-1] == 0 and 0 not in lits[:-1], "one clause per line"
            lits = lits[:-1]
            if n < len(base):
                assert lits == list(base[n]), f"{tag} base clause {n} differs"
            else:
                assert all(1 <= abs(v) <= len(x) for v in lits), "suffix literal is not a triangle"
                cl = tuple(sorted(set(lits)))
                assert len(cl) == len(lits) and not {-v for v in cl} & set(cl)
                h = hashlib.sha256(packed(cl)).hexdigest()
                assert h not in suffix, "duplicate suffix clause"
                suffix[h] = cl
            n += 1
    assert header and header[1] == n and n >= len(base)
    X.append(x)
    PAIR.append([tuple(2 * v for v in p) for p in c["pair"]])
    SUFFIX.append(suffix)
    rows.append({"tag": tag, "base": len(base), "suffix": len(suffix), "triangles": len(x)})
    print(tag, rows[-1], round(time.time() - T0, 1), flush=True)

D4 = {(a, 0, 0, b) for a in (1, -1) for b in (1, -1)} | {(0, a, b, 0) for a in (1, -1) for b in (1, -1)}
FAN = {}


def canonical(t):
    t = tuple(sorted(map(tuple, t)))
    a = [p for p in t if p[0] % 2 == 0 and p[1] % 2 == 0]
    assert len(a) == 1, f"tile {t}"
    ax, ay = a[0]
    if a[0] not in FAN:
        FAN[a[0]] = set(enc.patch(ax - 1, ax + 1, ay - 1, ay + 1))
    assert t in FAN[a[0]], f"not an encoder tile: {t}"
    return t


def apply(t, m, o):
    return tuple(sorted((m[0] * a + m[1] * b + o[0], m[2] * a + m[3] * b + o[1]) for a, b in t))


by_file = defaultdict(list)
nwit = 0
with gzip.open(PROV / "clause-witnesses.jsonl.gz", "rt") as f:
    for line in f:
        w = json.loads(line)
        by_file[w["guard_file"]].append((w["record"], w["case"], w["clause_sha256"], tuple(w["matrix"]), tuple(w["origin"])))
        nwit += 1

used = [set() for _ in cases]
stats = Counter()
for fi, p in enumerate(guardfiles):
    if fi not in by_file:
        continue
    if p.suffix == ".jsonl":
        recs = {i: json.loads(l) for i, l in enumerate(open(p), 1) if l.strip()}
    else:
        raw = json.load(open(p))
        recs = dict(enumerate(raw if isinstance(raw, list) else [raw], 1))
    for rec_no, ci, h, m, o in by_file[fi]:
        r = recs[rec_no]
        q = tuple(r["q"])
        assert len(q) == 2 and q != (0, 0) and all(v % 2 == 0 for v in q)
        assert r["path"][0] == [[0, 1], [0, 1]]
        assert all(c[1] > 0 and c[0] == q[j] * c[1] for j, c in enumerate(r["path"][-1]))
        U = {canonical(t) for t in r["U"]}
        Z = {canonical(t) for t in r["Z"]}
        assert not U & Z
        assert m in D4
        s, t = PAIR[ci]
        assert o in (s, t)
        end = t if o == s else s
        assert (m[0] * q[0] + m[1] * q[1], m[2] * q[0] + m[3] * q[1]) == (end[0] - o[0], end[1] - o[1])
        x = X[ci]
        mu = [apply(u, m, o) for u in U]
        assert all(u in x for u in mu), "required tile outside the universe"
        mz = [apply(z, m, o) for z in Z]
        kept = [x[z] for z in mz if z in x]
        cl = tuple(sorted({-x[u] for u in mu} | set(kept)))
        assert len(cl) == len(U) + len(kept)
        assert hashlib.sha256(packed(cl)).hexdigest() == h, "witness digest"
        assert SUFFIX[ci][h] == cl, "witness clause differs from formula clause"
        assert h not in used[ci], "clause witnessed twice"
        used[ci].add(h)
        stats["reversed" if o == t else "forward"] += 1
        stats["absent_tiles_dropped"] += len(mz) - len(kept)
        stats["clauses_with_dropped_absent"] += len(mz) > len(kept)
        stats[f"file_{min(fi, 3)}"] += 1
    print("guard file", fi, len(by_file[fi]), round(time.time() - T0, 1), flush=True)

for ci, r in enumerate(rows):
    assert used[ci] == set(SUFFIX[ci]), f"{r['tag']}: unwitnessed suffix clauses"
for p, g in zip(guardfiles, manifest["guards"]):
    assert sha(p) == g["sha256"]
res = {"status": "PASS", "cases": len(rows), "base_clauses": sum(r["base"] for r in rows),
       "suffix_clauses": sum(r["suffix"] for r in rows), "witnesses": nwit,
       "base_only_cases": sum(r["suffix"] == 0 for r in rows), "stats": dict(stats),
       "seconds": round(time.time() - T0, 1), "rows": rows}
json.dump(res, open(HERE / "witness_check.json", "w"), indent=1)
print("PASS", {k: v for k, v in res.items() if k != "rows"}, flush=True)
