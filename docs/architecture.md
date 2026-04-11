# Architecture notes

## Core model

The repository follows the supplied CORE-32/RUBIC papers at a software-architecture level:

- `Z32 = {0..31}` with phase decomposition `x = b + 16p`
- canonical dual map `δ32(x) = x ^ 16`
- ten public digit codes `{0, 16, 1, 4, 2, 17, 8, 18, 20, 24}`
- eleven base meta lanes `{3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15}` expressed as 22 phase-paired states
- operator families `rho32`, `pi10`, `L32`, and `swap_pair(k)`
- reversible supervisor semantics with append-only BEGIN/COMMIT/ROLLBACK records

## Package responsibilities

- `constants.py` defines the canonical tables.
- `encoding.py` handles state decomposition and validation.
- `primitives.py` implements algebraic permutations.
- `payloads.py` translates primitives into registry payloads.
- `registry.py` guarantees explicit inverse registration.
- `schedule.py` implements the frozen J-ordered swap schedule.
- `supervisor.py` enforces policy and logs execution.
- `cnlt.py` is a placeholder for observer-layer and lattice-facing extensions.

## Why this layout

This split keeps the formal model separate from orchestration. It also matches the papers' own decomposition into:

1. algebraic foundations,
2. state architecture,
3. operators,
4. transaction protocol,
5. access control,
6. scheduling,
7. future lattice / observer extensions.
