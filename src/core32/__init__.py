"""CORE-32 / RUBIC package."""

from .constants import DIGIT_CODES, META_BASES, PHASE_MASK, STATE_SPACE_SIZE
from .primitives import (
    cauldron_l32,
    cauldron_l32_inv,
    delta32,
    pi10,
    pi10_inv,
    rho32,
    rho32_inv,
    swap_pair,
)
from .schedule import FrozenSwapSchedule, schedule_default
from .supervisor import Core32Supervisor

__all__ = [
    "STATE_SPACE_SIZE",
    "PHASE_MASK",
    "DIGIT_CODES",
    "META_BASES",
    "delta32",
    "rho32",
    "rho32_inv",
    "pi10",
    "pi10_inv",
    "cauldron_l32",
    "cauldron_l32_inv",
    "swap_pair",
    "FrozenSwapSchedule",
    "schedule_default",
    "Core32Supervisor",
]
