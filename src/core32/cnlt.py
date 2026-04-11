"""Small scaffolding for CNLT-oriented extensions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LayerObserver:
    name: str
    visible_states: frozenset[int]
    rotor_orbits_touched: int
    power_note: str


LAYER_OBSERVERS = {
    "MEMBRANE": LayerObserver("MEMBRANE", frozenset({7, 23}), 1, "Minimal: sees only boundary gate pair"),
    "INGRESS": LayerObserver("INGRESS", frozenset({7, 23, 8, 24}), 3, "Adds validation states"),
    "BUFFER": LayerObserver("BUFFER", frozenset({7, 23, 8, 24, 9, 10, 25, 26}), 5, "Adds staging buffers"),
    "SANDBOX": LayerObserver("SANDBOX", frozenset({7, 23, 8, 24, 9, 10, 25, 26, 14, 15, 30, 31}), 6, "Adds execution environments"),
    "PAYLOAD": LayerObserver("PAYLOAD", frozenset(range(32)), 10, "Full access to all orbits"),
}
