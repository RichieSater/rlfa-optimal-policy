from fractions import Fraction
from itertools import permutations

from rlfa_optimal_policy.dp import expected_audit_length
from rlfa_optimal_policy.logical import (
    LogicalStoppingRule,
    expected_plackett_luce_rank,
    fixed_risk_oracle_gap_family,
    oracle_gap_family,
    solve_logical_unit_cost,
)
from rlfa_optimal_policy.model import AuditInstance
from rlfa_optimal_policy.policies import FixedPriorityPolicy, OracleContributionPolicy


def test_arbitrary_n_logical_optimum_matches_all_permutations() -> None:
    instance = AuditInstance.from_values(
        weights=("5/12", "1/4", "1/6", "1/6"),
        misstatements=("1/5", "2/5", "3/5", "4/5"),
        epsilon="1/4",
        delta="1/20",
    )
    solution = solve_logical_unit_cost(instance)
    assert solution.cover_number == 3
    brute_force = min(
        next(
            t
            for t in range(1, instance.size + 1)
            if sum((instance.weights[index] for index in order[:t]), Fraction(0))
            >= 1 - instance.epsilon
        )
        for order in permutations(range(instance.size))
    )
    assert solution.cover_number == brute_force


def test_priority_policy_attains_general_logical_optimum() -> None:
    instance = AuditInstance.from_values(
        weights=("1/2", "1/3", "1/6"),
        misstatements=("1/2", "1/2", "1/2"),
        epsilon="1/3",
        delta="1/20",
    )
    policy = FixedPriorityPolicy(instance.weights, "descending-pi")
    expectation = expected_audit_length(
        instance, policy, LogicalStoppingRule(), support_mode="simplex"
    )
    assert expectation == solve_logical_unit_cost(instance).cover_number == 2


def test_plackett_luce_rank_formula() -> None:
    rates = (Fraction(1), Fraction(2), Fraction(3))
    assert expected_plackett_luce_rank(rates, 0) == Fraction(29, 12)


def test_oracle_gap_family_equal_contributions() -> None:
    family = oracle_gap_family(9, contribution_ratio=1)
    assert len(set(family.instance.contribution(i) for i in range(9))) == 1
    assert family.oracle_expected_length == 5
    assert family.literal_simplex_optimum == 1
    assert family.prop_m_expected_length == Fraction(33, 25)
    # For equal contributions the exact logical enumeration agrees with rank.
    expectation = expected_audit_length(
        family.instance,
        OracleContributionPolicy(),
        LogicalStoppingRule(),
        support_mode="full",
    )
    assert expectation == family.oracle_expected_length


def test_oracle_ratio_approaches_sharp_horizon_bound() -> None:
    size = 20
    family = oracle_gap_family(size, contribution_ratio="1/1000")
    assert family.oracle_expected_length == 1 + Fraction(size - 1, 1 + Fraction(1, 1000))
    assert family.oracle_expected_length > Fraction(199, 200) * size
    assert family.uniform_wealth_bound < 1 / family.instance.delta


def test_fixed_risk_family_has_two_surviving_grid_witnesses() -> None:
    size = 50
    family = fixed_risk_oracle_gap_family(size, contribution_ratio="1/1000")
    instance = family.instance
    lower, upper = family.witness_candidates
    grid_denominator = family.witness_grid_size - 1
    assert lower * grid_denominator == 1
    assert upper * grid_denominator == 5
    assert upper - lower == family.witness_separation == 2 * instance.epsilon
    assert family.candidate_wealth_bound < 2 < 1 / instance.delta
    assert family.oracle_expected_length > Fraction(999, 1000) * size
    assert family.prop_m_rank_upper_bound < Fraction(101, 100)
