# Project instructions

- Use exact rational arithmetic for every mathematical certificate. Floating-point
  output may be included only as a human-readable supplement or a clearly
  labeled synthetic benchmark.
- Do not broaden the proved claims. The sharp arbitrary-`N` theorem concerns
  the pinned mathematical ApproxKelly payoff, released zero initialization and
  bet cap, logical intersection, running intersection, and the stated candidate
  grid. The certified-score theorem is exact for the simultaneous box
  certificate, not for every betting-CS intersection.
- The finite-grid/action-mesh Bellman solver is globally exact only for its
  stated discretization; never call it a continuous-action solution.
- Distinguish derived conjectures from claims actually made by Shekhar et al.;
  they pose a broader optimization direction but do not state oracle global
  optimality verbatim.
- Do not call synthetic stress-test savings real-world or industry estimates.
- Every generated certificate must be reproducible with `make certificate` and
  checked by `make test`.
- Git author and committer identity must be
  `Richie Sater <15129476+RichieSater@users.noreply.github.com>`.
