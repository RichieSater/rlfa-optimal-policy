"""Arbitrary-population logical stopping and sharp oracle-gap families."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .model import AuditInstance, History, RationalInput, as_fraction


@dataclass(frozen=True)
class LogicalStoppingRule:
    """Stop when the unaudited monetary weight is at most ``epsilon``."""

    name: str = "logical"

    def stops(self, instance: AuditInstance, history: History) -> bool:
        instance.validate_history(history)
        return instance.logical_interval(history).diameter <= instance.epsilon


@dataclass(frozen=True)
class LogicalOptimalSolution:
    order: tuple[int, ...]
    cover_number: int
    optimal_prefix: tuple[int, ...]
    residual_weights: tuple[Fraction, ...]


def solve_logical_unit_cost(instance: AuditInstance) -> LogicalOptimalSolution:
    """Return the minimum-cardinality risk-zero logical certificate."""

    order = tuple(
        sorted(range(instance.size), key=lambda index: (-instance.weights[index], index))
    )
    target = 1 - instance.epsilon
    audited_weight = Fraction(0)
    cover_number = 0
    residuals = [Fraction(1)]
    while audited_weight < target:
        audited_weight += instance.weights[order[cover_number]]
        cover_number += 1
        residuals.append(1 - audited_weight)
    return LogicalOptimalSolution(
        order=order,
        cover_number=cover_number,
        optimal_prefix=order[:cover_number],
        residual_weights=tuple(residuals),
    )


def expected_plackett_luce_rank(rates: tuple[Fraction, ...], index: int) -> Fraction:
    """Expected rank of one item under sequential probability-proportional sampling."""

    if not rates or index < 0 or index >= len(rates):
        raise ValueError("index must identify an item in a nonempty rate vector")
    if any(rate <= 0 for rate in rates):
        raise ValueError("Plackett-Luce rates must be strictly positive")
    selected_rate = rates[index]
    return 1 + sum(
        (
            rate / (selected_rate + rate)
            for other, rate in enumerate(rates)
            if other != index
        ),
        Fraction(0),
    )


@dataclass(frozen=True)
class OracleGapFamily:
    """A population in which stopping is exactly the rank of one large item."""

    instance: AuditInstance
    large_index: int
    small_weight: Fraction
    contribution_ratio: Fraction
    default_bet_cap: Fraction
    oracle_expected_length: Fraction
    prop_m_expected_length: Fraction
    literal_simplex_optimum: Fraction
    uniform_wealth_bound: Fraction


@dataclass(frozen=True)
class FixedRiskOracleGapFamily:
    """Sharp oracle lower bound at the conventional risk limit ``delta=1/20``."""

    instance: AuditInstance
    large_index: int
    small_weight: Fraction
    contribution_ratio: Fraction
    witness_candidates: tuple[Fraction, Fraction]
    witness_grid_size: int
    witness_separation: Fraction
    candidate_wealth_bound: Fraction
    oracle_expected_length: Fraction
    prop_m_rank_upper_bound: Fraction
    literal_simplex_optimum: Fraction


def oracle_gap_family(
    size: int,
    large_weight: RationalInput = Fraction(3, 4),
    contribution_ratio: RationalInput = 1,
    epsilon: RationalInput = Fraction(1, 3),
    *,
    default_bet_cap: RationalInput = Fraction(5, 2),
) -> OracleGapFamily:
    """Construct an exact arbitrary-``N`` oracle lower-bound instance.

    Small transactions have ``f=1``.  The large transaction's contribution is
    ``rho`` times a small transaction's contribution.  The risk limit is chosen
    below a uniform wealth bound, forcing the released combined CS to coincide
    with its logical component under both oracle and prop-M sampling.
    """

    if size < 2:
        raise ValueError("the oracle-gap family requires at least two transactions")
    p = as_fraction(large_weight)
    rho = as_fraction(contribution_ratio)
    eps = as_fraction(epsilon)
    lambda_max = as_fraction(default_bet_cap)
    if not Fraction(1, 2) < p < 1:
        raise ValueError("large_weight must lie in (1/2, 1)")
    if rho <= 0 or rho > p * (size - 1) / (1 - p):
        raise ValueError("contribution_ratio must be positive and keep f_large <= 1")
    if not 1 - p <= eps < p:
        raise ValueError("epsilon must satisfy 1-large_weight <= epsilon < large_weight")
    if lambda_max <= 0:
        raise ValueError("default_bet_cap must be positive")

    small_weight = (1 - p) / (size - 1)
    f_large = rho * small_weight / p
    weights = (p,) + (small_weight,) * (size - 1)
    misstatements = (f_large,) + (Fraction(1),) * (size - 1)

    # Under prop-M, |Z_t-mu_t(m)| <= 2.  With |lambda_t| <= lambda_max,
    # every nonnegative wealth factor is at most 1+2*lambda_max.  The
    # integer base below is strictly larger, so 1/delta dominates every
    # possible wealth value through the finite horizon.
    payoff_wealth_bound = 1 + 2 * lambda_max
    integer_base = payoff_wealth_bound.numerator // payoff_wealth_bound.denominator + 1
    delta = Fraction(1, integer_base**size)
    instance = AuditInstance(weights, misstatements, eps, delta)

    contribution_rates = tuple(instance.contribution(index) for index in range(size))
    oracle_expected = expected_plackett_luce_rank(contribution_rates, 0)
    prop_m_expected = expected_plackett_luce_rank(instance.weights, 0)
    return OracleGapFamily(
        instance=instance,
        large_index=0,
        small_weight=small_weight,
        contribution_ratio=rho,
        default_bet_cap=lambda_max,
        oracle_expected_length=oracle_expected,
        prop_m_expected_length=prop_m_expected,
        literal_simplex_optimum=Fraction(1),
        uniform_wealth_bound=payoff_wealth_bound**size,
    )


def fixed_risk_oracle_gap_family(
    size: int, contribution_ratio: RationalInput = 1
) -> FixedRiskOracleGapFamily:
    """Give a sharp factor-``N`` family while fixing ``delta=0.05``.

    Set ``epsilon=1/(20N)`` and give one transaction weight
    ``1-epsilon/2``.  Until that transaction is audited, two grid candidates
    separated by ``2*epsilon`` survive every oracle wealth update.  Therefore
    the combined released confidence sequence cannot stop early, and the
    stopping time is exactly the large transaction's Plackett--Luce rank.
    """

    if size < 2:
        raise ValueError("the fixed-risk family requires at least two transactions")
    rho = as_fraction(contribution_ratio)
    if not 0 < rho <= 1:
        raise ValueError("contribution_ratio must lie in (0, 1]")

    epsilon = Fraction(1, 20 * size)
    residual_mass = epsilon / 2
    large_weight = 1 - residual_mass
    small_weight = residual_mass / (size - 1)
    f_large = rho * small_weight / large_weight
    weights = (large_weight,) + (small_weight,) * (size - 1)
    misstatements = (f_large,) + (Fraction(1),) * (size - 1)
    instance = AuditInstance(weights, misstatements, epsilon, Fraction(1, 20))

    lower_witness = residual_mass
    upper_witness = residual_mass + 2 * epsilon
    grid_size = 40 * size + 1
    # For either witness, the oracle payoff has magnitude below 2*epsilon.
    # The released |lambda| <= 5/2 cap makes every factor at most
    # 1+5*epsilon = 1+1/(4N).
    wealth_bound = (1 + Fraction(1, 4 * size)) ** size
    contribution_rates = tuple(instance.contribution(index) for index in range(size))
    oracle_expected = expected_plackett_luce_rank(contribution_rates, 0)
    prop_m_rank = expected_plackett_luce_rank(instance.weights, 0)
    return FixedRiskOracleGapFamily(
        instance=instance,
        large_index=0,
        small_weight=small_weight,
        contribution_ratio=rho,
        witness_candidates=(lower_witness, upper_witness),
        witness_grid_size=grid_size,
        witness_separation=2 * epsilon,
        candidate_wealth_bound=wealth_bound,
        oracle_expected_length=oracle_expected,
        prop_m_rank_upper_bound=prop_m_rank,
        literal_simplex_optimum=Fraction(1),
    )
