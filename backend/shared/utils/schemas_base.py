from datetime import datetime
from uuid import UUID

import pytz
from pydantic import BaseConfig, BaseModel, validator


class BaseSchema(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        orm_mode = True


# for locale see: https://www.geeksforgeeks.org/how-to-make-a-timezone-aware-datetime-object-in-python/
class DateTimeModelMixin(BaseModel):
    created_at: None | datetime
    updated_at: None | datetime

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.now(pytz.timezone("America/Caracas"))


class IDModelMixin(BaseModel):
    id: UUID
