# Scope and nonclaims

## What is proved

The repeated `pi_i f_i` oracle is not globally optimal for expected audit
length under the explicitly pinned, released ApproxKelly-plus-logical
construction. A paper-defined, implementable alternative (prop-M) has strictly
smaller exact expected stopping time on a two-item rational instance.

More strongly, the complete `N=2` problem is solved. For the literal simplex of
first-stage distributions,

```text
V* = 2  if epsilon < min(pi_1,pi_2),
V* = 1  otherwise.
```

The optimizer set and the exact oracle-optimality criterion are given in
`proof.md`. Under strict full support, the same number is the infimum; it is
not attained when exactly one first draw can stop the audit.

## What is not proved

- The original UAI paper is not being corrected: it proves one-step surrogate
  optimality, not global expected-stopping-time optimality.
- This repository does not analyze a betting CS used without the logical CS.
- It does not claim that prop-M is globally optimal; in the certified instance
  it is not, because the literal-simplex optimum is deterministic.
- It does not solve the imperfect-information minimax problem for AI risk
  scores.
- It does not provide a novelty guarantee. The literature note records a
  focused search, but independent expert review remains necessary.

## Why the mechanism matters

The one-step oracle eliminates variance in the importance-weighted monetary
contribution. The stopping rule, however, also uses a logical interval whose
width depends on **remaining recorded-value weight**, not remaining monetary
misstatement. Those objectives can point in different directions. The
two-transaction family isolates this mismatch.

## The next research question

The negative result redirects the project toward a genuine optimization target:

1. solve the augmented-state Bellman equation in `bellman.md` for `N >= 3`;
2. determine whether a scalar index can balance wealth growth and logical-width
   reduction;
3. solve or approximate the implementable minimax problem when only bounded-
   error scores are available.
