# d56 campaign aggregate: runs/full

ALERT file present: False. Alert job files: none

| Set | jobs done | rooms | pairs | lit (bound 40) | lit (bound 120 only) | survivors | verify failures | cert-tested pairs | certified | tripwires | cert n/a (sheared only) | CPU s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 520 of 520 | 169672127 | 285299577 | 285299577 | 0 | 0 | 0 | 2852044 | 0 | 0 | 0 | 4095 |
| E | 400 of 400 | 945884 | 5238044332 | 5236565128 | 1479204 | 0 | 0 | 52379888 | 0 | 0 | 42693277 | 12845 |

Set E extras: index-3 regression rooms 9631, pairs 43623736, lit 43623736; index-6 pairs 8296, lit 8296.
Certificate instances, set A: {'par': 0, 'rig': 0, 'cut': 0, 'lift_pairs_flagged': 0, 'targets_certified': 0, 'tw_zerofreeRig': 0, 'tw_nonV': 0, 'tw_D20shape': 0, 'tw_lemmaZ': 0, 'tw_notpillow': 0, 'corrupt_rejected': 0}
Certificate instances, set E: {'par': 3454268, 'rig': 0, 'cut': 16, 'lift_pairs_flagged': 0, 'targets_certified': 3454268, 'tw_zerofreeRig': 0, 'tw_nonV': 0, 'tw_D20shape': 0, 'tw_lemmaZ': 0, 'tw_notpillow': 0, 'corrupt_rejected': 0}

## Rates and extrapolation (CPU)

- Set A: 24.13 us per room, 14.35 us per pair (CPU per room and per pair, everything included).
  Full set A: 1.13 CPU-h (range 0.55 to 3.15: mean, min, max sampled job x 520 jobs); 4095 CPU s done.
- Set E: 13579.67 us per room, 2.45 us per pair (CPU per room and per pair, everything included).
  Full set E: 3.57 CPU-h (range 1.22 to 9.49: mean, min, max sampled job x 399 jobs, plus job 0); 12845 CPU s done.
- Both sets: 4.70 CPU-h (range 1.77 to 12.64).

## Survivors (unresolved unless certified; send to the orbit decider)

none

## Count reconciliation

- Set A rooms 169672127 vs census 169672127: OK
