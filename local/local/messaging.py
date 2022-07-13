import asyncio
import logging

import zmq
import zmq.asyncio
from sqlalchemy.orm import Session

from local.models import engine
from local.schemas import CloudStatisticsReadSchema, SensorDataCachedReadSchema
from local.service import delete_cached_sensor_data, get_all_cached_sensor_data

LOG = logging.getLogger(__name__)


async def start_reliable_zmq_listener(ctx: zmq.asyncio.Context, endpoint: str):
    """Start reliable ZeroMQ listener.

    Args:
        ctx (zmq.asyncio.Context): Asynchronous ZeroMQ context.
        endpoint (str): Endpoint URL.
    """

    socket = ctx.socket(zmq.REP)
    socket.bind(endpoint)

    while True:
        message = await socket.recv()

        cloud_statistic = CloudStatisticsReadSchema.parse_raw(message.decode("utf-8"))
        LOG.info(f"Received message: '{cloud_statistic}'")
        await socket.send_string(str(cloud_statistic.sequence))


# inspired by: https://zguide.zeromq.org/docs/chapter4/#Client-Side-Reliability-Lazy-Pirate-Pattern
async def start_reliable_zmq_sender(ctx: zmq.asyncio.Context, endpoint: str):
    """Start reliable ZeroMQ sender.

    Args:
        ctx (zmq.asyncio.Context): Asynchronous ZeroMQ context.
        endpoint (str): Endpoint URL.
    """

    # create zero mq socket connection
    socket = ctx.socket(zmq.REQ)
    socket.connect(endpoint)
    LOG.info(f"Connected to socket at: '{endpoint}'")

    while True:
        # access database cached data
        with Session(engine) as session:
            cached_sensor_data = [
                SensorDataCachedReadSchema.from_orm(data)
                for data in get_all_cached_sensor_data(session)
            ]

        LOG.info(f"Loaded '{len(cached_sensor_data)}' sensor data from cache.")

        # send message to cloud
        for sensor_data in cached_sensor_data:

            message = sensor_data.json().encode("utf-8")
            await socket.send(message)

            while True:
                if (await socket.poll(3000) & zmq.POLLIN) != 0:
                    answer = await socket.recv()

                    try:
                        received_sequence = int(answer)
                    except ValueError:
                        LOG.error(
                            f"Received answer from cloud is not a sequence: '{answer}'!"
                        )
                        continue

                    if received_sequence != sensor_data.sequence:
                        LOG.error(
                            f"Received sequence from cloud does not match with "
                            f"required sequence: '{received_sequence} != {sensor_data.sequence}'"
                        )
                        continue

                    with Session(engine) as session:
                        delete_cached_sensor_data(
                            session, sensor_sequence=sensor_data.sequence
                        )

                    LOG.info(
                        f"Send sensor data: '{sensor_data.name}' "
                        f"sequence: '{sensor_data.sequence}'"
                    )
                    break

                LOG.warning("No response from server received!")

                socket.close(linger=0)

                LOG.info("Trying to reconnect to server...")
                socket = ctx.socket(zmq.REQ)
                socket.connect(endpoint)
                LOG.info(f"Resending data: '{message}'")
                await socket.send(message)

        LOG.info("Waiting for new sensor data for 10 seconds...")
        await asyncio.sleep(10)