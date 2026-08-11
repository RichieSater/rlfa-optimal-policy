# Exact problem pinned in this repository

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

The exact verifier requires every positive-contribution remaining transaction
to receive positive sampling mass. This is the support condition needed for
the importance-weighted observation to preserve the remaining total in
expectation. Both compared policies have full support on the certified
instance.
