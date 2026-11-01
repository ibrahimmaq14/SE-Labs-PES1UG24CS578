# Lab 6 Code and Branch Coverage Analysis

**SRN:** PES1UG24CS578

**Program:** Smart Thermostat Controller

**Original repository:** [SETAPESU26/L6_L7_29_thermostat_control](https://github.com/SETAPESU26/L6_L7_29_thermostat_control/tree/main/lab6)

**Original source commit:** `c0f13aa2cd72bd1a451c1a7a65e4502b0d25b892`

## Code coverage deliverables

- `CodeCoverageTest_thermostat_control.py`: 14 parameterized test cases.
- `screenshots/code_coverage.png`: screenshot of actual Python terminal output in a local browser output viewer.
- `code_coverage_report.txt`: corresponding commands, stdout and exit codes.
- `thermostat_control.py`: unchanged assigned application for reproducible runs.

## Results

The two original starter tests pass but cover only 9/35 statements (25.71%,
displayed as 26%). The updated line suite covers 33/35 statements (94.29%,
displayed as 94%), exceeding the required 90%.

The line tests cover every temperature outcome, idle/normal heating/normal
cooling, and all energy alert outcomes. The two uncovered statements are
the `heat_boost` and `cool_boost` returns at application lines 23 and 26.

## Reproduce

Run from this `LAB6` directory using Python 3.11:

```powershell
python -m pip install -r requirements.txt
python -m coverage run --data-file=.coverage.line --source=thermostat_control -m pytest -q CodeCoverageTest_thermostat_control.py
python -m coverage report --data-file=.coverage.line -m --fail-under=90
```

Coverage is limited to the application, so test code is not included in
the percentage. `pytest.ini` enables discovery of the required submission
filenames. Only results above the required threshold are screenshotted.
