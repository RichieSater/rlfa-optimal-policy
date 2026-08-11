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


@dataclass(frozen=True)
class FixedPriorityPolicy:
    """Audit the remaining item of greatest fixed priority.

    Ties are resolved by index so the policy is deterministic and certificates
    are reproducible.  Zero priorities are permitted.
    """

    priorities: tuple[Fraction, ...]
    name: str = "fixed-priority"

    @classmethod
    def from_values(
        cls, priorities: tuple[RationalInput, ...], name: str = "fixed-priority"
    ) -> FixedPriorityPolicy:
        return cls(tuple(as_fraction(value) for value in priorities), name)

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution:
        if len(self.priorities) != instance.size:
            raise ValueError("priority vector has the wrong population size")
        remaining = instance.remaining(history)
        selected = min(remaining, key=lambda index: (-self.priorities[index], index))
        return {index: Fraction(index == selected) for index in remaining}


@dataclass(frozen=True)
class FixedScoreProportionalPolicy:
    """Sample without replacement proportionally to fixed nonnegative scores."""

    scores: tuple[Fraction, ...]
    name: str = "fixed-score-proportional"

    @classmethod
    def from_values(
        cls, scores: tuple[RationalInput, ...], name: str = "fixed-score-proportional"
    ) -> FixedScoreProportionalPolicy:
        return cls(tuple(as_fraction(value) for value in scores), name)

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution:
        if len(self.scores) != instance.size:
            raise ValueError("score vector has the wrong population size")
        remaining = instance.remaining(history)
        scores = {index: self.scores[index] for index in remaining}
        if any(score < 0 for score in scores.values()):
            raise ValueError("sampling scores cannot be negative")
        if sum(scores.values(), Fraction(0)) == 0:
            scores = {index: Fraction(1) for index in remaining}
        return _normalize(scores)


@dataclass(frozen=True)
class ProportionalMonetaryScorePolicy:
    """The paper's prop-MS rule for a fixed side-information vector."""

    scores: tuple[Fraction, ...]
    name: str = "prop-MS"

    @classmethod
    def from_values(
        cls, scores: tuple[RationalInput, ...], name: str = "prop-MS"
    ) -> ProportionalMonetaryScorePolicy:
        return cls(tuple(as_fraction(value) for value in scores), name)

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution:
        if len(self.scores) != instance.size:
            raise ValueError("score vector has the wrong population size")
        remaining = instance.remaining(history)
        if any(self.scores[index] < 0 for index in remaining):
            raise ValueError("side-information scores cannot be negative")
        rates = {
            index: instance.weights[index] * self.scores[index] for index in remaining
        }
        if sum(rates.values(), Fraction(0)) == 0:
            rates = {index: instance.weights[index] for index in remaining}
        return _normalize(rates)


@dataclass(frozen=True)
class SmoothedPriorityPolicy:
    """Exploit the largest priority while retaining strict uniform support."""

    priorities: tuple[Fraction, ...]
    exploration: Fraction = Fraction(1, 20)
    name: str = "smoothed-priority"

    @classmethod
    def from_values(
        cls,
        priorities: tuple[RationalInput, ...],
        exploration: RationalInput = Fraction(1, 20),
        name: str = "smoothed-priority",
    ) -> SmoothedPriorityPolicy:
        return cls(
            tuple(as_fraction(value) for value in priorities),
            as_fraction(exploration),
            name,
        )

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution:
        if len(self.priorities) != instance.size:
            raise ValueError("priority vector has the wrong population size")
        if not 0 < self.exploration <= 1:
            raise ValueError("exploration must lie in (0, 1]")
        remaining = instance.remaining(history)
        selected = min(remaining, key=lambda index: (-self.priorities[index], index))
        baseline = self.exploration / len(remaining)
        return {
            index: baseline + (1 - self.exploration) * Fraction(index == selected)
            for index in remaining
        }


@dataclass(frozen=True)
class MeshPriorityPolicy:
    """Put the minimum mesh mass on all nonpriority items."""

    priorities: tuple[Fraction, ...]
    denominator: int
    name: str = "mesh-certified-priority"

    def probabilities(self, instance: AuditInstance, history: History) -> Distribution:
        if len(self.priorities) != instance.size:
            raise ValueError("priority vector has the wrong population size")
        remaining = instance.remaining(history)
        if self.denominator < len(remaining):
            raise ValueError("denominator is too small for strict full support")
        selected = min(remaining, key=lambda index: (-self.priorities[index], index))
        return {
            index: Fraction(
                self.denominator - len(remaining) + 1 if index == selected else 1,
                self.denominator,
            )
            for index in remaining
        }


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
