from typing import List, Optional, Tuple

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from local.models import Metadata, SensorDataCached
from local.schemas import SensorDataCachedCreateSchema


def create_cached_sensor_data(
    session: Session, sensor_data_create: SensorDataCachedCreateSchema
) -> SensorDataCached:
    """Create cached sensor data and saved them to the database.

    Args:
        session (Session): Database session.
        sensor_data_create (SensorDataCachedCreateSchema): Cached sensor data create schema.

    Returns:
        SensorDataCached: Cached sensor data database model.
    """

    sequence = get_and_increment_sequence(session)
    db_sensor_data = SensorDataCached(**sensor_data_create.dict(), sequence=sequence)
    session.add(db_sensor_data)
    session.commit()
    session.refresh(db_sensor_data)
    return db_sensor_data


def delete_cached_sensor_data(session: Session, sensor_sequence: int):
    """Delete cached sensor data by sequence.

    Args:
        session (Session): Database session.
        sensor_sequence (int): Sequence of the data.
    """

    session.execute(
        delete(SensorDataCached)
        .where(SensorDataCached.sequence == sensor_sequence)
        .execution_options(synchronize_session="fetch")
    )
    session.commit()


def get_all_cached_sensor_data_stats(session: Session) -> int:
    """Get all cached sensor data statistics from the database.

    Args:
        session (Session): Database session.

    Returns:
        int: Number of cached sensor data.
    """

    return session.execute(select(func.count(SensorDataCached.id))).one()


def get_all_cached_sensor_data(session: Session) -> List[SensorDataCached]:
    """Get list of all cached sensor data from the database.

    Args:
        session (Session): Database session.

    Returns:
        List[SensorDataCached]: List of all cached sensor data.
    """

    return session.scalars(select(SensorDataCached)).all()


def get_metadata(session: Session) -> Optional[Metadata]:
    """Get metadata from the database.

    Args:
        session (Session): Database session.

    Returns:
        Optional[Metadata]: Metadata
    """

    return session.scalar(select(Metadata))


def get_and_increment_sequence(session: Session) -> int:
    """Get and increment sequence from the metadata.

    Args:
        session (Session): Database session.

    Returns:
        int: Sequence.
    """

    db_metadata = session.scalar(select(Metadata))
    sequence = db_metadata.sequence
    db_metadata.sequence = sequence + 1
    return sequence


def initialize_metadata(session: Session) -> Metadata:
    """Create new metadata with sequence = 0.

    Args:
        session (Session): Database session.

    Returns:
        Metadata: Metadata.
    """

    db_metadata = Metadata(sequence=0)
    session.add(db_metadata)
    session.commit()
    session.refresh(db_metadata)
    return db_metadata
