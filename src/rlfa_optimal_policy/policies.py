"""Exact sampling policies for finite populations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Literal, Protocol

from .model import AuditInstance, History, RationalInput, as_fraction

Distribution = dict[int, Fraction]
SupportMode = Literal["simplex", "positive-contributions", "full"]


class SamplingPolicy(Protocol):
    name: str

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution: ...


def _normalize(scores: Mapping[int, Fraction]) -> Distribution:
    total = sum(scores.values(), Fraction(0))
    if total <= 0:
        raise ValueError("sampling scores must have a positive total")
    return {index: score / total for index, score in scores.items()}


@dataclass(frozen=True)
class OracleContributionPolicy:
    """Repeated one-step oracle: ``q_t(i)`` proportional to ``pi_i f_i``."""

    name: str = "oracle-pi-f"

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution:
        remaining = instance.remaining(history)
        scores = {index: instance.contribution(index) for index in remaining}
        if sum(scores.values(), Fraction(0)) == 0:
            # The paper does not need a special choice after all remaining
            # contributions vanish. Proportional-to-value is a fully supported,
            # deterministic fallback; the counterexample never reaches it.
            scores = {index: instance.weights[index] for index in remaining}
        return _normalize(scores)


@dataclass(frozen=True)
class ProportionalValuePolicy:
    """The paper's implementable prop-M rule: ``q_t(i)`` proportional to ``pi_i``."""

    name: str = "prop-M"

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution:
        return _normalize(
            {index: instance.weights[index] for index in instance.remaining(history)}
        )


@dataclass(frozen=True)
class FixedFirstDistributionPolicy:
    """Use a prescribed first distribution and prop-M thereafter."""

    first_distribution: tuple[Fraction, ...]
    name: str = "fixed-first"

    @classmethod
    def from_values(
        cls, probabilities: tuple[RationalInput, ...], name: str = "fixed-first"
    ) -> FixedFirstDistributionPolicy:
        return cls(tuple(as_fraction(value) for value in probabilities), name)

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution:
        remaining = instance.remaining(history)
        if not history:
            if len(self.first_distribution) != instance.size:
                raise ValueError("first distribution has the wrong population size")
            return dict(enumerate(self.first_distribution))
        return _normalize({index: instance.weights[index] for index in remaining})


def validate_distribution(
    instance: AuditInstance,
    history: History,
    distribution: Mapping[int, Fraction],
    support_mode: SupportMode = "positive-contributions",
) -> None:
    """Check exact normalization under one of three support conventions.

    ``simplex`` permits boundary distributions, matching the literal simplex
    in the paper. ``positive-contributions`` requires mass wherever the fixed
    importance-weighted contribution is positive. ``full`` requires strictly
    positive mass on every remaining transaction.
    """

    remaining = set(instance.remaining(history))
    if set(distribution) != remaining:
        raise ValueError("a policy must assign a probability to every remaining index")
    if any(probability < 0 for probability in distribution.values()):
        raise ValueError("sampling probabilities cannot be negative")
    if sum(distribution.values(), Fraction(0)) != 1:
        raise ValueError("sampling probabilities must sum exactly to one")
    if support_mode == "simplex":
        return
    if support_mode == "positive-contributions":
        for index, probability in distribution.items():
            if instance.contribution(index) > 0 and probability == 0:
                raise ValueError(
                    "positive-contribution transactions require positive sampling mass"
                )
        return
    if support_mode == "full":
        if any(probability == 0 for probability in distribution.values()):
            raise ValueError("full support requires every remaining probability to be positive")
        return
    raise ValueError(f"unknown support mode: {support_mode}")
