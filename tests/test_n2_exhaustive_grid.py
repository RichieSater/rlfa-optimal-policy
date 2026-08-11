from fractions import Fraction

from rlfa_optimal_policy.confidence import ReleasedApproxKellyLogicalN2
from rlfa_optimal_policy.dp import expected_audit_length
from rlfa_optimal_policy.model import AuditInstance
from rlfa_optimal_policy.n2 import characterize_n2, expected_length_from_first_distribution
from rlfa_optimal_policy.policies import FixedFirstDistributionPolicy


def test_complete_small_rational_grid_matches_closed_form() -> None:
    weights = [Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3)]
    values = [Fraction(0), Fraction(1, 2), Fraction(1)]
    epsilons = [Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(3, 4)]
    actions = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)]
    rule = ReleasedApproxKellyLogicalN2()

    for pi_1 in weights:
        for f_1 in values:
            for f_2 in values:
                for epsilon in epsilons:
                    instance = AuditInstance.from_values(
                        (pi_1, 1 - pi_1), (f_1, f_2), epsilon, Fraction(1, 20)
                    )
                    result = characterize_n2(instance)
                    action_values = []
                    for q_1 in actions:
                        distribution = {0: q_1, 1: 1 - q_1}
                        policy = FixedFirstDistributionPolicy.from_values(
                            (q_1, 1 - q_1)
                        )
                        closed_form = expected_length_from_first_distribution(
                            instance, distribution
                        )
                        dynamic_program = expected_audit_length(
                            instance, policy, rule, support_mode="simplex"
                        )
                        assert dynamic_program == closed_form
                        action_values.append(closed_form)
                    assert min(action_values) == result.optimal_value
