from fractions import Fraction

import pytest

from rlfa_optimal_policy.confidence import ReleasedApproxKellyLogicalN2
from rlfa_optimal_policy.counterexample import COUNTEREXAMPLE
from rlfa_optimal_policy.dp import enumerate_terminal_paths, expected_audit_length
from rlfa_optimal_policy.model import AuditInstance
from rlfa_optimal_policy.n2 import characterize_n2, expected_length_from_first_distribution
from rlfa_optimal_policy.policies import FixedFirstDistributionPolicy


def test_counterexample_has_exact_unrestricted_optimum_one() -> None:
    result = characterize_n2(COUNTEREXAMPLE)

    assert result.stopping_items == (0,)
    assert result.nonstopping_items == (1,)
    assert result.optimal_value == 1
    assert result.unrestricted_attained
    assert result.full_support_infimum == 1
    assert not result.full_support_attained
    assert result.importance_support_infimum == 1
    assert not result.importance_support_attained
    assert result.oracle_defined
    assert result.oracle_expected_length == Fraction(3, 2)
    assert not result.oracle_is_globally_optimal


def test_deterministic_large_item_policy_stops_with_certainty() -> None:
    policy = FixedFirstDistributionPolicy.from_values((1, 0), "large-item-first")
    rule = ReleasedApproxKellyLogicalN2()

    assert (
        expected_audit_length(
            COUNTEREXAMPLE, policy, rule, support_mode="simplex"
        )
        == 1
    )
    paths = enumerate_terminal_paths(
        COUNTEREXAMPLE, policy, rule, support_mode="simplex"
    )
    assert [(path.history, path.probability, path.stopping_time) for path in paths] == [
        ((0,), Fraction(1), 1)
    ]


def test_deterministic_policy_fails_conservative_support_checks() -> None:
    policy = FixedFirstDistributionPolicy.from_values((1, 0), "large-item-first")
    rule = ReleasedApproxKellyLogicalN2()

    with pytest.raises(ValueError, match="positive-contribution"):
        expected_audit_length(COUNTEREXAMPLE, policy, rule)
    with pytest.raises(ValueError, match="full support"):
        expected_audit_length(COUNTEREXAMPLE, policy, rule, support_mode="full")


def test_eta_policies_approach_the_full_support_infimum() -> None:
    eta = Fraction(1, 100)
    policy = FixedFirstDistributionPolicy.from_values((1 - eta, eta), "eta-policy")
    rule = ReleasedApproxKellyLogicalN2()

    value = expected_audit_length(
        COUNTEREXAMPLE, policy, rule, support_mode="full"
    )
    assert value == 1 + eta


def test_no_first_round_stopping_makes_every_policy_optimal() -> None:
    instance = AuditInstance.from_values(
        ("3/5", "2/5"), ("1/2", "1"), "1/3", "1/20"
    )
    result = characterize_n2(instance)

    assert result.stopping_items == ()
    assert result.optimal_value == 2
    assert result.full_support_attained
    assert result.importance_support_attained
    assert result.oracle_is_globally_optimal
    assert expected_length_from_first_distribution(instance, {0: Fraction(1), 1: Fraction(0)}) == 2


def test_both_items_stopping_makes_every_policy_optimal() -> None:
    instance = AuditInstance.from_values(
        ("1/2", "1/2"), ("1/2", "1"), "3/5", "1/20"
    )
    result = characterize_n2(instance)

    assert result.stopping_items == (0, 1)
    assert result.optimal_value == 1
    assert result.full_support_attained
    assert result.importance_support_attained
    assert result.oracle_is_globally_optimal
    assert expected_length_from_first_distribution(instance, {0: Fraction(1), 1: Fraction(0)}) == 1


def test_importance_support_can_attain_boundary_when_nonstop_contribution_is_zero() -> None:
    instance = AuditInstance.from_values(
        ("3/4", "1/4"), ("1", "0"), "1/3", "1/20"
    )
    result = characterize_n2(instance)

    assert result.stopping_items == (0,)
    assert result.importance_support_attained
    assert result.oracle_expected_length == 1
    assert result.oracle_is_globally_optimal


def test_zero_total_leaves_the_proportional_oracle_undefined() -> None:
    instance = AuditInstance.from_values(
        ("3/4", "1/4"), ("0", "0"), "1/3", "1/20"
    )
    result = characterize_n2(instance)

    assert not result.oracle_defined
    assert result.oracle_expected_length is None
    assert result.oracle_is_globally_optimal is None
