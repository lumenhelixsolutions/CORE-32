# Repository structure rationale

This repository stack is designed so the implementation can grow in three directions without a future rewrite:

## 1. Normative engine

The `src/core32/` package is where the canonical single-node implementation lives.

## 2. Research supplements

The original papers mention Python and GAP supplements for verification, classification, flower analysis, and 3D extensions. Those fit naturally under:

- `scripts/` for runnable verification helpers
- `research/` or `scripts/gap/` for larger supplements later
- `docs/` for rendered explanatory material

## 3. Distributed / lattice work

The tessellation + CNLT paper points toward a multi-node lattice simulator. That can be added later as:

- `src/core32/lattice.py`
- `src/core32/node.py`
- `src/core32/observer.py`
- `tests/test_lattice.py`

The current scaffold keeps those future seams clean.
