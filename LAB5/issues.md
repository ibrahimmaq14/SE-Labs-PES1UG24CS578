# Identified issues and fixes

Line numbers refer to the unchanged `original/digital_wallet.py`. Bandit
severity labels below are copied from the actual report, with high and medium
first. Priority for the other tools is an assessment for this lab; Pylint and
Flake8 do not use Bandit's severity scheme.

| Issue | Type | Line(s) | Description | Fix Approach |
| --- | --- | --- | --- | --- |
| B324 - weak PIN hash | Bandit: High | 14 | SHA-1 hashes the PIN directly without salt or a work factor. | Replace with PBKDF2-HMAC-SHA256, 600,000 iterations, a fresh 16-byte random salt and a stored in-memory verifier. Compare verifiers with `hmac.compare_digest`. |
| B306 - unsafe receipt filename | Bandit: Medium | 60 | `tempfile.mktemp` returns a name without atomically creating a file, allowing a race. | Use `mkstemp`, close the returned descriptor, and document caller cleanup. Test that distinct empty files actually exist. |
| B105 - embedded gateway key | Bandit: Low | 6 | A gateway secret is embedded in source. | Configure credentials explicitly. The demo reads environment values or generates ephemeral random credentials; remove the literal key. Also remove the embedded PIN at line 7 and successful-payment PIN literals at 70-73 as related manual hardening. |
| B311 - predictable OTP source | Bandit: Low | 64 | `random.randint` is not intended for security tokens. | Use `secrets.randbelow(900000) + 100000`; the OTP remains six digits. |
| W0102 - mutable default argument | Pylint: correctness priority | 17, 23 | The same default log list is reused on calls that omit the argument. | Use `log=None` and create a fresh list inside the function; keep caller-provided logs working. |
| W0603 - global rebinding | Pylint: maintainability priority | 28-29 | Updating the limit rebinds a module global. | Store balance and limit in the explicit `WALLET` state dictionary, so the function needs no `global` statement. |
| W0613 - unused category argument | Pylint: maintainability priority | 50 | `merchantType` is accepted but ignored. | Rename it to `merchant_type` and validate that it is a nonempty category; preserve the documented flat 2% rate for every category. |
| C0103 - naming conventions | Pylint: convention | 9, 13, 17, 27, 32, 45, 50, 54, 58, 78 | Mixed camelCase names and a lowercase limit constant reduce consistency. | Use snake_case function/argument/local names and uppercase names for module state containers and constants. |
| C0114 / C0116 - missing documentation | Pylint: convention | 1, 13, 17, 27, 32, 45, 50, 54, 58, 63 | The module and its functions have no docstrings. | Document the demo, state model, validation, credential handling and receipt cleanup. |
| E261 - inline comment spacing | Flake8: style | 76 | Only one space precedes the inline comment. | Insert the required two spaces. |
| E225 - assignment spacing | Flake8: style | 78 | Assignment has no surrounding spaces. | Format the assignment with spaces and wrap the comprehension. |
| E231 - comma spacing | Flake8: style | 79 | The print call omits a space after a comma. | Add the required space. |
| E305 - missing blank lines | Flake8: style | 80 | A module-level call immediately follows the function definition. | Separate top-level blocks with two blank lines and use an `if __name__ == "__main__"` guard. |

## Additional defects found by inspection

These were not reported by the baseline tools and are not counted as tool
findings. Regression tests cover them because fixing warnings alone does not
prove behavior is correct.

| Issue | Type | Line(s) | Description | Fix Approach |
| --- | --- | --- | --- | --- |
| Negative/nonfinite payments | Manual correctness review | 35-39 | A negative debit increases the balance; NaN can bypass comparisons and poison state. | Reject zero, negative, nonfinite, boolean and nonnumeric payment amounts before authentication or mutation. Apply the same validation to credits and limits. |
| Invalid limit | Manual correctness review | 27-29 | Any value can replace the cap. | Require a positive finite number and raise `ValueError` before changing the previous cap. |
| Zero statement count | Manual correctness review | 45-46 | `transactions[-0:]` prints the entire history. | Return without output for count 0 and reject invalid counts. |
| Import side effects | Manual maintainability review | 80 | Importing the module runs payments and prints an OTP. | Guard the demo entry point; reset state when explicitly rerunning the demo. |

## Verification

- Before: 25 Pylint messages, score 5.69/10; 4 Bandit findings; 4 Flake8 findings.
- After: Pylint 10.00/10, no messages; Bandit 0 findings; Flake8 0 findings.
- All 18 regression tests pass. The demo's output after the OTP line matches
  the original, including Rs. 1900.0 balance and Rs. 2500 credited.
- Raw tool outputs and exit codes are under `reports/before/` and
  `reports/after/`; the original source is retained to make line references
  and reported findings independently checkable.

## References

- [Python hashlib: password key derivation](https://docs.python.org/3/library/hashlib.html#key-derivation)
- [Python secrets: secure token generation](https://docs.python.org/3/library/secrets.html)
- [Python tempfile: securely creating temporary files](https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp)
- Bandit's saved baseline report includes rule-specific documentation URLs.
