"""A bounded exact search that rediscovers two-transaction counterexamples."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .confidence import ReleasedApproxKellyLogicalN2
from .dp import expected_audit_length
from .model import AuditInstance
from .policies import OracleContributionPolicy, ProportionalValuePolicy


@dataclass(frozen=True)
class SearchHit:
    instance: AuditInstance
    oracle_expectation: Fraction
    alternative_expectation: Fraction


def reduced_fractions(max_denominator: int) -> tuple[Fraction, ...]:
    values = {
        Fraction(numerator, denominator)
        for denominator in range(2, max_denominator + 1)
        for numerator in range(1, denominator)
    }
    return tuple(sorted(values, key=lambda value: (value.denominator, value.numerator)))


def find_n2_counterexample(max_denominator: int = 6) -> SearchHit | None:
    """Search a small rational grid using exact dynamic programming.

    Item 1 is constrained to be the larger transaction. The search compares
    the repeated oracle with the paper's prop-M rule and stops at the first
    strict exact inequality.
    """

    fractions = reduced_fractions(max_denominator)
    rule = ReleasedApproxKellyLogicalN2()
    oracle = OracleContributionPolicy()
    alternative = ProportionalValuePolicy()
    for pi_1 in fractions:
        if pi_1 <= Fraction(1, 2):
            continue
        pi_2 = 1 - pi_1
        for f_1 in fractions:
            for f_2 in (*fractions, Fraction(1)):
                if f_1 >= f_2:
                    continue
                for epsilon in fractions:
                    if not pi_2 <= epsilon < pi_1:
                        continue
                    instance = AuditInstance.from_values(
                        (pi_1, pi_2), (f_1, f_2), epsilon, Fraction(1, 20)
                    )
                    oracle_value = expected_audit_length(instance, oracle, rule)
                    alternative_value = expected_audit_length(instance, alternative, rule)
                    if alternative_value < oracle_value:
                        return SearchHit(instance, oracle_value, alternative_value)
    return None
