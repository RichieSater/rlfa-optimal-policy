# A sharp arbitrary-population lower bound for the one-step oracle

This note proves that the repeated Proposition-2 oracle has the worst possible
finite-horizon approximation ratio even when the risk limit is fixed at
`delta=1/20`.  The proof controls both pieces of the released combined
confidence sequence; it does not assume that the betting interval is absent.

## Construction

Fix `N >= 2` and `rho in (0,1]`.  Put

```text
epsilon = 1/(20N),       a = epsilon/2,
pi_0 = 1-a,              pi_i = a/(N-1),  i >= 1,
f_0 = rho*pi_i/pi_0,     f_i = 1,          i >= 1,
delta = 1/20.
```

Write `w=a/(N-1)`.  The monetary contributions are `rho*w` for item 0
and `w` for every other item.  Every contribution is positive.

The released grid size can be set to `40N+1`.  Its grid then contains

```text
m_- = a = 1/(40N),       m_+ = 5a = 1/(8N),
```

whose separation is `2*epsilon`.

## Lemma 1: the two witnesses survive until item 0 is audited

Suppose item 0 has not been sampled.  If `k` small items have been sampled,
the logical lower endpoint is `kw <= a`, while the logical upper endpoint is
at least the remaining weight `pi_0`.  Hence both `m_-` and `m_+` belong to
the logical interval.

Under oracle sampling, let `C_R` be the sum of the remaining monetary
contributions and `L` the observed monetary contribution.  For every sampled
item `i`,

```text
Z = (pi_i f_i)/(pi_i f_i/C_R) = C_R.
```

Since `C_R=m_star-L` and the candidate residual mean is `m-L`, the payoff is

```text
Z-(m-L) = m_star-m.
```

It is constant across the possible next items.  Here

```text
m_star = a+rho*w.
```

For either witness, `|m_star-m| < 2*epsilon`.  The released implementation
caps every ApproxKelly bet at absolute value `5/2`, so each nonnegative wealth
factor is at most

```text
1 + (5/2)(2*epsilon) = 1 + 1/(4N).
```

Consequently, through the whole horizon,

```text
W_t(m_-) and W_t(m_+)
    <= (1+1/(4N))^N
    < exp(1/4)
    < 2
    < 20 = 1/delta.
```

Neither candidate is rejected by the betting CS.  Because both candidates
also survive the logical interval at every preceding round, the running
intersection contains both.  Its diameter is therefore at least
`2*epsilon > epsilon`, and the audit cannot stop before item 0 is sampled.

When item 0 is sampled, the remaining total monetary weight is at most
`a=epsilon/2`; the logical interval then has width at most `epsilon` and the
audit stops.  The stopping time is exactly the rank of item 0.

## Lemma 2: exact oracle expectation

Sequential sampling proportional to fixed positive rates is a
Plackett--Luce ordering, equivalently the ordering of independent exponential
clocks with those rates.  The expected rank of item 0 is

```text
1 + sum_{i=1}^{N-1} P(clock_i < clock_0)
= 1 + sum_{i=1}^{N-1} w/(rho*w+w)
= 1 + (N-1)/(1+rho).
```

## Theorem: sharp factor `N`

Auditing item 0 first makes the first-round logical width `a <= epsilon`.
The released first bet is zero, so this deterministic policy stops in one
audit.  Thus the literal-simplex optimum is exactly one, whereas

```text
E[tau_oracle] = 1 + (N-1)/(1+rho).
```

Every audit stopping time lies between 1 and `N`, so no policy can have an
approximation ratio exceeding `N` relative to an optimum of at least one.  As
`rho` decreases to zero, the displayed oracle expectation increases to `N`.
Therefore the worst-case approximation-ratio supremum of the repeated oracle
is exactly `N`.

All oracle actions have strict full support for every `rho>0`.  Under a strict
full-support convention for competing policies, the optimal value one is an
infimum: put probability `1-eta` on item 0 at the first round and use any
fully supported continuation.  Its expected length is at most
`1+eta(N-1)`, which tends to one.  The same sharp ratio holds relative to this
infimum.

## Prop-M and perfect-score comparison

Under prop-M, stopping occurs no later than the rank of item 0.  Its expected
rank is

```text
1 + (N-1) w/(pi_0+w)
= 1 + a/(pi_0+w)
< 1/pi_0.
```

This approaches one in the family, while the oracle approaches `N`.  If an AI
score is perfect, `S_i=f_i`, then prop-MS is exactly the oracle and inherits
the same lower bound.  The example therefore isolates a practical failure:
perfect ranking of monetary misstatement contribution can be maximally bad
for a stopping rule with a terminal residual-mass condition.

## Scope

The theorem uses the paper's mathematical betting construction and a uniform
grid allowed by the released implementation (`nG=40N+1`).  It fixes the
released ApproxKelly cap `lambda_max=5/2`, zero initialization, logical
intersection, and running intersection.  It is a worst-case structural result,
not a claim that typical audit populations attain the bound.
