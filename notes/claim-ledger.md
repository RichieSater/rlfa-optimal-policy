# Claim ledger

| ID | Claim | Status | Evidence |
|---|---|---|---|
| C1 | The released ApproxKelly first bet is zero. | Verified | Source audit and unit test |
| C2 | For the certified instance, stopping at time 1 occurs exactly when item 1 is sampled. | Verified | Exact first-round intervals |
| C3 | The oracle expected length is `3/2`. | Verified | Exact DP and history certificate |
| C4 | prop-M expected length is `5/4`. | Verified | Exact DP and history certificate |
| C5 | The repeated oracle is not globally optimal for the pinned construction. | Proved | `5/4 < 3/2` |
| C6 | The mechanism yields an infinite rational family. | Proved | Symbolic calculation in `proof.md` |
| C7 | No prior work contains this counterexample. | **Not claimed** | Focused search is not exhaustive |
| C8 | prop-M is globally optimal. | **Not claimed** | Not investigated |
