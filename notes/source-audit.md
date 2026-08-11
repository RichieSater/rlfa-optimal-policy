# Source-code audit

The mathematical reduction is pinned to the authors' public repository at
commit [`a834e459a47f9efa74fa1706f1b1dd8173ffa30b`](https://github.com/sshekhar17/WeightedWoRConfSeq/tree/a834e459a47f9efa74fa1706f1b1dd8173ffa30b).

Relevant implementation facts:

1. [`Payoff_vals` is initialized to zero](https://github.com/sshekhar17/WeightedWoRConfSeq/blob/a834e459a47f9efa74fa1706f1b1dd8173ffa30b/src/weightedCSsequential.py#L442-L448).
2. [`get_next_bet` returns the previous-payoff sum divided by the squared-payoff sum plus a positive tolerance](https://github.com/sshekhar17/WeightedWoRConfSeq/blob/a834e459a47f9efa74fa1706f1b1dd8173ffa30b/src/weightedCSsequential.py#L249-L278). On the initial zero array this is zero.
3. [The released run loop leaves the first raw betting bounds at `[0,1]`](https://github.com/sshekhar17/WeightedWoRConfSeq/blob/a834e459a47f9efa74fa1706f1b1dd8173ffa30b/src/weightedCSsequential.py#L442-L487).
4. [`predictive_correction1` intersects those bounds with the logical interval and optionally takes the running intersection](https://github.com/sshekhar17/WeightedWoRConfSeq/blob/a834e459a47f9efa74fa1706f1b1dd8173ffa30b/src/utils.py#L240-L282).

The exact verifier does not import or modify that code. It implements only the
four consequences needed for `N=2`, using rational arithmetic and no numerical
tolerances.
