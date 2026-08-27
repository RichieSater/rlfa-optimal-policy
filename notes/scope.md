# Scope and nonclaims

## What is proved

The repeated `pi_i f_i` oracle is not globally optimal for expected audit
length. The complete released-ApproxKelly `N=2` problem is solved, including
boundary and strict-support conventions.

The failure is sharp far beyond that implementation. Fix any finite population
size `N>=2`, risk limit `delta in (0,1)`, and finite uniform stake bound `L`.
For every valid predictable non-control-variate RLFA betting strategy satisfying
`abs(lambda_t(m))<=L`, a rational family has

```text
E[tau_oracle] = 1 + (N-1)/(1+rho),
V_star = 1.
```

The proof uses the continuous candidate set, logical and running intersections,
and only the uniform stake bound. It does not use zero ApproxKelly
initialization. Letting `rho` decrease to zero makes the ratio approach the
universal horizon bound `N`.

For known review costs with `max(c)/min(c)<=kappa`, the exact worst-case
oracle-to-optimal expected-cost ratio supremum is

```text
1 + (N-1)*kappa.
```

Without bounded cost heterogeneity, there is no finite guarantee even for
`N=2`.

For simultaneously certified AI intervals `l_i <= f_i <= u_i`, the repository
solves a distinct implementable minimax problem exactly. The residual box width
is

```text
sum_{i unaudited} pi_i (u_i-l_i),
```

so descending dollar-weighted interval width is pathwise optimal for unit
review costs. An exact covering-knapsack dynamic program handles heterogeneous
costs. A union-bound risk allocation makes this certificate composable with a
betting confidence sequence.

A unifying family supplies point scores equal to the realized taints and valid
simultaneous intervals on the same transactions. Randomized prop-MS then
approaches `N` reviews and the sharp cost bound, while certified uncertainty
identifies a one-review, unit-cost optimum.

## What is not proved

- The original UAI paper is not being corrected: it proves one-step surrogate
  optimality, not global expected-stopping-time optimality.
- The bounded-betting theorem does not cover strategies without a finite
  uniform stake cap or arbitrary control-variate wealth processes.
- The repository does not analyze a betting CS used without the logical CS.
- It does not claim that prop-M is globally optimal.
- Scores that equal realized taints in the calibration family are not called a
  proved zero-error model. The simultaneous intervals carry the certificate.
- It does not claim that uncalibrated point scores define a valid uncertainty
  class. The AI theorem requires simultaneous intervals or a deterministic
  guarantee.
- It does not prove that certified-interval priority minimizes the stopping
  time of the intersection with every nontrivial betting CS. It exactly solves
  the box-certificate component and gives a valid hybrid risk allocation.
- It does not solve the continuous-action augmented-state Bellman problem. The
  supplied finite-grid/action-mesh solver is exact only for its discretization.
- It does not provide a novelty guarantee. Focused searches and source
  comparisons are recorded, but they do not establish priority.
- Synthetic benchmarks are stress tests, not empirical estimates for any
  audit firm, client, industry, or regulator.

## Why the mechanism matters

The one-step oracle eliminates variance in the next importance-weighted
monetary contribution. The stopping rule also has terminal value governed by
remaining recorded-value or certified-uncertainty mass. Those objectives can
point in opposite directions. The lower bounds make the mismatch sharp in both
reviews and effort; the interval theorem gives an exact policy when certified
predictive uncertainty is available.

## Frozen offensive scope

The main claims are now frozen. Continuous-action Bellman theory, correlated
uncertainty sets, multiple-account materiality allocation, and field-data
validation are separate projects.
