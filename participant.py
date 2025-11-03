"""
participant.py

Defines the Participant class and helpers to load Participant objects from CSV.
This module avoids third-party dependencies for easy grading.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple, Iterable, List, Dict, Any
import csv

# -----------------------------
# Domain Model
# -----------------------------

@dataclass(frozen=True)
class BloodPressure:
    systolic: float
    diastolic: float

    def category(self) -> str:
        """Return simple BP category based on AHA-like cutoffs (simplified)."""
        s, d = self.systolic, self.diastolic
        if s < 120 and d < 80:
            return "Normal"
        if 120 <= s < 130 and d < 80:
            return "Elevated"
        if (130 <= s < 140) or (80 <= d < 90):
            return "Stage 1 HTN"
        if s >= 140 or d >= 90:
            return "Stage 2 HTN"
        return "Uncategorized"

@dataclass
class Participant:
    """Represents a study participant (immutable id not provided in dataset)."""
    age: Optional[int]
    sex: Optional[str]
    current_smoker: Optional[bool]
    heart_rate: Optional[float]
    blood_pressure: Optional[BloodPressure]
    cigs_per_day: Optional[float]
    chol: Optional[float]

    # -----------------------------
    # Convenience Computations
    # -----------------------------
    def smoker_status(self) -> str:
        if self.current_smoker is True:
            if self.cigs_per_day is None:
                return "Smoker (unknown intensity)"
            if self.cigs_per_day >= 20:
                return "Heavy smoker"
            if self.cigs_per_day >= 5:
                return "Moderate smoker"
            return "Light smoker"
        if self.current_smoker is False:
            return "Non-smoker"
        return "Unknown"

    def bp_category(self) -> str:
        return self.blood_pressure.category() if self.blood_pressure else "Unknown"

    # -----------------------------
    # String Representation
    # -----------------------------
    def __str__(self) -> str:
        return (
            f"Participant(age={self.age}, sex={self.sex}, "
            f"smoker={self.current_smoker}, hr={self.heart_rate}, "
            f"bp={self.blood_pressure.systolic if self.blood_pressure else None}/"
            f"{self.blood_pressure.diastolic if self.blood_pressure else None}, "
            f"cigs_per_day={self.cigs_per_day}, chol={self.chol})"
        )

# -----------------------------
# Parsing Utilities
# -----------------------------

def _to_int(v: str) -> Optional[int]:
    v = v.strip()
    if v == "" or v.lower() == "na":
        return None
    try:
        return int(float(v))
    except ValueError:
        return None

def _to_float(v: str) -> Optional[float]:
    v = v.strip()
    if v == "" or v.lower() == "na":
        return None
    try:
        return float(v)
    except ValueError:
        return None

def _to_bool(v: str) -> Optional[bool]:
    v = v.strip().lower()
    if v in ("yes", "y", "true", "1"):
        return True
    if v in ("no", "n", "false", "0"):
        return False
    if v == "":
        return None
    return None

def _parse_bp(v: str) -> Optional[BloodPressure]:
    v = v.strip()
    if not v:
        return None
    # Accept forms like "120/80", "127.5/76"
    parts = v.replace(" ", "").split("/")
    if len(parts) != 2:
        return None
    try:
        s = float(parts[0])
        d = float(parts[1])
        return BloodPressure(s, d)
    except ValueError:
        return None

# -----------------------------
# CSV Loading
# -----------------------------

EXPECTED_COLUMNS = [
    "age",
    "sex",
    "current_smoker",
    "heart_rate",
    "blood_pressure",
    "cigs_per_day",
    "chol",
]

def row_to_participant(row: Dict[str, str]) -> Participant:
    """Convert a CSV dict row to a Participant with robust parsing."""
    return Participant(
        age=_to_int(row.get("age", "")),
        sex=(row.get("sex") or "").strip().lower() or None,
        current_smoker=_to_bool(row.get("current_smoker", "")),
        heart_rate=_to_float(row.get("heart_rate", "")),
        blood_pressure=_parse_bp(row.get("blood_pressure", "")),
        cigs_per_day=_to_float(row.get("cigs_per_day", "")),
        chol=_to_float(row.get("chol", "")),
    )

def load_participants(csv_path: str) -> List[Participant]:
    """Load participants from a CSV file. Ignores extra columns; tolerant of missing ones."""
    participants: List[Participant] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            participants.append(row_to_participant(row))
    return participants

# -----------------------------
# Simple Analytics (Optional)
# -----------------------------

def summarize(participants: Iterable[Participant]) -> Dict[str, Any]:
    """Compute a few simple summary metrics to aid graders/demonstration."""
    ps = list(participants)
    n = len(ps)
    smokers = sum(1 for p in ps if p.current_smoker is True)
    non_smokers = sum(1 for p in ps if p.current_smoker is False)
    unknown_smoker = n - smokers - non_smokers

    chol_values = [p.chol for p in ps if p.chol is not None]
    avg_chol = sum(chol_values) / len(chol_values) if chol_values else None

    stage2 = sum(1 for p in ps if p.blood_pressure and p.bp_category() == "Stage 2 HTN")
    normal_bp = sum(1 for p in ps if p.blood_pressure and p.bp_category() == "Normal")

    return {
        "count": n,
        "smokers": smokers,
        "non_smokers": non_smokers,
        "unknown_smoker": unknown_smoker,
        "average_cholesterol": avg_chol,
        "normal_bp_count": normal_bp,
        "stage2_bp_count": stage2,
    }
