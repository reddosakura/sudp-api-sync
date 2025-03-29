import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class VisitorPassageBaseSchema(BaseModel):
    pass_date: Optional[datetime.datetime]
    status: bool
    visitor_id: uuid.UUID

    class Config:
        from_attributes = True


class VisitorPassageSchema(VisitorPassageBaseSchema):
    id: uuid.UUID
    visitor: dict

    class Config:
        from_attributes = True


class ListVisitorPassageSchema(BaseModel):
    v_passages: list[VisitorPassageSchema]
