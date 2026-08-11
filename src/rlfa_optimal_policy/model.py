"""Finite-population audit objects represented with exact rational arithmetic."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from typing import TypeAlias

RationalInput: TypeAlias = Fraction | int | str
History: TypeAlias = tuple[int, ...]


def as_fraction(value: RationalInput) -> Fraction:
    """Convert an exact input to ``Fraction`` and reject accidental floats."""

    if isinstance(value, float):
        raise TypeError("floating-point inputs are forbidden in exact certificates")
    if isinstance(value, Fraction):
        return value
    return Fraction(value)


@dataclass(frozen=True)
class Interval:
    """A closed rational interval."""

    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise ValueError("interval lower endpoint exceeds upper endpoint")

    @property
    def diameter(self) -> Fraction:
        return self.upper - self.lower


@dataclass(frozen=True)
class AuditInstance:
    """A finite RLFA instance.

    ``weights`` are the normalized recorded-value fractions ``pi_i`` and must
    sum to one. ``misstatements`` are the fixed fractions ``f_i``.
    """

    weights: tuple[Fraction, ...]
    misstatements: tuple[Fraction, ...]
    epsilon: Fraction
    delta: Fraction

    def __post_init__(self) -> None:
        weights = tuple(as_fraction(value) for value in self.weights)
        misstatements = tuple(as_fraction(value) for value in self.misstatements)
        epsilon = as_fraction(self.epsilon)
        delta = as_fraction(self.delta)
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "misstatements", misstatements)
        object.__setattr__(self, "epsilon", epsilon)
        object.__setattr__(self, "delta", delta)

        if not weights:
            raise ValueError("an audit population cannot be empty")
        if len(weights) != len(misstatements):
            raise ValueError("weights and misstatements must have the same length")
        if any(weight <= 0 for weight in weights):
            raise ValueError("every transaction weight must be positive")
        if sum(weights, Fraction(0)) != 1:
            raise ValueError("transaction weights must sum exactly to one")
        if any(value < 0 or value > 1 for value in misstatements):
            raise ValueError("misstatement fractions must lie in [0, 1]")
        if not 0 < epsilon < 1:
            raise ValueError("epsilon must lie in (0, 1)")
        if not 0 < delta < 1:
            raise ValueError("delta must lie in (0, 1)")

    @classmethod
    def from_values(
        cls,
        weights: Iterable[RationalInput],
        misstatements: Iterable[RationalInput],
        epsilon: RationalInput,
        delta: RationalInput,
    ) -> AuditInstance:
        return cls(
            tuple(as_fraction(value) for value in weights),
            tuple(as_fraction(value) for value in misstatements),
            as_fraction(epsilon),
            as_fraction(delta),
        )

    @property
    def size(self) -> int:
        return len(self.weights)

    @property
    def total_misstatement(self) -> Fraction:
        return sum(
            (
                weight * value
                for weight, value in zip(self.weights, self.misstatements, strict=True)
            ),
            Fraction(0),
        )

    def contribution(self, index: int) -> Fraction:
        return self.weights[index] * self.misstatements[index]

    def validate_history(self, history: History) -> None:
        if len(set(history)) != len(history):
            raise ValueError("a without-replacement history cannot repeat an index")
        if any(index < 0 or index >= self.size for index in history):
            raise ValueError("history contains an index outside the population")

    def remaining(self, history: History) -> tuple[int, ...]:
        self.validate_history(history)
        seen = set(history)
        return tuple(index for index in range(self.size) if index not in seen)

    def logical_interval(self, history: History) -> Interval:
        """Return the logical CS after the given ordered sample history."""

        self.validate_history(history)
        observed = sum((self.contribution(index) for index in history), Fraction(0))
        remaining_weight = sum(
            (self.weights[index] for index in self.remaining(history)), Fraction(0)
        )
        return Interval(observed, observed + remaining_weight)
