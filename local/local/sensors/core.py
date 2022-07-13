from abc import ABC, abstractmethod
import random


class Sensor(ABC):
    def __init__(self, name: str, interval: float = 5.0) -> None:
        self.name = name
        self.interval = interval
        self._t = 0
        self._seed = random.randrange(-5, 5)

    @abstractmethod
    def read(self) -> str:
        return
