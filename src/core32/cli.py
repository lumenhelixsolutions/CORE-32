"""CLI for CORE-32 / RUBIC demo runs."""

from __future__ import annotations

import argparse
import json

from .supervisor import Core32Supervisor


def cmd_demo() -> int:
    sup = Core32Supervisor(state=0)
    sup.execute("P_DELTA32", ctx="demo")
    sup.execute("P_RHO32", ctx="demo")
    sup.set_sandbox(True)
    sup.execute("P_SWAPPAIR_0", ctx="demo")
    payload = {
        "state": sup.state,
        "tick": sup.tick,
        "accumulator": sup.accumulator,
        "swap_cursor_k": sup.swap_cursor_k,
        "swap_epoch": sup.swap_epoch,
        "records": [record.__dict__ for record in sup.log.records],
    }
    print(json.dumps(payload, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="core32")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    args = parser.parse_args()
    if args.cmd == "demo":
        return cmd_demo()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
