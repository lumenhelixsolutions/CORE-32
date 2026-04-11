"""Payload registry helpers."""

from __future__ import annotations

from .payloads import PAYLOADS, Payload


class PayloadRegistry:
    def __init__(self) -> None:
        self._payloads = dict(PAYLOADS)

    def get(self, payload_id: str) -> Payload:
        return self._payloads[payload_id]

    def has_inverse(self, payload_id: str) -> bool:
        payload = self._payloads[payload_id]
        return payload.inverse_id in self._payloads

    def inverse_of(self, payload_id: str) -> str:
        return self._payloads[payload_id].inverse_id

    def ids(self) -> list[str]:
        return sorted(self._payloads.keys())
