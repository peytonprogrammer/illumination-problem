# Immersed-disc census

Complete through area 16 at W ≤ 20. Every one of the 857,156 control pairs is lit. No dark or undecided pairs remain. counts.tsv gives all 195 nonzero disc-count rows. Each absent row in scope has zero discs and zero pairs.

## Reproduce the gates

Run from this directory, serially:

```sh
nice -n 10 clang++ -O3 -std=c++17 enum.cpp -o enumerate
nice -n 10 clang -O3 ../../d55-relaxed-lab/orbitr.c -o orbitr
/usr/bin/time -p nice -n 10 python3 unfold.py >g3.log 2>g3.time
nice -n 10 ./enumerate 11 2>enum.log
nice -n 10 python3 gates.py >g1.log
```

G1 matched all 57 embedded area/wall rows through area 11, totaling 22,292 rooms. Enumeration took 0.329 CPU seconds including the area-11 validation layer. G3 returned FULL 2592 1 0 1 on the known pair in the d205 control (0.05 CPU seconds including the Python driver). Compilation and the count comparison are outside those timings. The coordinator confirmed G2. G4 and production results follow.

## Enumeration

Contract each maximal horizontal run to a vertex. Every vertical gluing between two runs occupies their full projected overlap. Stopping an attachment inside both runs would produce a forbidden four-cell path unless the missing edge closed the link. Contacts with different neighbors on the same side must have disjoint closed footprints, for the same reason. The run graph is connected. Gluing rectangles along these disjoint intervals gives Euler characteristic equal to the number of runs minus the number of contacts. Thus the graph is a tree.

Conversely, attaching a leaf by its full overlap, with closed footprint disjoint from existing contacts on that side, gives a disc with allowed links. Deleting leaves proves completeness. Different abstract cells can have identical projected coordinates. The generator retains all wall counts in intermediate trees. Direction-labelled BFS codes remove duplicates under horizontal and vertical reflections during construction. At counting time the codes also identify quarter turns. Multiple cells at the extremal coordinate are tried as roots.

jobs.txt stores control discs with at least two marks, including the area-11 G1 layer. Each line starts with the area, followed by cell records (x,y,east,north,west,south), with zero-based neighbor IDs and -1 for a wall. unfold.py labels marks by abstract corner components.

## G4 pilot and pre-production forecast

G2 passed the independent comparison on all 69 nonzero rows (discs and pairs). The serial pilot enumerated through area 12 in 1.16 CPU seconds. Lighting its 353 eligible control discs took 0.06 CPU seconds including the child decider. All 373 pairs were lit.

| Area | TOUCHING pairs | OVERLAP pairs |
|---|---:|---:|
| 1–9 (each) | 0 | 0 |
| 10 | 1 | 0 |
| 11 | 29 | 0 |
| 12 | 339 | 4 |

The through-16 forecast uses 4× enumeration growth per additional cell (recent unconstrained counts grew 3.8×), giving 297 CPU seconds. At 8× pair growth from area 12, cumulative pairs are 1,605,613 and total CPU time is 555 seconds. A 5× scenario gives 267,913 pairs and 340 seconds. Holding the observed 343/29 pair-growth ratio constant gives 7,332,347 pairs and 1,476 seconds. These are scenarios, not bounds. They use pilot lighting CPU per pair, before any unusually expensive survivors. All three forecasts pass G4.

## Production through area 16

| Bucket | Discs | Mark pairs | Lighting |
|---|---:|---:|---|
| EMBEDDED | 9,460,065 | 6,422,521 | Count validation only |
| TOUCHING | 1,858,447 | 752,689 | All lit |
| OVERLAP | 587,670 | 104,467 | All lit |

The 2,446,117 control discs included 552,166 with at least two marks. Each eligible disc went directly to the d55 modular-orbit decider with a 100,000-state cap and early exit on positive witnesses for all pairs. No cap or crash left any pair unresolved. dark.tsv and undecided.tsv contain headers only. reconcile.py checked dispositions against independently tallied enumeration pair counts for every area and bucket, and compared all through-12 rows with the pilot. The observed 857,156 control pairs exceeded 10,000. The control stops at area 16.

Production enumeration took 377.68 CPU seconds (368.36 user, 9.32 system); peak RSS was 3,904,225,280 bytes. Lighting took 103.35 CPU seconds (100.32 user, 3.03 system). Together the stages took 481.03 CPU seconds, or 8.02 CPU-minutes. The earlier in-memory production attempt used another 51.85 CPU seconds before the switch to disk-backed final-area deduplication. The disk-backed validation run reproduced pilot counts and lighting totals exactly. Compilation and report generation are excluded. All census processes ran at nice 10.

To reproduce production on macOS, run from this directory after building orbitr as above:

```sh
nice -n 10 clang++ -O3 -std=c++17 enum_disk.cpp -o enumerate_disk
mkdir -p pilot production
(cd pilot && nice -n 10 ../enumerate 12 && nice -n 10 python3 ../light.py)
(cd production && /usr/bin/time -lp nice -n 10 ../enumerate_disk 16 2>enum.log && /usr/bin/time -lp nice -n 10 python3 ../light.py 2>light.time)
nice -n 10 python3 reconcile.py
```

The disk version groups exact final-area canonical BFS codes in 64 scratch files, then compares full codes within each file. Hashes choose a file only. The final-area cell order and orientation may differ from the in-memory enumerator's. Lower-area counts follow the same run-tree construction. production/lighting.tsv contains the actual pair dispositions by area and bucket.
