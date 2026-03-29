from __future__ import annotations

import time
from dataclasses import dataclass, field

#CS50.DEV

def _fmt_seconds(total: float) -> str:
    if total < 0:
        total = 0.0
    ms = int((total - int(total)) * 1000)
    sec = int(total) % 60
    minutes = (int(total) // 60) % 60
    hours = int(total) // 3600
    return f"{hours:02d}:{minutes:02d}:{sec:02d}.{ms:03d}"


@dataclass
class Stopwatch:
    _running: bool = False
    _start: float | None = None
    _accum: float = 0.0
    _laps: list[float] = field(default_factory=list)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._start = time.perf_counter()

    def pause(self) -> None:
        if not self._running:
            return
        now = time.perf_counter()
        if self._start is not None:
            self._accum += now - self._start
        self._start = None
        self._running = False

    def reset(self) -> None:
        self._running = False
        self._start = None
        self._accum = 0.0
        self._laps.clear()

    def lap(self) -> float:
        elapsed = self.elapsed_seconds()
        self._laps.append(elapsed)
        return elapsed

    def elapsed_seconds(self) -> float:
        if not self._running or self._start is None:
            return self._accum
        return self._accum + (time.perf_counter() - self._start)

    def status(self) -> str:
        return "RUNNING" if self._running else "PAUSED"

    def laps(self) -> list[float]:
        return list(self._laps)

    def render(self) -> str:
        return _fmt_seconds(self.elapsed_seconds())

    def render_laps(self) -> list[str]:
        return [_fmt_seconds(x) for x in self._laps]

