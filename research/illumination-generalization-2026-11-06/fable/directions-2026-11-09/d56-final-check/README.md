# d56 final check: D20 and non-lattice marks

This directory holds the checker for the two finite checks specified in
`../d50-review-d49/review.md` section 7, its validation, a 1% pilot, and a
one-command launcher. The full run hasn't been launched.

Tags: PROVED, CITED, COMPUTED, GUESSED.

## Status

- Ready to launch. The full run is estimated at 4.2 CPU-hours (range 2.3 to
  7.1) (COMPUTED from the pilot).
- Pilot: 10 of 920 jobs, 0 survivors, 0 certified pairs, 0 tripwires
  (COMPUTED).
- Shortcut: works for D20 and finds 0 certified pairs (COMPUTED). A
  completeness argument is in `shortcut/NOTES.md`; it wasn't refereed.

## What the checker does

`check` (`src/check.c`) is one process per job. Each job enumerates rooms
with the d9 Redelmeier enumerator. The split is round-robin at size 11
(SPLIT = 11), so job J of 520 is a subset of d9 job J mod 26.

### Sets

- **Set A (D20).** Strictly simple rooms with W = 20 and area 20. The pairs
  are different-class interior lattice pairs over Λ = Z².
- **Set E.** Normalized class (iii) rooms with 12 ≤ W ≤ 20 and
  area ≤ W − 4.
  - Class (iii) means no direction with max(p, q) ≤ 15 gives 2 cylinder
    components.
  - Marks are pairs that aren't both in Z². Each mark must be admissible
    for one of the 10 lattices of index 2 or 4 through some lift pair
    (ρ(x, y) = (x, −y)).
  - The W = 16 area 8 room also gets the 12 index-6 lattices.
  - (1/2)Z² pairs are skipped when area ≤ 14, as the spec says.
  - 1% of rooms get a (1/3)Z² regression sample.

### Per pair

1. The checker shoots billiard paths in the 4-fold unfolding with
   p + q ≤ 40. If the pair isn't lit, it retries up to p + q ≤ 120.
   - The shooter cuts each direction's square permutation into segments at
     corner squares. All points on one segment are mutually lit.
   - Every lighting path is re-verified by the independent
     `src/verify_plane.c` (copied from d9).
2. Survivors, plus a deterministic 1% hash sample of all pairs, go to the
   certificate fallback over the pillowcase of the room.
   - The fallback runs Par, Rig with the live graph (d48 item 2) and Cut.
     Cut runs only where Lemma Z allows: n ≤ 3r, or n ≤ 4r + 4 with x
     vertex-only.
   - Rectangular Λ = diag(1/a, 1/b)Z² is handled through the scaled room
     (d47 Prop 2.1).
3. The fallback also checks these tripwires:
   - zero-free Rig with d ≠ 4 or Λ ⊉ (1/2)Z²;
   - a non-V target certificate with z ≥ 1 and n > 4r;
   - a D20 Rig shape other than (4, 5, 2);
   - Lemma Z: Par with z ≥ 1 and n > 8r, Rig with n > 5r, Cut with
     n > 3r;
   - a zero-free certificate with p ≠ 4.

### Exit codes and output

`check` exits 0 for OK, 10 for a certified pair (POSITIVE) and 11 for a
tripwire. It writes one output file per job. The file has a `SUMMARY` line
with counts and CPU seconds, per-(W, area) room counts, certificate
instance counts, and a `SURVIVOR` line with full room data for each
unlit pair.

### Driver and aggregate

`run_jobs.py` runs the jobs.

- **Resume.** A job counts as done only after `check` exits 0 with a
  SUMMARY line. Its `.tmp` file is then renamed to `.out`.
- **Alerts.** On exit 10 or 11, the driver writes `ALERT` and
  `job_<name>.POSITIVE` or `.TRIPWIRE`. It kills the other jobs and
  refuses to resume.
- **CPU limit.** CPU is counted with `wait4` rusage and `ps -o cputime`.
  The driver stops when this invocation reaches the limit. Each job also
  gets an RLIMIT_CPU backstop.
- **Binary hash.** The campaign is tied to the binary hash
  `e0ea94acbfc169d0`. The driver refuses to run with a different binary.

`aggregate.py` sums the outputs, lists survivors, extrapolates CPU, and
reconciles counts when a set is complete:

- Set A: the total against 169,672,127, and the 26 d9 residues against
  `runs/a20/job-J.counts`.
- Set E: each (W, area) cell's rooms, reduced and c3 counts against
  `partA-totals.json`.
- Set E: the c3 total for each W against the d50 table (22, 287, 3,875,
  59,893, 881,807).
