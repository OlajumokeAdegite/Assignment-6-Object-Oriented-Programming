# Assignment-6-Object-Oriented-Programming
# Participant Class Assignment (Python)

This repo contains a small, **no-dependency** Python solution that:

- Defines a `Participant` user-defined class with attributes and methods.
- Loads your dataset and creates one `Participant` object **per row**.
- Demonstrates simple analytics and a CLI for usability.
- Includes robust parsing and error handling.
- Is organized and well-documented for readability.

## Files

- `participant.py` — Core domain classes (`Participant`, `BloodPressure`) and CSV loading utilities.
- `main.py` — Command-line interface to preview participants and print a JSON summary.
- `test_quickcheck.py` — Minimal quick checks (can be run with `python -m pytest -q` if available).

## How to Run

```bash
python main.py /mnt/data/smoking_health_data_final.csv --limit 5
python main.py /mnt/data/smoking_health_data_final.csv --filter smoker --limit 10
```

## GitHub Steps (quick guide)

1. **Initialize locally**:
   ```bash
   git init
   git add .
   git commit -m "Participant class assignment: initial commit"
   ```
2. **Create new repo** on GitHub (private is fine).
3. **Add remote & push**:
   ```bash
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git branch -M main
   git push -u origin main
   ```
