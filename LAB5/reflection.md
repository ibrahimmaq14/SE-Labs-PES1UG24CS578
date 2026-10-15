# Reflection

The attached three-page handout has no explicit reflection questions. The
assigned README requests four answers, so the following four questions were
chosen from the lab objectives with the user's approval. They are not presented
as quotations from the handout.

## 1. What did each tool contribute, and why use all three?

Pylint found code-quality and maintainability issues: the shared default log,
global rebinding, unused category argument, inconsistent names and missing
docstrings. Bandit highlighted security-sensitive APIs and data: SHA-1 PIN
hashing, a hardcoded gateway key, an unsafe temporary filename and an OTP
generated with `random`. Flake8 found spacing and top-level layout defects.
Their scopes overlap but complement one another. A good formatting result
would not have shown that the PIN hashing or temporary-file handling was
unsafe, while a clean Bandit run would not have fixed the shared list.

## 2. How were findings prioritized, and what did the fixes change?

The first priority was the high-severity B324 PIN hash finding, followed by
medium-severity B306 temporary-file creation. I replaced direct SHA-1 with
salted PBKDF2-HMAC-SHA256, and `mktemp` with atomic `mkstemp` creation. I then
addressed both low-severity Bandit findings by generating OTPs with `secrets`
and moving credentials out of source. The remaining work corrected the
mutable log default and other Pylint issues before normalizing Flake8
formatting. Bandit's severity was used as reported; the low rating of the
embedded demo key does not mean real embedded credentials are acceptable.

## 3. How was correctness checked, and what did static analysis miss?

I saved the original output and all three reports before changing the code.
Afterwards, Pylint improved from 5.69/10 to 10.00/10, all four Bandit findings
were removed and Flake8 produced no findings. Eighteen regression tests
checked the original demonstration, payment rejection, limits, credential
validation, isolated logs, receipt-file creation and import behavior. The
demo still prints the same results after the randomly generated OTP line.
Manual inspection also found negative-debit and NaN bugs that the tools did
not report. Testing those boundaries showed why static analysis must be
combined with code review and execution tests.

## 4. How does this improve maintainability, and what are the limits?

Clear names and docstrings make the wallet easier to explain and modify.
Explicit state and credential setup make behavior more predictable, while
tests catch regressions when the implementation changes. I would run these
tools before commits or in continuous integration and review new findings
instead of suppressing them just to improve a score. A clean report remains
limited to the rules and paths analyzed: this demo still uses in-memory
state, a per-payment cap rather than cumulative daily accounting, numeric
money values inherited from the source and console OTP output. Production
work would require persistent transactions, exact currency accounting,
rate-limited authentication and private OTP delivery. The lab establishes a
repeatable quality-checking process rather than proof of complete security.