- Set E: the 4 Part A residues against `runs/partA/a16/job-J.out`.

Tools copied verbatim from d9, d10 and d46 are in `reused/`.

## Validation

All results are COMPUTED. Logs are in `val/`.

| Test | Result |
| --- | --- |
| Positive control: 22-wall room, pair (1,3),(3,5), mode X | Survives bound 120. Par certifies it at classes b, c, d for all 4 lift pairs (12 instances). `check` writes POSITIVE and exits 10. |
| Alert path through the driver (`CHECK_TESTROOM`) | `ALERT` and `job_A0000.POSITIVE` written, other jobs killed, resume refused. |
| Negative control: 12-wall cross, mode X | 10 pairs, all lit. Pair (1,2),(3,2) gets Par at d and Cut at c, none at b, matching `check_even.log` and d38. |
| Cross with Set E marks, mode Y | 3,776 pairs lit, 0 certified, 3,120 sheared-only. |
| Corrupted paths (`CHECK_CORRUPT=1`) | 523 of 523 rejected. |
| Shooting against the exact decider `orbitc` | 2,431 lattice pairs on 328 rooms agree, including the 22-wall DARK pair. 29,696 half-grid pairs on 185 doubled rooms agree. |
| C certificate code against the d10 Python reference (`val_cert.py`) | 2,572 groups, 0 disagreements. Reference instances: Par 54, Cut 8. Rig ran on 297 groups with a nontrivial R_y. |
| Counts against the census | 0 mismatches: area 14 at W ≤ 22, area 15 at W 18 to 22, and all Set E cells with area ≤ 12. Full W = 12, 14, 16 rows give 22, 287, 3,875. |
| Segment shooter against the per-source shooter | Same verdicts on 5 rooms: 14,731 lit at bound 40 and 1 at bound 120. |

Limitation: no test produced a positive Rig separation. Rig is checked
against the reference only in the "not separated" direction.

## Pilot

The pilot ran 10 of 920 jobs in `runs/full/`:

- Set A: A0037, A0141, A0259, A0377 and A0499.
- Set E: E0000, E0097, E0203, E0311 and E0389. E0000 also holds every
  room with area under 11.

The full aggregate is in `runs/full/aggregate_pilot.md`. The pilot used
201 CPU seconds, within the 8-process cap.

| Set | Jobs | Rooms | Pairs | Lit, bound 40 | Lit, bound 120 only | Survivors | Verify failures | Cert-tested | Certified | Tripwires | CPU s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 5 of 520 | 1,461,137 | 2,405,837 | 2,405,837 | 0 | 0 | 0 | 23,751 | 0 | 0 | 42 |
| E | 5 of 400 | 12,209 | 66,412,053 | 66,392,040 | 20,013 | 0 | 0 | 663,725 | 0 | 0 | 159 |

More Set E results:

- Index-3 regression: 132 rooms and 574,440 pairs, all lit.
- Index-6 lattices: 8,296 pairs, all lit.
- Certificate sample: 541,063 of the 663,725 sampled pairs (82%) are
  admissible only for sheared lattices. The checker counts them as
  `cert_na`.
- Par certified 43,302 instances on lit sampled pairs. These are
  single-class instances, not certified pairs.

Shooting bound: every pilot pair was lit by p + q ≤ 120. 20,013 Set E
pairs (0.03%) needed a bound above 40. No Set A pair did.

## Extrapolation

Each estimate is the mean, minimum or maximum CPU of the sampled jobs,
times the job count. Set E job 0 is counted separately.

| Set | Per pair | Full set, CPU-hours | Range |
| --- | --- | --- | --- |
| A | 17.5 µs | 1.21 | 0.82 to 1.67 |
| E | 2.4 µs | 2.97 | 1.45 to 5.40 |
| Both | | 4.19 | 2.27 to 7.07 |

Per-job CPU: Set A 5.7 to 11.6 s; Set E 12.9 to 52.5 s (E0000 is the
52.5 s job). The spec guessed 12 to 30 CPU-hours (GUESSED there). The
segment shooter is about 47 times faster per pair than the per-source
shooter used first. The per-source shooter projected about 460 CPU-hours
for Set E.

## Shortcut (task 1)

A subagent adapted the d52 fold enumeration to Rig quotients (`shortcut/`,
under 3 CPU seconds). Read `shortcut/NOTES.md` for details.

- 12 labelled quotient shapes (5 cells, z = 2, identity at y) give 8
  covers. They give 1 strictly simple room up to isometry, with W = 20 and
  area 20 (COMPUTED).
