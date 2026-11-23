# d56 campaign aggregate: runs/full

ALERT file present: False. Alert job files: none

| Set | jobs done | rooms | pairs | lit (bound 40) | lit (bound 120 only) | survivors | verify failures | cert-tested pairs | certified | tripwires | cert n/a (sheared only) | CPU s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 5 of 520 | 1461137 | 2405837 | 2405837 | 0 | 0 | 0 | 23751 | 0 | 0 | 0 | 42 |
| E | 5 of 400 | 12209 | 66412053 | 66392040 | 20013 | 0 | 0 | 663725 | 0 | 0 | 541063 | 159 |

Set E extras: index-3 regression rooms 132, pairs 574440, lit 574440; index-6 pairs 8296, lit 8296.
Certificate instances, set A: {'par': 0, 'rig': 0, 'cut': 0, 'lift_pairs_flagged': 0, 'targets_certified': 0, 'tw_zerofreeRig': 0, 'tw_nonV': 0, 'tw_D20shape': 0, 'tw_lemmaZ': 0, 'tw_notpillow': 0, 'corrupt_rejected': 0}
Certificate instances, set E: {'par': 43302, 'rig': 0, 'cut': 0, 'lift_pairs_flagged': 0, 'targets_certified': 43302, 'tw_zerofreeRig': 0, 'tw_nonV': 0, 'tw_D20shape': 0, 'tw_lemmaZ': 0, 'tw_notpillow': 0, 'corrupt_rejected': 0}

## Rates and extrapolation (CPU)

- Set A: 28.75 us per room, 17.46 us per pair (CPU per room and per pair, everything included).
  Full set A: 1.21 CPU-h (range 0.82 to 1.67: mean, min, max sampled job x 520 jobs); 42 CPU s done.
- Set E: 13042.84 us per room, 2.40 us per pair (CPU per room and per pair, everything included).
  Full set E: 2.97 CPU-h (range 1.45 to 5.40: mean, min, max sampled job x 399 jobs, plus job 0); 159 CPU s done.
- Both sets: 4.19 CPU-h (range 2.27 to 7.07).

## Survivors (unresolved unless certified; send to the orbit decider)

none

## Count reconciliation

- Set A: 5 of 520 jobs done; total reconciliation runs when all are done.
- Set E: 5 of 400 jobs done; reconciliation runs when all are done. Pilot cells sampled: 27.
