# Optimal Sampling for Risk-Limiting Financial Audits

This repository proves complementary sharp negative and exact positive results about AI-guided,
finite-population financial audits:

1. **Bounded-betting theorem.** Repeating the one-step rule
   `q_t(i) proportional to pi_i f_i` can have the worst possible expected
   stopping-time approximation ratio for every risk limit and every uniformly
   bounded predictable betting strategy in the non-control-variate RLFA class:
   its worst-case supremum is exactly `N`.
2. **Sharp effort theorem.** If review costs vary by a factor at most `kappa`,
   the exact worst-case cost-ratio supremum is `1+(N-1)kappa`. Without bounded
   cost heterogeneity, there is no finite guarantee, already for `N=2`.
3. **Exact implementable policy.** If an AI system supplies simultaneous
   intervals `lower_i <= f_i <= upper_i`, audit in descending order of
   `pi_i * (upper_i-lower_i)`. This is pathwise minimax-optimal for the robust
   interval certificate for every finite population.

The project includes exact rational certificates, an exact heterogeneous-cost
solver, a finite-grid/action-mesh ApproxKelly Bellman solver, independent
verifiers, a manuscript, and reproducible benchmarks.

## Main theorem: the oracle can be maximally bad

Fix any `N >= 2`, `delta in (0,1)`, and finite uniform stake cap `L`. For every
valid predictable non-control-variate RLFA betting strategy with
`abs(lambda_t(m)) <= L`, choose a sufficiently small rational `epsilon`. There
are rational weights and taints such that

```text
V*            = 1,
E[tau_oracle] = 1 + (N-1)/(1+rho).
```

As `rho` decreases to zero, the ratio approaches `N`. Since every audit ends by
round `N`, this matches the universal upper bound.

The proof does not discard the probabilistic confidence sequence. Two
continuous-set candidate totals separated by `2*epsilon` remain below the
betting rejection threshold and inside the logical interval until one large
transaction is audited. The oracle's stopping time is therefore exactly that
transaction's Plackett–Luce rank. The argument uses neither ApproxKelly's zero
initialization nor a candidate grid. It does not cover unbounded stakes or
arbitrary control-variate constructions.

The released ApproxKelly result is the corollary
`delta=1/20`, `L=5/2`, and `epsilon=1/(20N)`.

For the checked `N=100`, `rho=1/1000` certificate:

```text
optimal expected audits       = 1
oracle expected audits        = 9091/91  = 99.901098...
prop-M expected audits        <= 396001/395902 = 1.000250...
```

If point scores happen to equal the realized taints (`S=f`), prop-MS equals the
oracle and inherits the lower bound. This statement does not call the model
certified or zero-error; it isolates the mismatch between next-draw variance
and terminal stopping value.

See [`notes/general-n-proof.md`](notes/general-n-proof.md) and
[`certificates/industry-results.json`](certificates/industry-results.json).

## Main effort theorem: no cost-independent guarantee

Let `C_tau` be total manual-review cost. Give the terminating large transaction
cost `1` and each small transaction cost `kappa >= 1`. On the same family,

```text
V_c*                = 1,
E[C_oracle]         = 1 + (N-1)kappa/(1+rho),
sharp ratio sup     = 1 + (N-1)kappa.
```

The matching upper bound is universal: after normalizing the minimum cost to
one, a complete audit costs at most `1+(N-1)kappa`, while every nontrivial audit
costs at least one. If cost heterogeneity is unrestricted, the ratio diverges
already at `N=2`.

For the checked `N=100`, `rho=1/1000`, `kappa=100` certificate:

```text
optimal expected cost = 1
oracle expected cost  = 900091/91 = 9891.109890...
sharp supremum        = 9901
```

See [`notes/general-n-proof.md`](notes/general-n-proof.md).

## Exact certified-score policy

Suppose intervals hold simultaneously:

```text
lower_i <= f_i <= upper_i,  for every transaction i.
```

After auditing a set `A`, the exact robust interval has width

```text
D(A) = sum_{i not in A} pi_i * (upper_i-lower_i).
```

Define

```text
d_i = pi_i * (upper_i-lower_i).
```

Sorting transactions by decreasing `d_i` is globally optimal. If `k*` is the
first prefix leaving residual width at most `epsilon`, no adaptive or randomized
policy can stop before `k*` on any path, and the sorted policy stops at `k*`.
Thus

```text
inf_q sup_f E_f[tau_box(q)] = k*.
```

For the multiplicative guarantee

```text
(1-a) f_i <= S_i <= (1+a) f_i,
```

the implied bounds are

```text
lower_i = S_i/(1+a),
upper_i = min(1, S_i/(1-a)).
```

