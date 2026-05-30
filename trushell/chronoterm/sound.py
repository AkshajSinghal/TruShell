from __future__ import annotations
import sys
import os


def play_alarm() -> None:
    """Play alarm sound compatible with all platforms and terminals."""
    try:
        if sys.platform.startswith("win"):
            import winsound
            winsound.Beep(1200, 400)
            winsound.Beep(900, 400)
        
        elif sys.platform == "darwin":
            os.system("afplay /System/Library/Sounds/Glass.aiff > /dev/null 2>&1")
        
        else:  # Linux/Unix
            # Try various sound systems
            for cmd in [
                "paplay /usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga &",
                "aplay /usr/share/sounds/alsa/Front_Center.wav &",
                "canberra-gtk-play --id='alarm-clock-elapsed' &",
            ]:
                if os.system(f"which {cmd.split()[0]} > /dev/null 2>&1") == 0:
                    os.system(cmd)
                    return
            
            # Fallback to terminal bell
            sys.stdout.write("\007" * 3)
            sys.stdout.flush()
    
    except Exception:
        sys.stdout.write("\007")
        sys.stdout.flush()