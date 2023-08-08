import time


class WatcherRoutineTimer:
    def __init__(self, interval_seconds: int = 1):
        self.interval_seconds = interval_seconds
        self.start_time = time.time()
        self.end_time = self.start_time + self.interval_seconds
        self.temp_interval = None

    def check_and_reset(self) -> bool:
        if self._temp_check():
            return True
        if time.time() >= self.end_time:
            self.reset()
            return True
        return False

    def reset(self) -> None:
        self.start_time = time.time()
        self.end_time = self.start_time + self.interval_seconds
        self.temp_interval = None

    def set_temp_and_reset(self, temp_interval_seconds: int = 1) -> None:
        self.temp_interval = time.time() + temp_interval_seconds

    def _temp_check(self) -> bool:
        if self.temp_interval is not None:
            if time.time() >= self.temp_interval:
                self.reset()
                return True
        return False
