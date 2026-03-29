from __future__ import annotations

import sys

#CS50.DEV

def play_alarm() -> None:
    try:
        # Windows sound
        if sys.platform.startswith("win"):
            import winsound
            winsound.Beep(1200, 600)
            winsound.Beep(900, 600)
        else:
            # Terminal bell fallback
            print("\a")
    except Exception:
        print("\a")