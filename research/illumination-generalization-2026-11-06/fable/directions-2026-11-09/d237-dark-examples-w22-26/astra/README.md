# Immersed discs with 22, 24 or 26 walls

The generator uses the d236 run-tree growth and disk-backed last-area deduplication. Only the count filter and lighting job selection changed. Every eligible complex goes directly to d55 orbitr with cap 100000. FULL survivors are recorded individually and the census continues.

G2 checkpoint: gate11/raw-counts.tsv has two nonzero rows and no pairs. Missing rows have zero discs and pairs. Coordinator handles independent comparison.

G3 passed. Through area 13 enumeration took 5.25 CPU seconds and lighting 0.03. All 74 pairs were lit (70 EMBEDDED and 4 TOUCHING, all at area 13 and W=22). No earlier pair exists, so the pilot cannot estimate a successive-area growth ratio. The pre-production planning scenario assumes 20× per area, giving 623,154 cumulative pairs and approximately 253 lighting CPU seconds. The same area-16 enumeration cost 378 CPU seconds in d236, giving roughly 11 CPU-minutes total. At 40× instead the estimate is about 39 CPU-minutes. Neither scenario is a bound.

## Completed census

G1 passed. Production found one DARK pair. Its marked complex is the known area-15, 22-wall embedded control, up to translation and square symmetry. Both deciders exhausted 2,592 states. No other pair was dark at any wall count in scope. No pair was undecided. G2 passed against the validator's two nonzero rows through area 11. G3 passed before production.

| Bucket | Discs | Pairs | DARK |
|---|---:|---:|---:|
| EMBEDDED | 5,748,169 | 788,386 | 1 |
| TOUCHING | 2,416,984 | 209,124 | 0 |
| OVERLAP | 576,812 | 17,521 | 0 |
| Total | 8,741,965 | 1,015,031 | 1 |

counts.tsv has 44 nonzero rows; omitted rows have zero discs and pairs. lighting.tsv reconciles to every census pair count. dark.tsv and undecided.tsv include the cell array (x,y,east,north,west,south), with zero-based neighbor IDs and -1 for walls. Each mark gives its abstract (cell ID,corner) followed by its projected coordinates; corners 0,1,2,3 are SW,SE,NW,NE. checks.log records independent confirmation from the validator's unfolding and Python orbit decider. The fold-certificate stage awaits the coordinator's brief.

## Timing and commands

CPU seconds (user + system): area-11 gate 0.29; pilot enumeration 5.25; pilot lighting 0.03; production enumeration 411.74; production lighting 170.78; reconciliation and independent replay 0.44. Production used 9.71 CPU-minutes. Peak enumeration RSS was 3,437,232,128 bytes. Timings exclude compilation. The enumeration and lighting commands ran serially at nice 10.

Run from this directory:

```sh
nice -n 10 clang++ -O3 -std=c++17 enum.cpp -o enumerate
nice -n 10 clang -O3 ../../d55-relaxed-lab/orbitr.c -o orbitr
mkdir -p gate11 pilot production
(cd gate11 && /usr/bin/time -lp nice -n 10 ../enumerate 11 2>enum.log)
cp gate11/raw-counts.tsv counts.tsv
(cd pilot && /usr/bin/time -lp nice -n 10 ../enumerate 13 2>enum.log && /usr/bin/time -lp nice -n 10 python3 ../light.py 2>light.time)
(cd production && /usr/bin/time -lp nice -n 10 ../enumerate 16 2>enum.log && /usr/bin/time -lp nice -n 10 python3 ../light.py 2>light.time)
/usr/bin/time -lp nice -n 10 python3 check.py >checks.log 2>checks.time
```
