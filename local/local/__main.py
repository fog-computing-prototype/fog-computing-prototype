from random import random
import sys
from time import sleep
import zmq
from dataclasses import field, dataclass
from datetime import datetime
from queue import Empty, Queue
import random
from threading import Thread
import logging
import itertools

BROKER_ENDPOINT = "tcp://localhost:5556"
sensor_data_queue = Queue()


# ------------------------------------------------------------------------------------ #
#                                   Setup logging                                      #
# ------------------------------------------------------------------------------------ #

# LOG = logging.getLogger("local")
# LOG.setLevel(logging.INFO)

# formatter = logging.Formatter(
#     "[{asctime}] [{levelname:<7}] [{name}] {message}",
#     datefmt="%d.%m.%Y %H:%M:%S",
#     style="{",
# )

# stream = logging.StreamHandler(sys.stdout)
# stream.setFormatter(formatter)
# LOG.addHandler(stream)

# ------------------------------------------------------------------------------------ #
#                              Sensor data message                                     #
# ------------------------------------------------------------------------------------ #


@dataclass
class SensorData:
    sensor_id: str
    value: str
    sequence: int = -1
    time: datetime = field(default_factory=datetime.now)

    def serialize(self):
        return f"{self.sensor_id} {self.value} {self.sequence} {self.time.timestamp()}"

    @staticmethod
    def deserialize(string: str) -> "SensorData":
        splitted_string = string.split()
        assert len(splitted_string) == 4, "string must match exactly 4 words"
        sensor_id, value, sequence, time = splitted_string
        return SensorData(
            sensor_id=sensor_id,
            value=value,
            sequence=int(sequence),
            time=datetime.fromtimestamp(float(time)),
        )

    def __str__(self) -> str:
        return f"SensorData(sensor_id: {self.sensor_id:<15}, sequence: {self.sequence:<15}, ...)"


def produce_sensor_data(sensor_id: str) -> SensorData:
    while True:
        data = SensorData(
            sensor_id=sensor_id,
            value=str(random.randrange(0, 100)),
        )
        sensor_data_queue.put_nowait(data)
        LOG.info(f"Produced sensor data for sensor_id: '{sensor_id}'")
        sleep(5)


def start_sensor(sensor_id: str):
    Thread(
        target=produce_sensor_data, kwargs={"sensor_id": sensor_id}, daemon=True
    ).start()


start_sensor("temp-01-shed")
start_sensor("temp-02-pool")
start_sensor("temp-03-kitchen")

# inspired by: https://zguide.zeromq.org/docs/chapter4/#Client-Side-Reliability-Lazy-Pirate-Pattern
def message_sender():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(BROKER_ENDPOINT)
    LOG.info(f"Connected to socket at: '{BROKER_ENDPOINT}'")

    sequence = 0
    while True:
        try:
            data = sensor_data_queue.get(block=False)
        except Empty:
            continue

        data.sequence = sequence
        LOG.info(f"Sending sensor data: '{data}'")
        socket.send_string(data.serialize())

        retries = 10
        while True:
            if (socket.poll(3000) & zmq.POLLIN) != 0:
                ack = socket.recv_string()
                sequence += 1
                break

            retries -= 1
            LOG.warning("No response from server")

            socket.setsockopt(zmq.LINGER, 0)
            socket.close()
            if retries == 0:
                LOG.error("Server seems to be offline, abandoning")
                sys.exit()

            LOG.info("Reconnecting to server…")
            # Create new connection
            socket = context.socket(zmq.REQ)
            socket.connect(BROKER_ENDPOINT)
            LOG.info(f"Resending data: '{data}'")
            socket.send_string(data.serialize())


Thread(target=message_sender, daemon=True).start()

try:
    input()
except KeyboardInterrupt:
    sys.exit(0)
