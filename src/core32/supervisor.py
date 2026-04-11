"""Minimal reversible CORE-32 / RUBIC supervisor."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .constants import DIGIT_CODES, MASK64, SPLITMIX_BETA, SPLITMIX_PHI
from .encoding import assert_state
from .log import AuditLog, LogRecord
from .payloads import UnknownPayloadError
from .registry import PayloadRegistry
from .schedule import FrozenSwapSchedule, schedule_default


class HaltError(RuntimeError):
    pass


class PolicyError(RuntimeError):
    pass


@dataclass(slots=True)
class Core32Supervisor:
    state: int = 0
    tick: int = 0
    accumulator: int = 0
    membrane_open: bool = True
    fault_armed: bool = False
    halt_requested: bool = False
    sandbox_mode: bool = False
    swap_cursor_k: int = 0
    swap_epoch: int = 0
    tx_counter: int = 0
    log: AuditLog = field(default_factory=AuditLog)
    registry: PayloadRegistry = field(default_factory=PayloadRegistry)
    schedule: FrozenSwapSchedule = field(default_factory=lambda: schedule_default)
    _history: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.state = assert_state(self.state)

    def _mix(self, state: int, tick: int, ctx: str) -> int:
        value = (state * SPLITMIX_PHI + tick * SPLITMIX_BETA + len(ctx)) & MASK64
        value ^= (value >> 30)
        value = (value * SPLITMIX_BETA) & MASK64
        value ^= (value >> 27)
        value = (value * SPLITMIX_PHI) & MASK64
        value ^= (value >> 31)
        return value & MASK64

    def _append(self, kind: str, tx_id: int, payload_id: str | None = None, **details: Any) -> None:
        self.log.append(LogRecord(kind=kind, tx_id=tx_id, tick=self.tick, state=self.state, payload_id=payload_id, details=details))

    def _halt(self, reason: str, tx_id: int) -> None:
        self.halt_requested = True
        self._append("HALT", tx_id, reason=reason)
        raise HaltError(reason)

    def _check_policy(self, payload_id: str) -> None:
        if self.halt_requested:
            raise PolicyError("HALT gate active")
        payload = self.registry.get(payload_id)
        if self.fault_armed and not (payload_id.endswith("_INV") or payload_id in {"P_NOOP32", "P_DELTA32"} or payload_id.startswith("P_SWAPPAIR_")):
            raise PolicyError("FAULT gate active: rollback-only operations permitted")
        if payload.requires_membrane_open and not self.membrane_open:
            raise PolicyError("MEMBRANE gate blocks phase-crossing digit payload")
        if payload.requires_digit_state and self.state not in DIGIT_CODES:
            raise PolicyError("Payload requires digit-embedded state")
        if payload.swap_k is not None:
            k = payload.swap_k
            expected = self.swap_cursor_k
            if k != expected:
                raise PolicyError(f"Swap schedule violation: expected k={expected}, got k={k}")
            if k in {0, 1, 2, 4, 8} and not self.sandbox_mode:
                raise PolicyError("Digit swap requires sandbox mode or override")

    def execute(self, payload_id: str, *, ctx: str = "default") -> int:
        tx_id = self.tx_counter
        self.tx_counter += 1
        try:
            if not self.registry.has_inverse(payload_id):
                self._halt("unknown inverse", tx_id)
            self._check_policy(payload_id)
            self._append("BEGIN", tx_id, payload_id=payload_id)
            self.accumulator ^= self._mix(self.state, self.tick, ctx)
            before = self.state
            self.state = self.registry.get(payload_id).run(self.state)
            self.state = assert_state(self.state)
            history_entry = {
                "tx_id": tx_id,
                "payload_id": payload_id,
                "inverse_id": self.registry.inverse_of(payload_id),
                "before": before,
                "after": self.state,
                "tick_before": self.tick,
                "acc_before": self.accumulator,
                "ctx": ctx,
            }
            self.tick += 1
            if payload_id.startswith("P_SWAPPAIR_"):
                self.swap_cursor_k = self.schedule.next_after(self.swap_cursor_k)
                self.swap_epoch += 1
            self._history.append(history_entry)
            self._append("COMMIT", tx_id, payload_id=payload_id, accumulator=self.accumulator, swap_cursor_k=self.swap_cursor_k, swap_epoch=self.swap_epoch)
            return self.state
        except UnknownPayloadError:
            self._halt("unknown inverse", tx_id)
        except Exception:
            if self.log.records and self.log.records[-1].kind == "BEGIN":
                self.rollback(reason="auto")
            raise

    def rollback(self, *, reason: str = "manual") -> int:
        if not self._history:
            return self.state
        last = self._history.pop()
        tx_id = self.tx_counter
        self.tx_counter += 1
        self._append("ROLLBACK", tx_id, payload_id=last["inverse_id"], reason=reason)
        inverse = self.registry.get(last["inverse_id"])
        self.state = inverse.run(self.state)
        self.state = assert_state(self.state)
        self.tick = max(0, self.tick - 1)
        self.accumulator ^= self._mix(self.state, self.tick, last["ctx"])
        self.fault_armed = False
        if last["payload_id"].startswith("P_SWAPPAIR_"):
            self.swap_epoch = max(0, self.swap_epoch - 1)
            self.swap_cursor_k = int(last["payload_id"].split("_")[-1])
        self._append("FAULT_CLEAR", tx_id, payload_id=last["inverse_id"], state_restored=self.state)
        return self.state

    def arm_fault(self) -> None:
        self.fault_armed = True

    def release_halt(self) -> None:
        self.halt_requested = False

    def set_membrane(self, is_open: bool) -> None:
        self.membrane_open = is_open

    def set_sandbox(self, enabled: bool) -> None:
        self.sandbox_mode = enabled
