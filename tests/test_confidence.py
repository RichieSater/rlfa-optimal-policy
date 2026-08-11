from fractions import Fraction

from rlfa_optimal_policy.confidence import (
    ReleasedApproxKellyLogicalN2,
    first_round_betting_interval,
    first_round_combined_interval,
    released_approx_kelly_initial_bet,
)
from rlfa_optimal_policy.counterexample import COUNTEREXAMPLE


def test_first_bet_is_zero_and_betting_cs_is_unit_interval() -> None:
    assert released_approx_kelly_initial_bet() == 0
    interval = first_round_betting_interval(COUNTEREXAMPLE)
    assert interval.lower == 0
    assert interval.upper == 1


def test_first_round_stop_is_driven_by_remaining_weight() -> None:
    high_value_first = first_round_combined_interval(COUNTEREXAMPLE, 0)
    low_value_first = first_round_combined_interval(COUNTEREXAMPLE, 1)
    rule = ReleasedApproxKellyLogicalN2()

    assert high_value_first.diameter == Fraction(1, 4)
    assert low_value_first.diameter == Fraction(3, 4)
    assert rule.stops(COUNTEREXAMPLE, (0,))
    assert not rule.stops(COUNTEREXAMPLE, (1,))
    assert rule.stops(COUNTEREXAMPLE, (1, 0))
