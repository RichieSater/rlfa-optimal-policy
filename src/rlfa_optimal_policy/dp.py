"""Exact history enumeration and dynamic programming."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from typing import Protocol

from .model import AuditInstance, History, Interval
from .policies import SamplingPolicy, SupportMode, validate_distribution


class StoppingRule(Protocol):
    name: str

    def stops(self, instance: AuditInstance, history: History) -> bool: ...


@dataclass(frozen=True)
class TerminalPath:
    history: History
    probability: Fraction
    stopping_time: int
    final_interval: Interval


def enumerate_terminal_paths(
    instance: AuditInstance,
    policy: SamplingPolicy,
    stopping_rule: StoppingRule,
    *,
    support_mode: SupportMode = "positive-contributions",
) -> tuple[TerminalPath, ...]:
    """Enumerate every terminal sampling history with its exact probability."""

    paths: list[TerminalPath] = []

    def visit(history: History, path_probability: Fraction) -> None:
        if stopping_rule.stops(instance, history):
            paths.append(
                TerminalPath(
                    history=history,
                    probability=path_probability,
                    stopping_time=len(history),
                    final_interval=instance.logical_interval(history),
                )
            )
            return
        if len(history) == instance.size:
            raise ValueError("stopping rule did not stop after a complete audit")
        distribution = policy.probabilities(instance, history)
        validate_distribution(instance, history, distribution, support_mode)
        for index in instance.remaining(history):
            probability = distribution[index]
            if probability:
                visit(history + (index,), path_probability * probability)

    visit((), Fraction(1))
    if sum((path.probability for path in paths), Fraction(0)) != 1:
        raise AssertionError("terminal path probabilities do not sum to one")
    return tuple(paths)


def expected_audit_length(
    instance: AuditInstance,
    policy: SamplingPolicy,
    stopping_rule: StoppingRule,
    *,
    support_mode: SupportMode = "positive-contributions",
) -> Fraction:
    """Compute ``E[tau]`` by an exact Bellman recursion over ordered histories."""

    @cache
    def value(history: History) -> Fraction:
        if stopping_rule.stops(instance, history):
            return Fraction(len(history))
        if len(history) == instance.size:
            raise ValueError("stopping rule did not stop after a complete audit")
        distribution = policy.probabilities(instance, history)
        validate_distribution(instance, history, distribution, support_mode)
        return sum(
            (
                distribution[index] * value(history + (index,))
                for index in instance.remaining(history)
            ),
            Fraction(0),
        )

    return value(())
