"""D113 claim 4: arithmetic of the compact covering problem's stated counts. python3 -B count.py"""
tot = sum(m ** (2 * m) * (m - 1) ** 4 for m in range(2, 11))
print('sum_{m=2}^{10} m^(2m) (m-1)^4 =', tot, f'= {tot:.3e}', ' m=10 term =', f'{10**20 * 9**4:.3e}')
for m in (2, 10):
    print(f'max variables at W={2*m}: (m-2)+(m-2)+4 =', 2 * (m - 2) + 4)
for B in (1, 2, 5, 10):
    m = 10
    w = 1 + 2 * m * sum((2 * m - 1) ** j for j in range(B))
    brute = 1 + sum(2 * m * (2 * m - 1) ** (j - 1) for j in range(1, B + 1))
    print(f'words through length {B} at m=10: {w} (direct count of no-immediate-repeat words {brute})')
