import time


class Period:
    def __init__(self, timeout_ms: int):
        self._timeout = timeout_ms / 1000  # ms → sekundy
        self._last_time = time.monotonic()

    def isTime(self) -> bool:
        now = time.monotonic()
        if now - self._last_time >= self._timeout:
            self._last_time = now
            return True
        return False
