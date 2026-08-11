# RLFA Optimal Policy: an Exact Counterexample

This repository gives a rational, machine-checkable counterexample to the
claim that repeatedly sampling transaction `i` with probability proportional
to `pi_i f_i` globally minimizes expected audit length.

The claim is tested for the betting confidence sequence in Shekhar, Xu,
Lipton, Liang, and Ramdas (UAI 2023), using the authors' released ApproxKelly
initialization and the paper's logical-CS intersection. The original paper
poses the broader multistage policy problem but **does not state this global
optimality conjecture verbatim**.

## Result

Take two transactions with

| `i` | `pi_i` | `f_i` | `pi_i f_i` |
|---:|---:|---:|---:|
| 1 | `3/4` | `1/3` | `1/4` |
| 2 | `1/4` | `1` | `1/4` |

and set

```text
epsilon = 1/3,    delta = 1/20.
```

The released ApproxKelly implementation has first bet `lambda_1 = 0`.
Consequently, its first-round betting CS is `[0,1]`; after intersection with
the logical CS, the diameter is exactly the total weight of the unobserved
transactions.

- If transaction 1 is sampled first, the diameter is `1/4 <= 1/3`, so
  `tau = 1`.
- If transaction 2 is sampled first, the diameter is `3/4 > 1/3`; the full
  audit then ends at `tau = 2`.

The oracle sees equal contributions and therefore samples each transaction
with probability `1/2`. Its expected audit length is

```text
E[tau_oracle] = (1/2) 1 + (1/2) 2 = 3/2.
```

The paper's implementable prop-M policy samples proportionally to `pi`, so it
selects transaction 1 first with probability `3/4`. Hence

```text
E[tau_prop-M] = (3/4) 1 + (1/4) 2 = 5/4 < 3/2.
```

The strict exact gap is `1/4`; prop-M uses `5/6` as many transactions in
expectation. The same mechanism gives a parametric family, proved in
[`notes/proof.md`](notes/proof.md).

## Verify

The verifier uses only Python's exact `fractions.Fraction` arithmetic.

```sh
make install
make test
make certificate
make search
```

The checked certificate is
[`certificates/counterexample.json`](certificates/counterexample.json). It
enumerates every terminal history and records exact path probabilities and
stopping times.

To rebuild the short note:

```sh
make paper
```

## Scope

This result settles the universal oracle-global-optimality claim negatively
for the explicitly pinned construction. It does **not** settle:

- the betting CS without the logical intersection;
- a different first-round betting initialization;
- the imperfect-information minimax problem driven by AI scores;
- the globally optimal implementable policy for general finite populations.

See [`notes/scope.md`](notes/scope.md) and
[`notes/literature.md`](notes/literature.md) before reusing the claim.

## Sources

- [UAI 2023 paper and supplementary material](https://proceedings.mlr.press/v216/shekhar23a.html)
- [Authors' released implementation](https://github.com/sshekhar17/WeightedWoRConfSeq)
- [CMU Accounting AI Research Lab research page](https://www.cmu.edu/tepper/accounting-lab/research/index.html)

## License

MIT. See [`LICENSE`](LICENSE).
