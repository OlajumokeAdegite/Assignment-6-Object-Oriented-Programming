# Minimal quick checks (optional).
# Run with: python -m pytest -q       (if pytest is available)
from participant import row_to_participant, BloodPressure

def test_bp_parse_and_category():
    p = row_to_participant({"blood_pressure": "127.5/76"})
    assert p.blood_pressure is not None
    assert p.bp_category() in {"Normal", "Elevated", "Stage 1 HTN", "Stage 2 HTN", "Uncategorized"}

def test_bool_parse():
    p = row_to_participant({"current_smoker": "yes"})
    assert p.current_smoker is True
    p = row_to_participant({"current_smoker": "no"})
    assert p.current_smoker is False