- That room has 14 different-class pairs: 0 lift pairs separated, 0
  certified (COMPUTED). `check` agrees: 14 pairs lit, 0 certificates,
  0 tripwires.
- R_y is ι-invariant (PROVED in NOTES.md, not refereed). Completeness
  follows from d48's (4, 5, 2) shape (CITED).
- Caveat: no positive control exists for its live-graph reachability.

The shortcut covers the D20 certificate question but not Set E. The full
run is still needed for the shooting side of D20 and for all of Set E.

## Launch the full run

To start or resume the full run, run this command. Choose the process
count and the CPU-hour cap.

```sh
cd d56-final-check && ./run_full.sh 8 10
```

The script does the following:

1. Builds `check` and `orbitc` if they're missing. A rebuilt `check` may
   hash differently, and then the driver refuses to run. Keep the shipped
   binary.
2. Initializes `runs/full` only if `config.json` is missing. The pilot
   jobs stay done.
3. Runs pending jobs until all are done, CPU_HOURS is reached, or an
   alert fires.
4. Writes `runs/full/aggregate.md` and prints the totals.

With 8 processes and a 10-hour cap, the run should finish in under 1 hour
of wall time. To resume after a stop, run the same command. Each
invocation has its own CPU budget. `runs/full/cpu_ledger.txt` records
each invocation's total.

## Read the result

- **Clean result.** `runs/full/aggregate.md` shows all jobs done, 0
  survivors, 0 certified, 0 tripwires and 0 verify failures. Every
  reconciliation line reads OK or 0 mismatches. That closes both finite
  checks.
- **ALERT present.** Read `runs/full/ALERT`, then the named
  `job_*.POSITIVE` or `job_*.TRIPWIRE`. The last lines hold the room,
  pair, lattice and certificate data.
  - A POSITIVE is a certified pair that survived shooting. That's a
    candidate dark pair.
  - A TRIPWIRE means a proof assumption failed at that room.
  - Remove `ALERT` only after you've investigated.
- **Survivors without a certificate.** These are unresolved. Run them
  through the exact decider.
  - `orbitc` handles rooms with at most 40 cells.
  - Scaled Set E rooms may need `reused/orbit.py`.
  - Survivors aren't sent to the decider automatically.
- **Failures.** `runs/full/failures.log` lists jobs that crashed. Those
  jobs stay pending and rerun on resume.

## Spec readings and deviations

When the spec was ambiguous, the checker uses the conservative reading.

- **Lift pairs.** A Set E mark counts if any lift pair is admissible, not
  only all of them.
- **Sampling.** The certificate fallback also runs on the 1% sample of
  lit pairs. The sample is per pair, by hash.
- **Alerts.** The run stops on tripwires as well as positives. The Lemma Z
  bounds are added as tripwires.
- **Sheared lattices.** The certificate code covers Λ = Z² and the
  rectangular lattices: 5 of 10 at index 2 or 4, and 4 of 12 at index 6.
  It doesn't implement sheared Λ. A survivor admissible only for sheared
  Λ would be unresolved and goes to the exact decider. In the pilot, 82%
  of sampled Set E pairs were sheared-only, and no pair survived.
- **Shooter.** The segment method tests the same path set as the spec's
  per-source shooter. Verdicts were checked equal on 5 rooms.
- **CPU limit.** The limit applies per invocation. Polling is every
  second, so a run can overshoot by up to 1 CPU second per running process.
  One test spent 4.0 s against a 2.88 s budget.
- **Tiny driver test.** One tiny test passed `--env` pairs as a single zsh
  word, so it ran with Set E defaults and spent about 246 CPU seconds.
  The driver behaved correctly. The test campaign was deleted. Pass each
  `--env K=V` as a separate argument.

## Caps used

- CPU: about 520 s (0.14 CPU-hours) of the 1 CPU-hour cap, all COMPUTED:
  - tiny driver tests: about 254 s;
  - pilot: 201 s;
  - validation: about 60 s;
  - shortcut: about 3 s.
- Processes: at most 6 at once, under the cap of 8.
- Disk: about 1.7 MB, under the 20 MB cap.
- Memory: under 2 GB. The largest process stayed far below the cap.

## Files

- `check`, `src/check.c`, `src/verify_plane.c`: the checker and its
  verifier.
- `orbitc`, `src/orbitc.c`: the exact decider.
- `run_jobs.py`, `aggregate.py`, `run_full.sh`: the driver, the aggregate
  and the launcher.
- `val/`: validation inputs, scripts and logs.
- `shortcut/`: the fold-enumeration shortcut.
- `runs/full/`: the pilot jobs, reused by the full run.
- `reused/`: verbatim copies of the source tools.
