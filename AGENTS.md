# Project instructions

- Use exact rational arithmetic for every mathematical certificate. Floating-point
  output may be included only as a human-readable supplement or a clearly
  labeled synthetic benchmark.
- The sharp arbitrary-`N` theorem covers the original non-control-variate RLFA
  wealth class only when the predictable stakes have a finite uniform cap. It
  uses the logical and running intersections. Do not extend it to unbounded
  stakes or arbitrary control-variate constructions.
- The released ApproxKelly theorem is a corollary with `delta=1/20`, cap `5/2`,
  and an allowed grid. The broader theorem uses the continuous candidate set
  and does not rely on zero initialization or a grid.
- The sharp review-cost ratio `1+(N-1)kappa` assumes positive known costs with
  `max(c)/min(c)<=kappa`. Without that bound, state the ratio as unbounded.
- In the calibration separation, say that scores equal the realized taints on
  the constructed population. Do not call the point model certified or
  zero-error; the simultaneous intervals carry the coverage claim.
- The certified-score theorem is exact for the simultaneous box certificate,
  not for every betting-CS intersection.
- The finite-grid/action-mesh Bellman solver is globally exact only for its
  stated discretization; never call it a continuous-action solution.
- Distinguish derived conjectures from claims actually made by Shekhar et al.;
  they pose a broader optimization direction but do not state oracle global
  optimality verbatim.
- Do not call synthetic stress-test savings real-world or industry estimates.
- The offensive mathematical scope is frozen after the bounded-betting, sharp
  cost, and calibration-separation results. New extensions require a separate
  project; prioritize adversarial review of existing claims.
- Every generated certificate must be reproducible with `make certificate` and
  checked by `make test`.
- Git author and committer identity must be
  `Richie Sater <15129476+RichieSater@users.noreply.github.com>`.
