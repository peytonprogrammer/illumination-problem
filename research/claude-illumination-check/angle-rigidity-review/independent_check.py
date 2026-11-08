"""Independent exact check of Codex's angle-changing escape direction (claimed on the board 2026-11-02).

No derivatives, no Codex code, and no new words, directions, rooms, or paths. Only the 147 saved event words.
1. Base room: each saved word is a legal path from S to T through exactly one corner, which it passes
   with zero reflections or exactly one reflection at an incident wall. The connecting side is derived
   from the unfolded corner wedge and compared with the saved perturb_side.
2. Tilted room V0 + eps*d for the strict escape vector d (eps = 1e-9 and 1e-12; 1e-6 is recorded only): the room stays strictly simple with interior
   marks; each word's unfolded line passes the corner on its non-connecting side, by the wedge rule
   recomputed in the tilted geometry; and f(eps)/eps approaches Codex's saved derivative values.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODEX = HERE.parents[1] / "illumination-k4-codex"
AR, RR = CODEX / "angle-rigidity", CODEX / "rigidity-review"

res = json.load(open(AR / "result.json"))
V0 = [tuple(map(F, v)) for v in res["vertices"]]
S0, T0 = (tuple(map(F, m)) for m in res["marks"])
events = json.load(open(RR / "events.json"))
esc = json.load(open(AR / "strict-escape.json"))
d = [F(x) for x in esc["delta"]]
saved = [F(x) for x in esc["constraint_values"]]
n = len(V0)
assert n == 22 and len(events) == 147 and len(d) == 48

# The same room, traced by hand from the preprint's five squares (attainment-review/findings.md).
HAND = [(-1, -1), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1), (5, 0),
        (3, 0), (3, 1), (1, 1), (1, -1), (2, -1), (2, -3), (1, -3), (1, -2), (0, -2), (0, -1)]


def sub(a, b): return (a[0] - b[0], a[1] - b[1])
def add(a, b): return (a[0] + b[0], a[1] + b[1])
def mul(k, a): return (k * a[0], k * a[1])
def cross(a, b): return a[0] * b[1] - a[1] * b[0]
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def sgn(x): return (x > 0) - (x < 0)


def reflect(p, a, b):
    e, v = sub(b, a), sub(p, a)
    return sub(add(a, mul(2 * dot(e, v) / dot(e, e), e)), v)


def unfold(p, walls, V):
    """Image of p in the copy reached after reflecting in walls[0], walls[1], ... (apply the last one first)."""
    for i in reversed(walls):
        p = reflect(p, V[i], V[(i + 1) % n])
    return p


def fold(p, walls, V):
    for i in walls:
        p = reflect(p, V[i], V[(i + 1) % n])
    return p


def inside(q, V):
    c = False
    for i in range(n):
        a, b = V[i], V[(i + 1) % n]
        if (a[1] > q[1]) != (b[1] > q[1]):
            c ^= q[0] < a[0] + (q[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
    return c


def proper_cross(p, q, a, b):
    d1, d2 = cross(sub(a, p), sub(q, p)), cross(sub(b, p), sub(q, p))
    d3, d4 = cross(sub(p, a), sub(b, a)), cross(sub(q, a), sub(b, a))
    return d1 * d2 < 0 and d3 * d4 < 0


def on_open(v, p, q):
    r, e = sub(v, p), sub(q, p)
    return cross(r, e) == 0 and 0 < dot(r, e) < dot(e, e)


def strictly_simple(V):
    for i in range(n):
        a, b = V[i], V[(i + 1) % n]
        if a == b or cross(sub(a, V[i - 1]), sub(b, a)) == 0:
            return False
        for j in range(i + 2, n):
            if (j + 1) % n == i:
                continue
            c, e = V[j], V[(j + 1) % n]
            if proper_cross(a, b, c, e) or any(on_open(x, a, b) for x in (c, e)) or any(on_open(x, c, e) for x in (a, b)):
                return False
    return True


def analyze(ev, V, S, T, base):
    """Unfold the saved word; locate the corner; return (cross(A,C), connecting sign, kind)."""
    w, c = ev["word"], V0.index(tuple(map(F, ev["corner"])))
    A = sub(unfold(T, w, V), S)
    beta = []  # parameter where leg j meets its wall
    for j, i in enumerate(w):
        a, b = unfold(V[i], w[:j], V), unfold(V[(i + 1) % n], w[:j], V)
        den = cross(A, sub(b, a))
        assert den != 0, "leg parallel to its wall"
        beta.append(cross(sub(a, S), sub(b, a)) / den)
    bounds = [F(0)] + beta + [F(1)]
    if base:
        assert all(x < y for x, y in zip(bounds, bounds[1:])), "legs out of order"
    # The corner leg is fixed by the base geometry and reused for the tilted room.
    k = None if base else ev["_leg"]
    if base:
        hits = []
        for j in range(len(w) + 1):
            Cj = sub(unfold(V[c], w[:j], V), S)
            t = dot(A, Cj) / dot(A, A)
            if cross(A, Cj) == 0 and bounds[j] <= t <= bounds[j + 1] and 0 < t < 1:
                hits.append((j, t))
        assert hits and len({unfold(V[c], w[:j], V) for j, _ in hits}) == 1, "corner not unique"
        if len(hits) == 1:
            k, kind = hits[0][0], "pass"
            assert bounds[k] < hits[0][1] < bounds[k + 1]
        else:
            assert len(hits) == 2 and hits[1][0] == hits[0][0] + 1 and hits[0][1] == bounds[hits[0][0] + 1]
            k, kind = hits[0][0], "reflect"
        ev["_leg"], ev["_kind"] = k, kind
    kind = ev["_kind"]
    C = sub(unfold(V[c], w[:k], V), S)
    # Corner wedge: directions from the corner along its two walls, mapped into copy k.
    Ck = unfold(V[c], w[:k], V)
    u_in = sub(unfold(V[c - 1], w[:k], V), Ck)        # along wall c-1 -> c, toward its far end
    u_out = sub(unfold(V[(c + 1) % n], w[:k], V), Ck)  # along wall c -> c+1
    if kind == "pass":
        s1, s2 = sgn(cross(A, u_in)), sgn(cross(A, u_out))
        assert s1 == s2 != 0, "line direction inside the exterior wedge"
        connect = s1  # connect iff the corner lies on the side the wedge points to
    else:
        i = w[k]
        assert c in (i, (i + 1) % n), "reflecting wall is not incident to the corner"
        wv, other = (u_out, u_in) if i == c else (u_in, u_out)
        assert sgn(cross(wv, A)) == sgn(cross(wv, other)) != 0, "line does not cross the wall toward the reflected copy"
        connect = -sgn(cross(A, wv))  # connect iff the wall ray points toward the line
    return cross(A, C), connect, kind, bounds, A


def legal_path_except_corner(ev, V, S, T, bounds, A):
    """Each leg, folded back to the room: no proper wall crossing, no corner inside except the event corner, midpoints inside (split at the event corner)."""
    w, c = ev["word"], V0.index(tuple(map(F, ev["corner"])))
    for j in range(len(w) + 1):
        p = fold(add(S, mul(bounds[j], A)), w[:j], V)
        q = fold(add(S, mul(bounds[j + 1], A)), w[:j], V)
        for i in range(n):
            assert not proper_cross(p, q, V[i], V[(i + 1) % n]), "leg crosses a wall"
        for v in range(n):
            assert v == c or not on_open(V[v], p, q), "leg passes another corner"
        # Split the leg at the event corner if it passes it, then test each piece's midpoint.
        pieces = [(p, V[c]), (V[c], q)] if on_open(V[c], p, q) else [(p, q)]
        assert all(inside(mul(F(1, 2), add(a, b)), V) for a, b in pieces), "leg leaves the room"
    for j, i in enumerate(w):
        hit = fold(add(S, mul(bounds[j + 1], A)), w[:j], V)
        a, b = V[i], V[(i + 1) % n]
        assert cross(sub(hit, a), sub(b, a)) == 0, "bounce is not on its wall"
        if j != ev.get("_leg", -1) or ev["_kind"] != "reflect":
            assert on_open(hit, a, b), "bounce is not inside its wall"


def main():
    assert V0[0] in [tuple(map(F, h)) for h in HAND]
    hand = [tuple(map(F, h)) for h in HAND]
    r = hand.index(V0[0])
    rot = hand[r:] + hand[:r]
    same_room = rot == V0 or [rot[0]] + rot[1:][::-1] == V0
    assert strictly_simple(V0) and inside(S0, V0) and inside(T0, V0)

    out = {"same_room_as_preprint_Q": same_room, "events": 147}
    kinds, side_ok = {"pass": 0, "reflect": 0}, 0
    for ev in events:
        f, connect, kind, bounds, A = analyze(ev, V0, S0, T0, base=True)
        assert f == 0
        legal_path_except_corner(ev, V0, S0, T0, bounds, A)
        kinds[kind] += 1
        side_ok += ev["perturb_side"] == -connect  # f = side*cross < 0 must be the connecting side
    out["base"] = {"legal_words_through_one_corner": 147, "zero_reflection": kinds["pass"],
                   "one_reflection": kinds["reflect"], "perturb_side_matches_wedge_rule": side_ok}

    # Escape direction: not a symmetry, and it tilts walls.
    dv = [(d[2 * i], d[2 * i + 1]) for i in range(n)]
    tilt = [i for i in range(n) if cross(sub(V0[(i + 1) % n], V0[i]), sub(dv[(i + 1) % n], dv[i])) != 0]
    out["walls_tilted_by_d"] = len(tilt)

    rows = []
    # 10^-6 is informational: second-order terms already beat the smallest derivative (about 1.05e-4) there.
    for eps in (F(1, 10**6), F(1, 10**9), F(1, 10**12)):
        V = [add(V0[i], mul(eps, dv[i])) for i in range(n)]
        S, T = add(S0, mul(eps, (d[44], d[45]))), add(T0, mul(eps, (d[46], d[47])))
        assert strictly_simple(V) and inside(S, V) and inside(T, V)
        nonconnect, positive, ratio_err = 0, 0, F(0)
        for ev, g in zip(events, saved):
            f, connect, _, _, _ = analyze(ev, V, S, T, base=False)
            nonconnect += f != 0 and sgn(f) == -connect  # corner on the wedge side: this word is blocked
            positive += ev["perturb_side"] * f > 0
            ratio_err = max(ratio_err, abs(ev["perturb_side"] * f / eps - g) / g)
        rows.append({"eps": str(eps), "strictly_simple_marks_interior": True,
                     "words_blocked_by_wedge_rule": nonconnect, "side_times_f_positive": positive,
                     "max_relative_gap_f_over_eps_vs_saved_derivative": float(ratio_err)})
    out["tilted"] = rows
    ok = side_ok == 147 and all(r["words_blocked_by_wedge_rule"] == r["side_times_f_positive"] == 147 for r in rows[1:])
    out["status"] = "PASS" if ok else "FAIL"
    json.dump(out, open(HERE / "independent_check.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
