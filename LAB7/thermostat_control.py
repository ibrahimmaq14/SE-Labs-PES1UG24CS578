"""Smart thermostat input validation.

All public parsers return None for invalid input rather than raising.
Surrounding whitespace is ignored. Numeric inputs must be finite decimal
numbers (scientific notation is supported); no physical range is imposed.
"""

import math
import re
from statistics import mean


_NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def _finite_number(text):
    text = text.strip()
    if not _NUMBER.fullmatch(text):
        return None
    try:
        value = float(text)
    except (ValueError, OverflowError):
        return None
    return value if math.isfinite(value) else None


def parse_setpoint(text):
    """Parse a number followed by C/F (case insensitive), rounded to 0.1 C."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    if len(text) < 2 or text[-1].upper() not in {"C", "F"}:
        return None
    value = _finite_number(text[:-1])
    if value is None:
        return None
    if text[-1].upper() == "F":
        # Keep ordinary rounding behavior; scale first only if the product
        # would overflow for an otherwise finite Fahrenheit input.
        delta = value - 32
        value = delta * 5 / 9 if abs(delta) <= 1e307 else delta * (5 / 9)
    return round(value, 1) if math.isfinite(value) else None

def average_temperature(readings_csv):
    """Average nonempty CSV readings; reject the entire CSV if any is invalid."""
    if not isinstance(readings_csv, str):
        return None
    values = [_finite_number(token) for token in readings_csv.split(",")]
    if any(value is None for value in values):
        return None
    # statistics.mean uses an exact sum internally: avoid intermediate
    # overflow, cancellation and underflow from dividing each value first.
    result = mean(values)
    return result if math.isfinite(result) else None

def schedule_slot(time_text):
    """Parse ASCII HH:MM (00:00-23:59); night is before 06:00.

    Both labels use an unpadded integer minute, e.g. 'night 5', 'day 5'.
    """
    if not isinstance(time_text, str):
        return None
    time_text = time_text.strip()
    if not re.fullmatch(r"[0-9]{2}:[0-9]{2}", time_text):
        return None
    hour, minute = map(int, time_text.split(":"))
    if hour > 23 or minute > 59:
        return None
    return ("night" if hour < 6 else "day") + " " + str(minute)

def main():
    print("==== Running parse_setpoint ====")
    user_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    result = parse_setpoint(user_input)
    print("Setpoint in Celsius:", result if result is not None else "Invalid setpoint; use a finite number followed by C or F.")

    print("\n==== Running average_temperature ====")
    user_input = input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): ")
    result = average_temperature(user_input)
    print("Average Temperature:", result if result is not None else "Invalid readings; use nonempty CSV of finite numbers.")

    print("\n==== Running schedule_slot ====")
    user_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    result = schedule_slot(user_input)
    print("Schedule Slot:", result if result is not None else "Invalid time; use HH:MM from 00:00 to 23:59.")

if __name__ == "__main__":
    main()
