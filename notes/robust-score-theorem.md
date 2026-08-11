# Exact minimax auditing from certified AI intervals

Point risk scores are not enough to support a risk guarantee.  Suppose instead
that the AI system supplies simultaneous bounds

```text
l_i <= f_i <= u_i,    i=1,...,N.
```

The event that all bounds hold may be deterministic or may have calibrated
probability at least `1-delta_AI`.

## Exact certificate

After auditing a set `A` and observing its true values, the image of the box
under the monetary-total functional is exactly

```text
[ sum_{i in A} pi_i f_i + sum_{i not in A} pi_i l_i,
  sum_{i in A} pi_i f_i + sum_{i not in A} pi_i u_i ].
```

Because the box is a Cartesian product, both endpoints are attainable.  Its
diameter is

```text
D(A) = sum_{i not in A} d_i,
d_i  = pi_i (u_i-l_i).
```

Observed values change the location but not the width.

## Unit-cost minimax theorem

Let `d_(1) >= ... >= d_(N)` be the sorted uncertainty contributions and set

```text
k_star = min {k : sum_{r=k+1}^N d_(r) <= epsilon}.
```

Auditing in descending `d_i` order stops after exactly `k_star` reviews.  No
adaptive or randomized policy can stop on any path in fewer reviews: after
`t<k_star` audits, it can have removed at most the sum of the largest `t`
values, so its residual width is still greater than `epsilon`.  Hence

```text
inf_q sup_{f in F(l,u)} E_f[tau_box(q)] = k_star,
```

and descending dollar-weighted uncertainty is a globally optimal policy.
The lower bound and construction match pathwise, not merely in expectation.

Adaptivity has zero value for this box certificate because an observation
does not alter any other coordinate's certified interval.

## Multiplicative score guarantees

The condition

```text
S_i/f_i in [1-a,1+a],    0 <= a < 1,
```

is equivalently represented by the clipped interval

```text
l_i = S_i/(1+a),
u_i = min(1, S_i/(1-a)).
```

When no upper endpoint clips at one,

```text
d_i = pi_i S_i * 2a/(1-a^2).
```

Thus the optimal deterministic priority is `pi_i S_i`: the same index that
motivates prop-MS, but used as a descending priority rather than as a
randomized probability.  If clipping occurs, the exact priority is
`pi_i(u_i-l_i)` and can differ from the prop-MS point-score ranking.

## Heterogeneous review costs

For positive manual-review costs `c_i`, the exact optimization is the covering
knapsack

```text
minimize   sum_i c_i x_i
subject to sum_i d_i x_i >= D(empty)-epsilon,
           x_i in {0,1}.
```

The repository implements an exact rational Pareto-frontier dynamic program.
It caps removed width at the target and prunes a state whenever another state
has at least as much removed width at no greater cost.  This returns a global
optimum; worst-case exponential complexity is unavoidable for general rational
covering knapsack.

## Risk accounting and hybrid CS

On the simultaneous-box event, the box interval contains `m_star` at every
time under every adaptive sampling rule.  It is therefore already a
time-uniform confidence sequence with failure probability `delta_AI`.

If it is intersected with a betting confidence sequence having failure
probability `delta_CS`, the combined sequence has simultaneous coverage at
least

```text
1-delta_AI-delta_CS
```

by a union bound.  Independence is not required.  The randomized betting
policy may depend on the pre-audit scores because the RLFA construction allows
predictable adaptive sampling.  An implementation must nevertheless allocate
the two risk budgets explicitly; an uncalibrated point prediction corresponds
to no valid `delta_AI` claim.

This theorem solves the robust certificate component exactly.  It does not
claim that the descending policy minimizes the stopping time of the
intersection with a nontrivial betting CS for every `f`; that augmented-state
Bellman problem remains separate.
