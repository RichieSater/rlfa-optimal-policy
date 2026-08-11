# Claim ledger

| ID | Claim | Status | Evidence |
|---|---|---|---|
| C1 | The released ApproxKelly first bet is zero. | Verified | Source audit and unit test |
| C2 | For `N=2`, `E_q[tau] = 2 - sum_{i:1-pi_i<=epsilon}q(i)`. | Proved | First-round lemma and exhaustive histories |
| C3 | The literal-simplex optimum is `1` if `epsilon >= min(pi)`, otherwise `2`. | Proved | Exact `N=2` theorem and tests |
| C4 | For the instance, deterministic-large-first has expected length `1`. | Verified | Exact DP and independent certificate |
| C5 | For the instance, prop-M has expected length `5/4`. | Verified | Exact DP and independent certificate |
| C6 | For the instance, the oracle has expected length `3/2`. | Verified | Exact DP and independent certificate |
| C7 | The repeated oracle is not globally optimal for the pinned construction. | Proved | `1 < 5/4 < 3/2` |
| C8 | Under strict full support, the singleton-regime infimum is `1` but is unattained. | Proved | `q_eta` family and positivity |
| C9 | The mechanism yields an infinite rational family. | Proved | Symbolic calculation in `proof.md` |
| C10 | No prior work contains this result. | **Not claimed** | Focused search is not exhaustive |
| C11 | A general-`N` optimal policy has been found. | **Not claimed** | Only the Bellman formulation is given |
