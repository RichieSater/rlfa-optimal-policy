# Completed offensive research program

The `N=2` result identifies the terminal-value defect in the one-step oracle.
The finished project separates three questions that should not be conflated.

## A. Bounded-betting RLFA

For every fixed risk limit and every uniformly bounded predictable betting
strategy in the original non-control-variate class, the paper gives a sharp
arbitrary-population lower bound for the repeated contribution oracle. The
construction controls the probabilistic confidence sequence, logical interval,
and running intersection. It proves the exact worst-case review-count ratio and
the exact bounded-heterogeneity review-cost ratio. The released ApproxKelly
implementation is a corollary, not the theorem's boundary.

The augmented state and finite-grid/action-mesh transition remain documented
in [`bellman.md`](bellman.md). That solver is verification and structure
discovery, not a continuous-action solution.

## B. Certified AI uncertainty

Point scores alone do not describe what remains uncertain. The operational
input is a simultaneous uncertainty box

```text
F(l,u) = {f : l_i <= f_i <= u_i for every i}.
```

After auditing a set `A`, the exact range of total monetary misstatement has
width

```text
D(A) = sum_{i not in A} pi_i (u_i-l_i).
```

Auditing in nonincreasing `d_i=pi_i(u_i-l_i)` is pathwise minimax-optimal under
unit costs. Heterogeneous costs form an exact covering-knapsack problem. The
calibration-separation corollary shows on one population that scores can equal
the realized taints while randomized point-score sampling approaches the sharp
negative bounds and simultaneous intervals identify a one-review optimum.

## C. Hybrid risk-limiting audits

A simultaneous `(1-delta_AI)` score box can be intersected with a conditionally
valid `(1-delta_CS)` sequential confidence sequence. A union bound gives total
failure probability at most `delta_AI+delta_CS`, without independence. A
practical architecture can:

1. audit a certainty stratum selected by certified dollar uncertainty;
2. run randomized confidence-sequence sampling on the residual population;
3. intersect the score-box, logical, and betting intervals at every round.

The risk split must be explicit, and an uncalibrated point score must never be
treated as a confidence guarantee.

## Publication threshold and freeze

The project now contains:

1. a sharp arbitrary-`N` bounded-betting theorem;
2. matching review-count and review-cost constructions and upper bounds;
3. an exact minimax ordering theorem and heterogeneous-cost solver for
   simultaneous intervals;
4. machine-checkable rational certificates, independent verifiers, and
   exhaustive small-grid tests;
5. reproducible synthetic stress tests and a candid novelty/scope audit.

No additional offensive extension belongs in this paper. Continuous actions,
correlated uncertainty, multiple-account materiality allocation, and field data
are separate projects. The current work moves to adversarial review.
