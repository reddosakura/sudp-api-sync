import uuid
import datetime
from typing import Optional

from pydantic import BaseModel


class ApprovalBaseSchema(BaseModel):
    # id: str
    request_id: int
    user_id: uuid.UUID
    request_status_id: uuid.UUID
    comment: str
    created_date: datetime.datetime = datetime.datetime.now()

    class Config:
        from_attributes = True


class ApprovalSchema(ApprovalBaseSchema):
    id: uuid.UUID
    userobj: Optional[dict]
    status: Optional[dict]

    class Config:
        from_attributes = True
