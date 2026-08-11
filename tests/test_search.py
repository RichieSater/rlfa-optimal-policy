from rlfa_optimal_policy.search import find_n2_counterexample


def test_bounded_exact_search_finds_a_counterexample() -> None:
    hit = find_n2_counterexample(max_denominator=4)

    assert hit is not None
    assert hit.instance.size == 2
    assert hit.alternative_expectation < hit.oracle_expectation
