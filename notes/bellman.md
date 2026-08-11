# Bellman formulation for arbitrary finite populations

The exact `N=2` solution collapses before the betting state becomes nontrivial.
For general `N`, the sampling distribution changes both the transition
probabilities and the next confidence state, so the correct Bellman state must
remember more than the set of audited transactions.

## State

At time `t`, let `x_t` contain:

- the ordered audited history and revealed `f_i` values;
- the remaining set `R_t`;
- the current betting wealth function `W_t(m)`;
- the ApproxKelly payoff accumulators needed to compute `lambda_{t+1}(m)`;
- the current logical interval and running confidence-set intersection.

For the oracle problem the full fixed vector `f` is known to the controller. In
the implementable problem it is replaced by the information state induced by
the scores and revealed transactions.

## Action and transition

An action `q` is a distribution on `R_t`, under whichever support convention is
chosen. If item `i` is drawn, the importance-weighted observation is

```text
Z_{t+1} = pi_i f_i / q(i),
```

and the complete next state is

```text
x_{t+1} = Phi(x_t, q, i).
```

The dependence of `Phi` on `q` is essential. It is why optimizing only the
probability of drawing a desirable item is not a valid general-`N` reduction.

## Bellman equation

Let `D` be the stopping region where the confidence-set diameter is at most
`epsilon`, and let `V(x)` be the minimum expected number of additional audits.
Then

```text
V(x) = 0,                                           x in D,
V(x) = 1 + inf_q sum_{i in R(x)} q(i) V(Phi(x,q,i)), x not in D.
```

The boundary condition at a complete audit is `V=0`. The initial expected
audit length is `V(x_0)`.

The Proposition-2 oracle minimizes a local variance term inside one transition;
it does not solve this equation because it omits the continuation value
`V(Phi(x,q,i))`.

## Why `N=2` is exactly solvable

For the pinned released construction, `lambda_1=0`. The first betting CS is
therefore `[0,1]`, and the first transition enters the stopping region exactly
when the other transaction's weight is at most `epsilon`. If the transition
does not stop, the only remaining action audits the second item and terminates.
Thus the augmented state disappears and the Bellman equation reduces to

```text
V(q) = 2 - sum_{i: 1-pi_i <= epsilon} q(i).
```

The next research problem is to identify a sufficient finite-dimensional state
or a provable approximation for `N >= 3`.
