from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo

from rich.table import Table

try:
    from .state import AppState, StateStore
except ImportError:
    from state import AppState, StateStore

#CS50.DEV

def _local_now() -> datetime:
    return datetime.now().astimezone()


def _time_format_string(clock_format: str) -> str:
    if clock_format == "12h":
        return "%I:%M %p"
    return "%H:%M"


def format_time_for_display(current_time: datetime, clock_format: str) -> str:
    time_format = _time_format_string(clock_format)
    return current_time.strftime(time_format)


def _is_local_timezone(current_time: datetime, zone_name: str) -> bool:
    zone_time = current_time.astimezone(_safe_zoneinfo(zone_name))
    local_zone_name = current_time.tzname()
    target_zone_name = zone_time.tzname()
    same_offset = zone_time.utcoffset() == current_time.utcoffset()
    same_name = target_zone_name == local_zone_name
    return same_offset and same_name


def _safe_zoneinfo(name: str) -> ZoneInfo:
    return ZoneInfo(name)


@dataclass
class TimezoneManager:
    store: StateStore
    state: AppState
    lock: threading.Lock = field(default_factory=threading.Lock)

    def list(self) -> list[str]:
        return list(self.state.timezones)

    def add(self, tz_name: str) -> None:
        _safe_zoneinfo(tz_name)
        if self.lock:
            with self.lock:
                if tz_name not in self.state.timezones:
                    self.state.timezones.append(tz_name)
                    self.store.save(self.state)
            return

        if tz_name not in self.state.timezones:
            self.state.timezones.append(tz_name)
            self.store.save(self.state)

    def remove(self, tz_name: str) -> bool:
        if self.lock:
            with self.lock:
                if tz_name in self.state.timezones:
                    self.state.timezones.remove(tz_name)
                    self.store.save(self.state)
                    return True
                return False

        if tz_name in self.state.timezones:
            self.state.timezones.remove(tz_name)
            self.store.save(self.state)
            return True
        return False

    def now_table(self) -> Table:
        current_time = _local_now()
        table = Table(title="Current Time")
        table.add_column("Zone", style="bold")
        table.add_column("Time")
        current_zone_name = str(current_time.tzinfo) if current_time.tzinfo else "Local"
        table.add_row(current_zone_name, format_time_for_display(current_time, self.state.clock_format))
        return table

    def world_table(self) -> Table:
        current_time = _local_now()
        table = Table(title="World Time")
        table.add_column("Zone", style="bold")
        table.add_column("Time")
        local_time_text = format_time_for_display(current_time, self.state.clock_format)
        table.add_row("[bold green]Local[/bold green]", local_time_text)

        for current_zone_name in self.state.timezones:
            target_zone = _safe_zoneinfo(current_zone_name)
            target_time = current_time.astimezone(target_zone)
            zone_label = current_zone_name

            if _is_local_timezone(current_time, current_zone_name):
                zone_label = f"[bold green]{current_zone_name} (Local)[/bold green]"

            table.add_row(zone_label, format_time_for_display(target_time, self.state.clock_format))
        return table

