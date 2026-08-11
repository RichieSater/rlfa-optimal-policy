"""Exact audit policies for simultaneously certified transaction intervals."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from functools import cache

from .model import History, Interval, RationalInput, as_fraction


@dataclass(frozen=True)
class BoxAuditProblem:
    """Finite-population total with a simultaneous interval for every item.

    The uncertainty set is the Cartesian product ``lower_i <= f_i <= upper_i``.
    The bounds are assumed to hold simultaneously; their calibration risk is
    external to this deterministic optimization problem.
    """

    weights: tuple[Fraction, ...]
    lower: tuple[Fraction, ...]
    upper: tuple[Fraction, ...]
    epsilon: Fraction

    def __post_init__(self) -> None:
        weights = tuple(as_fraction(value) for value in self.weights)
        lower = tuple(as_fraction(value) for value in self.lower)
        upper = tuple(as_fraction(value) for value in self.upper)
        epsilon = as_fraction(self.epsilon)
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "lower", lower)
        object.__setattr__(self, "upper", upper)
        object.__setattr__(self, "epsilon", epsilon)

        if not weights:
            raise ValueError("an audit population cannot be empty")
        if len(weights) != len(lower) or len(weights) != len(upper):
            raise ValueError("weights and interval endpoints must have equal lengths")
        if any(weight <= 0 for weight in weights):
            raise ValueError("every transaction weight must be positive")
        if sum(weights, Fraction(0)) != 1:
            raise ValueError("transaction weights must sum exactly to one")
        if any(lo < 0 or hi > 1 or lo > hi for lo, hi in zip(lower, upper, strict=True)):
            raise ValueError("every uncertainty interval must lie in [0, 1]")
        if epsilon < 0 or epsilon >= 1:
            raise ValueError("epsilon must lie in [0, 1)")

    @classmethod
    def from_values(
        cls,
        weights: Iterable[RationalInput],
        lower: Iterable[RationalInput],
        upper: Iterable[RationalInput],
        epsilon: RationalInput,
    ) -> BoxAuditProblem:
        return cls(
            tuple(as_fraction(value) for value in weights),
            tuple(as_fraction(value) for value in lower),
            tuple(as_fraction(value) for value in upper),
            as_fraction(epsilon),
        )

    @property
    def size(self) -> int:
        return len(self.weights)

    @property
    def uncertainty_contributions(self) -> tuple[Fraction, ...]:
        """Return ``d_i = pi_i (upper_i-lower_i)``."""

        return tuple(
            weight * (hi - lo)
            for weight, lo, hi in zip(self.weights, self.lower, self.upper, strict=True)
        )

    @property
    def initial_width(self) -> Fraction:
        return sum(self.uncertainty_contributions, Fraction(0))

    def validate_history(self, history: History) -> None:
        if len(set(history)) != len(history):
            raise ValueError("a without-replacement history cannot repeat an index")
        if any(index < 0 or index >= self.size for index in history):
            raise ValueError("history contains an index outside the population")

    def remaining(self, history: History) -> tuple[int, ...]:
        self.validate_history(history)
        seen = set(history)
        return tuple(index for index in range(self.size) if index not in seen)

    def residual_width(self, history: History) -> Fraction:
        contributions = self.uncertainty_contributions
        return sum((contributions[index] for index in self.remaining(history)), Fraction(0))

    def stops(self, history: History) -> bool:
        return self.residual_width(history) <= self.epsilon

    def certificate_interval(
        self, history: History, observed: Mapping[int, RationalInput]
    ) -> Interval:
        """Return the exact range of the total after the audited observations."""

        self.validate_history(history)
        if set(observed) != set(history):
            raise ValueError("observed values must be supplied exactly for the audited indices")
        values = {index: as_fraction(value) for index, value in observed.items()}
        if any(value < 0 or value > 1 for value in values.values()):
            raise ValueError("observed misstatement fractions must lie in [0, 1]")
        for index, value in values.items():
            if value < self.lower[index] or value > self.upper[index]:
                raise ValueError(
                    "observed value violates its certified interval; risk claim invalid"
                )
        audited = sum(
            (self.weights[index] * values[index] for index in history), Fraction(0)
        )
        remaining = self.remaining(history)
        lower = audited + sum(
            (self.weights[index] * self.lower[index] for index in remaining), Fraction(0)
        )
        upper = audited + sum(
            (self.weights[index] * self.upper[index] for index in remaining), Fraction(0)
        )
        return Interval(lower, upper)


@dataclass(frozen=True)
class BoxOptimalSolution:
    """Exact unit-cost minimax solution for a box uncertainty set."""

    order: tuple[int, ...]
    cover_number: int
    optimal_prefix: tuple[int, ...]
    initial_width: Fraction
    target_removed_width: Fraction
    residual_widths: tuple[Fraction, ...]


@dataclass(frozen=True)
class CostOptimalBoxSolution:
    """Exact minimum-cost cover of the required uncertainty width."""

    selected: tuple[int, ...]
    total_cost: Fraction
    removed_width: Fraction
    residual_width: Fraction


def solve_box_unit_cost(problem: BoxAuditProblem) -> BoxOptimalSolution:
    """Audit in descending dollar-weighted uncertainty and return its certificate."""

    contributions = problem.uncertainty_contributions
    order = tuple(sorted(range(problem.size), key=lambda index: (-contributions[index], index)))
    target = max(Fraction(0), problem.initial_width - problem.epsilon)
    removed = Fraction(0)
    cover_number = 0
    residuals = [problem.initial_width]
    while removed < target:
        removed += contributions[order[cover_number]]
        cover_number += 1
        residuals.append(problem.initial_width - removed)
    return BoxOptimalSolution(
        order=order,
        cover_number=cover_number,
        optimal_prefix=order[:cover_number],
        initial_width=problem.initial_width,
        target_removed_width=target,
        residual_widths=tuple(residuals),
    )


def solve_box_costs(
    problem: BoxAuditProblem, costs: Iterable[RationalInput]
) -> CostOptimalBoxSolution:
    """Solve heterogeneous manual-review costs by an exact Pareto-frontier DP.

    The running removed width is capped at the target because all larger values
    are equivalent for feasibility.  Dominated states are pruned exactly: a
    state is discarded if another has at least as much removed width at no
    greater cost.  Worst-case complexity is exponential, as expected for a
    covering-knapsack problem, but all arithmetic and optimality are exact.
    """

    cost_values = tuple(as_fraction(value) for value in costs)
    if len(cost_values) != problem.size:
        raise ValueError("cost vector has the wrong population size")
    if any(cost <= 0 for cost in cost_values):
        raise ValueError("every audit cost must be positive")
    target = max(Fraction(0), problem.initial_width - problem.epsilon)
    contributions = problem.uncertainty_contributions

    # removed width -> (cost, selected indices)
    states: dict[Fraction, tuple[Fraction, tuple[int, ...]]] = {
        Fraction(0): (Fraction(0), ())
    }
    for index, (width, item_cost) in enumerate(
        zip(contributions, cost_values, strict=True)
    ):
        candidates = dict(states)
        for removed, (cost, selected) in states.items():
            next_removed = min(target, removed + width)
            next_value = (cost + item_cost, selected + (index,))
            incumbent = candidates.get(next_removed)
            if incumbent is None or next_value[0] < incumbent[0]:
                candidates[next_removed] = next_value

        # Scan from greater removal to smaller removal.  A state survives only
        # if its cost is strictly below every state with greater removal.
        pruned: dict[Fraction, tuple[Fraction, tuple[int, ...]]] = {}
        best_cost: Fraction | None = None
        for removed in sorted(candidates, reverse=True):
            value = candidates[removed]
            if best_cost is None or value[0] < best_cost:
                pruned[removed] = value
                best_cost = value[0]
        states = pruned

    total_cost, selected = states[target]
    removed_width = sum((contributions[index] for index in selected), Fraction(0))
    return CostOptimalBoxSolution(
        selected=selected,
        total_cost=total_cost,
        removed_width=removed_width,
        residual_width=problem.initial_width - removed_width,
    )


def stopping_time_for_order(problem: BoxAuditProblem, order: tuple[int, ...]) -> int:
    """Evaluate any deterministic complete ordering."""

    if tuple(sorted(order)) != tuple(range(problem.size)):
        raise ValueError("order must be a permutation of all transaction indices")
    history: History = ()
    if problem.stops(history):
        return 0
    for index in order:
        history += (index,)
        if problem.stops(history):
            return len(history)
    raise AssertionError("a complete audit must have zero residual width")


def expected_time_proportional_to(
    problem: BoxAuditProblem, scores: Iterable[RationalInput]
) -> Fraction:
    """Exact subset DP for sampling proportionally to fixed scores.

    If all remaining scores vanish, the fallback is uniform.  This convention
    makes the policy total without changing any positive-score history.
    """

    fixed_scores = tuple(as_fraction(value) for value in scores)
    if len(fixed_scores) != problem.size:
        raise ValueError("score vector has the wrong population size")
    if any(score < 0 for score in fixed_scores):
        raise ValueError("scores cannot be negative")

    @cache
    def value(history_set: frozenset[int]) -> Fraction:
        history = tuple(sorted(history_set))
        if problem.stops(history):
            return Fraction(0)
        remaining = tuple(index for index in range(problem.size) if index not in history_set)
        denominator = sum((fixed_scores[index] for index in remaining), Fraction(0))
        if denominator == 0:
            probabilities = {index: Fraction(1, len(remaining)) for index in remaining}
        else:
            probabilities = {
                index: fixed_scores[index] / denominator for index in remaining
            }
        return 1 + sum(
            (
                probabilities[index] * value(history_set | {index})
                for index in remaining
            ),
            Fraction(0),
        )

    return value(frozenset())


def multiplicative_score_box(
    weights: Iterable[RationalInput],
    scores: Iterable[RationalInput],
    relative_error: RationalInput,
    epsilon: RationalInput,
) -> BoxAuditProblem:
    """Convert ``S_i/f_i in [1-a,1+a]`` to an exact clipped box."""

    weight_values = tuple(as_fraction(value) for value in weights)
    score_values = tuple(as_fraction(value) for value in scores)
    a = as_fraction(relative_error)
    if not 0 <= a < 1:
        raise ValueError("relative_error must lie in [0, 1)")
    if any(score < 0 or score > 1 for score in score_values):
        raise ValueError("scores must lie in [0, 1]")
    lower = tuple(score / (1 + a) for score in score_values)
    upper = tuple(min(Fraction(1), score / (1 - a)) for score in score_values)
    return BoxAuditProblem(weight_values, lower, upper, as_fraction(epsilon))
