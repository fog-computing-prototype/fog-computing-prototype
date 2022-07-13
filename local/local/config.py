import logging
import os
from functools import lru_cache

LOG = logging.getLogger(__name__)


class Config:
    # URL for the cloud endpoint
    cloud_endpoint_url = os.environ.get(
        "LOCAL_CLOUD_ENDPOINT_URL", "tcp://localhost:5556"
    )
    # URL for the local listener endpoint
    local_listener_endpoint_url = os.environ.get(
        "LOCAL_LISTENER_ENDPOINT_URL", "tcp://*:5557"
    )
    # path to the sensor file
    sensor_file = "./sensors.yaml"


@lru_cache()
def get_config():
    LOG.info("Initialized config parameters.")
    return Config()
