# Short-note revision: September 19, 2026

Base repository snapshot: `d2edf02b2399c7ddceb112c24a8294171068e006`.

## Manuscript changes

- The main paper is five pages including references, with an illustrative
  two-item example, the complete sharp factor-N proof, and the short cost
  corollary. Its argument does not rely on supplemental computations.
- The seven-page supplement preserves the conditional interval results,
  ApproxKelly specialization, finite-grid solver, and synthetic experiments.
- The theorem fixes one betting-rule functional, requires full support,
  defines optimal values as infima, restricts oracle comparisons to positive
  contributions, and states that sharpness ranges over tolerances as well as
  populations. Rational rho is explicit. Empty confidence sets have diameter zero.
- The incorrect universal nonattainment assertion is removed. A continuous-set
  counterexample gives an attained value one under full support while retaining
  the true total on both branches. The zero-first-stake N=2 nonattainment result
  remains intact.
- The finite-grid table discloses oracle information in every policy's betting
  bounds and labels its randomized mesh-priority comparator correctly.
- The box-only policy section explicitly allows deterministic selection and
  time-zero stopping, separately from the importance-weighted full-support class.
- Kato and Nakagawa's citation uses the August 13, 2026 revision and current title.

## Evidence

- Ordinary proof checks covered the candidate witnesses, wealth bound, rank
  identity, full-support approximation, matching universal upper bounds, cost
  extension, and support-attainment counterexample. An independent second
  pass checked the main and supplement statements. This is not formal proof.
- `make check`: all lint checks and 58 tests passed, including the new exact
  rational support-attainment regression.
- Both package certificate verifiers and both standalone independent
  certificate scripts passed. These check finite certificates, not a formal
  encoding of the general theorem.
- `make paper`: both PDFs built successfully with pdfLaTeX, two passes each.
  No remaining LaTeX warnings, undefined references, or overfull boxes.
- Every rendered page was visually inspected: five main pages and seven
  supplemental pages.
- `git diff --check` and the existing public-text check passed.
- A pre-existing import-spacing lint issue in the public-text script was fixed
  without changing its behavior. The Makefile now builds both PDFs and falls
  back to pdfLaTeX when Tectonic is unavailable.

## Literature positioning and limits

The original UAI paper's Section 3 and Proposition 2 distinguish multistage
optimization from their one-step variance/wealth surrogate. The revised note
claims a sharp limitation of the repeated rule, not a correction of their
one-step theorem. The pinned implementation's first-stake calculation was
checked directly at commit `a834e459a47f9efa74fa1706f1b1dd8173ffa30b`.

The primary-source checks on September 19 also confirmed that Imberg et al.
optimize asymptotic estimation error and Kato and Nakagawa v2 concern binary
simple-random-sampling audits, explicitly excluding monetary-unit and variables
sampling. These comparisons support the narrow positioning. They are not an
exhaustive priority search; subscription indexes were not accessed.

The main theorem does not cover unbounded stakes, arbitrary control-variate
processes, or sharpness at every fixed tolerance. Benchmarks do not establish
field performance. Existing solver and certificate implementations were
exercised by the suite; no comprehensive re-audit of all implementation internals
or rerun of unchanged Monte Carlo workloads was performed.
