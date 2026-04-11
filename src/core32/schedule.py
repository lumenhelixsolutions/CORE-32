"""Frozen canonical swap schedule for CORE-32 / RUBIC."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SwapEntry:
    rank: int
    k: int
    dual: int
    moment: int
    base_type: str
    constraint: str


class FrozenSwapSchedule:
    """Canonical J-ordered swap schedule."""

    def __init__(self) -> None:
        self._entries = [
            SwapEntry(
                rank=i + 1,
                k=i,
                dual=i ^ 16,
                moment=self.moment(i),
                base_type="DIGIT" if i in {0, 1, 2, 4, 8} else "META",
                constraint="Sandbox / override" if i in {0, 1, 2, 4, 8} else "Standard",
            )
            for i in range(16)
        ]

    @staticmethod
    def moment(k: int) -> int:
        if not 0 <= k <= 15:
            raise ValueError(f"k out of range: {k}")
        return k * k + (k ^ 16) * (k ^ 16)

    @property
    def entries(self) -> list[SwapEntry]:
        return list(self._entries)

    def next_after(self, k: int) -> int:
        if not 0 <= k <= 15:
            raise ValueError(f"k out of range: {k}")
        return (k + 1) % 16


schedule_default = FrozenSwapSchedule()
