# Adversarial checks

This checklist records the most likely objections and the exact answers
supported by the current proof.

## A. Bounded-betting theorem

### A1. Is the result an ApproxKelly initialization artifact?

No. The arbitrary-`N` proof never uses the formula producing `lambda_t`, its
initial value, or previous-payoff accumulators. It uses only predictability,
valid nonnegative wealth factors, and the uniform bound
`abs(lambda_t(m))<=L`. Zero initialization remains necessary only for the
separate exact `N=2` characterization.

### A2. Is the result a candidate-grid artifact?

No. The theorem places two explicit candidates in the continuous confidence
set. The released grid is mentioned only in a corollary because it happens to
contain both candidates.

### A3. Could a bounded strategy reject a witness by choosing the sign of the
stake adversarially?

No. Under oracle sampling the payoff is the outcome-independent constant
`m_star-m`. For either sign,

```text
1 + lambda_t(m)(m_star-m)
    <= 1 + abs(lambda_t(m))*abs(m_star-m)
    < 1 + 2*L*epsilon.
```

The RLFA validity constraint keeps the factor nonnegative. Multiplying the
upper bounds through at most `N` rounds stays strictly below `1/delta`.

### A4. Do the witnesses remain in the logical interval after every possible
history?

Yes. Before item 0, a history is characterized by the number `k` of identical
small items already reviewed. The logical lower endpoint is `k*w<=a`, and the
upper endpoint is actually `1`; the proof uses the weaker bound
`pi_0>5a`. Both candidates survive for every `k=0,...,N-1`.

### A5. Does running intersection change the argument?

No. Each witness belongs to both the betting and logical sets at every
preceding time. Intersecting those sets over time therefore retains both.

### A6. Does the result cover all RLFA betting confidence sequences?

No. It covers the original single-product, non-control-variate wealth class
with a finite uniform stake cap. It does not cover unbounded stakes, arbitrary
mixtures outside that representation, or every control-variate construction.
This is a stated boundary, not an implicit generalization.

## B. Cost theorem

### B1. Why is the oracle expected cost exact?

The stopping time is exactly item 0's rank in a Plackett--Luce order. For each
small item `i`, exponential-clock comparison gives

```text
P(i precedes 0) = w/(w+rho*w) = 1/(1+rho).
```

Linearity of expectation applies to the cost indicators without requiring
independence among their events.

### B2. Why is `1+(N-1)kappa` a matching universal upper bound?

Normalize `min_i c_i=1`. At least one item costs exactly one, and every other
item costs at most `kappa`, so a full without-replacement audit costs at most
`1+(N-1)kappa`. A nontrivial audit must review at least one item and therefore
has optimal expected cost at least one. The construction approaches the bound.

### B3. What if policies must have strict full support?

The optimal value one becomes an unattained infimum. Put first-round mass
`1-eta` on item 0, split `eta` positively over all small items, and use a fully
supported continuation. Expected extra effort is bounded by `eta` times a
finite full-audit cost and vanishes with `eta`.

### B4. Why is the unrestricted cost ratio infinite already for `N=2`?

At fixed `rho>0`, use costs `(1,kappa)`. The exact ratio is
`1+kappa/(1+rho)`, which diverges as `kappa` grows.

## C. Calibration separation

### C1. Are the intervals valid for the realized taints?

Yes. Small taints equal one and lie in `[0,1]`. For the large item,
`pi_0 f_0=rho*w<=2*epsilon`, so
`f_0<=2*epsilon/pi_0`. The upper endpoint is below one because
`epsilon<1/3`.

### C2. Can the certified box stop without item 0?

No. Its residual width always includes `d_0=2*epsilon>epsilon`. After item 0,
the total small-item uncertainty is only `epsilon/2`, so it always stops.

### C3. Does `S=f` mean the model is certified perfect?

No. It means only that the supplied point scores happen to equal the realized
taints on the constructed population. The simultaneous intervals carry the
coverage claim. Manuscript and repository wording enforce this distinction.

## D. Reproducibility attacks

- Exact certificates use `fractions.Fraction`; floats are rejected as theorem
  inputs.
- `make certificate` regenerates both JSON artifacts.
- Independent verifiers do not import the package.
- Unit tests compare the terminal-cost identity to an independent subset
  recursion and the heterogeneous box DP to exhaustive subsets.
- The finite-grid Bellman results remain explicitly discretized.
- Synthetic workloads remain labeled non-client stress tests.

## E. Application boundary

The mathematical results do not establish regulatory compliance, field
performance, or applicability to a particular audit engagement. Those claims
would require separate evidence and authorized audit data.
4. The original authors should be asked whether the bounded-betting mechanism
   or support convention was anticipated.
5. Subscription-index and citation-graph searches remain necessary; the web
   review is not a novelty guarantee.
