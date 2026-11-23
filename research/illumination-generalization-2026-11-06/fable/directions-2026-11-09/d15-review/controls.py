"""Negative controls for the review harness.

1. The T room of theorems.md, section "Candidates that fail". The one-door
   family through the tab door has no member that reaches T. The harness
   must still find a Lemma B instance after the role swap, and its paths
   must trace.
2. The U room of theorems.md, candidate (i). The direct segment meets two
   reflex vertices, so the tracer must report 'vertex'. The V-path of
   Lemma A2 must trace.
3. Shots at every vertex of a room must report 'vertex' in both tracers.

Usage: python3 -B controls.py
"""
import random
import sys
from fractions import Fraction as Fr

sys.dont_write_bytecode = True
import rv  # noqa: E402

Q = rv.field(2)


def q(v):
    return Q(Fr(v))


def P(x, y):
    return (q(x), q(y))


def both(R, S, D, T):
    a = rv.trace(R, S, D, T)
    b = rv.trace_fast(R, S, D, T)
    assert a == b, (a, b)
    return a[0]


def main():
    rng = random.Random(3)
    ok = True

    # --- control 1: T room -------------------------------------------------
    R = rv.Room(3, 2, [(0, 0), (1, 0), (2, 0), (1, 1)], [q(0), q(20), q(30), q(31)], [q(0), q(10), q(12)])
    S, T = P(5, 1), P(21, 11)
    assert R.interior(S) and R.interior(T) and len(R.walls()) == 8
    # x* = crossing of the door line y = 10. A member goes straight to the
    # door line when 0 < x* < 31 (no reflection in an end wall of the bar).
    seen = {}
    in_door = 0
    for eps in (1, -1):
        for k in range(-40, 41):
            X = Fr(20 + eps * 1 + 20 * k)
            xstar = 5 + Fr(9, 10) * (X - 5)
            if 20 < xstar < 30:
                in_door += 1
            if 0 < xstar < 31:
                st = both(R, S, (q(X) - S[0], T[1] - S[1]), T)
                seen[st] = seen.get(st, 0) + 1
    print("control 1: one-door family through the tab door, 162 members; members with x* in the door:",
          in_door, "; tracer statuses of the members that go straight to the door line:", seen)
    ok &= in_door == 0 and 'ok' not in seen
    insts = rv.all_instances(R, S, T, rng)
    names = sorted({i['lem'] for i in insts})
    verdicts = [(i['lem'], i['key'], rv.evaluate(R, i, rng)[0]) for i in insts]
    print("control 1: lemma instances found:", names)
    for v in verdicts:
        print("   ", v)
    ok &= any(v[0] == 'B' and v[1][1] == 1 and v[2] == 'ok' for v in verdicts)
    ok &= all(v[2] == 'ok' for v in verdicts)

    # --- control 2: U room -------------------------------------------------
    R = rv.Room(2, 3, [(0, 0), (1, 0), (0, 1), (0, 2), (1, 2)], [q(0), q(2), q(4)], [q(0), q(2), q(4), q(6)])
    S, T = P(2, 1), P(2, 5)
    st = both(R, S, (T[0] - S[0], T[1] - S[1]), T)
    print("control 2: direct segment through two reflex vertices:", st)
    ok &= st == 'vertex'
    # V-path off the wall x = 0 through (0, 3): unfolded target (-2, 5)
    st = both(R, S, (q(-2) - S[0], T[1] - S[1]), T)
    print("control 2: V-path of Lemma A2 through (0, 3):", st)
    ok &= st == 'ok'
    insts = rv.all_instances(R, S, T, rng)
    print("control 2: lemma instances found:", sorted({i['lem'] for i in insts}),
          [rv.evaluate(R, i, rng)[0] for i in insts])
    ok &= all(i['lem'] != 'A' for i in insts)

    # --- control 3: shots at vertices ---------------------------------------
    n = 0
    legal = 0
    stat = {}
    for (vx, vy) in R.vertices():
        for S in (P(1, 1), P(Fr(1, 3), Fr(17, 5)), P(3, Fr(1, 2))):
            D = ((vx - S[0]) + (vx - S[0]), (vy - S[1]) + (vy - S[1]))
            st = both(R, S, D, P(1, 5))
            n += 1
            stat[st] = stat.get(st, 0) + 1
            # a shot can be blocked by a wall or meet another vertex first;
            # it must never be reported as a legal path
            legal += st == 'ok'
    print("control 3: shots at vertices:", n, stat, "reported legal:", legal)
    ok &= legal == 0
    print("ALL CONTROLS PASS" if ok else "CONTROL FAILURE")


if __name__ == "__main__":
    main()
