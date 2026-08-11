from fractions import Fraction

from rlfa_optimal_policy.approxkelly import (
    ApproxKellyConfig,
    evaluate_policy,
    initial_state,
    solve_action_mesh,
    transition,
)
from rlfa_optimal_policy.counterexample import COUNTEREXAMPLE
from rlfa_optimal_policy.logical import fixed_risk_oracle_gap_family
from rlfa_optimal_policy.model import AuditInstance
from rlfa_optimal_policy.policies import (
    OracleContributionPolicy,
    ProportionalValuePolicy,
)


def test_full_grid_evaluator_recovers_n2_certificate() -> None:
    config = ApproxKellyConfig(grid_size=13)
    assert evaluate_policy(COUNTEREXAMPLE, OracleContributionPolicy(), config) == Fraction(
        3, 2
    )
    assert evaluate_policy(COUNTEREXAMPLE, ProportionalValuePolicy(), config) == Fraction(
        5, 4
    )


def test_action_mesh_recovers_best_full_support_n2_action() -> None:
    result = solve_action_mesh(
        COUNTEREXAMPLE, action_denominator=4, config=ApproxKellyConfig(grid_size=13)
    )
    assert result.expected_length == Fraction(5, 4)
    assert result.initial_action == ((0, Fraction(3, 4)), (1, Fraction(1, 4)))


def test_fixed_risk_witnesses_survive_every_small_item_history() -> None:
    family = fixed_risk_oracle_gap_family(5, contribution_ratio="1/100")
    instance = family.instance
    config = ApproxKellyConfig(grid_size=family.witness_grid_size)
    policy = OracleContributionPolicy()
    state = initial_state(config)
    lower_witness, upper_witness = family.witness_candidates
    for sampled_index in range(1, instance.size):
        distribution = policy.probabilities(instance, state.history)
        state = transition(instance, state, distribution, sampled_index, config)
        assert state.combined_lower <= lower_witness
        assert state.combined_upper >= upper_witness
        assert state.diameter >= 2 * instance.epsilon


def test_n3_augmented_state_mesh_beats_both_comparators() -> None:
    instance = AuditInstance.from_values(
        weights=("1/2", "1/3", "1/6"),
        misstatements=("1/6", "1/4", "1"),
        epsilon="1/3",
        delta="1/20",
    )
    config = ApproxKellyConfig(grid_size=21)
    result = solve_action_mesh(instance, action_denominator=6, config=config)
    oracle = evaluate_policy(instance, OracleContributionPolicy(), config)
    prop_m = evaluate_policy(instance, ProportionalValuePolicy(), config)
    assert result.expected_length == Fraction(37, 18)
    assert result.expected_length < prop_m == Fraction(43, 20)
    assert prop_m < oracle == Fraction(29, 12)
    assert result.initial_action == (
        (0, Fraction(2, 3)),
        (1, Fraction(1, 6)),
        (2, Fraction(1, 6)),
    )
