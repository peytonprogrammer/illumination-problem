from pathlib import Path
import json, math
from collections import Counter
base=Path('../../../../qclass-closure/bbbb')
# This script runs from the profile directory.
base=Path('../../../..')/'qclass-closure/bbbb'
links='../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/seed-profile-a21/'
hist=Counter()
for line in Path('audit.log').read_text().splitlines():
 v=line.split()
 if v[0]=='BIN':
  r,h,c=map(int,v[1:]);hist[r,h]+=c
summary='\n'.join('| '+str(h)+' | '+' | '.join(f'{hist[r,h]:,}' if hist[r,h] else '·' for r in range(9))+' |' for h in range(1,27))
family=json.loads(Path('family.json').read_text())
families='\n'.join(f'| {i} | {n} | {j} | {p} |' for i,n,axis,j,p,v,ok in family if ok)
s=fr'''Advances: L1 — the straight-chord seed for interior lattice pairs, using the exact-area-21 L2 census.

# What the first seed looks like at area 21

The largest **first-found** primitive height was 26, attained twice. Those two seeds made 42 and 51 reflections. A different pattern accounts for much of the hard tail: a ray can bounce repeatedly across a narrow passage while crossing a particular horizontal section just once. In 18 of the 20 displayed rooms this gives an infinite family in which every pair stays lit.

## Measurement

In [d205 shoot.c, make_dirs](../{links}shoot.c) the outer loop is the sum (s=|p|+|q|), with decreasing (|p|) within a sum. The shooter tries the four signs and follows each ray to a forbidden corner, a return, or its finite step limit. It removes a target after its first verified hit. Thus e.g. (3,1) precedes (2,3). Height below means (h=max(|p|,|q|)) **of that first hit**. Exact minimum heights and their top-20 ranking cannot be read off this traversal. The first sum does give a lower bound (⌈s/2⌉) on the true minimum height, since every direction of smaller sum was exhausted.

Exact area 21 only, 84 original shards, nice 10, seven workers maximum, 46.29 worker CPU-minutes. Every shard reproduced its original room counts, expected pairs, parity counts and zero survivors. There were 538,025,823 canonical rooms, 364,183,172 with a pair, and 1,604,242,406 replay-verified first witnesses. Each witness was written to disk. A second pass decoded every record and reproduced the height histogram by reflex count; maxima over the archive were 17 primitive steps and 123 reflections (separate maxima). The hard-pair paths below were additionally reconstructed from exact intersections with the physical walls. [Run manifest]({links}a21/manifest.json) · [record layout]({links}records.md) · [decoded shard counts]({links}audit.log)

### Pairs by first-found height and reflex count, area 21

A dot is zero. Each column counts unordered pairs in canonical rooms with (r=(W-4)/2), including pairs in different parity classes.

| Height | r=0 | r=1 | r=2 | r=3 | r=4 | r=5 | r=6 | r=7 | r=8 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{summary}

### Twenty largest first-found heights

All 12 pairs of height at least 24 appear here, followed by eight of the 58 ties at height 23. Ties use shard number then original discovery order. Room ID is shard / one-based eligible-room ordinal. Launch at the signed direction shown, reflect specularly, and stop after (m) primitive lattice steps of developed displacement (m(p,q)). V and H count hits on vertical and horizontal walls. Green is the source and red the target. Each polyline shows the actual reflected path. [Exact ordered bounce coordinates for all 20]({links}paths.json)

![Twenty rooms and their first seed paths]({links}hardest.png)

| Rank | Room ID | r | Source → target | Launch | Height | m | V + H |
|---:|---|---:|---|---|---:|---:|---|
{Path('table.md').read_text()}

**Construction by rank.** Ranks 3, 9, 11 and 12 use a ray monotone in one coordinate with 7 or 13 parallel-wall reflections. Every other listed seed reverses both velocity components and makes at least 29 reflections. None of the 20 recorded seeds has the earlier one-wall-plus-roof itinerary. A simpler *different* witness remains possible. The drawings show why counting total reflections alone hides the distinction between repeated bounces across a passage and repeated trips through it.

## A conjecture the records can actually test

Let (Bₓ,Bᵧ) be the side lengths of the room's axis-aligned bounding box. Conjecture: every distinct interior lattice pair in a strictly simple orthogonal lattice room with (r ≤ 8) admits a legal seed with

**|p| ≤ 8Bₓ,  |q| ≤ 8Bᵧ,  min(m|p|/Bₓ, m|q|/Bᵧ) ≤ 15.**
Thus the proposed type is a path whose **total travel along at least one axis is at most 15 box spans**, regardless of how often it bounces on the other axis. Its primitive height is at most (8 max(Bₓ,Bᵧ)). The constants 8 and 15 are the separately rounded-up maxima over *all first records* in this one slice, computed before selecting the top 20. Both inequalities hold for the same witness of every pair here. They are empirical choices; there is no derivation of either from the reflex budget or evidence of optimality across areas.

## A proof for periodic stretches of the hard rooms

**Unit passage.** Suppose the entire horizontal slice through (y=j+1/2) is one interval of width one. Cut there, translate the entire upper part by an integer (E ≥ 0), and fill the gap with that same unit strip. The sides at the cut are straight and continue vertically, so wall count and strict simplicity are preserved. No new interior lattice mark fits across the strip. Old marks above the cut translate by (E); all others keep their positions.

Fix a base seed crossing the cut with (q ≠ 0). In the unfolded unit interval, its additional transverse displacement on each traversal is (± E|p/q|). A multiple of two restores both the horizontal position and the horizontal velocity sign, including a crossing at a side wall interpreted by continuation. The open strip has no corners on its straight sides. Thus (E) divisible by (2|q|/gcd(|p|,2|q|)) splices in a legal excursion at **every** crossing of that seed. A parallel ray from a lattice mark never lies along this half-integral cut. Noncrossing seeds carry over unchanged up to translation. Take the least common multiple of these periods for the chosen crossing seeds, one per base pair. Every pair in every resulting room is then lit.

**Quantitative part.** A seed crossing (v) times gains exactly (vE) units of total vertical travel, while (Bᵧ) increases by (E). If (m|q| ≤ 15Bᵧ) and (v ≤ 15), the new vertical travel is at most (15(Bᵧ+E)). The primitive direction stays the same, so the two height inequalities persist. A noncrossing seed keeps its original travel on both axes. This proves the conjectured estimates on the indicated growth progressions.

For each row below, exact wall intersections of **all** base-pair records give at most one crossing per seed at the displayed cut. Each crossing seed satisfies the initial vertical travel inequality. The period is the common period of their signed phases. This verifies the hypotheses on finite base data; the strip argument proves the conclusion for arbitrarily long extensions. [Cut and period checks]({links}profile.py) · [per-room results]({links}family.json)

| Rank | All base pairs | Cut row j | Permitted E (multiples of) |
|---:|---:|---:|---:|
{families}

For rank 1 the extremal seed crosses (y=5/2) at (x=4/3) travelling up-left in the interval ([1,2]). Its individual period is 3 and the six pairs together have period 6. For rank 2 the extremal seed crosses at (x=4/5) travelling up-left in ([0,1]); its period is 5 and the three pairs together have period 70. Ranks 11 and 18 have no internal unit row or column of this form.

**First open step.** Already for rank 1, adding one unit changes the extremal seed's unfolded phase by (26/3), nonzero modulo two. Its incoming state therefore fails the same-exit test. The length-one extension has area 22. Finding a compensating seed for all residues and all marks in this passage family remains open in this argument. The two rooms without a usable cut also require a different argument for growth. The census and the stretch proof supply no universal selection rule at (r=8).
'''
s=s.replace('../'+links+'shoot.c','../../illumination-generalization-2026-11-06/fable/directions-2026-11-09/d205-census-a21/shoot.c')
(base/'l1-seed-profile.md').write_text(s)
