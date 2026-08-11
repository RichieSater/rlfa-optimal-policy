# Exact Two-Transaction Sampling for Risk-Limiting Financial Audits

This repository solves the globally optimal first-stage sampling problem
exactly for `N=2` under a pinned risk-limiting financial audit construction. As
a corollary, it gives a rational, machine-checkable counterexample to the claim
that repeatedly sampling transaction `i` proportionally to `pi_i f_i` globally
minimizes expected audit length.

The construction is the betting confidence sequence in Shekhar, Xu, Lipton,
Liang, and Ramdas (UAI 2023), using the authors' released ApproxKelly
initialization and the logical-CS intersection. The original paper poses the
broader multistage problem but **does not state this global-optimality
conjecture verbatim**.

## Exact `N=2` theorem

The released implementation has first bet `lambda_1=0`. Therefore the
first-round betting CS is `[0,1]`, and the combined CS diameter after sampling
item `i` is exactly `1-pi_i`.

For any first-stage distribution `q`, define

```text
A = {i : 1-pi_i <= epsilon}.
```

Complete history enumeration gives

```text
E_q[tau] = 2 - sum_{i in A} q(i).
```

Consequently, over the literal simplex of sampling distributions,

```text
V* = 2,  if epsilon < min(pi_1,pi_2),
V* = 1,  if epsilon >= min(pi_1,pi_2).
```

- If `A` is empty, every distribution is optimal.
- If `A` contains one item, audit that item deterministically.
- If `A` contains both items, every distribution is optimal.

Thus the exact optimal `N=2` policy is independent of `f` and `delta`. The
unknown misstatements affect comparator policies such as the oracle, but not
the true optimum.

## Certified counterexample

Take

| `i` | `pi_i` | `f_i` | `pi_i f_i` |
|---:|---:|---:|---:|
| 1 | `3/4` | `1/3` | `1/4` |
| 2 | `1/4` | `1` | `1/4` |

with `epsilon=1/3` and `delta=1/20`. Item 1 is the unique first-round stopping
item. The exact expectations are

```text
E[tau_deterministic-large-first] = 1,
E[tau_prop-M]                    = 5/4,
E[tau_oracle]                    = 3/2.
```

The original full-support comparison `5/4 < 3/2` remains intact. The exact
literal-simplex solution strengthens it to

```text
1 < 5/4 < 3/2.
```

## Support convention

Definition 2 of the paper permits a probability distribution on the remaining
set, and Proposition 2 optimizes over the corresponding simplex. Read
literally, deterministic boundary actions are admissible.

Because the generic importance-weight identity suggests a stricter convention,
the repository also certifies:

- under strict full support, the singleton-regime infimum is `1` but is not
  attained;
- `q_eta=(1-eta,eta)` has exact expectation `1+eta`;
- under positive-contribution support, attainment occurs exactly when every
  nonstopping contribution is zero.

See [`notes/proof.md`](notes/proof.md) for the theorem and exact
oracle-optimality criterion.

## Verify

The verifier uses only Python's exact `fractions.Fraction` arithmetic.

```sh
make install
make test
make certificate
make search
uv run rlfa-optimal characterize-n2
```

The checked [`counterexample.json`](certificates/counterexample.json) records
all terminal histories, the deterministic optimum, and both conservative
support variants. A separate verifier recomputes the inequalities without
importing the package.

To rebuild the mathematical note:

```sh
make paper
```

## General finite populations

[`notes/bellman.md`](notes/bellman.md) gives the augmented-state Bellman
equation for arbitrary `N`. The action changes both the next-item probabilities
and the importance-weighted confidence state; this is precisely the
continuation-value effect omitted by the one-step surrogate.

The repository does **not** yet solve `N >= 3`, the betting CS without logical
intersection, a different first-round initialization, or the AI-score minimax
problem. See [`notes/scope.md`](notes/scope.md) and
[`notes/literature.md`](notes/literature.md).

## Sources

- [UAI 2023 paper and supplementary material](https://proceedings.mlr.press/v216/shekhar23a.html)
- [Authors' released implementation](https://github.com/sshekhar17/WeightedWoRConfSeq)
- [CMU Accounting AI Research Lab research page](https://www.cmu.edu/tepper/accounting-lab/research/index.html)

## License

MIT. See [`LICENSE`](LICENSE).
