# Point accuracy and certified audit value can separate sharply

Use the bounded-betting family from `general-n-proof.md`, and supply point
scores that happen to equal the realized taints:

```text
S_i = f_i.
```

Prop-MS then samples with rates `pi_i S_i=pi_i f_i`, exactly the contribution
oracle. Now attach the following simultaneous intervals to those same
transactions:

```text
large item:  [0, 2*epsilon/pi_0],
small item:  [0, 1]  for every i >= 1.
```

They contain all realized taints. In particular,
`pi_0 f_0=rho*w <= 2*epsilon`, so the realized large-item taint lies below its
upper endpoint. Their dollar-weighted uncertainties are

```text
d_0 = 2*epsilon,
sum_{i>=1} d_i = sum_{i>=1} pi_i = a = epsilon/2.
```

The box starts wider than `epsilon`. No audited set omitting item 0 can stop,
because its residual contains `d_0>epsilon`. Reviewing item 0 first leaves only
`epsilon/2`, so descending certified uncertainty stops in one review and is
pathwise optimal.

Under randomized prop-MS, stopping is exactly the rank of item 0. Consequently,

```text
tau_certified = 1,
E[tau_propMS] = 1 + (N-1)/(1+rho) -> N.
```

With costs `c_0=1` and `c_i=kappa`,

```text
C_certified = 1,
E[C_propMS] = 1 + (N-1)*kappa/(1+rho)
             -> 1+(N-1)*kappa.
```

The statement is deliberately that the point scores **equal the realized
taints on this population**. It does not call the point model certified or
zero-error. The intervals, not the coincident point predictions, supply the
simultaneous uncertainty guarantee used by the audit certificate.
