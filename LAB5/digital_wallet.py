import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

credentials = {}
wallet = {"balance": 0.0}
daily_limit = 1000
transactions = []


def hashPin(pin):
    return hashlib.pbkdf2_hmac(
        "sha256", pin.encode(), credentials["salt"], 600_000
    )


def configureCredentials(pin, gatewaySecret):
    credentials["salt"] = secrets.token_bytes(16)
    credentials["pin_hash"] = hashPin(pin)
    credentials["gateway_secret"] = gatewaySecret.encode()


def addMoney(amount, source="UPI", log=[]):
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({"type": "credit", "amount": amount, "party": source,
                         "time": datetime.now().isoformat()})
    log.append(amount)
    return True


def setDailyLimit(newLimit):
    global daily_limit
    daily_limit = newLimit


def payMerchant(merchant, amount, pin):
    if not credentials or not hmac.compare_digest(
            hashPin(pin), credentials["pin_hash"]):
        print("Wrong PIN for payment to", merchant)
        return False
    if amount > wallet["balance"] or amount > daily_limit:
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({"type": "debit", "amount": amount, "party": merchant,
                         "time": datetime.now().isoformat()})
    return True


def miniStatement(count=3):
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashbackFor(amount, merchantType):
    return round(amount * 0.02, 2)


def checkGateway(secret):
    return bool(credentials) and hmac.compare_digest(
        secret.encode(), credentials["gateway_secret"]
    )


def receiptPath():
    # Helper kept for the lab: not called by the demo
    descriptor, path = tempfile.mkstemp(suffix=".pdf")
    os.close(descriptor)
    return path


def main():
    pin = os.environ.get("WALLET_PIN") or str(secrets.randbelow(9000) + 1000)
    gateway_secret = (
        os.environ.get("GATEWAY_SECRET") or secrets.token_urlsafe(32)
    )
    configureCredentials(pin, gateway_secret)
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)
    addMoney(2000)
    addMoney(500, "Card")
    addMoney(-10)
    setDailyLimit(1500)
    payMerchant("Coffee Corner", 180, pin)
    payMerchant("Book Store", 5000, pin)
    payMerchant("Grocery Mart", 350, "")
    payMerchant("Pharmacy", 420, pin)
    miniStatement()
    print("Cashback on 420:", cashbackFor(420, "health"))
    print("Gateway check:", checkGateway("wrong")) # should be False
    print("Final balance: Rs.", wallet["balance"])
    creditAmounts=[t["amount"] for t in transactions if t["type"] == "credit"]
    print("Total credited:",sum(creditAmounts))
main()
