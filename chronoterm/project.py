from datetime import datetime
from zoneinfo import ZoneInfo

from shell import run_shell
from alarms import _parse_when
from timezones import TimezoneManager
from state import StateStore

#CS50.DEV

def main() -> None:
    run_shell()



def parse_alarm_time(time_str: str, tz_name: str | None = None) -> str:
    dt, _ = _parse_when(time_str, tz_name)
    return dt.isoformat(timespec="seconds")

def format_current_time(tz_name: str = "UTC") -> str:
    tz = ZoneInfo(tz_name)
    return datetime.now(tz).strftime("%H:%M")

def is_valid_timezone(tz_name: str) -> bool:
    try:
        ZoneInfo(tz_name)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    main()
