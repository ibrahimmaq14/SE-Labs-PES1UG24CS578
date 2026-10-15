# Lab 5 - Static Code Analysis

**SRN:** PES1UG24CS578

**Assigned program:** Digital Wallet & Payment Tracker

**Submission date:** 16 October 2026

The assigned repository was cloned and its original files preserved. The
cleaned program fixes every reported Bandit, Pylint and Flake8 finding without
disabling checks. Three commits separate the security, code-quality and
formatting work. See `source.md` for the upstream commit.

## Results

| Check | Before | After |
| --- | --- | --- |
| Pylint | 5.69/10; 25 messages | 10.00/10; 0 messages |
| Bandit | 4 findings: 1 high, 1 medium, 2 low | 0 findings |
| Flake8 | 4 findings | 0 findings |
| Regression tests | Not present in assigned source | 18 passed |
| Demo final balance | Rs. 1900.0 | Rs. 1900.0 |
| Demo total credited | Rs. 2500 | Rs. 2500 |

## Deliverables

- `digital_wallet.py`: cleaned program.
- `issues.md`: issue table with original line numbers, rule IDs and fixes.
- `reflection.md`: four relevant reflections approved for this submission.
- `Lab5_Static_Code_Analysis_Report.pdf`: consolidated submission report.
- `reports/before/`: three original tool reports, demo output and exit codes.
- `reports/after/`: three final tool reports, demo and test output, exit codes.
- `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`: final reports,
  also copied to the top level for the filenames required by the handout.
- `tests/test_digital_wallet.py`: regression checks.
- `original/`: unchanged assigned source and README, retained as evidence.
- `Lab_5_Static_Code_Analysis_Student_handout.pdf`: supplied lab instructions.

An empty final Flake8 report is expected: exit code 0 in
`reports/after/run_metadata.json` confirms the successful run.

## Set up and run (PowerShell, Python 3.12)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe digital_wallet.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The demo needs no input. It creates temporary in-memory credentials using
`secrets` when environment variables `WALLET_PIN` and `GATEWAY_SECRET` are
absent. To supply credentials, set those variables locally before running.
The PIN must contain 4-6 ASCII digits and the gateway key must be nonempty.
No real credentials belong in the source or repository.

## Reproduce the analysis

```powershell
.\.venv\Scripts\python.exe -m pylint --persistent=n digital_wallet.py
.\.venv\Scripts\python.exe -m bandit -r digital_wallet.py --format txt
.\.venv\Scripts\python.exe -m flake8 digital_wallet.py
```

For the baseline, substitute `original/digital_wallet.py`. Analyze the
submitted file explicitly: scanning the whole folder also scans the deliberately
unmodified baseline, which still contains the assigned defects. No exclusions,
`nosec` markers, Pylint disables or Flake8 ignores were used on the final file.
Tool versions are pinned in `requirements.txt`; full installed versions are
recorded in `reports/environment.txt`.

## Scope and limitations

This is the lab's single-process in-memory demonstration. For compatibility,
`set_daily_limit` retains the source's per-payment cap; it does not accumulate
spending across a calendar day. Money still uses the source's numeric model,
and merchant categories all receive the original flat 2% cashback. OTPs are
printed only as part of this local demonstration. Receipt paths refer to
securely created empty files; their callers must delete them. State and PIN
salt are not persisted. Passing analysis does not make this a production
payment system: decimal currency accounting, authentication throttling,
transaction persistence and private OTP delivery remain outside this lab.

The supplied three-page handout contains no reflection prompts, despite the
assigned README referring to four. The user approved four relevant questions
based on the stated learning outcomes. They are identified as such in
`reflection.md`.
