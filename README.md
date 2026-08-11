# Optimal Sampling for Risk-Limiting Financial Audits

This repository proves two complementary results about AI-guided,
finite-population financial audits:

1. **Sharp negative theorem.** Repeating the one-step rule
   `q_t(i) proportional to pi_i f_i` can have the worst possible expected
   stopping-time approximation ratio: its worst-case supremum is exactly `N`.
2. **Exact implementable policy.** If an AI system supplies simultaneous
   intervals `lower_i <= f_i <= upper_i`, audit in descending order of
   `pi_i * (upper_i-lower_i)`. This is pathwise minimax-optimal for the robust
   interval certificate for every finite population.

The project includes exact rational certificates, an exact heterogeneous-cost
solver, a finite-grid/action-mesh ApproxKelly Bellman solver, independent
verifiers, an 8-page manuscript, and reproducible benchmarks.

## Main theorem: the oracle can be maximally bad

Fix any `N >= 2` and `rho in (0,1]`. There is an exact rational instance at the
fixed risk limit `delta=1/20` such that

```text
V*            = 1,
E[tau_oracle] = 1 + (N-1)/(1+rho).
```

As `rho` decreases to zero, the ratio approaches `N`. Since every audit ends by
round `N`, this matches the universal upper bound.

The proof does not discard the probabilistic confidence sequence. Two candidate
totals separated by `2*epsilon` remain below the betting rejection threshold
and inside the logical interval until one large transaction is audited. The
oracle's stopping time is therefore exactly that transaction's Plackett–Luce
rank.

For the checked `N=100`, `rho=1/1000` certificate:

```text
optimal expected audits       = 1
oracle expected audits        = 9091/91  = 99.901098...
prop-M expected audits        <= 396001/395902 = 1.000250...
```

If scores are perfect (`S=f`), prop-MS equals the oracle and inherits the lower
bound. The failure is not prediction error; it is the mismatch between
next-draw variance and terminal stopping value.

See [`notes/general-n-proof.md`](notes/general-n-proof.md) and
[`certificates/industry-results.json`](certificates/industry-results.json).

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
- [`notes/scope.md`](notes/scope.md) — proved claims and nonclaims.

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

The novelty review also covers recent finite-population active sampling and
2026 sequential audit sampling. No located work gives the sharp factor-`N`
RLFA oracle bound or the exact certified-box ordering, but a literature search
is not a novelty guarantee. See [`notes/literature.md`](notes/literature.md).

## License

MIT. See [`LICENSE`](LICENSE).
