#!/bin/sh
# d56 full run: Set A (D20, 520 jobs) and Set E (non-lattice marks, 400 jobs), certificate sample 1%.
# usage: ./run_full.sh MAX_PROCS CPU_HOURS
# Start and resume with the same command.  Finished jobs (runs/full/job_*.out, including the 10 pilot
# jobs) are never rerun; jobs killed at the CPU limit or by Ctrl-C restart from scratch next time.
# CPU_HOURS caps the CPU time of this invocation, summed over all jobs.
# A certified pair (exit 10) or a tripwire (exit 11) stops everything and writes runs/full/ALERT.
set -e
cd "$(dirname "$0")"
P=${1:?usage: run_full.sh MAX_PROCS CPU_HOURS}
H=${2:?usage: run_full.sh MAX_PROCS CPU_HOURS}
[ -x check ] || clang -O3 -march=native -Wall -Wno-gnu-statement-expression -o check src/check.c src/verify_plane.c
[ -x orbitc ] || clang -O3 -o orbitc src/orbitc.c
C=runs/full
[ -f $C/config.json ] || python3 -B run_jobs.py init $C 520 400 10000
python3 -B run_jobs.py run $C --procs "$P" --cpu-hours "$H" || true
python3 -B aggregate.py $C > $C/aggregate.md
[ -f $C/ALERT ] && { echo "ALERT:"; cat $C/ALERT; }
grep -E '^\| [AE] \||^- Both|^- Set' $C/aggregate.md
