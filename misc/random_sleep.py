import random
import time


class RandomSleep:
    @staticmethod
    def sleep(base: float = 1, coefficient: float = 3):
        time.sleep(base + random.random() * coefficient)
