from local.sensors.core import Sensor
import math


class HumiditySensor(Sensor):
    def read(self) -> str:
        # humidity midpoint somewhere in between 40%
        f = math.sin(self._t) + 40 + self._seed
        g = math.sin(self._t / 4) * 5 + 40 + self._seed
        self._t += 1
        return str((g + f) - 40 + self._seed)
