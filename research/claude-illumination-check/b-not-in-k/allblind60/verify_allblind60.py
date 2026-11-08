"""Re-verify the 166 all-seven-blind rooms of 41-60 triangles with verify_blind.py's separate pipeline,
adding the five classes where the search saw the first load: (5,1), (5,2), (5,3), (6,1), (5,4)."""
import sys
sys.path.insert(0, ".")
import verify_blind as vb

vb.DIRECTIONS = vb.DIRECTIONS + [(5, 1), (5, 2), (5, 3), (6, 1), (5, 4)]
sys.argv = ["x", "allblind60/allblind60_rooms.json", "allblind60/verify_allblind60.json"]
vb.main()
