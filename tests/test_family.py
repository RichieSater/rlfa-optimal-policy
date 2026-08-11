from fractions import Fraction

import pytest

from rlfa_optimal_policy.confidence import ReleasedApproxKellyLogicalN2
from rlfa_optimal_policy.dp import expected_audit_length
from rlfa_optimal_policy.model import AuditInstance
from rlfa_optimal_policy.policies import OracleContributionPolicy, ProportionalValuePolicy


@pytest.mark.parametrize("p", [Fraction(2, 3), Fraction(3, 4), Fraction(4, 5), Fraction(9, 10)])
def test_parametric_counterexample_family(p: Fraction) -> None:
    instance = AuditInstance.from_values(
        (p, 1 - p), ((1 - p) / p, 1), Fraction(1, 2), Fraction(1, 20)
    )
    rule = ReleasedApproxKellyLogicalN2()

    oracle_value = expected_audit_length(instance, OracleContributionPolicy(), rule)
    prop_m_value = expected_audit_length(instance, ProportionalValuePolicy(), rule)

    assert oracle_value == Fraction(3, 2)
    assert prop_m_value == 2 - p
    assert oracle_value - prop_m_value == p - Fraction(1, 2)
    assert prop_m_value < oracle_value
