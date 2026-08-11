"""The exact part of the released ApproxKelly-plus-logical stopping rule."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .model import AuditInstance, History, Interval


def released_approx_kelly_initial_bet() -> Fraction:
    """Return the first bet used by the authors' released implementation.

    Its previous-payoff accumulator is initialized at zero, so the ApproxKelly
    ratio has numerator zero and the implementation returns ``lambda_1 = 0``.
    """

    return Fraction(0)


def first_round_betting_interval(instance: AuditInstance) -> Interval:
    """The betting CS is all of ``[0, 1]`` when ``lambda_1 = 0``."""

    if released_approx_kelly_initial_bet() != 0:  # pragma: no cover - explicit invariant
        raise AssertionError("the released initialization changed")
    # W_1(m) = 1 for every m, while 1 < 1/delta because delta is in (0, 1).
    if not Fraction(1) < 1 / instance.delta:  # pragma: no cover - model validates delta
        raise AssertionError("invalid risk limit")
    return Interval(Fraction(0), Fraction(1))


def first_round_combined_interval(instance: AuditInstance, sampled_index: int) -> Interval:
    """Intersect the first-round betting CS with the paper's logical CS."""

    betting = first_round_betting_interval(instance)
    logical = instance.logical_interval((sampled_index,))
    return Interval(max(betting.lower, logical.lower), min(betting.upper, logical.upper))


@dataclass(frozen=True)
class ReleasedApproxKellyLogicalN2:
    """Exact stopping rule for a two-transaction population.

    At time one the released ApproxKelly bet is zero, so the combined CS equals
    the logical CS. At time two the logical CS is a singleton. Those observations
    completely determine the stopping rule without numerical root finding.
    """

    name: str = "released-ApproxKelly+logical-N2"

    def stops(self, instance: AuditInstance, history: History) -> bool:
        if instance.size != 2:
            raise ValueError("this exact reduction is certified only for N = 2")
        instance.validate_history(history)
        if not history:
            return False
        if len(history) == instance.size:
            return True
        interval = first_round_combined_interval(instance, history[0])
        return interval.diameter <= instance.epsilon
