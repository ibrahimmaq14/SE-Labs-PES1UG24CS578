"""Branch and boundary tests, extending the first code coverage suite."""

import pytest

from thermostat_control import energy_alert, hvac_action, target_temperature


@pytest.mark.parametrize(
    "mode, occupied, hour, expected",
    [
        ("away", True, 12, 16),
        ("away", False, 23, 16),
        ("sleep", True, 0, 18),
        ("sleep", True, 5, 18),
        ("sleep", True, 6, 20),
        ("sleep", False, 12, 20),
        ("sleep", True, 21, 20),
        ("sleep", True, 22, 18),
        ("sleep", True, 23, 18),
        ("home", False, 7, 18),
        ("home", False, 18, 18),
        ("home", True, 0, 20),
        ("home", True, 5, 20),
        ("home", True, 6, 22),
        ("home", True, 7, 22),
        ("home", True, 8, 22),
        ("home", True, 9, 20),
        ("home", True, 12, 20),
        ("home", True, 16, 20),
        ("home", True, 17, 21),
        ("home", True, 18, 21),
        ("home", True, 21, 21),
        ("home", True, 22, 20),
        ("home", True, 23, 20),
    ],
)
def test_temperature_branches_and_hour_boundaries(mode, occupied, hour, expected):
    assert target_temperature(mode, occupied, hour) == expected


@pytest.mark.parametrize(
    "current, target, outside, expected",
    [
        (20, 20, 15, "idle"),
        (20, 20.5, 15, "idle"),
        (20, 20.99, 0, "idle"),
        (20, 19.01, 35, "idle"),
        (20, 19.5, 15, "idle"),
        (20, 21, 4.99, "heat_boost"),
        (20, 21, 5, "heat"),
        (18, 22, 10, "heat"),
        (18, 22, -5, "heat_boost"),
        (20, 19, 30.01, "cool_boost"),
        (20, 19, 30, "cool"),
        (24, 20, 25, "cool"),
        (24, 20, 35, "cool_boost"),
    ],
)
def test_hvac_branches_and_threshold_boundaries(current, target, outside, expected):
    assert hvac_action(current, target, outside) == expected


@pytest.mark.parametrize(
    "readings, limit, expected",
    [
        ([], 10, "ok"),
        ([2, 10], 10, "ok"),
        ([10], 10, "ok"),
        ([11], 10, "critical"),
        ([11, 5], 10, "warning"),
        ([11, 12, 5], 10, "critical"),
        ([11, 5, 6], 10, "warning"),
        ([11, 12, 5, 6], 10, "warning"),
        ([11, 12, 13, 5], 10, "critical"),
        ([11, 12, 13], 10, "critical"),
        ([0, 0], 0, "ok"),
        ([0.1, 0], 0, "warning"),
    ],
)
def test_energy_branches_and_majority_boundaries(readings, limit, expected):
    assert energy_alert(readings, limit) == expected


def test_energy_readings_are_not_modified():
    readings = [11, 5, 6]
    assert energy_alert(readings, 10) == "warning"
    assert readings == [11, 5, 6]
