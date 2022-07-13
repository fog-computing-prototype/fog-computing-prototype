from typing import Any

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

# path to the local database
LOCAL_DB_DATABASE = "./database.db"

engine = create_engine(
    f"sqlite:///{LOCAL_DB_DATABASE}",
    future=True,
)

Base: Any = declarative_base()


class Metadata(Base):
    """A sqlalchemy class to represent metadata.

    Args:
        Base (_type_): A base class for declarative class definitions.
    """    

    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True)
    sequence = Column(Integer)


class SensorDataCached(Base):
    """A sqlalchemy class to represent the cached sensor data.

    Args:
        Base (_type_): A base class for declarative class definitions.
    """    

    __tablename__ = "sensor_data_cached"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    timestamp = Column(DateTime)
    value = Column(String)
    sequence = Column(Integer)
