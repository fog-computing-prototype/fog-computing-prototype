from datetime import datetime
from typing import List

from pydantic import BaseModel


class SensorBaseSchema(BaseModel):
    """A class to represent a sensor. Base schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """

    name: str


class SensorReadSchema(SensorBaseSchema):
    """A class to represent a sensor. Read schema.

    Args:
        SensorBaseSchema (SensorBaseSchema): Sensor base schema.
    """

    id: int


class SensorCreateSchema(SensorBaseSchema):
    """A class to represent a sensor. Create schema.

    Args:
        SensorBaseSchema (SensorBaseSchema): Sensor base schema.
    """

    pass


class SensorDataBaseSchema(BaseModel):
    """A class to represent sensor data. Base schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """

    timestamp: datetime
    value: str
    sequence: int


class SensorDataReadSchema(SensorDataBaseSchema):
    """A class to represent sensor data. Read schema.

    Args:
        SensorDataBaseSchema (SensorDataBaseSchema): Sensor data base schema.
    """

    class Config:
        orm_mode = True


class SensorDataOrderedReadSchema(SensorDataBaseSchema):
    """A class to represent ordered sensor data. Base schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """

    name: str

    class Config:
        orm_mode = True


class SensorDataCreateSchema(SensorDataBaseSchema):
    """A class to represent ordered sensor data. Create schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """

    name: str


class SensorDataChartReadSchema(BaseModel):
    """A class to represent a sensor data chard. Read schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """

    name: str
    values: List[SensorDataReadSchema]


class CloudStatisticsBaseSchema(BaseModel):
    """A class to represent cloud statistics. Base schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """

    sensor_data_count: int
    sequence: int


class CloudStatisticsReadSchema(CloudStatisticsBaseSchema):
    """A class to represent cloud statistics. Read schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """

    class Config:
        orm_mode = True
