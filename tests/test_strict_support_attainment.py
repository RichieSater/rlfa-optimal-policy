"""Exact counterexample to universal nonattainment under strict support.

The continuous-candidate calculation is checked through its affine endpoint
bounds, rather than a candidate grid. This does not use ApproxKelly's zero
first stake: lambda_1(m) is 1 if m > epsilon, and 0 otherwise.
"""

from fractions import Fraction as F


def test_full_support_attains_one_with_valid_bounded_stakes() -> None:
    pi = (F(79, 80), F(1, 80))
    taints = (F(1, 79), F(1))
    q = (F(1679, 1680), F(1, 1680))
    epsilon, delta, cap = F(1, 40), F(1, 20), F(1)
    contributions = tuple(p * f for p, f in zip(pi, taints, strict=True))
    assert sum(q) == 1 and min(q) > 0
    assert sum(contributions) == epsilon
    assert (1 + 2 * cap * epsilon) ** 2 < 1 / delta

    # For any candidate in [0,1] and any possible observation Z >= 0,
    # the stake-one factor 1+Z-m is minimized at (Z,m)=(0,1).
    assert 1 + F(0) - F(1) == 0

    intervals = []
    for first in (0, 1):
        z = contributions[first] / q[first]
        logical_lower = contributions[first]
        logical_upper = logical_lower + pi[1 - first]
        if first == 0:
            # All logical candidates have stake zero and wealth one.
            assert logical_upper == epsilon
            interval = (logical_lower, logical_upper)
        else:
            assert z == 21
            # Wealth for every m > epsilon is decreasing affine in m;
            # its minimum on that range occurs at m=1 and exceeds threshold.
            assert 1 + z - 1 > 1 / delta
            # Candidates <= epsilon all have wealth one and remain.
            assert 1 < 1 / delta
            interval = (logical_lower, min(logical_upper, epsilon))
        assert interval == (F(1, 80), F(1, 40))
        assert interval[1] - interval[0] <= epsilon
        assert interval[0] <= sum(contributions) <= interval[1]
        intervals.append(interval)

    # Every branch stops at one, and the true-total stake is zero on both.
    assert len(intervals) == 2
    assert sum(probability * 1 for probability in q) == 1
