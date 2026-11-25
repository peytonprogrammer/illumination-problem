"""Coordinator check of bbbb/l1-two-list-closure.md, sections A and B.
Exact traces of the claimed chords only; no scan. Uses trace() from trace_check.py."""
import sys
from fractions import Fraction as F
from math import gcd
sys.argv = [sys.argv[0]]
from trace_check import trace

def nearest_progression(start, step, aim, X):
    # members K = start + step*i (i >= 0); choose K/X nearest to aim
    i = max(0, round((aim * X - start) / step))
    best = min((abs(F(start + step * ii, X) - aim), ii) for ii in (max(0, i - 1), i, i + 1))
    return start + step * best[1]

def A(m):
    N = 64 * m * m; X = 3 * N // 2 + 1
    K = nearest_progression(m, 3 * m * 2 * (m + 2), F(m, 2) + 1, X)
    lv = (-(m + 2), 0, 1, 1 + m, 2 + m, 3 + 2 * m)
    return K, X, trace(N, lv, (N - 1, 0), (5 * N // 2, 2 + m), F(X), F(K))

def B(m, N, a, t, H):
    X = 3 * N // 2 + 1
    cond = F(3 * m * H, gcd(m, 2 * H)) < F(X, 2)
    c = m + 1 - t
    K = nearest_progression(c, 3 * m * (2 * H // gcd(m, 2 * H)), m + F(1, 2), X)
    lv = (-a, 0, 1, m + 1, m + 1 + t, m + 1 + H)
    return cond, K, X, trace(N, lv, (N - 1, 0), (5 * N // 2, m + 1 + t), F(X), F(K))

if __name__ == "__main__":
    for m in range(2, 13):
        K, X, r = A(m)
        print(f"A m={m} K={K} X={X} slope~{float(F(K, X)):.4f} {r}")
    for (m, N, a, t, H) in [(3, 40, 1, 1, 5), (3, 40, 7, 4, 5), (4, 100, 2, 3, 9), (5, 64, 3, 6, 7), (7, 200, 1, 1, 30), (6, 36, 5, 2, 8), (3, 576, 5, 3, 7), (7, 3136, 9, 7, 10)]:
        cond, K, X, r = B(m, N, a, t, H)
        print(f"B m={m} N={N} a={a} t={t} H={H} cond={cond} K={K} {r}")
