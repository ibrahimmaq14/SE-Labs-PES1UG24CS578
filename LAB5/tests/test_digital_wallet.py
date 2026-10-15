"""Regression tests for the lab's wallet behavior and corrected defects."""

import contextlib
import io
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import unittest
from unittest.mock import patch

import digital_wallet as wallet


class WalletTests(unittest.TestCase):
    """Exercise successful operations, rejected operations and state safety."""

    def setUp(self):
        wallet.WALLET.update(balance=0.0, daily_limit=1000)
        wallet.TRANSACTIONS.clear()
        wallet.CREDENTIALS.clear()
        self.pin = str(secrets.randbelow(9000) + 1000)
        self.gateway_key = secrets.token_urlsafe(32)
        wallet.configure_credentials(self.pin, self.gateway_key)

    def pay(self, amount, pin=None):
        """Capture the demo's messages while returning a payment result."""
        with contextlib.redirect_stdout(io.StringIO()):
            return wallet.pay_merchant(
                "Test shop", amount, self.pin if pin is None else pin
            )

    def test_credit_updates_balance_transaction_and_supplied_log(self):
        log = []
        self.assertTrue(wallet.add_money(500, "Card", log))
        self.assertEqual(wallet.WALLET["balance"], 500)
        self.assertEqual(log, [500])
        self.assertEqual(wallet.TRANSACTIONS[0]["party"], "Card")

    def test_omitted_log_does_not_reuse_another_callers_log(self):
        log = []
        wallet.add_money(100, log=log)
        wallet.add_money(50)
        self.assertEqual(log, [100])
        self.assertEqual(wallet.add_money.__defaults__, ("UPI", None))

    def test_invalid_credits_do_not_mutate_state(self):
        for amount in (-10, 0, float("nan"), float("inf"), True, "50"):
            with self.subTest(amount=amount):
                self.assertFalse(wallet.add_money(amount))
                self.assertEqual(wallet.WALLET["balance"], 0)
                self.assertEqual(wallet.TRANSACTIONS, [])

    def test_valid_payment_debits_and_records(self):
        wallet.add_money(500)
        self.assertTrue(self.pay(180))
        self.assertEqual(wallet.WALLET["balance"], 320)
        self.assertEqual(wallet.TRANSACTIONS[-1]["type"], "debit")

    def test_wrong_pin_leaves_state_unchanged(self):
        wallet.add_money(500)
        self.assertFalse(self.pay(100, pin=""))
        self.assertEqual(wallet.WALLET["balance"], 500)
        self.assertEqual(len(wallet.TRANSACTIONS), 1)

    def test_insufficient_funds_and_limit_are_independent(self):
        wallet.add_money(2000)
        self.assertFalse(self.pay(1001))
        wallet.set_daily_limit(3000)
        self.assertFalse(self.pay(2001))
        self.assertEqual(wallet.WALLET["balance"], 2000)
        self.assertEqual(len(wallet.TRANSACTIONS), 1)

    def test_payment_at_exact_balance_and_limit_succeeds(self):
        wallet.add_money(1000)
        self.assertTrue(self.pay(1000))
        self.assertEqual(wallet.WALLET["balance"], 0)

    def test_invalid_debits_never_credit_the_wallet(self):
        wallet.add_money(500)
        for amount in (-10, 0, float("nan"), float("inf"), True, "50"):
            with self.subTest(amount=amount):
                self.assertFalse(self.pay(amount))
                self.assertEqual(wallet.WALLET["balance"], 500)
                self.assertEqual(len(wallet.TRANSACTIONS), 1)

    def test_invalid_limits_leave_previous_limit(self):
        for amount in (-1, 0, float("nan"), float("inf"), True, "50"):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    wallet.set_daily_limit(amount)
                self.assertEqual(wallet.WALLET["daily_limit"], 1000)

    def test_gateway_rejects_wrong_missing_and_unconfigured_keys(self):
        self.assertTrue(wallet.check_gateway(self.gateway_key))
        self.assertFalse(wallet.check_gateway(""))
        self.assertFalse(wallet.check_gateway(None))
        wallet.CREDENTIALS.clear()
        self.assertFalse(wallet.check_gateway(self.gateway_key))
        self.assertFalse(self.pay(100))

    def test_same_pin_receives_fresh_salt_and_verifier(self):
        old_salt = wallet.CREDENTIALS["salt"]
        old_hash = wallet.CREDENTIALS["pin_hash"]
        wallet.configure_credentials(self.pin, self.gateway_key)
        self.assertNotEqual(old_salt, wallet.CREDENTIALS["salt"])
        self.assertNotEqual(old_hash, wallet.CREDENTIALS["pin_hash"])
        self.assertNotIn(self.pin, wallet.CREDENTIALS.values())

    def test_invalid_configuration_is_rejected_atomically(self):
        previous = wallet.CREDENTIALS.copy()
        for pin in ("", "abcde", "123", "1234567", "１２３４", None):
            with self.subTest(pin=pin):
                with self.assertRaises(ValueError):
                    wallet.configure_credentials(pin, self.gateway_key)
                self.assertEqual(wallet.CREDENTIALS, previous)
        with self.assertRaises(ValueError):
            wallet.configure_credentials(self.pin, "")
        self.assertEqual(wallet.CREDENTIALS, previous)

    def test_receipt_files_exist_are_distinct_and_can_be_deleted(self):
        first = Path(wallet.receipt_path())
        second = Path(wallet.receipt_path())
        self.addCleanup(first.unlink, missing_ok=True)
        self.addCleanup(second.unlink, missing_ok=True)
        self.assertNotEqual(first, second)
        self.assertTrue(first.is_file())
        self.assertTrue(second.is_file())
        self.assertEqual(first.read_bytes(), b"")
        self.assertEqual(first.suffix, ".pdf")

    def test_mini_statement_and_zero_count(self):
        wallet.add_money(100, "UPI")
        wallet.add_money(50, "Card")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            wallet.mini_statement(1)
        self.assertEqual(output.getvalue(), "credit 50 Card\n")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            wallet.mini_statement(0)
        self.assertEqual(output.getvalue(), "")
        with self.assertRaises(ValueError):
            wallet.mini_statement(-1)

    def test_cashback_preserves_flat_rate_and_validates_inputs(self):
        self.assertEqual(wallet.cashback_for(420, "health"), 8.4)
        self.assertEqual(wallet.cashback_for(100, "food"), 2)
        with self.assertRaises(ValueError):
            wallet.cashback_for(-100, "food")
        with self.assertRaises(ValueError):
            wallet.cashback_for(100, "")

    def test_otp_has_six_digits(self):
        for _ in range(20):
            self.assertRegex(str(wallet.generate_otp()), r"^[1-9][0-9]{5}$")

    def test_import_has_no_demo_output_or_wallet_mutations(self):
        result = subprocess.run(
            [sys.executable, "-c", "import digital_wallet as w; "
             "print(w.WALLET['balance'], len(w.TRANSACTIONS), "
             "len(w.CREDENTIALS))"],
            cwd=Path(wallet.__file__).parent,
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(result.stdout, "0.0 0 0\n")

    def test_demo_matches_original_except_random_otp_and_is_repeatable(self):
        baseline_path = (
            Path(wallet.__file__).parent / "reports/before/program_output.txt"
        )
        expected = baseline_path.read_text(encoding="utf-8").splitlines()[1:]
        for _ in range(2):
            output = io.StringIO()
            with patch.dict(os.environ, {}, clear=True):
                with contextlib.redirect_stdout(output):
                    wallet.main()
            lines = output.getvalue().splitlines()
            self.assertTrue(re.fullmatch(r"OTP sent: [1-9][0-9]{5}", lines[0]))
            self.assertEqual(lines[1:], expected)


if __name__ == "__main__":
    unittest.main()
