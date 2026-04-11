"""Encoding helpers for CORE-32 state decomposition."""

from __future__ import annotations

from .constants import BASE_MASK, BASE_SPACE_SIZE, DIGIT_CODES, PHASE_MASK, STATE_SPACE_SIZE


def assert_state(x: int) -> int:
    if not 0 <= x < STATE_SPACE_SIZE:
        raise ValueError(f"state out of range: {x}")
    return x


def base_of(x: int) -> int:
    return assert_state(x) & BASE_MASK


def phase_of(x: int) -> int:
    return 1 if (assert_state(x) & PHASE_MASK) else 0


def compose_state(base: int, phase: int) -> int:
    if not 0 <= base < BASE_SPACE_SIZE:
        raise ValueError(f"base out of range: {base}")
    if phase not in (0, 1):
        raise ValueError(f"phase must be 0 or 1: {phase}")
    return base | (PHASE_MASK if phase else 0)


def is_digit_code(x: int) -> bool:
    return assert_state(x) in DIGIT_CODES
