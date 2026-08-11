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
| C11 | For every fixed `delta` and finite uniform bet cap `L`, the repeated oracle's worst-case stopping-time approximation-ratio supremum is `N` over the bounded non-CV RLFA class. | Proved | Two continuous-set witnesses, uniform wealth bound, Plackett--Luce rank, matching horizon upper bound |
| C12 | Point scores equal to the realized taints can make prop-MS inherit the sharp factor-`N` lower bound. | Proved | With `S=f` on the constructed population, prop-MS equals the oracle |
| C13 | For a simultaneous box, descending `pi_i(u_i-l_i)` is pathwise minimax-optimal under unit costs. | Proved | Modular residual width and matching prefix lower bound |
| C14 | The heterogeneous-cost box problem is solved exactly by the checked Pareto DP. | Verified | DP dominance proof, brute-force tests, independent certificate |
| C15 | The full continuous-action ApproxKelly Bellman problem is solved for arbitrary `N`. | **Not claimed** | Solver is exact only on its stated finite grid/action mesh |
| C16 | Synthetic score benchmarks establish real-world savings. | **Not claimed** | They are reproducible stress tests, not client data |
| C17 | With `max(c)/min(c) <= kappa`, the sharp oracle review-cost ratio supremum is `1+(N-1)kappa`. | Proved | Exact expected terminal-rank cost and matching total-cost upper bound |
| C18 | Without bounded cost heterogeneity, the oracle has no finite review-cost approximation guarantee, already for `N=2`. | Proved | `1+kappa/(1+rho)` diverges with `kappa` |
| C19 | On one family, scores equal the realized taints while prop-MS approaches the sharp review/count bounds and simultaneous intervals identify a one-review optimum. | Proved | Exact calibration-separation construction and certificate |
| C20 | The sharp theorem covers unbounded betting or arbitrary control-variate wealth processes. | **Not claimed** | The proof requires a finite uniform non-CV stake cap |
