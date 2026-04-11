"""Core reversible primitives for CORE-32 / RUBIC."""

from __future__ import annotations

from .constants import BASE_MASK, L32_NEXT, L32_PREV, PHASE_MASK, PI10_NEXT, PI10_PREV
from .encoding import assert_state


def delta32(x: int) -> int:
    return assert_state(x) ^ PHASE_MASK


def rho32(x: int) -> int:
    x = assert_state(x)
    base = x & BASE_MASK
    phase = x & PHASE_MASK
    return ((base + 1) & BASE_MASK) | phase


def rho32_inv(x: int) -> int:
    x = assert_state(x)
    base = x & BASE_MASK
    phase = x & PHASE_MASK
    return ((base - 1) & BASE_MASK) | phase


def pi10(x: int) -> int:
    x = assert_state(x)
    return PI10_NEXT.get(x, x)


def pi10_inv(x: int) -> int:
    x = assert_state(x)
    return PI10_PREV.get(x, x)


def cauldron_l32(x: int) -> int:
    x = assert_state(x)
    return L32_NEXT.get(x, x)


def cauldron_l32_inv(x: int) -> int:
    x = assert_state(x)
    return L32_PREV.get(x, x)


def swap_pair(x: int, k: int) -> int:
    x = assert_state(x)
    if not 0 <= k <= 15:
        raise ValueError(f"swap base out of range: {k}")
    return (k ^ PHASE_MASK) if x == k else (k if x == (k ^ PHASE_MASK) else x)
