import logging
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

from ruamel.yaml import YAML

from local.sensors import HumiditySensor, TemperatureSensor
from local.sensors.core import Sensor

yaml = YAML(typ="safe")
available_sensors = [TemperatureSensor, HumiditySensor]

LOG = logging.getLogger(__name__)


def load_sensors_from_yaml(path: str) -> List[Sensor]:
    """Load sensors from YAML file.

    Args:
        path (str): Path to YAML file.

    Returns:
        List[Sensor]: List of sensors.
    """

    sensor_path = Path(path)
    loaded_sensors: List[Sensor] = []
    if not sensor_path.exists():
        print(f"Sensor file '{path}' missing!")
        sys.exit(1)

    with sensor_path.open() as f:
        data: Dict[str, Any] = yaml.load(f)

    sensor_mapping = {
        sensor_class.__name__.lower(): sensor_class
        for sensor_class in available_sensors
    }

    for group, sensors in data.items():
        key = group.replace("_", "").lower().removesuffix("s")
        sensor_class = sensor_mapping.get(key, None)
        if sensor_class is None:
            print(
                f"Sensor file '{path}' is malformed. "
                f"Sensor group name '{group}' does not exist!"
            )
            sys.exit(1)

        # create sensor instances
        for sensor in sensors:
            loaded_sensors.append(sensor_class(**sensor))

    LOG.info(f"Loaded {len(loaded_sensors)} sensors from sensor file.")
    print("Loaded sensors:")
    for sensor_class_name, count in Counter(
        [sensor.__class__.__name__ for sensor in loaded_sensors]
    ).items():
        print(f"    - {sensor_class_name}: {count}")

    return loaded_sensors
