"""Report and hash the completed single pilot; never starts new work."""
from pathlib import Path
import hashlib
import json

R=Path(__file__).parent
D=json.loads((R/'result.json').read_text());V=json.loads((R/'verification.json').read_text())
assert V['status']=='PASS' and V['result_sha256']==hashlib.sha256((R/'result.json').read_bytes()).hexdigest()
S=D['stats']
text=f'''Seven-exception orthogonal20-wall pilot — one marked case
4 November 2026

[done] Pilot operational. All30distinct generated valid rooms illuminate. No undecided room or dark candidate. Stopped at the predeclared30-room cap; this case is NOT exhausted and the full tranche has not run.

Case: I2_1_1_p00, physical S=(0,0), T=(2,2), EXACTLY7transparent non-A points, at most20walls, exactlythetwofullAstars. Complete case/window data in case.json and the preceding k7-support-census/.

Measured result (one run)
  Valid rooms:30, all independently geometrically checked.
  Lit by the short-direction filter:22.
  Lit by finite-orbit direction extraction and actual-path replay:8.
  Undecided:0. Dark candidates:0. Geometry/worker errors:0.
  Rooms with20walls:24; rooms with18walls:6.
  Verified connecting paths:0–19reflections.
  New universal path guards:30, all separately triangle-audited.
  Short directions tested across the30rooms:1055.
  Orbit states recorded/discovered across the8fallback rooms:895.
  Search wall time:{D['search_wall_seconds']:.3f}seconds.
  SAT solve time:{S['sat_seconds']:.3f}seconds across30calls, no interrupts.
  Optical subprocess time:{S['optical_worker_seconds']:.3f}seconds, including startup/serialization.
  Guard derivation/audit:{S['guard_seconds']:.3f}seconds.
  Direct geometry checks:{S['geometry_seconds']:.3f}seconds.
  Geometry encoding:{D['encoding_seconds']:.3f}seconds, OUTSIDE the search timer.
  Prescribed control validation and final artifact replay are also OUTSIDE the search timer.

The timer starts after encoding/control validation and includes SAT calls, optical subprocesses, guards, geometry checks, progress/model/path/event writes. Every recorded timed result was consumed: rooms saved, paths replayed and universal guards added. Component timings sum below the search total, leaving ordinary coordination/I/O overhead. This is a single ballpark pilot, not a repeated benchmark or a comparison/speedup result. No runtime extrapolation to all56cases is supported. The solver/guard-driven rooms are not random or statistically representative; harder supports can have very different orbit growth.

Validation and limits
controls.json PASS: analytic W18/k7 positive fixture accepted with exact exception/corner channels; knownW22/k4 fixture rejected; samek7fixture rejected under exactk6; unpaired-unit triangles rejected. The initial17square notchfill control was geometrically found to havek6 and corrected before search. A prescribedleaftruncation gives the validk7positivecontrol.
verification.json PASS:30distinct saved unit-square sets, actualW/k/full-star/simplicity checks, frozen triangle geometry agreement, all30actual paths replayed, all30universal guards rechecked by the frozen separately authored checker, and event/result/count/source-hash reconciliation. No additional ray/orbit/SAT search occurred during verification.
The fallback supplied genuine physical connecting paths in all8cases where the short filter failed. No finite-orbit DARK/exhaustion branch was exercised. No state or time cap was mistaken for darkness.
The adapter is deliberately limited to this I2case. I3 needs a separate safe-window adaptation to the frozen encoder before a broader run. No generic all-case runner, formal refutation, independently reviewed new theorem or universalwallbound is claimed.

Artifacts
  result.json/progress.json/run.log/events.jsonl: run receipt and observed progress.
  models/:30valid rooms with cells, triangles, maximal polygon walls and exact counts.
  paths/:30actual connecting paths with directions/method/state counts.
  guards.jsonl:30passing universal U/Zcertificates and added clauses.
  controls.json/guard-control.json/verification.json: validation receipts.
  encoding-notes.txt: model extension, optical clause justification and budget semantics.
  inputs/sources.json: frozen source origins/hashes, including function-only guard checker extraction.

Judgment
The one-case pilot validates the operational path from exact-k7 geometry to verified illumination witnesses, including the orbit fallback. It is encouraging enough to consider a separately bounded, more diverse batch after the I3window adapter is checked. It does not establish that the entire56case tranche will be cheap or that there are no smaller dark rooms. All larger work remains unstarted.

Reproduction
  Use the existing bounded-proof/venv Python with python-sat1.9.dev17.
  verify.py and report.py read/recheck saved outputs and do not start a search.
  run.py intentionally refuses to overwrite result.json; a new search requires a separate explicitly chosen output directory and budget. Do not delete the receipt to trigger a silent repeat.
'''
(R/'findings.txt').write_text(text)
files=[p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json']
manifest={'status':'PILOT_COMPLETE','case':'I2_1_1_p00','same_agent_review':True,
          'sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}
(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'status':'PASS','files_bound':len(files),'valid_rooms':30,'lit':30,
                  'undecided':0,'search_wall_seconds':D['search_wall_seconds'],'stop_reason':D['stop_reason']},indent=2))
