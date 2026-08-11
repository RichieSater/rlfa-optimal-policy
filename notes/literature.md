# Focused literature and novelty check

Search date: **2026-08-11**.

## Bottom line

The original UAI 2023 paper clearly distinguishes its one-step surrogate from
the difficult multistage policy problem. The focused search below did not find
a later paper giving the exact `N=2` characterization proved in this repository
or resolving global optimality of the repeated `pi_i f_i` rule for the released
RLFA construction. A second ten-angle search for certified AI intervals,
finite-population active sampling, and 2024--2026 sequential-audit work did not
locate the sharp factor-`N` oracle lower bound or the exact
`pi_i(u_i-l_i)` box-certificate ordering. A third ten-angle search focused on
heterogeneous observation costs, controlled sensing, and robust query
optimization found important adjacent work but not the sharp
`1+(N-1)kappa` RLFA review-cost ratio. That is evidence of an open gap, not a
proof of novelty.

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
- [Imberg, Yang, Flannagan, and Bärgman, *Active Sampling: A Machine-Learning-Assisted Framework for Finite Population Inference with Optimal Subsamples*](https://doi.org/10.1080/00401706.2024.2374554)
  — optimizes an asymptotic-MSE importance-sampling objective and explicitly
  incorporates predictive variance. It does not optimize RLFA stopping time or
  a simultaneous box certificate.
- [Kato and Nakagawa, *Sequential Audit Sampling with Statistical Guarantees*](https://arxiv.org/abs/2604.06116)
  — studies exact sequential boundaries and expected stopping time for binary
  finite-population deviation-rate auditing. It expressly excludes monetary
  misstatement sampling and does not use weighted AI-guided actions.
- [Imberg, Jonasson, and Axelson-Fisk, *Optimal Sampling in Unbiased Active Learning*](https://proceedings.mlr.press/v108/imberg20a.html)
  — shows why deterministic and probabilistic uncertainty sampling must be
  judged against the inferential objective; its target is predictive
  performance, not a risk-limiting finite-population total.
- [Naghshvar and Javidi, *Active Sequential Hypothesis Testing*](https://arxiv.org/abs/1203.4626)
  — uses dynamic programming and asymptotic information-acquisition bounds for
  controlled hypothesis testing. It is not weighted finite-population
  estimation without replacement and does not give the RLFA ratio here.
- [Vershinin, Cohen, and Gurewitz, *Active Sequential Hypothesis Testing with Non-Homogeneous Costs*](https://arxiv.org/abs/2509.11632)
  — shows in a different active-testing model that optimizing information per
  cost myopically can be suboptimal. Its hypotheses, repeated actions, and
  asymptotic objective differ from the exact finite-population construction.
- [Nitinawarat and Veeravalli, *Controlled Sensing for Sequential Multihypothesis Testing with Controlled Markovian Observations and Non-Uniform Control Cost*](https://arxiv.org/abs/1310.1844)
  — studies general control costs and asymptotically optimal sequential tests,
  not an RLFA confidence-set stopping rule.
- [Goerigk et al., *The robust knapsack problem with queries*](https://doi.org/10.1016/j.cor.2014.09.010)
  — studies querying uncertain item weights under a query budget. It is an
  algorithmic neighbor but has a different robust objective; it does not imply
  the modular simultaneous-box audit certificate.
- [PCAOB AS 2315 (effective December 15, 2026)](https://pcaobus.org/oversight/standards/auditing-standards/details/as-2315--audit-sampling-%28effective-on-12-15-2026%29)
  — says sample efficiency concerns achieving the same objective with a
  smaller sample, discusses relative cost and effectiveness, distinguishes
  individually examined items from the residual sampled population, and
  requires items in a representative sample to have an opportunity for
  selection. This is operational context for, not a proof of, the proposed
  certainty-stratum-plus-random-residual architecture.
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

The closest new finite-population paper is Imberg et al. Their Proposition 2
selects importance probabilities using both predicted means and prediction
covariances to minimize expected asymptotic MSE. That is an important
conceptual neighbor: it confirms that prediction uncertainty, not just point
scores, should influence sampling. The result here is different in three
testable ways: it uses simultaneous coordinate intervals, optimizes the exact
number or cost of manual reveals needed for an interval-width certificate, and
obtains a pathwise finite-`N` optimum rather than an asymptotic variance
surrogate.

Kato and Nakagawa is the closest sequential-audit paper found after the
original 2023 RLFA work. Its hypergeometric binary model, uniform random order,
and hypothesis-testing objective do not cover weighted monetary totals or
adaptive transaction-selection distributions.

## Second ten-angle search

The expansion executed searches spanning exact-title citation follow-up;
financial-audit ML sampling; certainty strata and current audit standards;
optimal inspection of box uncertainty; active feature acquisition; conformal
or simultaneous prediction intervals for finite populations; robust audit
selection; active finite-population inference; and 2026 sequential-audit
methods. Search results and source snapshots were reviewed on **2026-08-11**.

## Third ten-angle search: effort and bounded betting

The final search used these angles:

1. RLFA sampling cost and optimal policy;
2. financial-audit sampling with heterogeneous review costs;
3. adaptive without-replacement confidence sequences with observation costs;
4. cost-sensitive active learning in finite populations;
5. PCAOB sample efficiency and relative cost/effectiveness;
6. sequential hypothesis testing with heterogeneous action costs;
7. stochastic-shortest-path sampling for confidence intervals;
8. box uncertainty, inspection, and covering knapsack;
9. exact-title citation follow-up for the 2023 RLFA paper;
10. bounded-stake betting confidence sequences and optimal sampling.

The closest results optimize different hypothesis-testing, asymptotic-MSE, or
robust-query objectives. None located states the exact RLFA terminal-rank cost
construction, its matching total-cost upper bound, or the continuous-set
bounded-betting witness theorem. The search does not establish novelty.

## Required follow-up before publication

- Search MathSciNet, zbMATH, Web of Science, and Google Scholar citation graphs.
- Ask the original authors whether the arbitrary-`N` mechanism or
  box-certificate policy is known, and whether a support convention
  intentionally excludes the boundary policy.
- Have a sequential-analysis researcher audit the continuous-set
  bounded-betting construction, sharp cost bound, and interpretation of
  expected audit length.
- Have an audit-methodology expert assess how a calibrated AI interval can be
  documented as other audit evidence and how the certainty stratum should be
  separated from the representative residual sample under applicable rules.
