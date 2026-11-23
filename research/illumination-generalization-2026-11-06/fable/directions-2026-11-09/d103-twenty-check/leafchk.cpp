// D103 exact leaf checker for shear certificates. Own surface model, written from
// the definitions in qclass-closure/twenty/method.md and two18/README.md (the d90
// model was the template; no author code is used).
//
// Input (stdin):
//   ROOM id L n x0 y0 x1 y1 ...        oriented cells; L = claimed row period
//   LEAF id fixed c0 cx0 cy0 a0 b0 c1 cx1 cy1 a1 b1 l0 h0 ... l5 h5 j p q tag
// Coordinates in a leaf box are integers over U = 65536:
//   z0,z1 = |dx|,|dy| of endpoint 0; z2,z3 = endpoint 1; z4,z5 = phases K*L*|dy|.
// fixed=1: K = 1, the transverse term uses (p + j*q*L)*|dy| and phases are unused.
// Output: one line per failed leaf, then a summary line.
#include <cstdio>
#include <cstdlib>
#include <climits>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <tuple>
#include <numeric>
#include <functional>
#include <algorithm>
#include <cassert>
using namespace std;
typedef long long ll;
static const ll U = 65536;
static ll fdiv(ll a, ll b) { ll q = a / b; if ((a % b != 0) && ((a < 0) != (b < 0))) q--; return q; }
static ll cdiv(ll a, ll b) { return -fdiv(-a, b); }

struct Room {
  vector<pair<int,int>> cells; map<pair<int,int>,int> idx; int L = 0;
  // squares: s = 4*c + 2*(ex<0) + (ey<0)
  int nsq() const { return 4 * (int)cells.size(); }
  bool has(int x, int y) const { return idx.count({x, y}); }
  int occ(int X, int Y) const { int k = 0; for (int i = 0; i < 2; i++) for (int j = 0; j < 2; j++) k += has(X - i, Y - j); return k; }
  bool corner(int X, int Y) const {
    int k = occ(X, Y); if (k == 1 || k == 3) return true;
    if (k == 2) return has(X - 1, Y - 1) == has(X, Y);
    return false;
  }
  static int sq(int c, int ex, int ey) { return 4 * c + 2 * (ex < 0) + (ey < 0); }
  void dec(int s, int& c, int& ex, int& ey) const { c = s / 4; ex = (s & 2) ? -1 : 1; ey = (s & 1) ? -1 : 1; }
  int R(int s) const { int c, ex, ey; dec(s, c, ex, ey); auto [a, b] = cells[c]; auto it = idx.find({a + ex, b}); return it != idx.end() ? sq(it->second, ex, ey) : sq(c, -ex, ey); }
  int T(int s) const { int c, ex, ey; dec(s, c, ex, ey); auto [a, b] = cells[c]; auto it = idx.find({a, b + ey}); return it != idx.end() ? sq(it->second, ex, ey) : sq(c, ex, -ey); }
  pair<int,int> c11(int s) const { int c, ex, ey; dec(s, c, ex, ey); auto [a, b] = cells[c]; return {a + (ex > 0), b + (ey > 0)}; }
  vector<int> row(int s) const { vector<int> r{s}; int t = R(s); while (t != s) { r.push_back(t); t = R(t); } return r; }
  int period() const { ll l = 1; for (int s = 0; s < nsq(); s++) { ll n = row(s).size(); l = l / std::gcd(l, n) * n; } return (int)l; }
};

struct Cyl {
  int p, q; vector<int> orbit; vector<char> crit; // orbit[s*(p+q)+(k+p)], crit[s*(p+q)+(m+p)]
  // per (c,sg) row data
  struct RowData { int P; vector<int> lab; vector<ll> run; vector<char> cr; vector<ll> nextcr; };
  map<pair<int,int>, RowData> rows;
};

