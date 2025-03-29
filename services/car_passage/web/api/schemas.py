import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class CarPassageBaseSchema(BaseModel):
    pass_date: Optional[datetime.datetime]
    status: bool
    car_id: uuid.UUID

    class Config:
        from_attributes = True


class CarPassageSchema(CarPassageBaseSchema):
    id: uuid.UUID
    car: dict

    class Config:
        from_attributes = True


class ListCarPassageSchema(BaseModel):
    c_passages: Optional[list[CarPassageSchema]]
