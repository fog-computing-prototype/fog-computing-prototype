from typing import List, Optional

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from cloud.models import CloudStatisticsDataCached, Metadata, Sensor, SensorData
from cloud.schemas import SensorCreateSchema, SensorDataCreateSchema


def create_sensor_data(
    session: Session, sensor_data_create: SensorDataCreateSchema
) -> SensorData:
    """Create sensor data.

    Args:
        session (Session): Database session.
        sensor_data_create (SensorDataCreateSchema): Sensor data create schema.

    Returns:
        SensorData: Sensor data model.
    """

    db_sensor_data = SensorData(**sensor_data_create.dict())
    session.add(db_sensor_data)
    session.commit()
    session.refresh(db_sensor_data)
    return db_sensor_data


def create_sensor_data_with_sensor(
    session: Session, sensor_data_create: SensorDataCreateSchema, sensor_id: int
) -> SensorData:
    """Create sensor data with sensor.

    Args:
        session (Session): Database schema.
        sensor_data_create (SensorDataCreateSchema): Sensor data create schema.
        sensor_id (int): Sensor ID.

    Returns:
        SensorData: Sensor data model.
    """

    db_sensor_data = SensorData(
        **dict(**sensor_data_create.dict(exclude={"name": True}), sensor_id=sensor_id)
    )
    session.add(db_sensor_data)
    session.commit()
    session.refresh(db_sensor_data)
    return db_sensor_data


def create_sensor(session: Session, sensor_create: SensorCreateSchema) -> SensorData:
    """Create sensor in database.

    Args:
        session (Session): Database session.
        sensor_create (SensorCreateSchema): Sensor create schema.

    Returns:
        SensorData: Sensor data model.
    """

    db_sensor = Sensor(**sensor_create.dict())
    session.add(db_sensor)
    session.commit()
    session.refresh(db_sensor)
    return db_sensor


def get_all_sensors(db: Session) -> List[Sensor]:
    """Get all sensors from database.

    Args:
        db (Session): Database session.

    Returns:
        List[Sensor]: List of sensor models.
    """

    return db.scalars(select(Sensor)).all()


def get_sensor_by_name(db: Session, name: str) -> Sensor:
    """Get sensor by sensor name from database.

    Args:
        db (Session): Database session.
        name (str): Name of the sensor.

    Returns:
        Sensor: Sensor model.
    """
    return db.scalars(select(Sensor).where(Sensor.name == name)).first()


def get_all_sensor_data(db: Session) -> List[SensorData]:
    """Get all sensor data from database.

    Args:
        db (Session): Database session.

    Returns:
        List[SensorData]: List of sensor data models.
    """

    return db.scalars(
        select(SensorData).order_by(SensorData.sequence.desc()).limit(100)
    ).all()


def get_all_sensor_data_by_name(db: Session, sensor_name: str) -> List[SensorData]:
    """Get all sensor data by sensor name from database.

    Args:
        db (Session): Database session.
        sensor_name (str): Name of the sensor.

    Returns:
        List[SensorData]: List of sensor data models.
    """

    return reversed(
        db.scalars(
            select(SensorData)
            .join(SensorData.sensor)
            .where(Sensor.name == sensor_name)
            .order_by(SensorData.sequence.desc())
            .limit(100)
        ).all()
    )


def get_all_cached_cloud_statistics(
    session: Session,
) -> List[CloudStatisticsDataCached]:
    """Get all cached cloud statistics from database.

    Args:
        session (Session): Database session.

    Returns:
        List[CloudStatisticsDataCached]: List of cloud statistics data cached model.
    """

    return session.scalars(select(CloudStatisticsDataCached)).all()


def create_statistic_data(session: Session):
    """Crate statistics data in database.

    Args:
        session (Session): Database Session.
    """

    sequence = get_and_increment_sequence(session)

    sensor_data_count = session.scalar(select(func.count(SensorData.id)))
    db_cloud_statistic = CloudStatisticsDataCached(
        sensor_data_count=sensor_data_count, sequence=sequence
    )
    session.add(db_cloud_statistic)
    session.commit()


def delete_cached_sensor_data(session: Session, sensor_sequence: int):
    """Delete cached sensor data in database.

    Args:
        session (Session): Database session.
        sensor_sequence (int): Sensor sequence.
    """

    session.execute(
        delete(CloudStatisticsDataCached)
        .where(CloudStatisticsDataCached.sequence == sensor_sequence)
        .execution_options(synchronize_session="fetch")
    )
    session.commit()


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
