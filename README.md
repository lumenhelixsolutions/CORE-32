# CORE-32 / RUBIC

A Python-first GitHub repository stack for the **CORE-32 / RUBIC** architecture: a 32-state reversible computation engine built on the involution `δ32(x) = x ^ 16`, with a 10-code public digit embedding, 22 engine-only meta states, explicit inverse registration, membrane gating, append-only audit logs, and frozen canonical swap scheduling.

This repository stack is organized around the structure described in the supplied CORE-32 papers:

- a `Z32` state space with phase decomposition and δ-paired channels
- a public digit embedding `D10^(32)` and 22 meta-lane states
- core permutation operators `delta32`, `rho32`, `pi10`, `L32`, and `swap_pair`
- a supervisor enforcing `HALT > FAULT > MEMBRANE > Payload Policy`
- reversible `COMMIT` and `ROLLBACK` transaction paths
- a frozen J-ordered swap schedule for deterministic, tamper-evident auditing
- optional CNLT/tessellation extensions as future-facing documentation hooks

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
python -m core32.cli demo
```

## Repository layout

```text
core32-rubic/
├── .github/workflows/ci.yml
├── docs/
│   ├── architecture.md
│   ├── repository-structure.md
│   └── research-map.md
├── examples/
│   └── basic_run.py
├── scripts/
│   └── core_verify.py
├── src/core32/
│   ├── __init__.py
│   ├── cli.py
│   ├── cnlt.py
│   ├── constants.py
│   ├── encoding.py
│   ├── log.py
│   ├── payloads.py
│   ├── primitives.py
│   ├── registry.py
│   ├── schedule.py
│   └── supervisor.py
├── tests/
│   ├── test_primitives.py
│   ├── test_schedule.py
│   └── test_supervisor.py
├── .gitignore
└── pyproject.toml
```

## Current scope

This repo is a **clean implementation scaffold**, not a camera-ready publication mirror. It gives CORE-32 a practical repository backbone with:

- runnable primitives
- a typed payload registry
- a minimal reversible supervisor
- deterministic audit logs
- tests for conformance-critical behavior

## Next recommended additions

1. Add the full paper reference implementation as a normative `reference/` module.
2. Add GAP and group-theory supplements under `research/` or `scripts/gap/`.
3. Add diagram assets and generated figures under `docs/assets/`.
4. Add a multi-node lattice simulator for the tessellation/CNLT work.
5. Add serialization schemas for audit packets and replay bundles.