static Cyl build(const Room& R, int p, int q) {
  Cyl C; C.p = p; C.q = q; int W = p + q, n = R.nsq();
  assert(p > 0 && q > 0 && std::gcd(p, q) == 1);
  auto id = [&](int s, int k) { return s * W + (k + p); };
  // line criticality by following each closed leaf (lines m = -p+1..q-1)
  vector<int> crit(n * W, -1);
  for (int s = 0; s < n; s++) for (int m = -p + 1; m < q; m++) {
    if (crit[id(s, m)] >= 0) continue;
    vector<int> leaf; bool marked = false; int cs = s, cm = m;
    while (true) {
      leaf.push_back(id(cs, cm));
      int ns, nm;
      if (cm > q - p) { ns = R.R(cs); nm = cm - q; }
      else if (cm < q - p) { ns = R.T(cs); nm = cm + p; }
      else { auto [X, Y] = R.c11(cs); if (R.corner(X, Y)) marked = true;
             int d1 = R.T(R.R(cs)), d2 = R.R(R.T(cs)); if (d1 != d2 && !R.corner(X, Y)) { fprintf(stderr, "unmarked cone\n"); exit(2); }
             ns = d1; nm = 0; }
      if (ns == s && nm == m) break;
      if ((int)leaf.size() > n * W + 5) { fprintf(stderr, "leaf loop\n"); exit(2); }
      cs = ns; cm = nm;
    }
    for (int z : leaf) crit[z] = marked;
  }
  vector<int> par(n * W); iota(par.begin(), par.end(), 0);
  function<int(int)> f = [&](int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; };
  auto uni = [&](int a, int b) { a = f(a); b = f(b); if (a != b) par[a] = b; };
  for (int s = 0; s < n; s++) {
    for (int k = -p; k < q; k++) { if (k <= q - p - 1) uni(id(s, k), id(R.T(s), k + p)); else uni(id(s, k), id(R.R(s), k - q)); }
    for (int m = -p + 1; m < q; m++) if (!crit[id(s, m)]) uni(id(s, m - 1), id(s, m));
  }
  vector<int> lab(n * W); for (int i = 0; i < n * W; i++) lab[i] = f(i);
  // half-turn: (c,ex,ey)->(c,-ex,-ey), k -> q-p-1-k ; must be a well-defined involution on labels
  map<int,int> H;
  for (int s = 0; s < n; s++) for (int k = -p; k < q; k++) {
    int c, ex, ey; R.dec(s, c, ex, ey); int img = lab[id(Room::sq(c, -ex, -ey), q - p - 1 - k)];
    auto it = H.find(lab[id(s, k)]); if (it == H.end()) H[lab[id(s, k)]] = img; else if (it->second != img) { fprintf(stderr, "H not well defined\n"); exit(2); }
  }
  for (auto [a, b] : H) if (H[b] != a) { fprintf(stderr, "H not involution\n"); exit(2); }
  C.orbit.resize(n * W); for (int i = 0; i < n * W; i++) C.orbit[i] = min(lab[i], H[lab[i]]);
  C.crit.assign(crit.begin(), crit.end());
  for (int c = 0; c < (int)R.cells.size(); c++) for (int sg : {1, -1}) {
    Cyl::RowData D; vector<int> rw = R.row(Room::sq(c, 1, sg)); D.P = q * rw.size();
    D.lab.resize(D.P); D.cr.resize(D.P);
    for (int k = 0; k < D.P; k++) { int i = k / q, m = k - q * i; D.lab[k] = C.orbit[id(rw[i], m)]; D.cr[k] = crit[id(rw[i], m)]; }
    // a non-critical line must separate strips of one label
    for (int k = 0; k < D.P; k++) if (!D.cr[k] && D.lab[k] != D.lab[(k - 1 + D.P) % D.P]) { fprintf(stderr, "regular line splits labels\n"); exit(2); }
    const ll INF = LLONG_MAX / 4; D.run.assign(D.P, 0); D.nextcr.assign(D.P, INF);
    bool allsame = true; for (int k = 0; k < D.P; k++) if (D.lab[k] != D.lab[0]) allsame = false;
    if (allsame) for (int k = 0; k < D.P; k++) D.run[k] = INF;
    else for (int k = 0; k < D.P; k++) { ll r = 1; while (D.lab[(k + r) % D.P] == D.lab[k]) r++; D.run[k] = r; }
    bool anycr = false; for (int k = 0; k < D.P; k++) anycr |= D.cr[k];
    if (anycr) for (int k = 0; k < D.P; k++) { ll r = 0; while (!D.cr[(k + r) % D.P]) r++; D.nextcr[k] = r; }
    C.rows[{c, sg}] = D;
  }
  return C;
}