Without clipping, `d_i` is proportional to `pi_i S_i`. The same score that
motivates randomized prop-MS becomes an **optimal deterministic priority** for
the robust certificate. With clipping, the exact interval width can change the
ranking.

Positive heterogeneous review costs reduce to an exact covering-knapsack
problem. The package solves it with a rational Pareto-frontier dynamic program.

```sh
uv run rlfa-optimal characterize-box \
  --pi 1/2 1/3 1/6 \
  --lower 0 0 0 \
  --upper 1 1 1 \
  --epsilon 1/2 \
  --costs 3 2 1
```

See [`notes/robust-score-theorem.md`](notes/robust-score-theorem.md).

## Same scores, different audit value

The point-score and certified-interval results can be placed on the same
population. Supply point scores equal to the realized taints, but valid
simultaneous intervals whose dollar uncertainty is `2*epsilon` on the large
transaction and totals only `epsilon/2` over all small transactions. Then

```text
certified optimal reviews       = 1
E[prop-MS reviews]              = 1 + (N-1)/(1+rho)  -> N
certified optimal review cost   = 1
E[prop-MS review cost]          = 1 + (N-1)kappa/(1+rho)
```

Prediction accuracy and certified audit value are therefore mathematically
different. The exact interval construction is in
[`notes/calibration-separation.md`](notes/calibration-separation.md).

## Original `N=2` certificate

The released ApproxKelly initialization has first bet zero. Consequently, for
`N=2` and any first distribution `q`,

```text
E_q[tau] = 2 - sum_{i: 1-pi_i <= epsilon} q(i).
```

The rational instance

```text
pi      = (3/4, 1/4)
f       = (1/3, 1)
epsilon = 1/3
delta   = 1/20
```

has exact expectations

```text
1 < 5/4 < 3/2
```

for deterministic-large-first, prop-M, and the oracle. This remains the compact
entry-point counterexample and support-convention audit.

## Bellman verification beyond `N=2`

[`src/rlfa_optimal_policy/approxkelly.py`](src/rlfa_optimal_policy/approxkelly.py)
implements the complete finite-grid state: history, wealth at every candidate,
ApproxKelly payoff accumulators, logical interval, and running intersection. It
solves

```text
V(x) = 1 + min_q sum_i q(i) V(Phi(x,q,i))
```

exactly on a stated strict-full-support probability mesh using rational
arithmetic. This is a global optimum for the discretized action set, **not** a
claim to have solved the continuous-action problem.

Exact small cases are checked in
[`benchmarks/small-exact.json`](benchmarks/small-exact.json).

## Reproduce everything

```sh
make install
make check
make certificate
make benchmark
make paper
```

`make check` runs the test suite, verifies both JSON certificates, and runs two
independent verifiers that deliberately do not import the package.

Key artifacts:

- [`paper/main.pdf`](paper/main.pdf) — manuscript;
- [`certificates/industry-results.json`](certificates/industry-results.json) —
  sharp `N=100` and certified-score examples;
- [`certificates/counterexample.json`](certificates/counterexample.json) — exact
  `N=2` history certificate;
- [`benchmarks/certified-score-synthetic.json`](benchmarks/certified-score-synthetic.json)
  — fixed-seed `N=1000` stress tests;
- [`notes/literature.md`](notes/literature.md) — current novelty audit;
- [`notes/scope.md`](notes/scope.md) — proved claims and nonclaims;
- [`notes/adversarial-review.md`](notes/adversarial-review.md) — frozen-scope
  referee attack checklist and remaining external defense.

## Risk accounting

A simultaneous AI interval event with failure probability `delta_AI` is already
time-uniform under arbitrary adaptive auditing. Intersecting it with a betting
confidence sequence of failure probability `delta_CS` gives total failure
probability at most

```text
delta_AI + delta_CS
```

without requiring independence. Uncalibrated point scores do **not** provide
this guarantee.

The proposed deployment architecture is a certainty stratum selected by
certified dollar uncertainty, followed by randomized risk-limiting sampling on
the residual population. The repository does not claim regulatory compliance
or real-world savings; those require independent expert review and authorized
audit data.

## Literature boundary

The starting paper is [Shekhar et al., UAI
2023](https://proceedings.mlr.press/v216/shekhar23a.html). It proves one-step
surrogate optimality and explicitly leaves the multistage policy problem open;
it does not state the global-optimality conjecture verbatim.

The novelty review also covers finite-population active sampling, cost-sensitive
sequential testing, robust query optimization, and 2026 sequential audit
sampling. No located work gives the bounded-betting factor-`N` theorem, sharp
RLFA review-cost ratio, or exact certified-box ordering, but a literature search
is not a novelty guarantee. See [`notes/literature.md`](notes/literature.md).

## License

MIT. See [`LICENSE`](LICENSE).
