import asyncio
import logging
import sys
from asyncio import Task
from datetime import datetime
from typing import List

import zmq
import zmq.asyncio
from sqlalchemy.orm import Session

from local import messaging
from local.config import get_config
from local.models import Base, engine
from local.schemas import SensorDataCachedCreateSchema, SensorDataCachedReadSchema
from local.sensors.core import Sensor
from local.service import (
    create_cached_sensor_data,
    delete_cached_sensor_data,
    get_all_cached_sensor_data,
    get_all_cached_sensor_data_stats,
    get_metadata,
    initialize_metadata,
)
from local.utils import load_sensors_from_yaml

loaded_sensors: List[Sensor] = []


running_sensor_tasks: List[Task[None]] = []

LOG = logging.getLogger("local")
LOG.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[{asctime}] [{levelname[0]}] [{name}] {message}",
    datefmt="%H:%M:%S",
    style="{",
)

stream = logging.StreamHandler(sys.stdout)
stream.setFormatter(formatter)
LOG.addHandler(stream)

config = get_config()

# create all tables
Base.metadata.create_all(engine)

# load sensors from yaml config file
loaded_sensors = load_sensors_from_yaml(config.sensor_file)

ctx = zmq.asyncio.Context()


async def publish_sensor_data(sensor: Sensor):
    """Produces sensor data for a given sensor in a given interval

    Args:
        sensor (Sensor): Sensor
    """

    LOG.info(
        f"Start sensor value production for: '{sensor.name}' with interval: '{sensor.interval}'"
    )

    while True:
        try:
            await asyncio.sleep(sensor.interval)
        except asyncio.exceptions.CancelledError:
            break

        data = SensorDataCachedCreateSchema(
            timestamp=datetime.now(),
            name=sensor.name,
            value=sensor.read(),
        )

        with Session(engine) as session:
            db_cached_sensor_data = create_cached_sensor_data(session, data)

        LOG.info(
            f"Sensor: '{data.name}' new data with sequence: '{db_cached_sensor_data.sequence}'"
        )


async def start_sensors():
    """Start sensor data producing tasks."""

    for sensor in loaded_sensors:
        publish_task = asyncio.create_task(publish_sensor_data(sensor))
        running_sensor_tasks.append(publish_task)


async def main():
    """Connect to database and start all sensors. Run the sender and listener to send
    and receive data.
    """

    with Session(engine) as session:
        # load metadata
        metadata = get_metadata(session)

        # check if metadata needs to be initialized
        if metadata is None:
            LOG.info("Initialize metadata with sequence = '0'")
            metadata = initialize_metadata(session)

        sensor_data_count = get_all_cached_sensor_data_stats(session)

    LOG.info(f"Loaded metadata with sequence: '{metadata.sequence}'")
    LOG.info(f"Loaded '{sensor_data_count}' messages from cache.")

    # start all sensors
    await start_sensors()

    # run sender and listener forever
    await asyncio.gather(
        messaging.start_reliable_zmq_sender(
            ctx=ctx, endpoint=config.cloud_endpoint_url
        ),
        messaging.start_reliable_zmq_listener(
            ctx=ctx, endpoint=config.local_listener_endpoint_url
        ),
    )


try:
    asyncio.run(main())
except KeyboardInterrupt:
    sys.exit(0)
