# Exact `N=2` solution

## First-round lemma

In the released ApproxKelly implementation, the previous-payoff array is
initialized to zero. Thus the returned first bet is exactly `lambda_1 = 0`.
For every candidate total `m`,

```text
W_1(m) = 1 + lambda_1 (Z_1 - mu_1(m)) = 1.
```

Because `delta in (0,1)`, one has `1 < 1/delta`. The first betting CS is
therefore all of `[0,1]`. After intersection with the logical CS, sampling item
`i` leaves an interval of diameter

```text
1 - pi_i.
```

This statement is independent of `f`, `delta`, and the first sampling
distribution.

## Complete characterization

For `N=2`, define the first-round stopping set

```text
A = {i : 1 - pi_i <= epsilon}.
```

If the first distribution is `q`, the audit stops at time 1 with probability
`sum_{i in A} q(i)`. Every other history audits the remaining item and stops at
time 2 because the logical CS is then a singleton. Hence

```text
E_q[tau] = 2 - sum_{i in A} q(i).                 (1)
```

Equation (1) solves the literal-simplex problem exactly:

```text
V* = 2,  if epsilon < min(pi_1,pi_2),
V* = 1,  if epsilon >= min(pi_1,pi_2).
```

The complete optimizer set is:

- `A` empty: every first distribution is optimal and every audit takes two;
- `A` a singleton: put probability one on its unique item;
- `A = {1,2}`: every first distribution is optimal and every audit stops after
  one item.

Thus the optimal policy is independent of both `f` and `delta`. In the
singleton regime it audits the larger-weight transaction deterministically.

## Support conventions

The paper defines an action as a probability distribution on the remaining set
and optimizes Proposition 2 over the corresponding simplex. Read literally,
this includes boundary distributions, so the deterministic optimum is
attained.

There is nevertheless a real technical ambiguity: the generic importance-
weight identity requires positive sampling mass on every positive-contribution
item. The result under conservative conventions is:

- **Strict full support.** The same value `1` is the infimum in the singleton
  regime, but it is not attained. The family
  `q_eta=(1-eta,eta)` has `E[tau]=1+eta`.
- **Positive-contribution support.** The infimum is again `1`; it is attained in
  the singleton regime exactly when every nonstopping item has zero
  contribution.

For the certified instance both contributions are positive, so neither
conservative convention attains its infimum. Under either convention, however,
the oracle is still not optimal: increasing the probability of the stopping
item strictly reduces (1).

## Oracle-optimality criterion

Assume `m_star > 0`, so the proportional oracle is defined. If `A` is empty or
contains both items, every policy is optimal and hence so is the oracle. If
`A={k}`, then

```text
E[tau_oracle]
  = 2 - pi_k f_k / (pi_1 f_1 + pi_2 f_2).
```

Under the literal simplex, this equals the optimum `1` exactly when the
nonstopping contribution is zero. If both contributions are positive, the
exact oracle suboptimality gap is

```text
pi_j f_j / (pi_1 f_1 + pi_2 f_2),
```

where `j` is the nonstopping item.

## Certified instance

Take

```text
pi = (3/4, 1/4),
f = (1/3, 1),
epsilon = 1/3,
delta = 1/20.
```

Here `A={1}` and both contributions are `1/4`. Therefore

```text
E[tau_deterministic] = 1,
E[tau_prop-M]        = 5/4,
E[tau_oracle]        = 3/2.
```

The original counterexample remains a full-support comparison, while the exact
literal-simplex solution strengthens it to `1 < 5/4 < 3/2`.

## Infinite rational family

Let rational `p in (1/2,1)` and set

```text
pi = (p, 1-p),
f = ((1-p)/p, 1),
1-p <= epsilon < p.
```

The contributions are equal, so the oracle is uniform. The large item is the
unique first-round stopping item. Consequently,

```text
E[tau_opt]    = 1,
E[tau_oracle] = 3/2,
E[tau_prop-M] = 2-p.
```

The oracle gap from the true literal-simplex optimum is the constant `1/2`
throughout this family; its gap from prop-M is `p-1/2`.
