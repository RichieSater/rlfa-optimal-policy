# Source-code audit

The mathematical reduction is pinned to the authors' public repository at
commit [`a834e459a47f9efa74fa1706f1b1dd8173ffa30b`](https://github.com/sshekhar17/WeightedWoRConfSeq/tree/a834e459a47f9efa74fa1706f1b1dd8173ffa30b).

Relevant implementation facts:

1. [`Payoff_vals` is initialized to zero](https://github.com/sshekhar17/WeightedWoRConfSeq/blob/a834e459a47f9efa74fa1706f1b1dd8173ffa30b/src/weightedCSsequential.py#L442-L448).
2. [`get_next_bet` returns the previous-payoff sum divided by the squared-payoff sum plus a positive tolerance](https://github.com/sshekhar17/WeightedWoRConfSeq/blob/a834e459a47f9efa74fa1706f1b1dd8173ffa30b/src/weightedCSsequential.py#L249-L278). On the initial zero array this is zero.
3. [The released run loop leaves the first raw betting bounds at `[0,1]`](https://github.com/sshekhar17/WeightedWoRConfSeq/blob/a834e459a47f9efa74fa1706f1b1dd8173ffa30b/src/weightedCSsequential.py#L442-L487).
4. [`predictive_correction1` intersects those bounds with the logical interval and optionally takes the running intersection](https://github.com/sshekhar17/WeightedWoRConfSeq/blob/a834e459a47f9efa74fa1706f1b1dd8173ffa30b/src/utils.py#L240-L282).

Relevant paper facts:

5. Definition 2 defines `q_t` as a probability distribution on the remaining
   set; it does not state strict positivity.
6. Proposition 2 optimizes over the simplex of distributions supported on the
   remaining set.
7. Remark 5 explicitly discusses deterministic sampling and says it convinces
   an observer once the weights of the unrevealed items sum to `epsilon`.

The exact verifier does not import or modify that code. It implements only the
consequences needed for `N=2`, using rational arithmetic and no numerical
tolerances. It exposes support conventions as explicit verifier options rather
than silently choosing one.

## Arbitrary-`N` theorem and implementation corollary

The general sharp theorem uses the paper's exact non-control-variate wealth
update and importance payoff `pi_i*f_i/q_i`, logical correction, and running
intersection. It assumes only that the predictable valid stakes have a finite
uniform absolute bound `L`. The two rational witness candidates belong to the
continuous theoretical confidence set; no ApproxKelly initialization or
candidate grid is used.

The released implementation is a corollary with `delta=1/20`, stake cap `5/2`,
and `epsilon=1/(20N)`. For that corollary the witnesses also occur on an
allowed uniform grid of size `40N+1`. The source code adds `1e-15` to a
denominator as a floating-point guard. That guard is not part of the
martingale formula and is intentionally omitted from the exact-rational
theorem and Bellman engine.

Machine tests verify every possible count of preceding small-item reviews,
the continuous witness inequalities, the general wealth condition for several
risk limits and caps, and the released grid specialization. Claims about
bit-for-bit floating-point behavior for astronomically small probabilities are
outside scope.
