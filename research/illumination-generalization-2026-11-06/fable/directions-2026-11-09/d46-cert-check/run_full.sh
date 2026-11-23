#!/bin/sh
# d46 full run: W = 20 (r = 8), areas 21..40, F* per room area, >= 3 corner classes, check on.
# usage: ./run_full.sh MAX_PROCS WALL_HOURS
# Start and resume with the same command.  Finished jobs (runs/full_W20/job_NNNN.out) are never
# rerun; jobs killed at the wall-clock limit or by Ctrl-C restart from scratch next time.
# A positive (exit 10) stops everything and writes runs/full_W20/ALERT.
set -e
cd "$(dirname "$0")"
P=${1:?usage: run_full.sh MAX_PROCS WALL_HOURS}
H=${2:?usage: run_full.sh MAX_PROCS WALL_HOURS}
[ -x cert_check ] || clang -O3 -march=native -Wall -o cert_check cert_check.c
C=runs/full_W20
[ -f $C/config.json ] || python3 run_jobs.py init $C 500 3 20 20 21 40 1 1 1 1
python3 run_jobs.py run $C --procs "$P" --hours "$H"
python3 aggregate.py $C --cells > $C/aggregate.md
tail -3 $C/aggregate.md
