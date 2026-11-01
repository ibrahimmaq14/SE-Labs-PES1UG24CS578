# Lab 6: Code and Branch Coverage Analysis

**SRN:** PES1UG24CS578

**Application:** Smart Thermostat Controller

**Assigned repository:** [SETAPESU26/L6_L7_29_thermostat_control](https://github.com/SETAPESU26/L6_L7_29_thermostat_control/tree/main/lab6)

## Deliverables

| File | Description |
| --- | --- |
| `CodeCoverageTest_thermostat_control.py` | 14 code coverage test cases |
| `BranchCoverageTest_thermostat_control.py` | 50 branch and boundary test cases |
| `code_coverage.png` | Code coverage result screenshot |
| `branch_coverage.png` | Branch coverage result screenshot |

## Results

- Code coverage suite: **94.29% statement coverage** (33/35 statements).
- Branch coverage suite: **100% statement and branch coverage** (35/35 statements and 28/28 branch outcomes).
- All **64 tests pass** across the two suites.

The application source is provided in the assigned repository. To rerun,
place these test files beside its `thermostat_control.py` and install
`coverage` and `pytest`.

```powershell
python -m coverage run --source=thermostat_control -m pytest -q CodeCoverageTest_thermostat_control.py
python -m coverage report -m
python -m coverage run --branch --source=thermostat_control -m pytest -q BranchCoverageTest_thermostat_control.py
python -m coverage report -m
```

## Coverage commits

- `b301057`: code coverage tests and result evidence.
- `dfb208f`: branch coverage tests and result evidence.