// u-interval [lo,hi] (in units of 1/U). Returns open set O and closure set C (each 0 or 1 label; -1 = empty).
static void query(const Cyl::RowData& D, ll lo, ll hi, int& O, int& Cl) {
  auto md = [&](ll k) { ll r = k % D.P; return r < 0 ? r + D.P : r; };
  ll k1 = fdiv(lo, U), k2 = cdiv(hi, U) - 1, n1 = cdiv(lo, U), n2 = fdiv(hi, U);
  if (k1 <= k2) {
    bool same = D.run[md(k1)] >= k2 - k1 + 1;
    Cl = same ? D.lab[md(k1)] : -1;
    bool nocrit = n1 > n2 || D.nextcr[md(n1)] > n2 - n1;
    O = (same && nocrit) ? D.lab[md(k1)] : -1;
  } else { // lo == hi, an integer line
    ll n = n1; O = D.cr[md(n)] ? -1 : D.lab[md(n)];
    Cl = -2; // closure is the pair {lab[n-1], lab[n]}; handled by caller
  }
}

int main() {
  map<int, Room> rooms; map<tuple<int,int,int>, Cyl> cache;
  string tok; ll nleaf = 0, nfail = 0;
  while (cin >> tok) {
    if (tok == "ROOM") {
      int id, L, n; cin >> id >> L >> n; Room R; R.cells.resize(n);
      for (int i = 0; i < n; i++) { cin >> R.cells[i].first >> R.cells[i].second; R.idx[R.cells[i]] = i; }
      R.L = R.period(); if (R.L != L) { printf("PERIOD MISMATCH room %d %d %d\n", id, R.L, L); return 1; }
      rooms[id] = R; continue;
    }
    if (tok != "LEAF") { fprintf(stderr, "bad token %s\n", tok.c_str()); return 1; }
    int id, fixed; cin >> id >> fixed; int c[2], cx[2], cy[2], a[2], b[2];
    for (int e = 0; e < 2; e++) cin >> c[e] >> cx[e] >> cy[e] >> a[e] >> b[e];
    ll z[6][2]; for (int i = 0; i < 6; i++) cin >> z[i][0] >> z[i][1];
    ll j; int p, q; string tag; cin >> j >> p >> q >> tag;
    const Room& R = rooms.at(id); ll L = R.L; nleaf++;
    auto key = make_tuple(id, p, q); auto it = cache.find(key);
    if (it == cache.end()) it = cache.emplace(key, build(R, p, q)).first;
    const Cyl& C = it->second;
    set<int> O[2], Cs[2];
    for (int e = 0; e < 2; e++) {
      if (R.cells[c[e]] != make_pair(a[e], b[e]) || (cx[e] != a[e] && cx[e] != a[e] + 1) || (cy[e] != b[e] && cy[e] != b[e] + 1)) { printf("BAD ENDS %s\n", tag.c_str()); return 1; }
      int sx = cx[e] == a[e] ? 1 : -1, sy = cy[e] == b[e] ? 1 : -1;
      for (int sg : {1, -1}) {
        ll Yb = sg == 1 ? (cy[e] - b[e]) : 1 - (cy[e] - b[e]);
        ll base = (ll)q * (cx[e] - a[e]) - (ll)p * Yb;
        vector<pair<ll, int>> terms; // coefficient, variable index
        terms.push_back({(ll)q * sx, 2 * e});
        if (fixed) terms.push_back({-(ll)sg * sy * ((ll)p + j * q * L), 2 * e + 1});
        else { terms.push_back({-(ll)sg * sy * p, 2 * e + 1}); terms.push_back({-(ll)sg * sy * q * j, 4 + e}); }
        __int128 lo = (__int128)base * U, hi = lo;
        for (auto [k, v] : terms) { __int128 u1 = (__int128)k * z[v][0], u2 = (__int128)k * z[v][1]; lo += min(u1, u2); hi += max(u1, u2); }
        if (lo < -(__int128)4e18 || hi > (__int128)4e18) { printf("OVERFLOW %s\n", tag.c_str()); return 1; }
        const auto& D = C.rows.at({c[e], sg});
        int o, cl; query(D, (ll)lo, (ll)hi, o, cl);
        if (o >= 0) O[e].insert(o);
        if (cl >= 0) Cs[e].insert(cl);
        else if (cl == -2) { ll n = (ll)lo / U; auto md = [&](ll k) { ll r = k % D.P; return r < 0 ? r + D.P : r; };
          Cs[e].insert(D.lab[md(n - 1)]); Cs[e].insert(D.lab[md(n)]); }
      }
    }
    bool ok = false;
    for (int e = 0; e < 2; e++) for (int l : O[e]) if (Cs[1 - e].count(l)) ok = true;
    if (!ok) { nfail++; if (nfail <= 30) printf("FAIL %s\n", tag.c_str()); }
  }
  printf("leaves %lld failed %lld directions %zu\n", nleaf, nfail, cache.size());
  return 0;
}
