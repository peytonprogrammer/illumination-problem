campaign runs/val_census_w22 config {'nj': 32, 'split': 3, 'args': [22, 22, 1, 16, 0, 0, 0, 1], 'env': {}, 'binary_sha256_16': '874fe08698861908'}
jobs done 32 of 32
W 22 canonical shapes 1206788 parity patterns 2962593 in scope (>= 3 classes) 2962593 passing F* at some area 2962593
| W | area | rooms generated | fixed rooms | rooms passing F* | rooms checked | pairs | positives |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 22 | 11 | 36 | 276 | 36 | 36 | 0 | 0 |
| 22 | 12 | 954 | 7,624 | 954 | 954 | 0 | 0 |
| 22 | 13 | 11,707 | 93,496 | 11,707 | 11,707 | 2 | 0 |
| 22 | 14 | 93,477 | 747,744 | 93,477 | 93,477 | 104 | 0 |
| 22 | 15 | 556,286 | 4,449,436 | 556,286 | 556,286 | 3,789 | 1 |
| 22 | 16 | 2,664,253 | 21,313,608 | 2,664,253 | 2,664,253 | 47,065 | 0 |
TOTAL shapes 1206788 rooms_generated 3326713 rooms_passing_fstar 3326713 rooms_checked 3326713 pairs_checked 50960 positives 1 cpu_s 705.5 (max job 23.5)
job_0003.out: POSITIVE W 22 r 9 area 15 corner_classes 4 rho 3 3 3 0 widths 1 1 1 1 1 1 heights 1 1 1 1 1 1 rows 4 6 3 51 30 12
job_0003.out: POSITIVE_PAIR origin_parity (1,1) S (1,3) T (3,5) blocks b c d 5 15 5
job_0003.out: POSITIVE_CELLS 15 2 0 1 1 2 1 0 2 1 2 0 3 1 3 4 3 5 3 1 4 2 4 3 4 4 4 2 5 3 5
