import logging
import os
from functools import lru_cache

LOG = logging.getLogger(__name__)


class Config:
    # URL for the cloud listener endpoint
    cloud_listener_endpoint_url = os.environ.get(
        "CLOUD_LISTENER_ENDPOINT_URL", "tcp://*:5556"
    )
    # URL for the local endpoint
    local_endpoint_url = os.environ.get(
        "CLOUD_LOCAL_ENDPOINT_URL", "tcp://localhost:5557"
    )


@lru_cache()
def get_config():
    LOG.info("Initialized config parameters.")
    return Config()
