"""Payload definitions and dispatch for CORE-32 / RUBIC."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .encoding import is_digit_code
from .primitives import cauldron_l32, cauldron_l32_inv, delta32, pi10, pi10_inv, rho32, rho32_inv, swap_pair

PayloadFn = Callable[[int], int]


@dataclass(frozen=True, slots=True)
class Payload:
    payload_id: str
    apply: PayloadFn
    inverse_id: str
    gating: str
    requires_membrane_open: bool = False
    requires_digit_state: bool = False
    swap_k: int | None = None

    def run(self, state: int) -> int:
        return self.apply(state)


class UnknownPayloadError(KeyError):
    pass


PAYLOADS: dict[str, Payload] = {
    "P_DELTA32": Payload("P_DELTA32", delta32, "P_DELTA32", "Always"),
    "P_RHO32": Payload("P_RHO32", rho32, "P_RHO32_INV", "Always"),
    "P_RHO32_INV": Payload("P_RHO32_INV", rho32_inv, "P_RHO32", "Always"),
    "P_PI10": Payload("P_PI10", pi10, "P_PI10_INV", "Membrane open", requires_membrane_open=True, requires_digit_state=True),
    "P_PI10_INV": Payload("P_PI10_INV", pi10_inv, "P_PI10", "Membrane open", requires_membrane_open=True, requires_digit_state=True),
    "P_L32": Payload("P_L32", cauldron_l32, "P_L32_INV", "Membrane open", requires_membrane_open=True, requires_digit_state=True),
    "P_L32_INV": Payload("P_L32_INV", cauldron_l32_inv, "P_L32", "Membrane open", requires_membrane_open=True, requires_digit_state=True),
    "P_NOOP32": Payload("P_NOOP32", lambda x: x, "P_NOOP32", "Always"),
}

for k in range(16):
    PAYLOADS[f"P_SWAPPAIR_{k}"] = Payload(
        payload_id=f"P_SWAPPAIR_{k}",
        apply=lambda state, kk=k: swap_pair(state, kk),
        inverse_id=f"P_SWAPPAIR_{k}",
        gating="Schedule + policy",
        swap_k=k,
    )


def get_payload(payload_id: str) -> Payload:
    try:
        return PAYLOADS[payload_id]
    except KeyError as exc:
        raise UnknownPayloadError(payload_id) from exc


def payload_requires_digit_state(payload_id: str, state: int) -> bool:
    payload = get_payload(payload_id)
    return payload.requires_digit_state and not is_digit_code(state)
