# Exact proof

## First-round lemma

In the released ApproxKelly implementation, the previous-payoff array is
initialized to zero. Thus the first numerator and denominator used by the
ApproxKelly ratio are both zero up to the positive numerical smoothing term,
and the returned first bet is exactly `lambda_1 = 0`.

Therefore, for every candidate total `m`,

```text
W_1(m) = 1 + lambda_1 (Z_1 - mu_1(m)) = 1.
```

Because `delta in (0,1)`, one has `1 < 1/delta`, so no candidate in `[0,1]` is
rejected by the first-round betting CS. After intersecting with the logical CS,

```text
C_1 = [pi_I f_I, pi_I f_I + sum_{j != I} pi_j].
```

Its diameter is exactly the total remaining transaction weight.

## Certified instance

Take

```text
N = 2,
pi = (3/4, 1/4),
f = (1/3, 1),
epsilon = 1/3,
delta = 1/20.
```

Both monetary contributions are `1/4`. Thus the repeated oracle's first-round
distribution is `(1/2,1/2)`, while prop-M's is `(3/4,1/4)`.

If item 1 is sampled, the remaining weight and first-round diameter are `1/4`,
so the audit stops at time 1. If item 2 is sampled, they are `3/4`, so the audit
does not stop at time 1. At time 2 every value is known and the logical CS has
diameter zero. Hence, for any policy that samples item 1 first with probability
`q`,

```text
E[tau] = q * 1 + (1-q) * 2 = 2-q.
```

It follows exactly that

```text
E[tau_oracle] = 2 - 1/2 = 3/2,
E[tau_prop-M] = 2 - 3/4 = 5/4,
5/4 < 3/2.
```

This is a strict gap of `1/4` and disproves the universal global-optimality
claim.

## Parametric family

Let `p` be any rational number in `(1/2,1)`, and set

```text
pi = (p, 1-p),
f = ((1-p)/p, 1).
```

The two contributions are equal to `1-p`, so the oracle is uniform. Choose any
rational `epsilon` with

```text
1-p <= epsilon < p
```

and any rational `delta in (0,1)`. Exactly the same history analysis gives

```text
E[tau_oracle] = 3/2,
E[tau_prop-M] = 2-p,
E[tau_oracle] - E[tau_prop-M] = p-1/2 > 0.
```

Thus the certificate is one member of an infinite rational family, not an
isolated numerical accident.
