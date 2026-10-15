# Lab 5 Static Code Analysis

**SRN:** PES1UG24CS578

**Program:** Digital Wallet and Payment Tracker

**Original repository:** [SETAPESU26/L5_29_digital_wallet](https://github.com/SETAPESU26/L5_29_digital_wallet)

**Original source commit:** `0d188e2b4c3588ba9e3e3f7362f426d10beb7d43`

## Deliverables

- `Lab5_Issues_Table.docx`: the completed issue table, with original line
  numbers, tool rule IDs, descriptions and fixes.
- Six tool reports containing the original and final analysis results:

| Tool | Before | After |
| --- | --- | --- |
| Pylint | `pylint_report_before.txt` | `pylint_report_after.txt` |
| Bandit | `bandit_report_before.txt` | `bandit_report_after.txt` |
| Flake8 | `flake8_report_before.txt` | `flake8_report_after.txt` |

## Results

| Tool | Before | After |
| --- | --- | --- |
| Pylint | 5.69/10; 25 messages | 10.00/10; 0 messages |
| Bandit | 4 findings: 1 high, 1 medium, 2 low | 0 findings |
| Flake8 | 4 findings | 0 findings |

The six reports are unchanged tool outputs. The empty Flake8 after report
means no findings; its run exited successfully with code 0. No tool rules
were disabled. Versions used: Pylint 4.1.3, Bandit 1.9.4 and Flake8 7.4.1.

The before reports analyze the original assigned script. The after reports
analyze the cleaned script, which remains available in the
[implementation commit](https://github.com/ibrahimmaq14/SE-Labs-PES1UG24CS578/blob/71e1ddc6f1da7b3310a2ab1d00403244d1a69a12/LAB5/digital_wallet.py).
The three earlier commits retain the security, Pylint and Flake8 fixes.
