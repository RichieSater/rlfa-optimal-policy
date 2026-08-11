# Project instructions

- Use exact rational arithmetic for every mathematical certificate. Floating-point
  output may be included only as a human-readable supplement.
- Do not broaden the proved claim. The exact `N=2` characterization concerns
  the authors' released ApproxKelly initialization, intersected with the
  logical confidence sequence, for the expected stopping-time objective stated
  in this repository. General `N` is not solved.
- Distinguish the conjecture investigated here from claims actually made by
  Shekhar et al.; they pose a broader optimization direction but do not state the
  global-optimality conjecture verbatim.
- Every generated certificate must be reproducible with `make certificate` and
  checked by `make test`.
- Git author and committer identity must be
  `Richie Sater <15129476+RichieSater@users.noreply.github.com>`.
