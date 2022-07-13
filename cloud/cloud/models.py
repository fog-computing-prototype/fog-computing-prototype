from typing import Any

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# path to the local database
LOCAL_DB_DATABASE = "./database.db"

engine = create_engine(
    f"sqlite:///{LOCAL_DB_DATABASE}",
    future=True,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: Any = declarative_base()


class Sensor(Base):
    """A sqlalchemy class to represent a sensor.

    Args:
        Base (_type_): A base class for declarative class definitions.
    """

    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class SensorData(Base):
    """A sqlalchemy class to represent sensor data.

    Args:
        Base (_type_): A base class for declarative class definitions.
    """

    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    value = Column(String)
    sequence = Column(Integer)
    sensor_id = Column(Integer, ForeignKey("sensor.id"))

    sensor: Sensor = relationship("Sensor")  # type: ignore


class Metadata(Base):
    """A sqlalchemy class to represent metadata.

    Args:
        Base (_type_): A base class for declarative class definitions.
    """

    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True)
    sequence = Column(Integer)


class CloudStatisticsDataCached(Base):
    """A sqlalchemy class to represent the cached cloud statistics.

    Args:
        Base (_type_): A base class for declarative class definitions.
    """

    __tablename__ = "cloud_statistics_cached"

    id = Column(Integer, primary_key=True)
    sequence = Column(Integer)
    sensor_data_count = Column(Integer)


Base.metadata.create_all(engine)
