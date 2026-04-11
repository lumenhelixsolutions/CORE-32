"""Audit log records for CORE-32 / RUBIC."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class LogRecord:
    kind: str
    tx_id: int
    tick: int
    state: int
    payload_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AuditLog:
    records: list[LogRecord] = field(default_factory=list)

    def append(self, record: LogRecord) -> None:
        self.records.append(record)
