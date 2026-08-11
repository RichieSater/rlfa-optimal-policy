# Scope and nonclaims

## What is proved

The repeated `pi_i f_i` oracle is not globally optimal for expected audit
length under the explicitly pinned ApproxKelly-plus-logical construction. The
complete `N=2` problem is solved, including boundary and strict-support
conventions.

The failure is sharp for arbitrary finite populations. At the fixed risk limit
`delta=1/20`, a rational `N`-transaction family has

```text
E[tau_oracle] = 1 + (N-1)/(1+rho),
V_star = 1.
```

Letting `rho` decrease to zero makes the ratio approach the universal horizon
bound `N`. Perfect point scores do not repair the problem: `S=f` makes prop-MS
equal the oracle on this family.

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

## What is not proved

- The original UAI paper is not being corrected: it proves one-step surrogate
  optimality, not global expected-stopping-time optimality.
- The repository does not analyze a betting CS used without the logical CS.
- It does not claim that prop-M is globally optimal.
- It does not claim that uncalibrated point scores define a valid uncertainty
  class. The AI theorem requires simultaneous intervals or a deterministic
  multiplicative guarantee.
- It does not prove that certified-interval priority minimizes the stopping
  time of the intersection with every nontrivial betting CS. It exactly solves
  the box-certificate component and gives a valid hybrid risk allocation.
- It does not solve the continuous-action augmented-state Bellman problem. The
  supplied finite-grid/action-mesh solver is exact only for its discretization.
- It does not provide a novelty guarantee. Two focused searches and an updated
  source comparison are recorded, but independent expert review remains
  necessary.
- Synthetic benchmarks are stress tests, not empirical estimates for any
  audit firm, client, industry, or regulator.

## Why the mechanism matters

The one-step oracle eliminates variance in the next importance-weighted
monetary contribution. The stopping rule also has a terminal component whose
width depends on remaining recorded-value or certified-uncertainty mass. Those
objectives can point in opposite directions. The arbitrary-`N` family proves
that the mismatch can be maximal, while the interval theorem gives an exact
policy when certified predictive uncertainty is available.

## Remaining research questions

1. derive a continuous-action approximation theorem for the augmented-state
   Bellman equation;
2. determine whether a scalar index can balance betting-wealth growth,
   recorded-value coverage, and certified predictive uncertainty;
3. replace coordinate boxes by calibrated correlated uncertainty sets without
   losing computational tractability;
4. validate the certainty-stratum hybrid on appropriately authorized audit
   populations and through independent statistical and audit-methodology
   review.
