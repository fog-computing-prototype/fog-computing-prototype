from local.sensors.core import Sensor
import math


class TemperatureSensor(Sensor):
    def read(self) -> str:
        # 10t equals roughly one day, equation is created based on visual representation
        t = self._t
        g = math.sin((math.sin(t * 4) /20  ) + (t / 2)) * 4 + 20 + self._seed
        s = g - (math.sin(t / 3) * self._seed)
        self._t += 1
        return str(s)
