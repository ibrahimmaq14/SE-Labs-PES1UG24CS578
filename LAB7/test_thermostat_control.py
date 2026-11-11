"""Run: python -m pytest test_thermostat_control.py -v

Requires pytest and hypothesis. Invalid inputs must return None; valid
inputs must produce finite temperatures or normalized schedule labels.
"""

import math

import pytest
from hypothesis import example, given, settings, strategies as st
from thermostat_control import parse_setpoint, average_temperature, schedule_slot


INPUTS = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.binary(), st.lists(st.integers()), st.dictionaries(st.text(), st.integers()),
)
FUZZ = settings(max_examples=500, derandomize=True, deadline=None)


@FUZZ
@given(INPUTS)
@example(None)
@example("")
@example("nanC")
@example("21X")
def test_parse_setpoint_no_crash(value):
    result = parse_setpoint(value)
    assert result is None or (isinstance(result, float) and math.isfinite(result))
    if not isinstance(value, str):
        assert result is None


@FUZZ
@given(INPUTS)
@example(None)
@example("")
@example("1,,3")
@example("nan")
def test_average_temperature_no_crash(value):
    result = average_temperature(value)
    assert result is None or (isinstance(result, float) and math.isfinite(result))
    if not isinstance(value, str):
        assert result is None


@FUZZ
@given(INPUTS)
@example(None)
@example("")
@example("24:00")
@example("06:60")
def test_schedule_slot_no_crash(value):
    result = schedule_slot(value)
    assert result is None or isinstance(result, str)
    if result is not None:
        label, minute = result.split()
        assert label in {"day", "night"}
        assert 0 <= int(minute) <= 59
    if not isinstance(value, str):
        assert result is None


@FUZZ
@given(st.integers(-100000, 100000), st.sampled_from(["C", "c", "F", "f"]))
def test_setpoint_conversion(tenths, unit):
    value = tenths / 10
    expected = value if unit.upper() == "C" else (value - 32) * 5 / 9
    assert parse_setpoint(f"  {value}{unit}  ") == round(expected, 1)


@FUZZ
@given(st.lists(st.integers(-1000000, 1000000), min_size=1, max_size=100))
def test_average_matches_arithmetic_mean(values):
    csv = ", ".join(str(value) for value in values)
    result = average_temperature(csv)
    assert result == pytest.approx(sum(values) / len(values), abs=1e-9)
    assert min(values) - 1e-9 <= result <= max(values) + 1e-9
    assert average_temperature(",".join(str(value) for value in reversed(values))) == result


@FUZZ
@given(st.integers(0, 23), st.integers(0, 59))
def test_schedule_valid_times(hour, minute):
    expected = "night" if hour < 6 else "day"
    assert schedule_slot(f" {hour:02d}:{minute:02d} ") == f"{expected} {minute}"


@FUZZ
@given(st.integers(24, 99), st.integers(0, 59))
def test_schedule_rejects_out_of_range_hours(hour, minute):
    assert schedule_slot(f"{hour:02d}:{minute:02d}") is None


@FUZZ
@given(st.integers(0, 23), st.integers(60, 99))
def test_schedule_rejects_out_of_range_minutes(hour, minute):
    assert schedule_slot(f"{hour:02d}:{minute:02d}") is None


@pytest.mark.parametrize("text", [
    "", " ", "C", "21", "21X", "nanC", "infF", "-infC", "1e309C", "21CC",
])
def test_invalid_setpoints(text):
    assert parse_setpoint(text) is None


@pytest.mark.parametrize("text", [
    "", " ", ",", "1,,3", ",1", "1,", "one,two", "nan", "inf", "1e309,2",
])
def test_invalid_readings(text):
    assert average_temperature(text) is None


@pytest.mark.parametrize("text", [
    "", " ", "-1:00", "24:00", "06:60", "12:-1", "7:30", "07:3",
    "12:00:00", "ab:cd", "\u0660\u0667:30",
])
def test_invalid_times(text):
    assert schedule_slot(text) is None


@pytest.mark.parametrize("text, expected", [
    ("21.5C", 21.5), ("70F", 21.1), ("32F", 0.0), ("-40F", -40.0),
    (" 21.5c ", 21.5), ("1e308F", round(1e308 * (5 / 9), 1)),
])
def test_setpoint_regressions(text, expected):
    assert parse_setpoint(text) == expected


@pytest.mark.parametrize("text, expected", [
    ("20.5,21,22.5", 64 / 3), ("0", 0.0), ("-10,10", 0.0),
    ("1e308,1e308", 1e308), ("-1e308,1e308", 0.0),
    ("1e308,1,-1e308", 1 / 3),
    ("1.7976931348623157e308,1.7976931348623157e308", 1.7976931348623157e308),
    ("5e-324,5e-324,5e-324", 5e-324),
])
def test_average_regressions(text, expected):
    result = average_temperature(text)
    if 0 < abs(expected) < 1e-300:
        assert result == expected
    else:
        assert result == pytest.approx(expected)


@pytest.mark.parametrize("text, expected", [
    ("00:00", "night 0"), ("05:59", "night 59"), ("06:00", "day 0"),
    ("07:05", "day 5"), ("23:59", "day 59"),
])
def test_schedule_boundaries(text, expected):
    assert schedule_slot(text) == expected
