from fractions import Fraction

import pytest

from rlfa_optimal_policy.model import AuditInstance


def test_counterexample_logical_intervals_are_exact() -> None:
    instance = AuditInstance.from_values(
        ("3/4", "1/4"), ("1/3", "1"), "1/3", "1/20"
    )

    assert instance.total_misstatement == Fraction(1, 2)
    assert instance.logical_interval((0,)).lower == Fraction(1, 4)
    assert instance.logical_interval((0,)).upper == Fraction(1, 2)
    assert instance.logical_interval((0,)).diameter == Fraction(1, 4)
    assert instance.logical_interval((1,)).lower == Fraction(1, 4)
    assert instance.logical_interval((1,)).upper == 1
    assert instance.logical_interval((1,)).diameter == Fraction(3, 4)
    assert instance.logical_interval((1, 0)).diameter == 0


def test_floats_are_rejected() -> None:
    with pytest.raises(TypeError, match="floating-point"):
        AuditInstance.from_values((0.75, "1/4"), ("1/3", "1"), "1/3", "1/20")


@pytest.mark.parametrize(
    "weights,misstatements,epsilon,delta",
    [
        (("1/2", "1/3"), ("0", "1"), "1/3", "1/20"),
        (("0", "1"), ("0", "1"), "1/3", "1/20"),
        (("1/2", "1/2"), ("0", "4/3"), "1/3", "1/20"),
        (("1/2", "1/2"), ("0", "1"), "1", "1/20"),
        (("1/2", "1/2"), ("0", "1"), "1/3", "0"),
    ],
)
def test_invalid_instances_are_rejected(weights, misstatements, epsilon, delta) -> None:
    with pytest.raises(ValueError):
        AuditInstance.from_values(weights, misstatements, epsilon, delta)
