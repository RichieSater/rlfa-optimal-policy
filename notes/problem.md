# Exact problems pinned in this repository

Let a finite population have positive normalized weights `pi_i`, fixed
misstatement fractions `f_i in [0,1]`, and total misstatement

```text
m_star = sum_i pi_i f_i.
```

At each round an auditor samples one unobserved transaction from a predictable
distribution `q_t`, observes its `f_i`, updates a confidence sequence, and
stops when the confidence-set diameter is at most `epsilon`.

Shekhar et al. prove that the one-step variance surrogate is minimized by

```text
q_t(i) proportional to pi_i f_i.
```

They explicitly describe the full policy problem as a multistage optimization
that is difficult to characterize. The derived conjecture investigated here is:

> Does repeating this one-step oracle minimize expected stopping time over all
> adaptive without-replacement policies for every finite instance?

## Construction fixed here

The stopping rule must be pinned before an expected-length comparison is
mathematically definite. This repository uses:

1. the betting CS from the UAI 2023 paper;
2. the ApproxKelly betting rule with the initialization in the authors'
   released code (commit `a834e459a47f9efa74fa1706f1b1dd8173ffa30b`), for
   which the first bet is zero;
3. intersection with the logical CS and the running intersection, as in
   equation (6) and the released `predictive_correction1` routine;
4. stopping at the first `t >= 1` with diameter at most `epsilon`.

For `N=2`, no numerical grid or root finder enters the proof. The zero first bet
makes the first betting CS exactly `[0,1]`, and a complete audit makes the
logical CS a singleton.

## Admissible policies

Definition 2 calls `q_t` a probability distribution on the remaining set, and
Proposition 2 optimizes over the simplex of such distributions. The literal
simplex includes boundary actions, including deterministic sampling. Remark 5
also discusses deterministic strategies and says they convince the observer
once the unrevealed weights sum to at most `epsilon`—exactly what happens here.

The paper does not explicitly state a full-support condition. Its generic
importance-weight identity does require mass on every item with positive fixed
contribution, however. The repository therefore reports three conventions:

1. literal simplex, including deterministic actions;
2. support on every positive-contribution item;
3. strict support on every remaining item.

The exact value is `1` under the literal simplex and is still the infimum under
both conservative conventions. Attainment is recorded separately.

## Arbitrary-`N` performance question

The repository also asks for the worst-case approximation ratio of the
repeated oracle relative to the stopping-time optimum. The result is sharp:
at fixed `delta=1/20`, the ratio supremum over `N`-transaction instances is
`N`. See [`general-n-proof.md`](general-n-proof.md). This theorem uses the
mathematical importance payoff rather than a floating-point denominator guard.

## Certified-score minimax question

For the implementable extension, point scores are replaced by a simultaneous
box `lower_i <= f_i <= upper_i`. The stopping interval is the exact image of
that box after each reveal. The unit-cost problem is

```text
inf_q sup_{f in box} E_f[tau_box(q)].
```

It is solved exactly by descending `pi_i*(upper_i-lower_i)`. This is a
different, risk-zero conditional certificate from the full betting-CS Bellman
problem; the two can be intersected with an explicit risk split.
