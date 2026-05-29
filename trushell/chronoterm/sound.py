from __future__ import annotations

import sys


def play_alarm() -> None:
    try:
        if sys.platform.startswith("win"):
            import winsound

            winsound.Beep(1200, 400)
            winsound.Beep(900, 400)
        else:
            print("", end="")
    except Exception:
        print("", end="")
