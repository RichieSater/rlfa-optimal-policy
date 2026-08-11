# Focused literature and novelty check

Search date: **2026-08-11**.

## Bottom line

The original UAI 2023 paper clearly distinguishes its one-step surrogate from
the difficult multistage policy problem. The focused search below did not find
a later paper proving or disproving global optimality of the repeated
`pi_i f_i` rule for the released RLFA construction. That is evidence of an open
gap, not a proof of novelty.

## Primary sources

- [Shekhar et al., *Risk-limiting financial audits via weighted sampling without replacement*](https://proceedings.mlr.press/v216/shekhar23a.html)
  — defines the RLFA construction, the logical CS, ApproxKelly, and Proposition
  2's one-step rule.
- [Supplementary material](https://proceedings.mlr.press/v216/shekhar23a/shekhar23a-supp.pdf)
  — proves Proposition 2 and links the released implementation.
- [Authors' source repository](https://github.com/sshekhar17/WeightedWoRConfSeq)
  — pins the first-round initialization used in this result.
- [Waudby-Smith and Ramdas, *Confidence sequences for sampling without replacement*](https://arxiv.org/abs/2006.04347)
  — predecessor for finite-population confidence sequences.
- [CMU Accounting AI Research Lab](https://www.cmu.edu/tepper/accounting-lab/research/index.html)
  — listed “Optimal Dynamic Sampling in Auditing” as an active project at the
  search date.

## Ten search angles executed

1. `Shekhar Xu Lipton Liang Ramdas risk-limiting financial audits UAI 2023 PMLR PDF`
2. `PMLR optimal dynamic sampling auditing confidence sequence betting rule finite population`
3. `site:github.com Shekhar Xu Lipton Liang Ramdas risk limiting financial audits code`
4. `"more complete characterization of the optimal policy" auditing`
5. `adaptive weighted sampling without replacement confidence sequence financial audit oracle q_i pi_i f_i`
6. `optimal expected stopping time finite population adaptive sampling dynamic programming confidence sequence`
7. `active hypothesis testing optimal expected sample size Chernoff allocation finite populations exact dynamic programming`
8. `optimal survey sampling without replacement sequential variance adaptive inclusion probabilities exact`
9. `Carnegie Mellon Accounting AI Research Lab "Optimal Dynamic Sampling in Auditing"`
10. `"Risk-limiting financial audits via weighted sampling without replacement" citations 2024 2025`

The search also checked the exact title in OpenAlex. Its record reported zero
citing works on the search date, but bibliographic indexes can be incomplete or
delayed.

## Adjacent literature found

The searches surfaced classical dynamic programming for sequential sampling,
optimal stopping for interval estimation, active hypothesis testing, unequal-
probability sampling without replacement, and election-audit betting methods.
None of the located works analyzed this exact combination of importance-
weighted betting CS, released ApproxKelly initialization, logical intersection,
and finite-population expected stopping time.

## Required follow-up before publication

- Search MathSciNet, zbMATH, Web of Science, and Google Scholar citation graphs.
- Ask the original authors whether this precise two-item mechanism is known or
  intentionally excluded by a convention not explicit in the paper/code.
- Have a sequential-analysis researcher audit the pinned construction and the
  interpretation of expected audit length.
