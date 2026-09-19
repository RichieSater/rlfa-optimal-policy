# Strict support and attainment: correction dated September 19, 2026

The earlier general assertion that strict support always makes the optimal
value one unattained was false. The factor-N and cost proofs establish infima;
neither relies on universal nonattainment.

An exact attained example uses

```text
N=2, delta=1/20, L=1, epsilon=1/40,
pi=(79/80,1/80), f=(1/79,1),
q=(1679/1680,1/1680).
```

Set the first stake to zero for m <= epsilon and one for m > epsilon;
set all later stakes to zero. These predictable stakes have uniform cap one
and are valid for any possible nonnegative importance observation Z, since
1+Z-m >= 0 for m in [0,1].

On the large-first branch the logical interval is [1/80,1/40], throughout
which the stake is zero. On the small-first branch Z=21; all m>epsilon have
wealth 22-m >=21>20 and are rejected, whereas all m<=epsilon have wealth one.
Intersecting with the logical interval [1/80,1] again gives [1/80,1/40].

Both branches stop in one review and retain the true total 1/40. Thus full
support attains expected review count one and, for unit costs, cost one.
The construction also satisfies (1+2L epsilon)^2=(21/20)^2<20.

The exact rational regression is `tests/test_strict_support_attainment.py`.
The mathematical inequalities above cover the continuous candidate range.

Nonattainment remains correct for the zero-first-stake two-item problem when
only one first draw has logical width at most epsilon. That separate result
and its existing certificates remain valid.
