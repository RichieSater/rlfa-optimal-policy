"""Exact-rational finite-grid ApproxKelly state transitions and mesh Bellman DP.

This module removes only the authors' floating-point denominator guard.  It
otherwise mirrors the mathematical payoff, released zero initialization,
ApproxKelly ratio and clipping, fixed candidate grid, logical intersection,
and running intersection.  The Bellman solver is globally exact for its stated
finite candidate grid and finite action mesh; it is not presented as a
continuous-action solution.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from typing import Literal

from .model import AuditInstance, History
from .policies import SamplingPolicy, validate_distribution

PayoffInformation = Literal["oracle", "worst-case"]


@dataclass(frozen=True)
class ApproxKellyConfig:
    grid_size: int = 41
    lambda_max: Fraction = Fraction(5, 2)
    tolerance: Fraction = Fraction(1, 10**10)
    payoff_information: PayoffInformation = "oracle"

    def __post_init__(self) -> None:
        if self.grid_size < 2:
            raise ValueError("grid_size must be at least two")
        if self.lambda_max <= 0:
            raise ValueError("lambda_max must be positive")
        if self.tolerance <= 0:
            raise ValueError("tolerance must be positive")
        if self.payoff_information not in ("oracle", "worst-case"):
            raise ValueError("unknown payoff-information convention")

    @property
    def grid(self) -> tuple[Fraction, ...]:
        return tuple(Fraction(index, self.grid_size - 1) for index in range(self.grid_size))


@dataclass(frozen=True)
class ApproxKellyState:
    history: History
    wealth: tuple[Fraction, ...]
    payoff_rows: tuple[tuple[Fraction, ...], ...]
    combined_lower: Fraction
    combined_upper: Fraction
    error: bool = False

    @property
    def diameter(self) -> Fraction:
        return max(Fraction(0), self.combined_upper - self.combined_lower)


def initial_state(config: ApproxKellyConfig) -> ApproxKellyState:
    """Replicate the released extra zero payoff column."""

    return ApproxKellyState(
        history=(),
        wealth=(Fraction(1),) * config.grid_size,
        payoff_rows=((Fraction(0),),) * config.grid_size,
        combined_lower=Fraction(0),
        combined_upper=Fraction(1),
    )


def state_stops(
    instance: AuditInstance, state: ApproxKellyState, *, allow_time_zero: bool = False
) -> bool:
    if not state.history and not allow_time_zero:
        return False
    return state.diameter <= instance.epsilon


def _allowed_bet(
    minimum_payoff: Fraction,
    maximum_payoff: Fraction,
    config: ApproxKellyConfig,
) -> tuple[Fraction, Fraction]:
    if maximum_payoff < minimum_payoff:
        raise ValueError("maximum payoff is below minimum payoff")
    tolerance = config.tolerance
    if minimum_payoff >= 0:
        lower = -1 / (maximum_payoff + tolerance)
        upper = config.lambda_max
    elif maximum_payoff > 0:
        lower = -1 / (maximum_payoff + tolerance)
        upper = 1 / (abs(minimum_payoff) + tolerance)
    else:
        lower = -config.lambda_max
        upper = 1 / (abs(minimum_payoff) + tolerance)
    return max(lower, -config.lambda_max), min(upper, config.lambda_max)


def _next_bet(
    previous_payoffs: tuple[Fraction, ...],
    allowed: tuple[Fraction, Fraction],
    config: ApproxKellyConfig,
) -> Fraction:
    numerator = sum(previous_payoffs, Fraction(0))
    denominator = sum((value * value for value in previous_payoffs), Fraction(0))
    raw = numerator / (denominator + config.tolerance)
    return max(allowed[0], min(allowed[1], raw))


def transition(
    instance: AuditInstance,
    state: ApproxKellyState,
    distribution: Mapping[int, Fraction],
    sampled_index: int,
    config: ApproxKellyConfig,
) -> ApproxKellyState:
    """Apply one forced sampling outcome to the complete finite-grid state."""

    validate_distribution(instance, state.history, distribution, "full")
    if sampled_index not in instance.remaining(state.history):
        raise ValueError("sampled index is not remaining")
    if distribution[sampled_index] <= 0:
        raise ValueError("sampled outcome must have positive probability")

    remaining = instance.remaining(state.history)
    observed = sum((instance.contribution(index) for index in state.history), Fraction(0))
    if config.payoff_information == "oracle":
        possible_observations = tuple(
            instance.contribution(index) / distribution[index] for index in remaining
        )
        minimum_observation = min(possible_observations)
        maximum_observation = max(possible_observations)
    else:
        minimum_observation = Fraction(0)
        maximum_observation = max(
            instance.weights[index] / distribution[index] for index in remaining
        )

    next_wealth: list[Fraction] = []
    next_payoff_rows: list[tuple[Fraction, ...]] = []
    for grid_index, candidate in enumerate(config.grid):
        residual_candidate = candidate - observed
        minimum_payoff = minimum_observation - residual_candidate
        maximum_payoff = maximum_observation - residual_candidate
        allowed = _allowed_bet(minimum_payoff, maximum_payoff, config)
        bet = _next_bet(state.payoff_rows[grid_index], allowed, config)
        payoff = (
            instance.contribution(sampled_index) / distribution[sampled_index]
            - residual_candidate
        )
        factor = 1 + bet * payoff
        if factor <= 0:
            # The mathematical range calculation should make this impossible.
            raise ArithmeticError("nonpositive wealth factor after safe-bet clipping")
        next_wealth.append(state.wealth[grid_index] * factor)
        next_payoff_rows.append(state.payoff_rows[grid_index] + (payoff,))

    accepted = tuple(
        candidate
        for candidate, wealth in zip(config.grid, next_wealth, strict=True)
        if wealth < 1 / instance.delta
    )
    error = state.error or not accepted
    if accepted:
        betting_lower, betting_upper = min(accepted), max(accepted)
    else:
        betting_lower, betting_upper = Fraction(0), Fraction(1)

    next_history = state.history + (sampled_index,)
    logical = instance.logical_interval(next_history)
    combined_lower = max(state.combined_lower, betting_lower, logical.lower)
    combined_upper = min(state.combined_upper, betting_upper, logical.upper)
    if combined_lower > combined_upper:
        error = True

    return ApproxKellyState(
        history=next_history,
        wealth=tuple(next_wealth),
        payoff_rows=tuple(next_payoff_rows),
        combined_lower=combined_lower,
        combined_upper=combined_upper,
        error=error,
    )


def evaluate_policy(
    instance: AuditInstance,
    policy: SamplingPolicy,
    config: ApproxKellyConfig | None = None,
) -> Fraction:
    """Enumerate a fixed history-based policy under the full grid state."""

    if config is None:
        config = ApproxKellyConfig()

    @cache
    def value(state: ApproxKellyState) -> Fraction:
        if state_stops(instance, state):
            return Fraction(0)
        distribution = policy.probabilities(instance, state.history)
        validate_distribution(instance, state.history, distribution, "full")
        return 1 + sum(
            (
                distribution[index]
                * value(transition(instance, state, distribution, index, config))
                for index in instance.remaining(state.history)
            ),
            Fraction(0),
        )

    return value(initial_state(config))


def _positive_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        if total >= 1:
            yield (total,)
        return
    for first in range(1, total - parts + 2):
        for tail in _positive_compositions(total - first, parts - 1):
            yield (first,) + tail


def action_mesh(remaining: tuple[int, ...], denominator: int) -> tuple[dict[int, Fraction], ...]:
    """Enumerate the strict-full-support simplex mesh of a given denominator."""

    if denominator < len(remaining):
        raise ValueError("mesh denominator is too small for strict full support")
    return tuple(
        {
            index: Fraction(numerator, denominator)
            for index, numerator in zip(remaining, composition, strict=True)
        }
        for composition in _positive_compositions(denominator, len(remaining))
    )


@dataclass(frozen=True)
class MeshBellmanResult:
    expected_length: Fraction
    initial_action: tuple[tuple[int, Fraction], ...]
    states_evaluated: int
    action_denominator: int
    grid_size: int


def solve_action_mesh(
    instance: AuditInstance,
    action_denominator: int,
    config: ApproxKellyConfig | None = None,
) -> MeshBellmanResult:
    """Solve the augmented-state Bellman equation exactly on a finite mesh."""

    if config is None:
        config = ApproxKellyConfig()

    optimal_actions: dict[ApproxKellyState, tuple[tuple[int, Fraction], ...]] = {}

    @cache
    def value(state: ApproxKellyState) -> Fraction:
        if state_stops(instance, state):
            return Fraction(0)
        remaining = instance.remaining(state.history)
        best_value: Fraction | None = None
        best_action: tuple[tuple[int, Fraction], ...] | None = None
        for distribution in action_mesh(remaining, action_denominator):
            candidate = 1 + sum(
                (
                    distribution[index]
                    * value(transition(instance, state, distribution, index, config))
                    for index in remaining
                ),
                Fraction(0),
            )
            action_key = tuple(sorted(distribution.items()))
            if (
                best_value is None
                or candidate < best_value
                or (candidate == best_value and action_key < best_action)
            ):
                best_value = candidate
                best_action = action_key
        if best_value is None or best_action is None:
            raise AssertionError("nonterminal state had no mesh actions")
        optimal_actions[state] = best_action
        return best_value

    start = initial_state(config)
    expected = value(start)
    return MeshBellmanResult(
        expected_length=expected,
        initial_action=optimal_actions[start],
        states_evaluated=value.cache_info().currsize,
        action_denominator=action_denominator,
        grid_size=config.grid_size,
    )
