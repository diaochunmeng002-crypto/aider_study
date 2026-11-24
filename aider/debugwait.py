from __future__ import annotations

import math
import os
import sys
import time


def apply_debugwait(argv: list[str]) -> list[str]:
    """Consume --debugwait and pause once when a positive delay is requested."""
    cleaned: list[str] = []
    value: str | None = None
    index = 0

    while index < len(argv):
        argument = argv[index]
        if argument == "--debugwait":
            if index + 1 >= len(argv):
                raise SystemExit("--debugwait requires a number of seconds")
            if value is not None:
                raise SystemExit("--debugwait may be specified only once")
            value = argv[index + 1]
            index += 2
            continue
        if argument.startswith("--debugwait="):
            if value is not None:
                raise SystemExit("--debugwait may be specified only once")
            value = argument.split("=", 1)[1]
            index += 1
            continue
        cleaned.append(argument)
        index += 1

    if value is None:
        return cleaned

    try:
        seconds = float(value)
    except ValueError as error:
        raise SystemExit(f"--debugwait must be a number, got {value!r}") from error
    if not math.isfinite(seconds) or seconds < 0:
        raise SystemExit("--debugwait must be a finite, non-negative number")

    if seconds > 0:
        print(
            f"[debugwait] pid={os.getpid()} waiting {seconds:g}s; attach now",
            file=sys.stderr,
            flush=True,
        )
        time.sleep(seconds)
        print("[debugwait] wait complete; continuing", file=sys.stderr, flush=True)

    return cleaned
