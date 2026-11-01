# Lab 6 Code and Branch Coverage Analysis

**SRN:** PES1UG24CS578

**Program:** Smart Thermostat Controller

**Original repository:** [SETAPESU26/L6_L7_29_thermostat_control](https://github.com/SETAPESU26/L6_L7_29_thermostat_control/tree/main/lab6)

**Original source commit:** `c0f13aa2cd72bd1a451c1a7a65e4502b0d25b892`

## Deliverables

- `CodeCoverageTest_thermostat_control.py`: 14 parameterized test cases.
- `BranchCoverageTest_thermostat_control.py`: 50 branch and boundary test cases.
- `screenshots/code_coverage.png` and `screenshots/branch_coverage.png`:
  screenshots of actual Python terminal output in a local browser output viewer.
- `code_coverage_report.txt` and `branch_coverage_report.txt`: corresponding
  commands, stdout and exit codes.
- `thermostat_control.py`: unchanged assigned application for reproducible runs.

## Results

The two original starter tests pass but cover only 9/35 statements (25.71%,
displayed as 26%). The updated line suite covers 33/35 statements (94.29%,
displayed as 94%), exceeding the required 90%.

| Submitted suite | Tests passed | Statements covered | Branch outcomes covered |
| --- | --- | --- | --- |
| Code coverage | 14 | 33/35 (94.29%) | Not measured in the line-only run |
| Branch coverage | 50 | 35/35 (100%) | 28/28 (100%) |

The line tests cover every temperature outcome, idle/normal heating/normal
cooling, and all energy alert outcomes. The two uncovered statements are
the `heat_boost` and `cool_boost` returns at application lines 23 and 26.

The branch suite retains all 14 first-stage inputs and extends them with
both boost modes and boundary cases. It checks sleep transitions at hours
5/6 and 21/22; occupied morning/evening transitions at 5/6, 8/9, 16/17 and
21/22; positive and negative HVAC differences just inside and exactly at
the one-degree idle threshold; outside temperatures below/at 5 and
at/above 30; and empty, below-limit, equal-limit, exactly-half-over-limit,
minority-over-limit and majority-over-limit energy readings. It also
checks that the energy function preserves the supplied list.

Line coverage measures executed statements; branch coverage measures
alternative control-flow outcomes. The branch report's `Cover` column
combines statement and branch opportunities, so the JSON totals were also
checked independently: `covered_lines=35`, `num_statements=35`,
`covered_branches=28`, `num_branches=28`, and no missing branches.
Every function and measured branch is exercised; this does not establish
exhaustive path coverage or correctness for every possible input.

## Reproduce

Run from this `LAB6` directory using Python 3.11:

```powershell
python -m pip install -r requirements.txt
python -m coverage run --data-file=.coverage.line --source=thermostat_control -m pytest -q CodeCoverageTest_thermostat_control.py
python -m coverage report --data-file=.coverage.line -m --fail-under=90
python -m coverage run --data-file=.coverage.branch --branch --source=thermostat_control -m pytest -q BranchCoverageTest_thermostat_control.py
python -m coverage report --data-file=.coverage.branch -m --fail-under=100
python -m pytest -q
```

Coverage is limited to the application, so test code is not included in
the percentage. `pytest.ini` enables discovery of the required submission
filenames. Only results above the required threshold are screenshotted.

## Submission commits

1. `b301057`: code coverage tests, application, result screenshot and report.
2. The following `LAB6: add branch coverage tests and 100 percent coverage evidence`
   commit adds the expanded branch suite, branch screenshot and report.
