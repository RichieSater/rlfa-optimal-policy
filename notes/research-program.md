# Research program beyond two transactions

The `N=2` result identifies the terminal-value defect in the one-step oracle,
but a larger result needs both a sharp negative theorem and a policy that an
auditor can actually deploy.  The project therefore separates three questions
that should not be conflated.

## A. The released RLFA construction

For the ApproxKelly betting confidence sequence, logical intersection, and
default bet cap released with Shekhar et al., determine the finite-horizon
stochastic-shortest-path value

```text
V(x) = 1 + inf_q sum_i q(i) V(Phi(x,q,i)).
```

The state and transition are pinned in [`bellman.md`](bellman.md).  The first
arbitrary-population target is a sharp approximation lower bound for the
repeated one-step oracle.  The construction must control the probabilistic
confidence sequence, rather than silently replacing the combined stopping rule
by the logical interval.

## B. Certified AI scores

Point scores alone do not describe what remains uncertain.  The operational
input is a simultaneous uncertainty box

```text
F(l,u) = {f : l_i <= f_i <= u_i for every i}.
```

After auditing a set `A`, the exact range of the total monetary misstatement
over this box has width

```text
D(A) = sum_{i not in A} pi_i (u_i-l_i).
```

This produces a zero-additional-risk certificate and a fully implementable
minimax problem.  For unit audit costs, the candidate theorem is that auditing
in nonincreasing order of

```text
d_i = pi_i (u_i-l_i)
```

is globally optimal for every finite population.  The matching lower bound is
the sum of the largest `t` uncertainty contributions.  Observed values cannot
improve this box width, so adaptivity and randomization cannot beat the
deterministic ordering.

For the multiplicative score guarantee

```text
S_i/f_i in [1-a,1+a],
```

the implied interval is

```text
l_i = S_i/(1+a),
u_i = min(1, S_i/(1-a)).
```

Without clipping, `d_i` is a common constant times `pi_i S_i`.  Thus the
correct robust policy uses the same priority score as prop-MS but audits in
descending order instead of drawing proportionally to it.  With clipping, the
exact priority is the dollar-weighted interval width, not the point score.

## C. Hybrid risk-limiting audits

A simultaneous `(1-delta_AI)` score box can be intersected with an independent
or conditionally valid `(1-delta_CS)` sequential confidence sequence.  A union
bound gives total failure probability at most `delta_AI+delta_CS`.  This yields
a practical architecture:

1. audit a certainty stratum in descending `d_i` order;
2. run randomized confidence-sequence sampling on the residual population;
3. intersect the score-box, logical, and betting intervals at every round.

The theoretical and numerical work must report the risk split explicitly and
must never treat an uncalibrated AI score as a confidence guarantee.

## Publication threshold

The expanded paper is ready only if it contains all of the following:

1. an arbitrary-`N` theorem with a matching construction for the released
   RLFA oracle;
2. the exact minimax ordering theorem for certified score intervals;
3. machine-checkable finite-population certificates and exhaustive small-grid
   verification;
4. benchmarks against oracle, prop-M, prop-MS, and the new policy;
5. a focused novelty audit and a candid scope statement distinguishing the
   exact robust result from the unresolved full betting-CS Bellman problem.
