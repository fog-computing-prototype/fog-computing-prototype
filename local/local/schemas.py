from datetime import datetime

from pydantic import BaseModel


class SensorDataCachedBaseSchema(BaseModel):
    """A class to represent the cached sensor data. Base schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """    

    name: str
    timestamp: datetime
    value: str


class SensorDataCachedCreateSchema(SensorDataCachedBaseSchema):
    """A class to represent the cached sensor data. Create schema.

    Args:
        SensorDataCachedBaseSchema (SensorDataCachedBaseSchema): Cached sensor data base schema.
    """    

    pass


class SensorDataCachedReadSchema(SensorDataCachedBaseSchema):
    """A class to represent the cached sensor data. Read schema.

    Args:
        SensorDataCachedBaseSchema (SensorDataCachedBaseSchema): Cached sensor data base schema.
    """    

    sequence: int

    class Config:
        orm_mode = True


class CloudStatisticsBaseSchema(BaseModel):
    """A class to represent the cloud statistics. Base schema.

    Args:
        BaseModel (BaseModel): Pydantic BaseModel.
    """    

    sensor_data_count: int
    sequence: int


class CloudStatisticsReadSchema(CloudStatisticsBaseSchema):
    """A class to represent the cloud statistics. Read schema.

    Args:
        CloudStatisticsBaseSchema (CloudStatisticsBaseSchema): Cloud statistics base schema.
    """  

    class Config:
        orm_mode = True
