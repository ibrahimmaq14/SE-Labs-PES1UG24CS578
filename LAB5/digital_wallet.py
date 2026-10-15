"""Digital-wallet lab demo with explicit credentials and validated payments.

State is in memory. The historical daily limit applies to each payment.
Running the module uses environment credentials or generates ephemeral ones.
"""

import hashlib
import hmac
import math
import os
import secrets
import tempfile
from datetime import datetime

CREDENTIALS = {}
WALLET = {"balance": 0.0, "daily_limit": 1000}
TRANSACTIONS = []
PIN_ITERATIONS = 600_000


def hash_pin(pin, salt):
    """Derive a PIN verifier using a random salt and PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac(
        "sha256", pin.encode(), salt, PIN_ITERATIONS
    )


def configure_credentials(pin, gateway_secret):
    """Configure a 4-6 digit PIN and a nonempty gateway key in memory."""
    if (not isinstance(pin, str) or not pin.isascii()
            or not pin.isdigit() or not 4 <= len(pin) <= 6):
        raise ValueError("PIN must contain 4-6 ASCII digits")
    if not isinstance(gateway_secret, str) or not gateway_secret:
        raise ValueError("Gateway key must be a nonempty string")
    salt = secrets.token_bytes(16)
    CREDENTIALS.update(
        salt=salt,
        pin_hash=hash_pin(pin, salt),
        gateway_secret=gateway_secret.encode(),
    )


def _is_positive_amount(amount):
    """Reject nonnumeric, nonfinite, zero and negative payment values."""
    return (isinstance(amount, (int, float))
            and not isinstance(amount, bool)
            and math.isfinite(amount) and amount > 0)


def add_money(amount, source="UPI", log=None):
    """Credit a positive finite amount, optionally recording a caller log."""
    if not _is_positive_amount(amount):
        return False
    if log is None:
        log = []
    WALLET["balance"] += amount
    TRANSACTIONS.append({
        "type": "credit", "amount": amount, "party": source,
        "time": datetime.now().isoformat(),
    })
    log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Set a positive per-payment cap, retaining the original lab behavior."""
    if not _is_positive_amount(new_limit):
        raise ValueError("Limit must be a positive finite number")
    WALLET["daily_limit"] = new_limit


def pay_merchant(merchant, amount, pin):
    """Debit only after checking the amount, PIN, funds and payment cap."""
    if not _is_positive_amount(amount):
        return False
    if (not CREDENTIALS or not isinstance(pin, str)
            or not hmac.compare_digest(
                hash_pin(pin, CREDENTIALS["salt"]),
                CREDENTIALS["pin_hash"],
            )):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > WALLET["balance"] or amount > WALLET["daily_limit"]:
        print("Payment to", merchant, "declined")
        return False
    WALLET["balance"] -= amount
    TRANSACTIONS.append({
        "type": "debit", "amount": amount, "party": merchant,
        "time": datetime.now().isoformat(),
    })
    return True


def mini_statement(count=3):
    """Print the latest count entries; a zero count produces no output."""
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise ValueError("Statement count must be a nonnegative integer")
    if count == 0:
        return
    for entry in TRANSACTIONS[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount, merchant_type):
    """Return the demo's flat 2 percent cashback for a named category."""
    if not _is_positive_amount(amount):
        raise ValueError("Cashback amount must be a positive finite number")
    if not isinstance(merchant_type, str) or not merchant_type.strip():
        raise ValueError("Merchant category must be a nonempty string")
    return round(amount * 0.02, 2)


def check_gateway(secret):
    """Compare an offered key with the configured key in constant time."""
    return (
        bool(CREDENTIALS) and isinstance(secret, str)
        and hmac.compare_digest(
            secret.encode(), CREDENTIALS["gateway_secret"]
        )
    )


def receipt_path():
    """Create an empty receipt file securely; the caller must delete it."""
    descriptor, path = tempfile.mkstemp(suffix=".pdf")
    os.close(descriptor)
    return path


def generate_otp():
    """Return a six-digit OTP generated with operating-system randomness."""
    return secrets.randbelow(900000) + 100000


def main():
    """Run the original demonstration with fresh in-memory wallet state."""
    pin = os.environ.get("WALLET_PIN") or str(secrets.randbelow(9000) + 1000)
    gateway_secret = (
        os.environ.get("GATEWAY_SECRET") or secrets.token_urlsafe(32)
    )
    configure_credentials(pin, gateway_secret)
    WALLET.update(balance=0.0, daily_limit=1000)
    TRANSACTIONS.clear()
    # This is a local demo; a real OTP must be delivered privately.
    print("OTP sent:", generate_otp())
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, pin)
    pay_merchant("Book Store", 5000, pin)
    pay_merchant("Grocery Mart", 350, "")
    pay_merchant("Pharmacy", 420, pin)
    mini_statement()
    print("Cashback on 420:", cashback_for(420, "health"))
    print("Gateway check:", check_gateway("wrong"))  # should be False
    print("Final balance: Rs.", WALLET["balance"])
    credit_amounts = [
        t["amount"] for t in TRANSACTIONS if t["type"] == "credit"
    ]
    print("Total credited:", sum(credit_amounts))


if __name__ == "__main__":
    main()
