import asyncio
import logging
import sys
from json import JSONDecodeError
from typing import Generator, List

import zmq
import zmq.asyncio
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from cloud.config import get_config
from cloud.models import SessionLocal, engine
from cloud.schemas import (
    CloudStatisticsReadSchema,
    SensorCreateSchema,
    SensorDataChartReadSchema,
    SensorDataCreateSchema,
    SensorDataOrderedReadSchema,
    SensorDataReadSchema,
)
from cloud.service import (
    create_sensor,
    create_sensor_data_with_sensor,
    create_statistic_data,
    delete_cached_sensor_data,
    get_all_cached_cloud_statistics,
    get_all_sensor_data,
    get_all_sensor_data_by_name,
    get_all_sensors,
    get_metadata,
    get_sensor_by_name,
    initialize_metadata,
)

LOG = logging.getLogger("cloud")
LOG.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[{asctime}] [{levelname[0]}] [{name}] {message}",
    datefmt="%H:%M:%S",
    style="{",
)

stream = logging.StreamHandler(sys.stdout)
stream.setFormatter(formatter)
LOG.addHandler(stream)

description = """
## Fog Computing Prototype 

### Features:

* **Get sensor data**.
* **Get sensor data ordered**.
"""

app = FastAPI(
    title="Dashboard API",
    description=description,
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# CORS settings for the dashboard API
origins = [
    "http://localhost:3000",
    "https://fog-computing-prototype.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks: List["asyncio.Task[None]"] = []


# ------------------------------------------------------------------------------------ #
#                              Sensor data message                                     #
# ------------------------------------------------------------------------------------ #


def process_data(data: SensorDataCreateSchema) -> SensorDataCreateSchema:
    """Process data further.

    Args:
        data (SensorDataCreateSchema): Sensor data create schema.

    Returns:
        SensorDataCreateSchema: Sensor data create schema.
    """

    return data


context = zmq.asyncio.Context()


async def start_reliable_zmq_listener_guarded(ctx: zmq.asyncio.Context, endpoint: str):
    """Catch cancelled error and return safely for listener.

    Args:
        ctx (zmq.asyncio.Context): Asynchronous ZeroMQ context.
        endpoint (str): Endpoint URL.
    """

    try:
        await start_reliable_zmq_listener(ctx, endpoint)
    except asyncio.CancelledError:
        return


async def start_reliable_zmq_sender_guarded(ctx: zmq.asyncio.Context, endpoint: str):
    """Catch cancelled error and return safely for sender.

    Args:
        ctx (zmq.asyncio.Context): Asynchronous ZeroMQ context.
        endpoint (str): Endpoint URL.
    """

    try:
        await start_reliable_zmq_sender(ctx, endpoint)
    except asyncio.CancelledError:
        return


async def publish_statistic_data():
    """Create statistic data every 5 seconds."""

    while True:
        try:
            await asyncio.sleep(5)
        except asyncio.exceptions.CancelledError:
            break
        with Session(engine) as session:
            # create statistic data
            create_statistic_data(session)


# inspired by: https://zguide.zeromq.org/docs/chapter4/#Client-Side-Reliability-Lazy-Pirate-Pattern
async def start_reliable_zmq_sender(ctx: zmq.asyncio.Context, endpoint: str):
    """Start reliable ZeroMQ sender.

    Args:
        ctx (zmq.asyncio.Context): Asynchronous ZeroMQ context.
        endpoint (str): Endpoint URL.
    """

    LOG.info("Start reliable zmq sender...")

    # create zero mq socket connection
    socket = ctx.socket(zmq.REQ)
    socket.connect(endpoint)
    LOG.info(f"Connected to socket at: '{endpoint}'")

    while True:
        with Session(engine) as session:
            # access database cached data
            cached_cloud_statistics_data = [
                CloudStatisticsReadSchema.from_orm(data)
                for data in get_all_cached_cloud_statistics(session)
            ]

        LOG.info(
            f"Loaded '{len(cached_cloud_statistics_data)}' statistics data from cache."
        )

        # send message to cloud
        for cloud_statistics_data in cached_cloud_statistics_data:

            message = cloud_statistics_data.json().encode("utf-8")
            await socket.send(message)

            while True:
                if (await socket.poll(3000) & zmq.POLLIN) != 0:
                    answer = await socket.recv()

                    try:
                        received_sequence = int(answer)
                    except ValueError:
                        LOG.error(
                            f"Received answer from edge is not a sequence: '{answer}'!"
                        )
                        continue

                    if not received_sequence == cloud_statistics_data.sequence:
                        LOG.error(
                            f"Received sequence from edge does not match with "
                            f"required sequence: '{received_sequence} != {cloud_statistics_data.sequence}'"
                        )
                        continue

                    with Session(engine) as session:
                        delete_cached_sensor_data(
                            session, sensor_sequence=cloud_statistics_data.sequence
                        )

                    LOG.info(
                        "Send statistic data with "
                        f"sequence: '{cloud_statistics_data.sequence}'"
                    )
                    break

                LOG.warning("No response from server received!")

                socket.close(linger=0)

                LOG.info("Trying to reconnect to server...")
                socket = ctx.socket(zmq.REQ)
                socket.connect(endpoint)
                LOG.info(f"Resending data: '{message}'")
                await socket.send(message)

        await asyncio.sleep(5)


async def start_reliable_zmq_listener(ctx: zmq.asyncio.Context, endpoint: str):
    """Start reliable ZeroMQ listener.

    Args:
        ctx (zmq.asyncio.Context): Asynchronous ZeroMQ context.
        endpoint (str): Endpoint URL.
    """

    socket = ctx.socket(zmq.REP)
    socket.bind(endpoint)

    while True:
        try:
            raw_data = await socket.recv()
        except asyncio.CancelledError:
            return

        if not isinstance(raw_data, bytes):
            raise Exception(
                f"Received a wrong datatype: '{type(raw_data)}'. " "Expected 'bytes'."
            )

        try:
            sensor_data = SensorDataCreateSchema.parse_raw(raw_data.decode("utf-8"))
        except JSONDecodeError as e:
            print(f"Error (JSONDecodeError): '${JSONDecodeError}'.")
            await socket.send_string("")
            continue
        except BaseException as e:
            print(f"Error: '${str(e)}'.")
            await socket.send_string("")
            continue

        with Session(engine) as session:
            db_sensor = get_sensor_by_name(session, sensor_data.name)
            if db_sensor is None:
                db_sensor = create_sensor(
                    session, SensorCreateSchema(name=sensor_data.name)
                )

            create_sensor_data_with_sensor(session, sensor_data, db_sensor.id)

        process_data(sensor_data)

        LOG.info(f"Received data with sequence: '{sensor_data.sequence}'")
        await socket.send_string(str(sensor_data.sequence))


def get_db() -> Generator[Session, None, None]:
    """Get a valid database session.

    Yields:
        Session: Database session.
    """

    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """Start event for dashboard API."""

    config = get_config()

    with Session(engine) as session:
        # load metadata
        metadata = get_metadata(session)
        # check if metadata needs to be initialized
        if metadata is None:
            LOG.info("Initialize metadata with sequence = '0'")
            metadata = initialize_metadata(session)
    LOG.info(f"Loaded metadata with sequence: '{metadata.sequence}'")

    # create tasks
    reliable_zmq_listener_task = asyncio.create_task(
        start_reliable_zmq_listener_guarded(
            ctx=context, endpoint=config.cloud_listener_endpoint_url
        )
    )
    reliable_zmq_sender_task = asyncio.create_task(
        start_reliable_zmq_sender_guarded(
            ctx=context, endpoint=config.local_endpoint_url
        )
    )

    tasks.append(reliable_zmq_listener_task)
    tasks.append(reliable_zmq_sender_task)
    tasks.append(asyncio.create_task(publish_statistic_data()))


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for dashboard API."""

    # cancel all running tasks before shutdown.
    for task in tasks:
        task.cancel()
        await task

    LOG.info("All tasks gracefully stopped.")


@app.get("/sensor-data", response_model=List[SensorDataChartReadSchema])
async def get_sensor_data(
    db: Session = Depends(get_db),
) -> List[SensorDataChartReadSchema]:
    """Sensor data endpoint for dashboard API.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        List[SensorDataChartReadSchema]: List of sensor data chart read schema.
    """

    db_sensors = get_all_sensors(db)

    data = []
    for db_sensor in db_sensors:
        values = [
            SensorDataReadSchema.from_orm(data)
            for data in get_all_sensor_data_by_name(db, db_sensor.name)
        ]
        data.append(SensorDataChartReadSchema(name=db_sensor.name, values=values))

    return data


@app.get("/sensor-data/ordered", response_model=List[SensorDataOrderedReadSchema])
async def get_sensor_data_ordered(
    db: Session = Depends(get_db),
) -> List[SensorDataOrderedReadSchema]:
    """Sensor data ordered endpoint for dashboard API.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        List[SensorDataOrderedReadSchema]: List of sensor data ordered read schema.
    """

    return [
        SensorDataOrderedReadSchema(
            name=db_sensor_data.sensor.name,
            timestamp=db_sensor_data.timestamp,
            value=db_sensor_data.value,
            sequence=db_sensor_data.sequence,
        )
        for db_sensor_data in get_all_sensor_data(db)
    ]
