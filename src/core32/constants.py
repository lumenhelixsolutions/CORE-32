"""Constants and canonical tables for CORE-32 / RUBIC."""

from __future__ import annotations

STATE_SPACE_SIZE = 32
BASE_SPACE_SIZE = 16
PHASE_MASK = 0x10
BASE_MASK = 0x0F

DIGIT_CODES = frozenset({0, 16, 1, 4, 2, 17, 8, 18, 20, 24})
DIGIT_EMBEDDING = {
    0: 0,
    1: 16,
    2: 1,
    3: 4,
    4: 2,
    5: 17,
    6: 8,
    7: 18,
    8: 20,
    9: 24,
}

META_BASES = frozenset({3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15})

META_LANES = {
    3: ("MODE", "Encode / compile", "Decode / decompile"),
    5: ("CHECK", "Accumulate tag", "Verify / compare"),
    6: ("TICK", "Tick ++", "Tick --"),
    7: ("MEMBRANE", "Boundary open", "Boundary closed"),
    9: ("PTR", "Pointer ++", "Pointer --"),
    10: ("KEYSEL", "Key bank 0", "Key bank 1"),
    11: ("ROUTE", "Branch A", "Branch B"),
    12: ("EVENT", "Commit marker", "Rollback marker"),
    13: ("FAULT", "Fault armed", "Fault cleared"),
    14: ("SANDBOX", "Experimental", "Mirror sandbox"),
    15: ("HALT", "Halt requested", "Halt released"),
}

PI10_NEXT = {0: 16, 16: 1, 1: 4, 4: 2, 2: 17, 17: 8, 8: 18, 18: 20, 20: 24, 24: 0}
PI10_PREV = {v: k for k, v in PI10_NEXT.items()}

L32_NEXT = {1: 4, 4: 2, 2: 8, 8: 17, 17: 20, 20: 18, 18: 24, 24: 1}
L32_PREV = {v: k for k, v in L32_NEXT.items()}

SPLITMIX_PHI = 0x9E3779B97F4A7C15
SPLITMIX_BETA = 0xBF58476D1CE4E5B9
MASK64 = 0xFFFFFFFFFFFFFFFF
