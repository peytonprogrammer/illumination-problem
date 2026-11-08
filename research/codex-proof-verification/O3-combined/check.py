"""Validate the combined proof map against independently checked receipts.

Read-only dependency/hash checks; no author execution or discovery search.
The actual fixed geometric witnesses are verified by the two owned checks
linked in statement.md. This file checks their immutable inputs and join.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESEARCH = ROOT.parent / "illumination-k4-codex"


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def load_checked(folder):
    path = ROOT / folder / "check.json"
    data = json.loads(path.read_text())
    assert data["checker_sha256"] == sha(ROOT / folder / "check.py"), folder
    for relative, expected in data["source_sha256"].items():
        assert sha(RESEARCH / relative) == expected, relative
    if "own_engine_sha256" in data:
        assert data["own_engine_sha256"] == sha(ROOT / "O3-five/check.py")
    return data, sha(path)


def main():
    first, first_hash = load_checked("O3-five")
    extension, extension_hash = load_checked("L70-extension")
    assert first["verdict"] == "NEW_FIVE_REFLECTION_OPTICAL_LEMMA_PASS"
    assert extension["verdict"] == "ACCEPT_PARENT_AND_TIGHTEN_WHOLE_LOCAL_O3_L70_TO_NINE"
    dispatch = first["family_dispatch"]
    cases = []
    for name, result in sorted(dispatch["short_forcing_witnesses"].items()):
        cases.append({"case": name, "bound": result["reflections"],
                      "evidence": "O3-five/check.json family_dispatch"})
    cases.extend([
        {"case": "Other partner: generic support", "bound": first["new_lemma"]["reflections"]},
        {"case": "D23: ordinary Tc empty/6", "bound": dispatch["D23_Tc_empty_or_6"]["reflections"]},
        {"case": "D23: ordinary Tc5", "bound": dispatch["D23_Tc_5"]["reflections"]},
        {"case": "L70: N7 absent", "bound": extension["independent_six_path"]["reflections"]},
        {"case": "L70: N7 and R3", "bound": extension["N7_extension"]["paths"]["nine"]["reflections"]},
        {"case": "L70: N7 and R4/empty", "bound": extension["N7_extension"]["paths"]["four_suffix"]["reflections"]},
    ])
    assert [row["bound"] for row in cases[-6:]] == [5, 4, 6, 6, 9, 4]
    root_windows = dispatch["symbolic_partner_dispatch"]
    assert len(root_windows) == 18
    excluded = [r["partner"] for r in root_windows if r["status"] == "EXPLICITLY_EXCLUDED"]
    assert excluded == ["L70"]
    assert max(row["bound"] for row in cases) == 9
    text = (HERE / "statement.md").read_text()
    assert "at most nine reflections" in text
    for token in ["{L7,D3,D4,B2,B6}", "{L1,L6,E3,E5,N7}",
                  "{L6,B2,R2,R4,N0,N5,N6}", "{R3,N0,N6}"]:
        assert token in text
    result = {
        "status": "COMBINED_LOCAL_TWO_ROOT_O3_LE9_VERIFIED_DEPENDENCY_JOIN",
        "maximum_reflections": 9,
        "case_bounds": cases,
        "root_windows_in_prior_dispatch": 18,
        "sole_previous_exclusion_now_covered": "L70",
        "review_receipt_sha256": {"O3-five/check.json": first_hash,
                                  "L70-extension/check.json": extension_hash},
        "statement_sha256": sha(HERE / "statement.md"),
        "checker_sha256": sha(Path(__file__)),
        "scope": "Established local two-root O3=B701 e2+e1+b1 class; classification inherited, all listed witnesses independently checked.",
        "limits": "No full surplus-four/universal theorem or new classification proof. No author execution, search or new room."
    }
    (HERE / "check.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: source hashes current; 18 symbolic partner windows joined; 10 case bounds max9; original proofs preserved.")


if __name__ == "__main__": main()
