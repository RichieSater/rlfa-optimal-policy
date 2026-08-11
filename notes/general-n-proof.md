# Sharp review-count and review-cost lower bounds

This note proves that the repeated Proposition-2 contribution oracle has the
worst possible finite-horizon approximation ratio. The result is not tied to
ApproxKelly initialization or to a numerical candidate grid.

## Confidence-sequence class

Fix:

```text
N >= 2,       delta in (0,1),       L < infinity.
```

Consider any valid predictable betting strategy in the original
non-control-variate RLFA wealth class

```text
W_t(m) = W_{t-1}(m) [1 + lambda_t(m)(Z_t-mu_t(m))],   W_0(m)=1,
```

with a uniform bound `abs(lambda_t(m)) <= L`. The usual stake constraint that
keeps every wealth factor nonnegative remains in force. Intersect the betting
set with the logical interval and take running intersections as in Shekhar et
al. The theorem does not prescribe how the bounded predictable stakes are
chosen.

Choose any positive rational `epsilon` satisfying

```text
epsilon < 1/3,
(1 + 2 L epsilon)^N < 1/delta.
```

Such a rational always exists. Fix `rho in (0,1]`, put

```text
a = epsilon/2,             w = a/(N-1),
pi_0 = 1-a,                pi_i = w              (i >= 1),
f_0 = rho*w/(1-a),         f_i = 1               (i >= 1).
```

The contributions are `rho*w,w,...,w`, all strictly positive.

## Lemma: two candidates survive until item 0

Use the continuous candidate set and define

```text
m_- = a,                   m_+ = 5a.
```

Their separation is `4a=2*epsilon`. If `k` small items have been audited but
item 0 has not, the logical lower endpoint is `k*w <= a`, while the logical
upper endpoint is at least `pi_0 > 5a`; the last inequality is equivalent to
`epsilon < 1/3`. Both witnesses therefore remain in the logical interval.

Under contribution-proportional oracle sampling, let `C_R` be the remaining
true contribution and let `A` be the contribution already observed. For every
possible next item,

```text
Z_t = (pi_i f_i)/(pi_i f_i/C_R) = C_R,
Z_t-mu_t(m) = C_R-(m-A) = m_star-m.
```

Thus the payoff at a fixed candidate is independent of which item is drawn.
Here `m_star=a+rho*w`, so both witnesses satisfy

```text
abs(m_star-m_-) < 2*epsilon,
abs(m_star-m_+) < 2*epsilon.
```

For every valid bounded bet, each nonnegative wealth factor at either witness
is at most `1+2*L*epsilon`. Hence, before item 0 is reviewed,

```text
W_t(m_-) and W_t(m_+)
    <= (1+2*L*epsilon)^t
    <= (1+2*L*epsilon)^N
    < 1/delta.
```

Neither candidate can be rejected. Because both survive the logical interval
at every preceding round, the running intersection retains both and has
diameter at least `2*epsilon > epsilon`.

Once item 0 is reviewed, at most total recorded weight `a=epsilon/2` remains,
so the logical interval forces stopping. Therefore the oracle stopping time is
exactly the rank of item 0.

## Sharp review-count theorem

Sequential probability-proportional sampling is a Plackett--Luce order,
equivalently an order of independent exponential clocks. Every small item
precedes item 0 with probability

```text
w/(w+rho*w) = 1/(1+rho).
```

Linearity of expectation gives

```text
E[tau_oracle] = 1 + (N-1)/(1+rho).
```

Auditing item 0 first leaves logical width `a <= epsilon`, so the
literal-simplex optimum is one under **every** betting strategy in the stated
class. No zero first bet is needed. Under strict full support, one is the
unattained infimum obtained by assigning item 0 first-round probability
`1-eta` and sending `eta` to zero.

Every without-replacement audit ends by round `N`, and every nontrivial audit
uses at least one review. The oracle-to-optimal review-count ratio is therefore
at most `N` on every instance, while the construction approaches `N` as
`rho` decreases to zero. Its worst-case supremum is exactly `N`.

### Released ApproxKelly corollary

Take

```text
delta = 1/20,       L = 5/2,       epsilon = 1/(20N).
```

Then

```text
(1+2*L*epsilon)^N = (1+1/(4N))^N < exp(1/4) < 20.
```

This recovers the released ApproxKelly result, but zero initialization is now
irrelevant. The two witnesses also happen to lie at indices 1 and 5 of the
allowed uniform grid with `40N+1` points. The general theorem itself uses the
continuous candidate set and no implementation grid.

## Sharp heterogeneous review-cost theorem

Let reviewing item `i` cost `c_i>0`, and define

```text
C_tau = sum_{t=1}^tau c_{I_t}.
```

On the construction, set

```text
c_0 = 1,                    c_i = kappa  (i >= 1),
```

where `kappa >= 1`. Because stopping is exactly the rank of item 0,

```text
E[C_oracle]
  = c_0 + sum_{i=1}^{N-1} c_i P(i precedes 0)
  = 1 + (N-1)*kappa/(1+rho).
```

Reviewing item 0 first costs one and stops, so `V_c^star=1` (or has infimum one
under strict full support). Letting `rho` decrease to zero makes the ratio tend
to

```text
1 + (N-1)*kappa.
```

This is the exact worst-case supremum whenever
`max_i c_i / min_i c_i <= kappa`. To prove the matching upper bound, normalize
`min_i c_i=1`. Any audit costs at most the total cost of all items, which is at
most `1+(N-1)*kappa`, while every nontrivial audit costs at least one.

With no bound on cost heterogeneity there is no finite guarantee, already for
`N=2`: at any fixed `rho>0`, the ratio

```text
1 + kappa/(1+rho)
```

diverges as `kappa` grows.

The unit-cost result is the special case `kappa=1`.

## Exact boundary

The theorem covers every risk limit, every finite uniform bet cap, arbitrary
bounded predictable stake initialization, and the continuous non-control-
variate RLFA confidence set with logical and running intersections. It does
**not** cover betting strategies without a finite uniform cap or every
control-variate wealth construction. Those are explicit nonclaims.
