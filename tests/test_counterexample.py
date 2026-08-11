from fractions import Fraction

from rlfa_optimal_policy.confidence import ReleasedApproxKellyLogicalN2
from rlfa_optimal_policy.counterexample import COUNTEREXAMPLE, build_certificate
from rlfa_optimal_policy.dp import enumerate_terminal_paths, expected_audit_length
from rlfa_optimal_policy.policies import OracleContributionPolicy, ProportionalValuePolicy


def test_first_round_distributions() -> None:
    oracle = OracleContributionPolicy().probabilities(COUNTEREXAMPLE, ())
    prop_m = ProportionalValuePolicy().probabilities(COUNTEREXAMPLE, ())

    assert oracle == {0: Fraction(1, 2), 1: Fraction(1, 2)}
    assert prop_m == {0: Fraction(3, 4), 1: Fraction(1, 4)}


def test_exact_expected_stopping_times() -> None:
    rule = ReleasedApproxKellyLogicalN2()
    oracle_value = expected_audit_length(COUNTEREXAMPLE, OracleContributionPolicy(), rule)
    prop_m_value = expected_audit_length(COUNTEREXAMPLE, ProportionalValuePolicy(), rule)

    assert oracle_value == Fraction(3, 2)
    assert prop_m_value == Fraction(5, 4)
    assert prop_m_value < oracle_value
    assert oracle_value - prop_m_value == Fraction(1, 4)


def test_every_terminal_history_is_enumerated() -> None:
    rule = ReleasedApproxKellyLogicalN2()
    oracle_paths = enumerate_terminal_paths(COUNTEREXAMPLE, OracleContributionPolicy(), rule)
    prop_m_paths = enumerate_terminal_paths(COUNTEREXAMPLE, ProportionalValuePolicy(), rule)

    assert [(path.history, path.probability) for path in oracle_paths] == [
        ((0,), Fraction(1, 2)),
        ((1, 0), Fraction(1, 2)),
    ]
    assert [(path.history, path.probability) for path in prop_m_paths] == [
        ((0,), Fraction(3, 4)),
        ((1, 0), Fraction(1, 4)),
    ]


def test_certificate_contains_strict_exact_inequality() -> None:
    certificate = build_certificate()

    assert certificate["result"] == "counterexample"
    assert certificate["comparison"]["strict_inequality"] == "5/4 < 3/2"
    assert certificate["comparison"]["oracle_minus_prop_M"] == "1/4"
    assert certificate["comparison"]["prop_M_over_oracle"] == "5/6"
